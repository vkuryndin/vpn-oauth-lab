# VPN OAuth Lab

Учебное веб-приложение на Flask с доступом только через WireGuard VPN и авторизацией через Keycloak по OAuth 2.0 / OpenID Connect.

## Stack

- Python 3.12
- Flask 3.1.3
- Authlib 1.8.0
- Requests 2.34.2
- Docker / Docker Compose
- Keycloak 26.7.4
- WireGuard

## Architecture

Приложение и Keycloak запускаются в Docker на Ubuntu-сервере.

- Flask: `http://10.10.10.1:5000`
- Keycloak: `http://10.10.10.1:8180`
- WireGuard server: `10.10.10.1/24`
- WireGuard client: `10.10.10.2/24`

Порты Flask и Keycloak публикуются только на VPN-интерфейсе `10.10.10.1`, поэтому доступ к приложению возможен только при активном WireGuard-туннеле.

## Authentication

Для авторизации используется Keycloak:

- Realm: `vpn-oauth-lab`
- Client: `flask-app`
- Protocol: OAuth 2.0 / OpenID Connect
- Flow: Authorization Code Flow

Все страницы приложения защищены авторизацией.

## Project structure

```text
vpn-oauth-lab/
├── app.py
├── auth.py
├── requirements.txt
├── Dockerfile
├── compose.yaml
└── templates/
```

Создать файл .env:
```text
KEYCLOAK_CLIENT_SECRET=<keycloak-client-secret>
FLASK_SECRET_KEY=<random-secret>
```

Запустить:
```text
sudo docker compose up -d --build
```
Проверить:
```text
sudo docker compose ps
```

После подключения к WireGuard открыть:
```text
http://10.10.10.1:5000
```
Access model
- VPN OFF → приложение недоступно
- VPN ON → приложение доступно
- пользователь не авторизован → перенаправление в Keycloak
- после успешной авторизации → доступ к защищённым страницам
- Logout → завершение сессии и возврат на страницу авторизации