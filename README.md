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

Metaland Web->>Office 365: 'Office 365로 로그인' 클릭
Office 365->>Office 365: Office 365 로그인
Office 365->>Metaland Accounts: authorization code를 callback API로 전달 (/jwt/microsoft/callback)
alt on success
    Note left of Metaland Accounts: Metaland Accounts는 Office 365에서 access token을 획득함
	Metaland Accounts-->>Metaland Web: 로그인 처리 및 리다이렉트
else on failure
	Metaland Accounts-->>Metaland Web: 리다이렉트 후 에러 표시
end
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
