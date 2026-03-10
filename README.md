# VPN для своих

VPN-сервер на DigitalOcean для доступа к независимым СМИ и YouTube.

## Конфигурация сервера

- **Провайдер:** DigitalOcean ($6/mo — 1 GB RAM, 1 CPU, 1 TB transfer)
- **Регион:** Amsterdam (209.38.42.79)
- **Протоколы:**
  - **VLESS + Reality** — порт 443 TCP, основной (маскируется под HTTPS к google.com)
  - **Hysteria2** — порт 8443 UDP, запасной (если VLESS заблокируют)
  - Outline/Shadowsocks — порт 20454, устарел (блокируется DPI)
- **Управление:** 3X-UI панель — `https://209.38.42.79:2053/secretpanel/` (креды в credentials.txt)

## Инструкции для пользователей

Размещены на GitHub Pages: [docs/](docs/)

- [Главная](docs/index.html) — выбор варианта
- [Телефон](docs/mobile.html) — v2rayNG (Android) / Streisand (iOS)
- [Только браузер](docs/browser.html) — v2rayN/V2RayXS + ZeroOmega
- [Полный VPN](docs/fullvpn.html) — v2rayN/V2RayXS в TUN-режиме

## Как добавить нового пользователя

### 1. Открой панель 3X-UI

Зайди на `https://209.38.42.79:2053/secretpanel/` (логин/пароль в credentials.txt).

### 2. Добавь клиента в VLESS-Reality

1. На главной странице найди инбаунд **VLESS-Reality** (порт 443)
2. Нажми **+** справа от него (кнопка "Add Client")
3. Заполни:
   - **Email** — имя друга (например: `valera`, `masha`). Это просто метка, не настоящий email
   - **UUID** — оставь пустым, нажми кнопку генерации (или оставь как есть — сгенерируется сам)
   - Остальное не трогай
4. Нажми **Save**

### 3. Получи ссылку для друга

1. В списке клиентов инбаунда VLESS-Reality найди нового клиента
2. Нажми на иконку **QR-код** или **копировать ссылку** (значок рядом с именем)
3. Получишь ссылку вида `vless://...` — отправь её другу

### 4. (Опционально) Добавь Hysteria2 ключ

Hysteria2 работает как запасной протокол. Если нужен отдельный ключ для друга:

1. SSH на сервер: `ssh root@209.38.42.79`
2. Открой конфиг: `nano /etc/hysteria/config.yaml`
3. Замени секцию `auth` на список паролей:
   ```yaml
   auth:
     type: password
     password: основной_пароль

   # Для нескольких пользователей:
   # auth:
   #   type: userpass
   #   userpass:
   #     valera: его_пароль
   #     masha: её_пароль
   ```
4. `systemctl restart hysteria-server`
5. Ссылка для друга: `hy2://пароль@209.38.42.79:8443?insecure=1&sni=209.38.42.79#VPN-Hysteria2`

## Мониторинг трафика

- Скрипт `scripts/check_traffic.py` запускается ежедневно по крону на дроплете
- Шлёт email-алерт при приближении к лимиту 1 TB/месяц
- DigitalOcean Dashboard → Droplet → **Graphs** — текущее потребление

## Совместимость с Zapret / Booster

При включённом полном VPN весь трафик идёт через туннель.
Zapret/Booster при этом **не нужны** и могут конфликтовать.
В режиме "только браузер" — конфликтов нет, Zapret/Booster работают параллельно.
