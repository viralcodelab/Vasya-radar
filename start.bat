@echo off
chcp 65001 >nul
echo ========================================
echo 🤖 Лид-Радар - Запуск бота
echo ========================================
echo.

cd /d "%~dp0"

echo 📦 Проверка зависимостей...
pip show aiogram >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Устанавливаю зависимости...
    pip install -r requirements.txt
    echo ✅ Зависимости установлены
) else (
    echo ✅ Зависимости уже установлены
)
echo.

echo 🚀 Запуск бота...
echo.
echo ⚡ ВАЖНО: При первом запуске вам придёт SMS с кодом
echo    Введите этот код когда увидите запрос
echo.
echo 📱 Код придёт на номер: +48694707313
echo.
echo ========================================
echo.

python main.py

pause
