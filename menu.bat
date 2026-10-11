@echo off
chcp 65001 >nul
cls
echo ╔════════════════════════════════════════════════════════════╗
echo ║          🚀 ЛИД-РАДАР - БЫСТРЫЙ СТАРТ                     ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo Выберите действие:
echo.
echo [1] 💻 Запустить бота ЛОКАЛЬНО (на этом компьютере)
echo [2] ☁️  Инструкция по деплою на ОБЛАКО (24/7)
echo [3] 📋 Список отслеживаемых каналов
echo [4] ⚙️  Настройки бота
echo [5] ❌ Выход
echo.
set /p choice="Введите номер (1-5): "

if "%choice%"=="1" goto local
if "%choice%"=="2" goto cloud
if "%choice%"=="3" goto channels
if "%choice%"=="4" goto settings
if "%choice%"=="5" exit
goto menu

:local
cls
echo ╔════════════════════════════════════════════════════════════╗
echo ║          💻 ЛОКАЛЬНЫЙ ЗАПУСК                              ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo ⚠️  ВАЖНО:
echo    - Бот будет работать только пока компьютер включён
echo    - При первом запуске придёт SMS с кодом
echo    - Номер телефона: +48694707313
echo.
set /p confirm="Запустить бота? (Y/N): "
if /i "%confirm%"=="Y" (
    start.bat
) else (
    goto menu
)
goto end

:cloud
cls
echo ╔════════════════════════════════════════════════════════════╗
echo ║          ☁️  ДЕПЛОЙ НА ОБЛАКО (24/7)                      ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo 🎯 РЕКОМЕНДУЕМЫЙ СПОСОБ: Render.com
echo.
echo Шаги:
echo 1. Откройте: https://render.com
echo 2. Войдите через GitHub
echo 3. New Web Service → выберите lead-radar-bot
echo 4. Добавьте переменные окружения (смотри .env файл)
echo 5. Deploy!
echo.
echo 📄 Подробная инструкция: QUICK_START.md
echo.
echo Варианты облачных хостингов:
echo   ✅ Render.com (рекомендуется)
echo   ✅ Railway.app
echo   ✅ Koyeb.com
echo   ✅ Fly.io
echo.
pause
goto menu

:channels
cls
echo ╔════════════════════════════════════════════════════════════╗
echo ║          📋 ОТСЛЕЖИВАЕМЫЕ КАНАЛЫ                          ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
type config\channels.json
echo.
echo Каналы можно изменить в файле: config\channels.json
echo Или через команду бота: /add_channel @название
echo.
pause
goto menu

:settings
cls
echo ╔════════════════════════════════════════════════════════════╗
echo ║          ⚙️  НАСТРОЙКИ БОТА                               ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo 📱 Ваши текущие настройки:
echo.
echo Bot Token: 8902728328:AAH_xJy4n***************
echo API ID: 30788345
echo Phone: +48694707313
echo Admin ID: 5558876395
echo.
echo Для изменения отредактируйте файл: .env
echo.
pause
goto menu

:end
exit
