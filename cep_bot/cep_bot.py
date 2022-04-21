#-- coding utf-8 --
import telebot
import json
import urllib

API_TOKEN = ''
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    cid = message.chat.id
    bot.reply_to(message, f'''
        Olá, esse é um bot criado por Pedro Portella para Consultas de CEP \n
        Nosso ID é {str(cid)}
    ''')
    send_cep(message)

@bot.message_handler(commands=['help'])
def send_help(message):
    cid = message.chat.id
    bot.reply_to(message, f'''
Selecione uma das opções abaixo:
Opção 1: /cep
Opção 2: /contato
Opção 3: /help
    ''')
    bot.send_message(cid, 'Obrigado por usar nosso bot!')


@bot.message_handler(commands=['contato'])
def send_categories(message):
    bot.reply_to(message, '''
Para entrar em contato comigo, envie um email para: pedro.kadjin.sg@gmail.com
LinkedIn: https://www.linkedin.com/in/pedro-padilha-portella-02a67318a/
''')


@bot.message_handler(commands=['cep'])
def send_cep(message):
    cid = message.chat.id
    msg_cep = bot.reply_to(message, f'Digite o CEP que deseja consultar:')
    bot.register_next_step_handler(msg_cep, get_cep)


def get_cep(message):
    try:
        cid = message.chat.id
        cep = message.text.replace('-', '').replace('.', '')
        url = f"https://viacep.com.br/ws/{cep}/json/"

        response = urllib.request.urlopen(url)
        data = json.loads(response.read().decode('utf-8'))
        dict_data = dict(data)
        print(dict_data)

        bot.send_message(cid, f'''
CEP: {dict_data['cep']}
Logradouro: {dict_data['logradouro']}
Bairro: {dict_data['bairro']}
Localidade: {dict_data['localidade']}
UF: {dict_data['uf']}
        ''')
    except Exception as error:
        print(error)
        bot.reply_to(message, 'Ocorreu um erro na sua consulta de CEP, verifique se o CEP está correto, espere alguns minutos e tente novamente.')


print("CEP Bot rodando...")
bot.polling()