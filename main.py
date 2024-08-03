import telebot
import func as call
from telebot import types

bot = telebot.TeleBot('YOUR_TELEGRAM_BOT_TOKEN')

# Globals
HISTORY = {}
GENRE = 'Horror'
STORE = []


@bot.message_handler(commands= ['start'])
def list_options(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    horror = types.InlineKeyboardButton('Horror',callback_data='gh')
    comedy = types.InlineKeyboardButton('Comedy',callback_data='gc')
    adventure = types.InlineKeyboardButton('Adventure',callback_data='ga')
    mystery = types.InlineKeyboardButton('Mystery',callback_data='gm')
    fantasy = types.InlineKeyboardButton('Fantasy',callback_data='gf')
    Romentic = types.InlineKeyboardButton('Romentic',callback_data='gr')
    cancel = types.InlineKeyboardButton('Cancel',callback_data='can')
    markup.add(horror,comedy,adventure,mystery,fantasy,Romentic,cancel)
    bot.send_message(message.chat.id,'Select anyone:',reply_markup=markup)

@bot.callback_query_handler(func=lambda call:True)
def initiate_story(callback):
    global STORE, GENRE, HISTORY
    if callback.message:
        if callback.data == 'gh':
            bot.send_message(callback.message.chat.id,'Get ready for the horror...')
            STORE = call.initiate_story('Horror')
            GENRE = "Horror"
            markup = types.InlineKeyboardMarkup(row_width=1)
            op1 = types.InlineKeyboardButton(str(STORE[1]),callback_data='o1')
            op2 = types.InlineKeyboardButton(STORE[2],callback_data='o2')
            op3 = types.InlineKeyboardButton("Exit",callback_data='ex')
            markup.add(op1,op2,op3)
            bot.send_message(callback.message.chat.id, str(STORE[0]) + "\n Select any option:", reply_markup=markup)
        elif callback.data == 'gc':
            bot.send_message(callback.message.chat.id,'Hehehehehe, Check this out...')
            STORE = call.initiate_story('Comedy')
            GENRE = "Comedy"
            markup = types.InlineKeyboardMarkup(row_width=1)
            op1 = types.InlineKeyboardButton(str(STORE[1]),callback_data='o1')
            op2 = types.InlineKeyboardButton(STORE[2],callback_data='o2')
            op3 = types.InlineKeyboardButton("Exit",callback_data='ex')
            markup.add(op1,op2,op3)
            bot.send_message(callback.message.chat.id, str(STORE[0]) + "\n Select any option:", reply_markup=markup)
        elif callback.data == 'ga':
            bot.send_message(callback.message.chat.id,'Are you ready for a new adventure?...')
            STORE = call.initiate_story('Adventure')
            GENRE = "Adventure"
            markup = types.InlineKeyboardMarkup(row_width=1)
            op1 = types.InlineKeyboardButton(str(STORE[1]),callback_data='o1')
            op2 = types.InlineKeyboardButton(STORE[2],callback_data='o2')
            op3 = types.InlineKeyboardButton("Exit",callback_data='ex')
            markup.add(op1,op2,op3)
            bot.send_message(callback.message.chat.id, str(STORE[0]) + "\n Select any option:", reply_markup=markup)
        elif callback.data == 'gm':
            bot.send_message(callback.message.chat.id,'Voh razz uske sath chala gaya...')
            STORE = call.initiate_story('Mystery')
            GENRE = "Mystery"
            markup = types.InlineKeyboardMarkup(row_width=1)
            op1 = types.InlineKeyboardButton(str(STORE[1]),callback_data='o1')
            op2 = types.InlineKeyboardButton(STORE[2],callback_data='o2')
            op3 = types.InlineKeyboardButton("Exit",callback_data='ex')
            markup.add(op1,op2,op3)
            bot.send_message(callback.message.chat.id, str(STORE[0]) + "\n Select any option:", reply_markup=markup)
        elif callback.data == 'gf':
            bot.send_message(callback.message.chat.id,'Aja le chalu tumhe taro ke shehar main...')
            STORE = call.initiate_story('Fantasy')
            GENRE = "Fantasy"
            markup = types.InlineKeyboardMarkup(row_width=1)
            op1 = types.InlineKeyboardButton(str(STORE[1]),callback_data='o1')
            op2 = types.InlineKeyboardButton(STORE[2],callback_data='o2')
            op3 = types.InlineKeyboardButton("Exit",callback_data='ex')
            markup.add(op1,op2,op3)
            bot.send_message(callback.message.chat.id, str(STORE[0]) + "\n Select any option:", reply_markup=markup)
        elif callback.data == 'gr':
            bot.send_message(callback.message.chat.id,'Ek chaand sa roshan chehera...')
            STORE = call.initiate_story('Romentic')
            GENRE = "Romentic"
            markup = types.InlineKeyboardMarkup(row_width=1)
            op1 = types.InlineKeyboardButton(str(STORE[1]),callback_data='o1')
            op2 = types.InlineKeyboardButton(STORE[2],callback_data='o2')
            op3 = types.InlineKeyboardButton("Exit",callback_data='ex')
            markup.add(op1,op2,op3)
            bot.send_message(callback.message.chat.id, str(STORE[0]) + "\n Select any option:", reply_markup=markup)
        elif callback.data == 'can':
            bot.send_message(callback.message.chat.id,'Bolo pencil, Aapki story cancel')
        elif callback.data == 'ex':
            if len(HISTORY) == 0:
                bot.send_message(callback.message.chat.id, 'Will wait for you to comeback soon...')
            else:
                bot.send_message(callback.message.chat.id, 'Never mind, see you next time...')
        elif callback.data == 'o1':
            option_text = callback.message.reply_markup.keyboard[0][0].text
            HISTORY[len(HISTORY)+1] = [str(STORE[0]), option_text]
            if len(STORE)<=3:

                STORE = call.continue_story(HISTORY, GENRE)
            else:
                STORE = call.terminate_story(HISTORY, GENRE)
            markup = types.InlineKeyboardMarkup(row_width=1)
            op1 = types.InlineKeyboardButton(str(STORE[1]),callback_data='o1')
            op2 = types.InlineKeyboardButton(STORE[2],callback_data='o2')
            op3 = types.InlineKeyboardButton("Exit",callback_data='ex')
            markup.add(op1,op2,op3)
            bot.send_message(callback.message.chat.id, str(STORE[0]) + "\n Select any option:", reply_markup=markup)


        elif callback.data == 'o2':
            option_text = callback.message.reply_markup.keyboard[1][0].text
            HISTORY[len(HISTORY)+1] = [str(STORE[0]), option_text]
            if len(STORE)<=3:

                STORE = call.continue_story(HISTORY, GENRE)
            else:
                STORE = call.terminate_story(HISTORY, GENRE)
            markup = types.InlineKeyboardMarkup(row_width=1)
            op1 = types.InlineKeyboardButton(str(STORE[1]),callback_data='o1')
            op2 = types.InlineKeyboardButton(STORE[2],callback_data='o2')
            op3 = types.InlineKeyboardButton("Exit",callback_data='ex')
            markup.add(op1,op2,op3)
            bot.send_message(callback.message.chat.id, str(STORE[0]) + "\n Select any option:", reply_markup=markup)
        else:
            pass


bot.polling()