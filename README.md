# Metaland Accounts
<a href="https://www.docker.com/"><img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=Docker&logoColor=white"/></a>
<a href="https://fastapi.tiangolo.com/ko/"><img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=FastAPI&logoColor=white"/></a>
>Metaland Accounts Server


## Getting Started  

### Installation

<pre><code>git clone https://github.com/deu-meta/metaland-accounts.git

pip install -r requirements.txt

echo "MARIADB_USER=[<b>MARIADB_USER</b>]" >> .env
echo "MARIADB_PASSWORD=[<b>MARIADB_PASSWORD</b>]" >> .env
echo "MARIADB_HOST=[<b>MARIADB_HOST</b>]" >> .env
echo "MARIADB_PORT=[<b>MARIADB_PORT</b>]" >> .env
echo "MARIADB_DATABASE=[<b>MARIADB_DATABASE</b>]" >> .env
</code></pre>

### Run

<pre><code>docker-compose up</code></pre>

## Auth Flow

### Login with Office 365 OAuth 2.0
```mermaid
sequenceDiagram

autonumber

actor Chrome
participant Frontend
participant Backend
participant Office 365

Chrome->>Frontend: Office 365로 로그인 클릭
note right of Chrome: GET http://localhost:3000/oauth/office365

Frontend->>Backend: Office 365 로그인 화면으로 리다이렉트 요청
note right of Frontend: GET http://localhost:8000/jwt/microsoft/login

Backend-->>Chrome: Office 365로 리다이렉트, Office 365 로그인 페이지 표시
note left of Backend: HTTP/1.1 307 Temporary Redirect<br>Location: https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize<br>?client_id={client_id}<br>&scope=openid<br>&response_type=code<br>&redirect_uri=http://localhost:8000/oauth/office365/callback

Chrome->>Office 365: Office 365 로그인
note right of Chrome: Office 365 ID: example@office.deu.ac.kr<br>Office 365 PW: example123

Office 365-->>Backend: 로그인 성공 및 Backend로 Authorization Code와 함께 리다이렉트
note left of Office 365: HTTP/1.1 307 Temporary Redirect<br>Location: http://localhost:8000/jwt/microsoft/callback<br>?code=0.AXIAwvCJkSy9cEmbuFLWulNZ3z

Backend->>Office 365: Authorization Code로 Access Token 요청
note right of Backend: GET https://login.microsoftonline.com/{tenant}/oauth2/token<br>?code=0.AXIAwvCJkSy9cEmbuFLWulNZ3z

Office 365-->>Backend: Access Token 응답
note left of Office 365: HTTP/1.1 200 OK<br>...<br>{ "access_token": "eyJ0eXAiO..." }

Backend->>Office 365: Access Token으로 사용자 정보 요청
note right of Backend: GET https://graph.microsoft.com<br>Authorization: Bearer eyJ0eXAiO...

Office 365-->>Backend: 사용자 정보 응답
note left of Office 365: HTTP/1.1 200 OK<br>...<br>{ "given_name": "김예제", "email": "example@office.deu.ac.kr" }

Backend->>Backend: 1. 사용자 정보 저장<br>2.JWT 토큰과 Refresh Token 생성<br>3. Refresh 토큰 DB에 저장

Backend-->>Frontend: 1. Refresh 토큰 저장 (HttpOnly)<br>2. 프론트엔드로 Redirect
note left of Backend: HTTP/1.1 307 Temporary Redirect<br>Location: http://localhost:3000/oauth/office365/callback<br>#35;jwt={JWT}<br>Set-Cookie: refresh_token=zfa23sClxzMd92

Frontend->>Backend: JWT 토큰으로 Backend 접근 (GET /user/me)
note right of Frontend: GET http://localhost:8000/user/me<br>Authorization: Bearer {JWT}

Backend-->>Frontend: /user/me 에 대한 응답
note left of Backend: HTTP/1.1 200 OK<br>...<br>{ "username": "example_user" }
```

### Verify minecraft account and link with metaland account
```mermaid
sequenceDiagram

actor Player
participant Metaland Netherite
participant Metaland Web
participant Metaland Accounts

Player->>Metaland Netherite: 게임 서버에 연결
Metaland Netherite->>Metaland Accounts: 마인크래프트 계정 연동 토큰 요청 (netherite's secret, player's uuid)
Metaland Accounts-->>Metaland Netherite: 연동 토큰 생성 및 응답
Metaland Netherite-->>Player: 연동 URL을 플레이어에게 표시
Player->>Metaland Web: 연동 URL을 클릭 및 토큰 전달
Metaland Web->>Metaland Web: 로그인 상태를 확인하고 로그인 되어있지 않다면 로그인
Metaland Web->>Metaland Accounts: 토큰 전달 및 연동 요청
Metaland Accounts->>Metaland Accounts: 토큰이 만료되었는지 확인하고 마인크래프트 계정 연동
Metaland Accounts-->>Metaland Web: 성공 여부 응답
alt on success
    Metaland Web-->>Player: 성공 메세지 출력
    Metaland Web-->>Metaland Netherite: 성공 여부 응답
    Metaland Netherite-->>Player: 게임 플레이 허용
else on failure
    Metaland Web-->>Player: 연동 실패 메세지 출력
end
```

## LICENSE

[MIT License](./LICENSE)
