#!/bin/bash
cd "$(dirname "$0")"

if ! command -v sslocal &>/dev/null; then
    echo ""
    echo "  sslocal не найден!"
    echo ""
    echo "  Установи через Homebrew:"
    echo "    brew install shadowsocks-rust"
    echo ""
    echo "  Если Homebrew не установлен:"
    echo "    /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    echo ""
    exit 1
fi

if [ ! -f key.txt ]; then
    echo ""
    echo "  key.txt не найден!"
    echo ""
    echo "  Создай файл key.txt в этой папке"
    echo "  и вставь в него ключ ss://..."
    echo ""
    exit 1
fi

KEY=$(tr -d '[:space:]' < key.txt)

echo ""
echo "  Прокси работает: 127.0.0.1:1080"
echo "  Нажми Ctrl+C чтобы остановить."
echo ""

sslocal --server-url "$KEY" -b 127.0.0.1:1080
