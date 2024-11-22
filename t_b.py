import telebot
import random

API_TOKEN = "8061173589:AAE-d5G9ZpWhH4nGXxRuNdyrogdmvN-tccM"  # Укажи свой токен
bot = telebot.TeleBot(API_TOKEN)

questions = {
    'easy': [
        {"question": "Какой океан самый большой?", "options": ["Атлантический", "Индийский", "Тихий", "Северный Ледовитый"], "answer": "Тихий"},
        {"question": "Какой континент считается родиной пингвинов?", "options": ["Австралия", "Антарктида", "Африка", "Южная Америка"], "answer": "Антарктида"}
    ],
    'medium': [
        {"question": "Какая столица Канады?", "options": ["Торонто", "Оттава", "Ванкувер", "Монреаль"], "answer": "Оттава"},
        {"question": "Какой самый длинный река в мире?", "options": ["Нил", "Амазонка", "Миссисипи", "Янцзы"], "answer": "Нил"}
    ],
    'hard': [
        {"question": "Какое государство является самым маленьким в мире?", "options": ["Монако", "Ватикан", "Сингапур", "Люксембург"], "answer": "Ватикан"},
        {"question": "Какой самый высокий водопад в мире?", "options": ["Тугела", "Анхель", "Игуасу", "Ниагара"], "answer": "Анхель"}
    ]
}

# Словарь для отслеживания пользователей
user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Хочешь поиграть в викторину по географии? Выбери уровень сложности: /easy, /medium, /hard")

@bot.message_handler(commands=['easy', 'medium', 'hard'])
def select_difficulty(message):
    level = message.text[1:]  # Получаем уровень сложности
    if level in questions:
        user_data[message.chat.id] = {"level": level, "score": 0, "current_question": 0}
        send_question(message.chat.id)
    else:
        bot.send_message(message.chat.id, "Такого уровня сложности нет. Пожалуйста, выбери /easy, /medium или /hard.")

def send_question(chat_id):
    user_info = user_data[chat_id]
    level = user_info["level"]
    question_data = questions[level][user_info["current_question"]]
    
    question_text = question_data["question"] + "\n" + "\n".join(question_data["options"])
    bot.send_message(chat_id, question_text)

@bot.message_handler(func=lambda message: message.chat.id in user_data)
def check_answer(message):
    user_info = user_data[message.chat.id]
    level = user_info["level"]
    question_data = questions[level][user_info["current_question"]]

    correct_answer = question_data["answer"]
    if message.text == correct_answer:
        user_info["score"] += 1
        bot.send_message(message.chat.id, "Верно! У тебя сейчас " + str(user_info["score"]) + " очков.")
    else:
        bot.send_message(message.chat.id, "Неправильно. Правильный ответ: " + correct_answer)
        
    user_info["current_question"] += 1

    if user_info["current_question"] < len(questions[level]):
        send_question(message.chat.id)
    else:
        bot.send_message(message.chat.id, f"Игра окончена! Твой результат: {user_info['score']} очков.")
        del user_data[message.chat.id]  # Очищаем данные пользователя

if __name__ == '__main__':
    bot.polling(none_stop=True)