DJGG 는 리그 오브 레전드 전적 조회 + 커뮤니티 + RAG 기반 챗봇 기능을 제공하는 웹 서비스입니다.
소환사 검색으로 전적/랭크/매치 상세를 조회하고, 게시판/댓글/투표/토큰/스티커/배너 등의 커뮤니티 기능과, LoL 관련 문서를 기반으로 하는 챗봇 기능을 제공합니다.
주요 기능
소환사 전적 조회
소환사 기본 정보, 랭크 정보, 최근 경기 요약/상세
챔피언 숙련도, 함께 플레이한 유저 정보 등
커뮤니티
게시글 작성/수정/삭제, 첨부 미디어 업로드
댓글 및 대댓글, 좋아요/반응(Reaction)
투표/배팅(Bet) 기능 및 정산 스케줄러
토큰 기반 상점/구매 내역, 유저 아이템, 배너/스티커 인벤토리
RAG 챗봇
lol_docs.csv 기반으로 LoL 관련 질문에 답변
Flask + ML 모델을 활용한 챗 인터페이스
인증/보안
JWT 기반 로그인/회원가입
Spring Security 기반 권한 제어
스토리지/인프라
Oracle Cloud ADB, OCI Object Storage 연동
(옵션) Docker 기반 실행 스크립트 제공
기술 스택
Backend
Java 21, Spring Boot 3.5
Spring Web / WebFlux, Spring Data JPA, Spring Security
JWT (io.jsonwebtoken)
DB: Oracle(실운영), H2(개발/테스트)
Oracle JDBC / OCI Object Storage SDK
Gradle
Frontend
React 19, Vite
React Router, React Icons
Axios
ChatBot
Python 3.x
Flask, requests, numpy, scikit-learn
ollama_gemma3_chat_flask_chat.py 기반 RAG 챗봇 서버
Infra / 기타
Docker / docker-compose (백엔드, DB 등)
Git, ESLint
디렉터리 구조
DJGG/├─ src/main/java/hyun│  ├─ LoLApplication.java           # Spring Boot 메인│  ├─ auth/                         # 인증/보안/유저/커뮤니티 도메인│  │  ├─ controller/                # Auth, Post, Comment, Bet, Shop 등 REST 컨트롤러│  │  ├─ dto/                       # 게시글/댓글 DTO│  │  ├─ jwt/                       # JwtAuthFilter, JwtService│  │  ├─ security/                  # SecurityConfig, SecurityBeans│  │  └─ service/                   # AuthService, PostService, BetService, ShopService 등│  ├─ db/│  │  ├─ config/                    # Oracle Naming 전략, 시퀀스 초기화│  │  ├─ entity/                    # User, Post, Comment, Bet, ShopItem 등 JPA 엔티티│  │  └─ repo/                      # 각 엔티티용 Repository│  └─ lol/                          # Riot API 연동│     ├─ config/                    # Riot API 클라이언트 설정│     ├─ controller/                # Summoner, Match 컨트롤러│     ├─ dto/                       # Summoner, Match, Mastery 등 DTO│     └─ service/                   # SummonerService, MatchService│├─ front/                           # React 프론트엔드│  ├─ src/│  │  ├─ components/                # 공통, 커뮤니티, 홈, 소환사 관련 컴포넌트│  │  ├─ pages/                     # HomePage, SummonerPage, CommunityPage 등│  │  ├─ data/                      # Backend/Riot API 연동 모듈│  │  ├─ hooks/, utils/, styles/    # 커스텀 훅, 유틸, 스타일│  │  └─ main.jsx, App.jsx          # 엔트리/루트 컴포넌트│  └─ docker-compose.backend.yml    # 백엔드 연동용 프론트 Docker 설정│├─ chatBot/│  ├─ ollama_gemma3_chat_flask_chat.py│  ├─ lol_docs.csv│  └─ requirements.txt│├─ docker/│  ├─ docker-compose.yml│  ├─ start-docker.ps1│  └─ stop-docker.ps1├─ Dockerfile.oracle├─ build.gradle└─ README.md
사전 준비
공통
Java 21 이상
Node.js (LTS) + npm
Python 3.x
Git
선택
Docker / Docker Compose
Oracle DB 또는 Oracle Cloud ADB
Riot API Key (전적 조회용)
Ollama 및 Gemma3 모델(챗봇 사용 시, 프로젝트 설정에 맞게 준비 필요)
Backend 실행 방법 (Spring Boot)
# 프로젝트 루트cd c:\soldesk\DJGG# (선택) 테스트용 H2 DB로 실행하는 경우 application.properties 설정 확인# Gradle Wrapper 사용 (Windows PowerShell).\gradlew.bat clean bootRun
기본 포트: 보통 8080 (실제 포트는 src/main/resources/application.properties 참고)
주요 도메인
hyun.lol.controller.* : 전적 조회용 Riot API 연동
hyun.auth.controller.* : 인증/회원/게시글/댓글/샵/배팅 등 커뮤니티 기능
Frontend 실행 방법 (React + Vite)
cd c:\soldesk\DJGG\front# 의존성 설치npm install# 개발 서버 실행npm run dev
기본 포트: Vite 기본값(보통 5173)
백엔드 연동용 API URL은 .env.backend 또는 src/data/backendApi.js 등에서 설정을 확인하고, 실제 백엔드 주소에 맞게 수정합니다.
ChatBot 서버 실행 방법 (Flask RAG 챗봇)
cd c:\soldesk\DJGG\chatBot# 가상환경(선택) 생성 후 패키지 설치pip install -r requirements.txt# Flask 서버 실행python ollama_gemma3_chat_flask_chat.py
lol_docs.csv 를 기반으로 RAG 검색을 수행해 LoL 관련 Q&A 제공
Ollama 및 Gemma3 모델, 또는 해당 스크립트 내에서 참조하는 외부 LLM 환경을 사전에 구성해야 합니다.
Flask 기본 포트(예: 5000)에서 동작하며, 프론트엔드 Chatbot 컴포넌트에서 이 엔드포인트를 호출하도록 설정합니다.
Docker로 실행 (선택)
cd c:\soldesk\DJGG\docker# 컨테이너 실행docker compose up -d# 중지docker compose down
docker-compose.yml 및 Dockerfile.oracle 에서 백엔드/DB 환경이 정의됩니다.
실제 Oracle ADB, 네트워크, 환경변수 설정은 각 환경에 맞게 수정해야 합니다.
주요 환경 변수 / 설정 예시
Backend (application.properties)
Oracle DB 연결 정보 (URL, USER, PASSWORD)
H2 사용 여부
Riot API Key
JWT 시크릿/만료 시간 등
Frontend (.env.backend 등)
VITE_BACKEND_BASE_URL (예: http://localhost:8080)
VITE_CHATBOT_BASE_URL (예: http://localhost:5000)
ChatBot
모델 경로/이름, 임베딩/벡터 스토어 위치 등 (스크립트 내부 또는 환경 변수로 관리)
개발 / 빌드
백엔드 빌드
cd c:\soldesk\DJGG.\gradlew.bat clean build# build/libs/DJGG-...jar 생성 후java -jar build\libs\DJGG-0.0.1-SNAPSHOT.jar
프론트엔드 빌드
cd c:\soldesk\DJGG\frontnpm run buildnpm run preview   # 로컬 프리뷰
향후 개선 아이디어
Riot API 요청 캐싱 및 레이트 리밋 관리 고도화
RAG 챗봇 성능 개선 (벡터 검색, 파인튜닝, 프롬프트 고도화 등)
테스트 코드 확충 (통합 테스트, E2E 테스트)