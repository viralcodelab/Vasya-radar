#!/bin/bash

echo "🚀 Автоматический деплой Лид-Радар бота на Koyeb"
echo ""

# Проверка наличия Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен. Установите Docker Desktop для Windows."
    exit 1
fi

echo "✅ Docker найден"
echo ""

# Создание Docker образа
echo "📦 Создание Docker образа..."
cd "D:\Сайти\Music plugin\lead-radar-bot"
docker build -t lead-radar-bot .

echo "✅ Docker образ создан"
echo ""

echo "🎯 Следующие шаги:"
echo "1. Зарегистрируйтесь на https://app.koyeb.com (бесплатно)"
echo "2. Создайте новый сервис: Deploy → Docker"
echo "3. Загрузите образ или подключите GitHub"
echo "4. Добавьте переменные окружения:"
echo "   BOT_TOKEN=8902728328:AAH_xJy4n1QJrd-wKP95kg-3f9w1eabJm_k"
echo "   API_ID=30788345"
echo "   API_HASH=81b2e1f9b800e4e0065b9fca201c40c5"
echo "   PHONE_NUMBER=+48694707313"
echo "   ADMIN_ID=5558876395"
echo ""
echo "Или используйте упрощённый вариант через GitHub..."
