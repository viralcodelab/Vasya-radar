# 🚀 ГОТОВО К ДЕПЛОЮ! 

## ✅ Бот полностью готов к работе!

### Что уже сделано:
- ✅ Весь код написан и настроен
- ✅ Ваши токены добавлены в конфигурацию
- ✅ 10 каналов настроены для мониторинга
- ✅ Фильтры и ключевые слова настроены
- ✅ Git репозиторий создан

---

## 🎯 ЗАПУСК ЗА 5 МИНУТ (3 простых шага)

### Вариант 1: Render.com (Рекомендуется ⭐)

#### Шаг 1: Загрузите код на GitHub
1. Откройте https://github.com/new
2. Название: `lead-radar-bot`
3. Сделайте Private (приватный)
4. Нажмите "Create repository"

5. **Если у вас установлен Git**, откройте командную строку (Win+R → cmd):
```bash
cd "D:\Сайти\Music plugin\lead-radar-bot"
git remote add origin https://github.com/ВАШ_USERNAME/lead-radar-bot.git
git branch -M main
git push -u origin main
```

6. **Если НЕТ Git**: просто загрузите все файлы через веб-интерфейс GitHub:
   - На странице репозитория нажмите "uploading an existing file"
   - Перетащите все файлы из папки `lead-radar-bot`
   - Нажмите "Commit changes"

#### Шаг 2: Деплой на Render
1. Откройте https://render.com
2. "Sign Up" → войдите через GitHub
3. "New +" → "Web Service"
4. "Connect a repository" → выберите `lead-radar-bot`
5. Настройки:
   ```
   Name: lead-radar-bot
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: python main.py
   Instance Type: Free
   ```
6. Нажмите "Create Web Service"

#### Шаг 3: Добавьте переменные окружения
В разделе "Environment" добавьте (кнопка "Add Environment Variable"):

```
BOT_TOKEN
8902728328:AAH_xJy4n1QJrd-wKP95kg-3f9w1eabJm_k

API_ID
30788345

API_HASH
81b2e1f9b800e4e0065b9fca201c40c5

PHONE_NUMBER
+48694707313

ADMIN_ID
5558876395
```

#### Шаг 4: Авторизация (ВАЖНО!)
После деплоя:
1. Откройте "Shell" (вкладка справа)
2. Выполните: `python main.py`
3. Вам придёт SMS с кодом на +48694707313
4. Введите код в консоли Shell
5. Если есть 2FA - введите пароль
6. Готово! Закройте Shell - бот продолжит работать автоматически

---

### Вариант 2: Railway.app (Альтернатива)

1. https://railway.app → войдите через GitHub
2. "New Project" → "Deploy from GitHub repo" → `lead-radar-bot`
3. Добавьте те же переменные окружения (Variables)
4. Авторизация через Logs (см. выше)

---

### Вариант 3: Без GitHub - через Heroku CLI

Если совсем не хотите разбираться с GitHub:

1. Скачайте Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
2. Откройте командную строку:
```bash
cd "D:\Сайти\Music plugin\lead-radar-bot"
heroku login
heroku create lead-radar-bot
heroku config:set BOT_TOKEN=8902728328:AAH_xJy4n1QJrd-wKP95kg-3f9w1eabJm_k
heroku config:set API_ID=30788345
heroku config:set API_HASH=81b2e1f9b800e4e0065b9fca201c40c5
heroku config:set PHONE_NUMBER=+48694707313
heroku config:set ADMIN_ID=5558876395
git push heroku main
```

⚠️ **Внимание:** Heroku больше не предлагает бесплатный план

---

## 📱 После запуска

1. Найдите своего бота в Telegram (имя, которое вы дали @BotFather)
2. Напишите `/start`
3. Бот ответит приветствием
4. Лиды начнут приходить автоматически! 🎉

### Команды бота:
- `/start` - Приветствие
- `/help` - Справка
- `/channels` - Список каналов
- `/add_channel @название` - Добавить канал
- `/remove_channel @название` - Удалить канал

---

## ❓ Нужна помощь?

**Проблема: "не могу загрузить на GitHub"**
→ Используйте веб-интерфейс GitHub (drag & drop файлов)

**Проблема: "не могу ввести код в Shell"**
→ В Render есть интерактивный Shell справа, там можно вводить

**Проблема: "бот не работает"**
→ Проверьте Logs - там будет видна причина

---

## 🎯 Что я рекомендую:

**Самый простой путь:**
1. Зарегистрируйтесь на Render.com через GitHub (2 минуты)
2. Создайте репозиторий на GitHub и загрузите файлы (3 минуты)
3. Подключите репозиторий к Render (2 минуты)
4. Добавьте переменные окружения (2 минуты)
5. Авторизуйте бота в Shell (1 минута)

**Итого: 10 минут до полностью работающего бота!**

---

## 📂 Все файлы готовы в папке:
```
D:\Сайти\Music plugin\lead-radar-bot\
```

Просто следуйте инструкции выше, и всё заработает!

Если что-то непонятно - спрашивайте, я помогу! 🚀
