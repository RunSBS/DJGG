# 파일명: ollama_gemma3_chat_flask_chat.py
import csv
import requests
import numpy as np
from flask import Flask, request, jsonify, render_template
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

model_name = "gemma3:4b"
api_url = "http://localhost:11434/api/chat"

csv_path = "./lol_docs.csv"

app = Flask(__name__)

chat_history = []          # [{"role": "user", "content": ...}, {"role": "assistant", "content": ...}]
last_doc_title = None      # 최근 선택된 대표 문서 제목

# ----------------------------------------
# 한글 전처리 (기본 유지)
# ----------------------------------------
def normalize_korean_text(text: str) -> str:
    if not text:
        return ""
    return text.strip().replace(" ", "")

# ----------------------------------------
# CSV 로드 및 TF-IDF 인덱스 생성
# ----------------------------------------
documents = []
corpus = []
vectorizer = None
doc_vectors = None

def load_documents_from_csv(path: str):
    docs = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            text = (row.get("text") or "").strip()
            intent = (row.get("intent") or "").strip()
            if not text or not intent:
                continue
            docs.append({"title": text, "content": intent})
    if not docs:
        raise ValueError("CSV에서 유효한 문서를 하나도 읽지 못했다.")
    return docs

def build_tfidf_index(docs):
    local_corpus = []
    for doc in docs:
        text = (doc["title"] + "\n" + doc["content"]).strip()
        local_corpus.append(text)
    local_vectorizer = TfidfVectorizer(
        preprocessor=normalize_korean_text,
        analyzer="char",
        ngram_range=(2, 4),
    )
    local_doc_vectors = local_vectorizer.fit_transform(local_corpus)
    return local_corpus, local_vectorizer, local_doc_vectors

try:
    documents = load_documents_from_csv(csv_path)
    corpus, vectorizer, doc_vectors = build_tfidf_index(documents)
    print(f"[정보] CSV에서 {len(documents)}개의 플랫폼 문서를 불러왔다.")
except Exception as e:
    print(f"[경고] 지식 베이스 초기화 실패: {e}")
    documents = []
    corpus = []
    vectorizer = None
    doc_vectors = None

# ----------------------------------------
# 검색 유틸리티
# ----------------------------------------
def retrieve_top_docs(query: str, top_k: int = 3):
    if not vectorizer or doc_vectors is None:
        return []
    query_vec = vectorizer.transform([query])
    sims = cosine_similarity(query_vec, doc_vectors)[0]
    ranked_indices = np.argsort(-sims)
    results = []
    for idx in ranked_indices[:top_k]:
        results.append((documents[idx], float(sims[idx])))
    return results

def format_context(docs_with_scores, min_score: float = 0.0) -> str:
    if not docs_with_scores:
        return "관련된 플랫폼 문서를 찾지 못했다."
    lines = []
    for i, (doc, score) in enumerate(docs_with_scores, start=1):
        if score < min_score:
            continue
        title = doc["title"] or f"문서 {i}"
        content = doc["content"] or ""
        lines.append(f"[문서 {i}] 질의(예시): {title}")
        lines.append(f"참고 내용: {content}")
        lines.append("")
    if not lines:
        return "관련된 플랫폼 문서를 찾지 못했다."
    return "\n".join(lines)

def build_rag_prompt(user_message: str, retrieval_query: str | None = None) -> str:
    global last_doc_title
    query_for_search = retrieval_query or user_message
    top_docs = retrieve_top_docs(query_for_search, top_k=5)
    if top_docs:
        last_doc_title = top_docs[0][0].get("title") or last_doc_title
    context_text = format_context(top_docs, min_score=0.05)
    topic_line = ""
    if last_doc_title:
        topic_line = (
            f"현재 대화의 주요 주제는 '{last_doc_title}' 관련 내용입니다.\n"
            "짧은 질문이라도 이 주제를 기준으로 해석하세요.\n\n"
        )
    prompt = (
        "당신은 '롤 전적조회 및 커뮤니티 플랫폼'에 특화된 도우미 챗봇입니다.\n"
        "아래 규칙을 반드시 지키고, 응답은 한국어로 하세요.\n\n"
        "규칙:\n"
        "1) 아래 제공된 플랫폼 문서(lol_docs.csv)의 text,intent 내용만 참고해 답변한다.\n"
        "2) 문서에 관련 정보가 없으면 '이 플랫폼과 관련된 내용이 아니라 답변을 드릴 수 없습니다.'라고만 답한다.\n"
        "3) 문서의 intent가 짧은 라벨(예: '신고절차')처럼 보이면 그 라벨을 이용해 간단히 분류 설명을 제공한다.\n"
        "4) intent가 설명 문장이라면 그 내용을 이해하기 쉽게 풀어서 답변한다.\n"
        "5) 개인정보, 보안 관련 질문은 내부 정책에 따라 안내하고 직접적인 민감정보를 제공하지 않는다.\n\n"
        f"{topic_line}"
        "# 플랫폼 문서(검색 결과)\n"
        f"{context_text}\n\n"
        "# 사용자 질문\n"
        f"{user_message}\n\n"
        "# 답변\n"
    )
    return prompt

# ----------------------------------------
# ollama 호출
# ----------------------------------------
def ask_ollama(prompt: str) -> str:
    messages = [
        {
            "role": "system",
            "content": (
                "너는 롤 전적조회 및 커뮤니티 플랫폼 문서를 참고해 사용자 질문에 답하는 보조 챗봇이다. "
                "문서에 없는 내용은 답변하지 말고 정해진 문구로 응답하라."
            ),
        }
    ]
    if chat_history:
        messages.extend(chat_history[-6:])
    messages.append({"role": "user", "content": prompt})
    payload = {"model": model_name, "messages": messages, "stream": False}
    resp = requests.post(api_url, json=payload, timeout=120)
    resp.raise_for_status()
    data = resp.json()
    message = data.get("message", {}) or {}
    content = message.get("content", "") or ""
    return content.strip()

# ----------------------------------------
# Flask 라우트
# ----------------------------------------
@app.route("/flask/chat", methods=["POST"])
def chat():
    global last_doc_title
    data = request.get_json(silent=True) or {}
    user_message = data.get("message", "").strip()
    if not user_message:
        return jsonify({"error": "메시지가 비어 있다."}), 400
    if not documents:
        return jsonify({"error": "플랫폼 문서 지식 베이스가 초기화되지 않았다."}), 500
    try:
        if last_doc_title:
            retrieval_query = f"{last_doc_title} {user_message}"
        else:
            retrieval_query = user_message
        rag_prompt = build_rag_prompt(user_message, retrieval_query=retrieval_query)
        answer = ask_ollama(rag_prompt)
        # 히스토리에는 원문 질문/답변만 저장
        chat_history.append({"role": "user", "content": user_message})
        chat_history.append({"role": "assistant", "content": answer})
        if len(chat_history) > 10:
            del chat_history[:-10]
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
