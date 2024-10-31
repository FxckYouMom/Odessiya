from telebot import TeleBot, types
from config import API_TOKEN
from cardusdt import CFULLDATA
from bankusdt import BFULLDATA
from steamitem import DATASTICKER  # Import DATASTICKER from the new file

bot = TeleBot(API_TOKEN)

# Dictionary to map sticker names to their corresponding data
STICKER_DATA = {
    "Count": "76561199227442738",
    "0100" : "76561199152948282",
    "Silver": "76561199132940278",
    "Main": "76561199486163596"
}

# Command to send a welcome message with buttons
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button1 = types.KeyboardButton("Карта $")
    button2 = types.KeyboardButton("Реал $")
    button3 = types.KeyboardButton("Стім")
    markup.add(button1, button2, button3)
    
    bot.send_message(message.chat.id, "Виберіть опцію:", reply_markup=markup)

# Handle button "Карта $"
@bot.message_handler(func=lambda message: message.text == "Карта $")
def handle_button1(message):
    if CFULLDATA:
        formatted_data = "\n".join(CFULLDATA)
        bot.send_message(message.chat.id, formatted_data)
    else:
        bot.send_message(message.chat.id, "Дані відсутні.")

# Handle button "Реал $"
@bot.message_handler(func=lambda message: message.text == "Реал $")
def handle_button2(message):
    if BFULLDATA:
        formatted_data = "\n".join(BFULLDATA)
        bot.send_message(message.chat.id, formatted_data)
    else:
        bot.send_message(message.chat.id, "Дані відсутні.")

# Handle button "Стікери"
@bot.message_handler(func=lambda message: message.text == "Стім")
def handle_stickers(message):
    # Create rows of buttons, with each row containing up to 5 buttons
    keyboard = []
    current_row = []
    for name in STICKER_DATA.keys():
        current_row.append(types.InlineKeyboardButton(name, callback_data=name))
        if len(current_row) == 5:  # If the row reaches 5 buttons, add it to the keyboard
            keyboard.append(current_row)
            current_row = []  # Reset the current row
    
    # If there are leftover buttons in current_row, add them to the keyboard
    if current_row:
        keyboard.append(current_row)

    reply_markup = types.InlineKeyboardMarkup(keyboard)
    bot.send_message(message.chat.id, "Оберіть Акк:", reply_markup=reply_markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    sticker_name = call.data
    if sticker_name in STICKER_DATA:
        data = STICKER_DATA[sticker_name]  # Get the data from the dictionary
        sticker_info = DATASTICKER(data)
        bot.send_message(call.message.chat.id, sticker_info)

# Start the bot
bot.polling()
