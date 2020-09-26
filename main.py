import telebot
import akinator
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


# Setup the bot:

# You should insert your token as it is a personal field for each person i can't insert one.
token = ''

bot = telebot.TeleBot(token)

akinator_keyboard = InlineKeyboardMarkup()
akinator_keyboard.add(InlineKeyboardButton("Yes", callback_data="y"),
                                InlineKeyboardButton("I don't know", callback_data="i"),
                                InlineKeyboardButton("No", callback_data="n"),
                                InlineKeyboardButton("Probably yes", callback_data="p"),                     
                                InlineKeyboardButton("Probably no", callback_data="pn"))
                                

# Done with the Setup now we go for the main part:

# For running the Akinator we use the akinator lib
# there are 2 objects of akinator class that should be kept for all users:
# 1- The "aki = akinator.Akinator()" object which is the object for each person to track their answers
# 2- the "q = aki.start_game()" str which is the question that should be askes next.
# So we are going to have a dictionary where the template looks like this: { message.chat.id : [ aki , q ] , ... }
# As it's obvious the 0 index is the aki object and the 1 index is the question str

users = {}

@bot.message_handler(commands=['start','help'])
def initialization(message):
    bot.send_message(message.chat.id,'Hi there!\nWelcome to Akinator Telegram Bot!\nWrite: "Hi Akinator" to start the game!')

@bot.message_handler(func= lambda message: message.text.lower() == 'hi akinator')
def akinator_start(message):
    # go to line 23 to understand what is happening below if you got confused
    bot.send_message(message.chat.id,"You are now in the game!\nFirst consider a character in your mind and obviously don't tell me who you are thinking of becuase that's my job!\nThen i will ask you questions and you should answer with the prepared keyboard!\nEasy right?\nLet's get started!\nAnd one more thing! you can exit the game anywhere you want by typing /exit\nEnjoy!")
    aki_temp = akinator.Akinator()
    q_temp = aki_temp.start_game()
    users.update({message.chat.id:[aki_temp,q_temp]})
    bot.send_message(message.chat.id,users[message.chat.id][1],reply_markup=akinator_keyboard)
    # Users that are playing the game won't come to this function anymore

@bot.callback_query_handler(func=lambda call: True)
def getting_answer(call):
    if call.data == "y" or call.data == "n" or call.data == "i" or call.data == "p" or call.data == "pn":
        users[call.from_user.id][1] = users[call.from_user.id][0].answer(call.data)
        # Now if the progression is above 90 in this case as below, we are going to answer.
        # You can change the 95 to whatever number you want. ther higher it is the more accurate the akinators guess it will be.
        if users[call.from_user.id][0].progression >= 90:
            users[call.from_user.id][0].win()
            str_to_send = 'Your character is:\n' + str(users[call.from_user.id][0].first_guess['name']) + ' - (' + str(users[call.from_user.id][0].first_guess['description']) +')\n' + "Am I right?"
            msg = bot.send_message(call.from_user.id,str_to_send)
            del users[call.from_user.id]
            bot.register_next_step_handler(msg,am_i_right)
        # this block of code will send the next message to the user
        else:
            bot.send_message(call.from_user.id,users[call.from_user.id][1],reply_markup=akinator_keyboard)

def am_i_right(message):
    if message.text.lower() in ['yes','yeah','yeap','ofcourse']:# You can add more or change the whole if elif thing here. it's totally up to you
        bot.message_handler(message.chat.id,'Yay!')
    elif message.text.lower() in ['no','nope','na','nah']:
        bot.message_handler(message.chat.id,'Hof!')
    else:
        pass

@bot.message_handler(commands=['exit'])
def exit_game(message):
    if message.chat.id in users:
        del users[message.chat.id]
        bot.send_message(message.chat.id,'You exited the game!\nTo play again type "Hi Akinator"')
    else:
        bot.send_message(message.chat.id,'You were not in a game!\nTo start the game type "Hi Akinator"')
bot.polling()

# I hope you enjoyed the code! Any suggestions would be appriciated! take care :)