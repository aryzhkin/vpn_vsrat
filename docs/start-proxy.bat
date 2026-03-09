@echo off
title VPN Proxy

if not exist sslocal.exe (
    echo.
    echo  sslocal.exe not found!
    echo.
    echo  1. Download: https://github.com/shadowsocks/shadowsocks-rust/releases
    echo     File: shadowsocks-...-x86_64-pc-windows-msvc.zip
    echo  2. Extract sslocal.exe to this folder
    echo.
    pause
    exit /b 1
)

if not exist key.txt (
    echo.
    echo  key.txt not found!
    echo.
    echo  Create key.txt in this folder
    echo  and paste your ss://... key
    echo.
    pause
    exit /b 1
)

set /p KEY=<key.txt

echo.
echo  Proxy running: 127.0.0.1:1080
echo  Close this window to stop.
echo.

sslocal.exe --server-url "%KEY%" -b 127.0.0.1:1080
pause
