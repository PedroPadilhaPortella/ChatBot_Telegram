#-- coding utf-8 --
import telebot

API_TOKEN = ''
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    cid = message.chat.id
    bot.reply_to(message, f'Olá, esse é um bot criado por Pedro Portella\nNosso ID é {str(cid)}')


@bot.message_handler(commands=['help'])
def send_help(message):
    cid = message.chat.id
    msg_help = bot.reply_to(message, f'''
Selecione uma das opções abaixo:\n
Opção 1: /cadastro\n
Opção 2: /categorias\n
Opção 3: /contato
''')
    bot.send_message(cid, 'Obrigado por usar nosso bot!')


@bot.message_handler(commands=['categorias'])
def send_categories(message):
    cid = message.chat.id
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add('Categoria 1', 'Categoria 2', 'Categoria 3')
    msg_cat = bot.reply_to(message, 'Escolha uma das categorias abaixo:', reply_markup=markup)


@bot.message_handler(commands=['contato'])
def send_categories(message):
    cid = message.chat.id
    msg_cct = bot.reply_to(message, '''
Para entrar em contato comigo, envie um email para:\n
pedro.kadjin.sg@gmail.com
LinkedIn: https://www.linkedin.com/in/pedro-padilha-portella-02a67318a/
''')


print("Bot rodando...")
bot.polling()