#-- coding utf-8 --
import telebot
import requests
import pymysql
from user import User

times = ('Corinthians', 'São Paulo', 'Palmeiras', 'Grêmio', 'Vasco', 'Flamengo', 'Cruzeiro', 'Botafogo', 'Internacional')

conn = pymysql.connect(
    host='localhost', 
    user='root', 
    passwd='root', 
    db='usuarios_telegram'
)

user = User()

API_TOKEN = '5200899633:AAFcRLNjNo6Y23Ua0zWFaJs2ZblafLxGZN8' #KADJINSPKN -> KadjinSPKNBot
bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    cid = message.chat.id
    bot.reply_to(message, f'Esse é o bot de Noticias do Torcedor Apaixonado por futebol.')
    bot.send_message(cid, f'Nosso id é {str(cid)}, enviaremos notícias do seu clube do coração.')
    msg = bot.reply_to(message, f'Para se cadastrar, começe digitando seu nome:')
    bot.register_next_step_handler(msg, process_name_step)


def process_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        user.chatId = chat_id
        user.name = name

        msg = bot.reply_to(message, f'Opa {name}, beleza. Pode nos dizer qual a sua idade?')
        bot.register_next_step_handler(msg, process_age_step)

    except Exception as e:
        bot.reply_to(message, e)

 
def process_age_step(message):
    try:
        chat_id = message.chat.id
        age = message.text

        if not age.isdigit():
            msg = bot.reply_to(message, f'Puts {user.name}, parece que essa não é uma idade válida.')
            bot.register_next_step_handler(msg, process_age_step)
            return

        user.age = age

        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add(*times)
        msg_time = bot.reply_to(message, 'Escolha seu time do coração:', reply_markup=markup)
        bot.register_next_step_handler(msg_time, process_team_step)

    except Exception as e:
        bot.reply_to(message, e)


def process_team_step(message):
    try:
        chat_id = message.chat.id
        team = message.text

        if(team not in times):
            raise Exception('Time inválido, escolha um time do coração.')

        user.team = team
        msg = bot.reply_to(message, 'Digite seu email:')
        bot.register_next_step_handler(msg, process_email_step)

    except Exception as e:
        bot.reply_to(message, e)


def process_email_step(message):
    # try:
        chat_id = message.chat.id
        email = message.text
        user.email = email
        save_data()
        bot.reply_to(message, f'Opa {user.name}, Obrigado por se cadastrar!')

    # except Exception as e:
    #     bot.reply_to(message, e)


def save_data():
    print(user)
    sql = 'insert into usuarios (nome, email, idade, chatId, propriedade) values (%s, %s, %s, %s, %s)'
    values = (user.name, user.email, user.age, user.chatId, user.team)
    cur = conn.cursor()
    cur.execute(sql, values)
    conn.commit()
    conn.close()


bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
print("Bot rodando...")
bot.polling()