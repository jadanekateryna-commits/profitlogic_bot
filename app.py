import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# НОВЫЙ токен
TOKEN = "8931679192:AAGTp6miE_7Q9ZI6b49g5qOJqT6XaBK3cr0"
bot = telebot.TeleBot(TOKEN)

# Словарь для хранения данных пользователей
user_data = {}

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user_data[chat_id] = {}
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Начать опрос", callback_data="start_quiz"))
    
    bot.send_message(
        chat_id,
        "🐱 Привет! Я Екатерина — экономист «Прибыльной логики».\n\n"
        "Я помогаю предпринимателям находить скрытую прибыль, "
        "считать себестоимость и анализировать затраты.\n\n"
        "Нажмите на кнопку, чтобы начать опрос и получить чек-лист.",
        reply_markup=markup
    )

# Обработчик нажатия на кнопку "Начать опрос"
@bot.callback_query_handler(func=lambda call: call.data == "start_quiz")
def start_quiz(call):
    chat_id = call.message.chat.id
    bot.delete_message(chat_id, call.message.message_id)
    ask_name(chat_id)

# Вопрос 1: Имя
def ask_name(chat_id):
    msg = bot.send_message(chat_id, "Вопрос №1: Как к вам обращаться? Напишите ваше имя.")
    bot.register_next_step_handler(msg, save_name)

def save_name(message):
    chat_id = message.chat.id
    user_data[chat_id]['name'] = message.text
    ask_contact(chat_id)

# Вопрос 2: Контакт
def ask_contact(chat_id):
    msg = bot.send_message(chat_id, "Вопрос №2: Как с вами связаться? Напишите номер телефона или Telegram-ник.")
    bot.register_next_step_handler(msg, save_contact)

def save_contact(message):
    chat_id = message.chat.id
    user_data[chat_id]['contact'] = message.text
    ask_business(chat_id)

# Вопрос 3: О бизнесе
def ask_business(chat_id):
    msg = bot.send_message(
        chat_id,
        "Вопрос №3: Расскажите пару слов о вашем бизнесе:\n"
        "- Чем занимаетесь?\n"
        "- Приблизительная выручка в месяц?\n"
        "- Что беспокоит больше всего (цены, затраты, себестоимость)?"
    )
    bot.register_next_step_handler(msg, save_business)

def save_business(message):
    chat_id = message.chat.id
    user_data[chat_id]['business'] = message.text
    send_final_message(chat_id)

# Финальное сообщение с чек-листом (отправляет картинку)
def send_final_message(chat_id):
    checklist_image_url = "https://i.ibb.co/xShy84b4/10.png"
    
    bot.send_photo(
        chat_id,
        checklist_image_url,
        caption=f"🎁 Спасибо, {user_data[chat_id].get('name', '')}! Я получила ваши данные.\n\n"
                f"В подарок — мой чек-лист «10 точек утечки прибыли». Сохраните его!\n\n"
                "Что дальше? Я свяжусь с вами в ближайшее время (обычно в течение нескольких часов). "
                "Мы обсудим ваш случай и я дам первые рекомендации — совершенно бесплатно.\n\n"
                "А пока можете посмотреть мой канал:\n"
                "https://t.me/ProfitLogicmew\n\n"
                "До связи! 🐱"
    )
    
    # Отправка уведомления вам в личку
    bot.send_message(
        7687338241,
        f"Новая заявка!\n"
        f"Имя: {user_data[chat_id].get('name', 'Не указано')}\n"
        f"Контакт: {user_data[chat_id].get('contact', 'Не указан')}\n"
        f"О бизнесе: {user_data[chat_id].get('business', 'Не указано')}"
    )

# Команда /checklist (тоже отправляет картинку)
@bot.message_handler(commands=['checklist'])
def checklist(message):
    checklist_image_url = "https://i.ibb.co/xShy84b4/10.png"
    bot.send_photo(
        message.chat.id,
        checklist_image_url,
        caption="🎁 Держите мой чек-лист «10 точек утечки прибыли».\n\n"
                "Сохраните его — он поможет быстро проверить, где бизнес теряет деньги.\n\n"
                "Если хотите разобрать ваш случай — пишите в личку: @Katrin_ova"
    )

# Команда /info
@bot.message_handler(commands=['info'])
def info(message):
    bot.send_message(
        message.chat.id,
        "🐱 Привет! Я Екатерина — экономист «Прибыльной логики».\n\n"
        "Я помогаю предпринимателям находить скрытую прибыль, "
        "считать себестоимость и анализировать затраты.\n\n"
        "Чтобы получить консультацию — просто напишите мне в личку: @Katrin_ova\n\n"
        "Или переходите в мой канал: https://t.me/ProfitLogicmew"
    )

# Команда /about
@bot.message_handler(commands=['about'])
def about(message):
    bot.send_message(
        message.chat.id,
        "👋 Меня зовут Екатерина, я экономист-практик.\n\n"
        "Помогаю предпринимателям видеть реальную финансовую картину, "
        "находить слабые места и увеличивать прибыль.\n\n"
        "📊 Мой канал: https://t.me/ProfitLogicmew"
    )

# Команда /contact
@bot.message_handler(commands=['contact'])
def contact(message):
    bot.send_message(
        message.chat.id,
        "📬 Связаться со мной:\n\n"
        "📍 Беларусь: +375 44 469 56 60\n"
        "📍 Россия: +7 924 854 41 15\n\n"
        "📱 Telegram: @Katrin_ova\n"
        "📸 Instagram: https://www.instagram.com/profitlogicmew/\n"
        "📊 Канал: https://t.me/ProfitLogicmew\n\n"
        "Пишите — разберу ваш случай бесплатно. 💬"
    )

# Запуск бота
if __name__ == "__main__":
    print("Бот запущен и работает!")
    bot.infinity_polling()