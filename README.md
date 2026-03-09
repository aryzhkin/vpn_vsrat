# VPN для своих

Outline VPN сервер на DigitalOcean для доступа к независимым СМИ и YouTube.

## Конфигурация сервера

- **Провайдер:** DigitalOcean
- **Тариф:** $6/mo — 1 GB RAM, 1 CPU, 1 TB transfer
- **Регион:** Amsterdam
- **Протокол:** Shadowsocks (Outline)

## Установка сервера

### 1. Создать дроплет

- Ubuntu 22.04 LTS
- $6/mo (1 GB / 1 CPU / 1 TB transfer)
- Регион: Amsterdam
- SSH-ключ: добавить свой

### 2. Подключиться и запустить скрипт

```bash
ssh root@<IP_DROPLET>
bash <(curl -s https://raw.githubusercontent.com/<YOUR_REPO>/main/setup.sh)
```

Или загрузить скрипт вручную:

```bash
scp setup.sh root@<IP_DROPLET>:~
ssh root@<IP_DROPLET>
bash setup.sh
```

### 3. Подключить к Outline Manager

1. Скачать [Outline Manager](https://getoutline.org/get-started/#step-1) на свой компьютер
2. Выбрать "Advanced" → вставить `apiUrl` из вывода скрипта
3. Готово — можно создавать ключи для друзей

## Добавить пользователя

В Outline Manager: нажать **"+"** → переименовать → отправить ключ другу.
Ключ выглядит как ссылка `ss://...`

## Мониторинг трафика

- DigitalOcean Dashboard → Droplet → **Graphs** — текущее потребление
- DigitalOcean Dashboard → Droplet → **Monitoring → Alerts** — настроить алерт на email при > 800 GB

Лимит тарифа: **1 TB/месяц**. При превышении: $0.01/GB сверху (дроплет не отключается).

## Инструкции для пользователей

> TODO: разместить на GitHub Pages

- Как включить VPN только в браузере (десктоп)
- Как подключиться с телефона

## Совместимость с Zapret / Booster

Когда VPN включён, весь трафик идёт через туннель — Discord и другие сервисы работают через него.
Zapret/Booster при включённом VPN **не нужны** и могут конфликтовать с маршрутизацией.
**Рекомендация пользователям:** отключать Zapret/Booster когда VPN активен.
