# 🚀 Инструкция по развертыванию Лид-Радар бота

## Вариант 1: Railway.app (Рекомендуется - самый простой)

### Шаги:

1. **Зарегистрируйтесь на Railway.app:**
   - Перейдите на https://railway.app
   - Нажмите "Start a New Project"
   - Войдите через GitHub (если нет аккаунта - создайте на github.com)

2. **Создайте GitHub репозиторий:**
   - Перейдите на https://github.com/new
   - Название: `lead-radar-bot`
   - Сделайте репозиторий Private (приватным)
   - Нажмите "Create repository"

3. **Загрузите код на GitHub:**
   ```bash
   cd "D:\Сайти\Music plugin\lead-radar-bot"
   git remote add origin https://github.com/ВАШ_USERNAME/lead-radar-bot.git
   git branch -M main
   git push -u origin main
   ```

4. **Деплой на Railway:**
   - В Railway нажмите "Deploy from GitHub repo"
   - Выберите `lead-radar-bot`
   - Railway автоматически обнаружит Python проект

5. **Настройте переменные окружения в Railway:**
   Перейдите в Variables и добавьте:
   ```
   BOT_TOKEN=8902728328:AAH_xJy4n1QJrd-wKP95kg-3f9w1eabJm_k
   API_ID=30788345
   API_HASH=81b2e1f9b800e4e0065b9fca201c40c5
   PHONE_NUMBER=+48694707313
   ADMIN_ID=5558876395
   ```

6. **Первый запуск - авторизация userbot:**
   - В Railway откройте Logs (логи)
   - Вы увидите запрос кода подтверждения
   - Telegram отправит вам SMS с кодом
   - Введите код в консоли Railway

7. **Готово!** Бот работает 24/7

---

## Вариант 2: Render.com (Альтернатива)

1. Перейдите на https://render.com
2. Зарегистрируйтесь через GitHub
3. Нажмите "New" → "Web Service"
4. Подключите GitHub репозиторий
5. Настройки:
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`
6. Добавьте Environment Variables (как в Railway)
7. Нажмите "Create Web Service"

---

## Вариант 3: Без GitHub - PythonAnywhere (если нет GitHub)

1. Зарегистрируйтесь на https://www.pythonanywhere.com (бесплатный план)
2. Откройте "Files" → "Upload a file"
3. Загрузите все файлы проекта:
   - `main.py`, `bot.py`, `userbot.py`, `filter.py`
   - `requirements.txt`
   - Папку `config/` с файлами
4. Откройте "Consoles" → "Bash"
5. Выполните команды:
   ```bash
   cd ~
   pip install -r requirements.txt
   python main.py
   ```
6. Когда появится запрос кода - введите код из SMS

⚠️ **Важно:** На PythonAnywhere бесплатный план ограничен, и бот может не работать постоянно.

---

## Вариант 4: Koyeb (Проще всех, с GitHub)

1. Зарегистрируйтесь на https://app.koyeb.com
2. Нажмите "Create App"
3. Выберите "GitHub" как источник
4. Выберите репозиторий `lead-radar-bot`
5. Настройки оставьте по умолчанию
6. Добавьте Environment Variables
7. Нажмите "Deploy"

---

## Вариант 5: Fly.io (Для продвинутых)

1. Установите Fly CLI: https://fly.io/docs/hands-on/install-flyctl/
2. Выполните:
   ```bash
   cd "D:\Сайти\Music plugin\lead-radar-bot"
   fly auth login
   fly launch
   ```
3. Следуйте инструкциям на экране
4. Добавьте secrets:
   ```bash
   fly secrets set BOT_TOKEN=8902728328:AAH_xJy4n1QJrd-wKP95kg-3f9w1eabJm_k
   fly secrets set API_ID=30788345
   fly secrets set API_HASH=81b2e1f9b800e4e0065b9fca201c40c5
   fly secrets set PHONE_NUMBER=+48694707313
   fly secrets set ADMIN_ID=5558876395
   ```
5. Деплой: `fly deploy`

---

## ⚡ Самый быстрый способ (Railway - 5 минут)

Я рекомендую **Railway.app** - это самый простой вариант:

1. ✅ Бесплатный план (500 часов/месяц)
2. ✅ Автоматический деплой при push в GitHub
3. ✅ Простая настройка переменных окружения
4. ✅ Удобные логи для ввода кода авторизации
5. ✅ Работает 24/7

---

## 📞 Что делать после деплоя?

1. Откройте логи на хостинге
2. Вы увидите запрос: "Please enter the code you received:"
3. Telegram отправит вам SMS с кодом
4. Введите этот код в консоли
5. Если у вас двухфакторная аутентификация - введите пароль
6. Готово! Бот авторизован и начнёт мониторить каналы

---

## 🔧 Тестирование бота

После успешного деплоя:

1. Откройте Telegram
2. Найдите вашего бота (имя, которое вы давали @BotFather)
3. Напишите `/start`
4. Попробуйте команды:
   - `/channels` - список каналов
   - `/help` - справка

Бот начнёт присылать лиды автоматически!

---

## ❓ Нужна помощь?

**Какой вариант выбрать:**
- 🥇 **Railway.app** - если хотите самое простое решение
- 🥈 **Render.com** - альтернатива Railway
- 🥉 **PythonAnywhere** - если совсем нет опыта с Git/GitHub

**У меня есть аккаунт на GitHub?**
→ Используйте Railway или Render

**У меня нет аккаунта GitHub и не хочу разбираться:**
→ Используйте PythonAnywhere (загрузка файлов через веб-интерфейс)

---

Скажите, какой вариант вы хотите использовать, и я помогу с настройкой!
