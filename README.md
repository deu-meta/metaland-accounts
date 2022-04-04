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

## LICENSE

[MIT License](./LICENSE)
