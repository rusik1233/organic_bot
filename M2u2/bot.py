import telebot
from config import TOKEN1
from bot_logic import game_word, sort_trash
bot = telebot.TeleBot(TOKEN1)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Обработчик команды /start."""
    bot.send_message(message.chat.id, f'Привет {message.from_user.first_name}!')
    bot.reply_to(message, "Я твой Telegram бот. Напиши что-нибудь!")
    bot.reply_to(message, 'Советую написать /help')


@bot.message_handler(commands=['help'])
def send_command(message):
    """Обработчик команды /help."""
    bot.reply_to(message, 'Доступные команды: /start /sort')

@bot.message_handler(commands=['sort'])
def handle_sort(message):
    """Оюраюотчик команды /sort"""
    try:

        parts = message.text.split(maxsplit=1)
        #проверяем правильность ввода
        if len(parts) < 2:
            bot.reply_to(message, "Пожалуйста, укажите материал для сортировки. Например: /sort бумага")
            return

        _, material = parts


        sorting_result = sort_trash(material)


        bot.reply_to(message, sorting_result)

    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "Произошла ошибка при обработке вашего запроса.")


game_running = False
last_word_used = None


@bot.message_handler(commands=['startgame'])

def start_game(message):
    global game_running, last_word_used
    if game_running:
        bot.reply_to(message, "Игра уже запущена! Введите слово на букву, которая является последней в предыдущем слове.")
        return

    game_running = True
    last_word_used = None
    bot.reply_to(message, "Игра началась! Введите первое слово. Оно должно заканчиваться на букву, которая есть в списке животных (а, л, ь, й, с, п, х, к).")


@bot.message_handler(commands=['stop'])
def stop_game(message):
    global game_running, last_word_used
    if not game_running:
        bot.reply_to(message, "Извините, но я не понимаю. Советую написать /help")
        return

    game_running = False
    last_word_used = None
    bot.reply_to(message, "Игра остановлена.")


@bot.message_handler(func=lambda message: game_running)
def play_game(message):
    global game_running, last_word_used

    word = message.text.strip().lower()

    if not word.isalpha():
        bot.reply_to(message, "Пожалуйста, введите только буквы.")
        return

    if last_word_used is None:

        result = game_word(word)
        if result:
            animal, last_letter = result
            last_word_used = word
            bot.reply_to(message, f"Отлично! Ваше животное: {animal}. Теперь введите слово на букву '{last_letter}'.")
        else:
            bot.reply_to(message, "Неверное слово. Оно должно заканчиваться на русскию букву")
        return



    expected_start_letter = game_word(last_word_used)[1]
    if word.startswith(expected_start_letter):
        result = game_word(word)
        if result:
            animal, last_letter = result
            last_word_used = word
            bot.reply_to(message, f"Отлично! Ваше животное: {animal}. Теперь введите слово на букву '{last_letter}'.")
        else:
            bot.reply_to(message, "Неверное слово. Оно должно заканчиваться на букву русского алфавита")
    else:
        bot.reply_to(message, f"Неверное слово. Оно должно начинаться на букву '{expected_start_letter}'. Игра окончена.")
        game_running = False
        last_word_used = None

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if not game_running and message.text.startswith('/'):
        return
    if not game_running:
        bot.reply_to(message, "Игра не запущена. Используйте /startgame для начала.")

print("Bot is running...")
bot.infinity_polling()




