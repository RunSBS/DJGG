## DJGG  

**DJGG** 는 **리그 오브 레전드 전적 조회 + 커뮤니티 + RAG 기반 챗봇** 기능을 제공하는 웹 서비스입니다.  
소환사 검색으로 전적/랭크/매치 상세를 조회하고, 게시판·댓글·투표·토큰·스티커·배너 등의 커뮤니티 기능과 LoL 관련 문서를 기반으로 하는 챗봇 기능을 제공합니다.  

---

## 주요 기능  

### 소환사 전적 조회  
- 소환사 기본 정보, 랭크 정보  
- 최근 경기 요약 및 상세 기록  
- 챔피언 숙련도, 함께 플레이한 유저 정보 등  

### 커뮤니티 기능  
- 게시글 작성 / 수정 / 삭제  
- 이미지·동영상 등 미디어 첨부  
- 댓글 / 대댓글, 좋아요 및 반응(Reaction)  
- 투표 / 배팅(Bet) 기능 및 자동 정산 스케줄러  
- 토큰 기반 상점, 구매 내역, 유저 아이템, 배너·스티커 인벤토리  

### RAG 챗봇  
- `lol_docs.csv` 기반 RAG 검색으로 LoL 관련 질문 응답  
- Flask 기반 API 서버 + ML 모델 연동  
- 프론트 `Chatbot` 컴포넌트와 연동  

### 인증 / 보안  
- JWT 기반 로그인 / 회원가입  
- Spring Security 기반 권한 제어 및 필터링  

### 스토리지 / 인프라  
- Oracle Cloud ADB 연동  
- OCI Object Storage를 이용한 파일 업로드  
- Docker / docker-compose 기반 실행 스크립트 제공  

---

## 기술 스택  

### Backend  
- Java 21  
- Spring Boot 3.5.x  
- Spring Web / WebFlux  
- Spring Data JPA  
- Spring Security + JWT (`io.jsonwebtoken`)  
- DB: Oracle(실제 운영), H2(개발/테스트)  
- Oracle JDBC 드라이버  
- OCI Object Storage SDK  
- Gradle  

### Frontend  
- React 19  
- Vite  
- React Router  
- React Icons  
- Axios  

### ChatBot  
- Python 3.x  
- Flask  
- requests, numpy, scikit-learn  
- `ollama_gemma3_chat_flask_chat.py` 기반 RAG 챗봇 서버  

### Infra / 기타  
- Docker / Docker Compose  
- Git  
- ESLint  
