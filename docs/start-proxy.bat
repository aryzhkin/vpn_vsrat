@echo off
chcp 65001 >nul 2>nul
title VPN Proxy

if not exist sslocal.exe (
    echo.
    echo  sslocal.exe не найден!
    echo.
    echo  1. Скачай: https://github.com/shadowsocks/shadowsocks-rust/releases
    echo     Файл: shadowsocks-...-x86_64-pc-windows-msvc.zip
    echo  2. Извлеки sslocal.exe в эту папку
    echo.
    pause
    exit /b 1
)

if not exist key.txt (
    echo.
    echo  key.txt не найден!
    echo.
    echo  Создай файл key.txt в этой папке
    echo  и вставь в него ключ ss://...
    echo.
    pause
    exit /b 1
)

set /p KEY=<key.txt

echo.
echo  Прокси работает: 127.0.0.1:1080
echo  Не закрывай это окно.
echo.

sslocal.exe --server-url "%KEY%" -b 127.0.0.1:1080
pause
