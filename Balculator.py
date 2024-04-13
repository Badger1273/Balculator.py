import telebot, datetime, time, math, re
from telebot import types

token = '' 
name_bot = 'Balculator_Bot'
bot = telebot.TeleBot(token)

time = 5 

start = """You are READY?"""

INF = """Information:
Стандартные функции:
    + - сложение;
    - - вычитание;
    \* - умножение;
    / - деление;
    \*\* - возведение в степнь.
    
Геометрические функции:
    cos(x) - косинус x;
    sin(x) - синус x;
    tg(x) - тангенс x;
    fact(x) - факториал x;
    sqrt(x) - квадратный корень х;
    sqr(x) - х в квадрате.

Логарифмы:
    log2(x) - логарифм х по основанию 2;
    lg(х) - десятичный логарифм х;
    ln(x) - натуральный логарифм x;
    log(b, х) - логарифм х по основанию b;

Система счисления:
    0bx - перевести двоичное число х в десятичное;
    0ox - перевести восьмиричное число х в десятичное;
    0xx - перевести шестнадцатиричное число х в десятичное;"""

pi = 3.141592653589793238462643 


def fact(float_):
    return math.factorial(float_)


def cos(float_):
    return math.cos(float_)


def sin(float_):
    return math.sin(float_)


def tg(float_):
    return math.tan(float_)
   
    
def tan(float_):
    return math.tan(float_)


def ln(float_):
    return math.log(float_)


def log(base, float_):
    return math.log(float_, base)


def lg(float_):
    return math.log10(float_)


def log2(float_):
    return math.log2(float_)


def exp(float_):
    return math.exp(float_)


@bot.message_handler(commands=['start', 'inf'])
def send_start(message):
    print('%s (%s): %s' %(message.chat.first_name, message.chat.username, message.text))
    msg = None

    if message.text.lower() == '/start':
        msg = bot.send_message(message.chat.id, start/, parse_mode='markdown')

    elif message.text.lower() == '/inf':
        msg = bot.send_message(message.chat.id, INF, parse_mode='markdown')
        
    if (msg):
        print('Ботий: %s'%msg.text)
        
        
@bot.message_handler(func = lambda message: True)
def answer_to_user(message):
    print('%s (%s): %s' %(message.chat.first_name, message.chat.username, message.text))
    msg = None

    user_message = message.text.lower()

    if name_bot:
        regex = re.compile(name_bot.lower())
        print(regex.search(user_message))
        if regex.search(user_message) == None:
            return

        regex = re.compile('%s[^a-z]'%(name_bot.lower()))
        user_message = regex.sub("", user_message)
    user_message = user_message.lstrip()
    user_message = user_message.rstrip()
    
    print(user_message)

    if user_message == 'start':
        msg = bot.send_message(message.chat.id, '*Start, %s*'%(message.chat.first_name), parse_mode='markdown')

    elif user_message == 'inf':
        msg = bot.send_message(message.chat.id, INF, parse_mode='markdown')

    else:
        try:
            answer = str(eval(user_message.replace(' ', '')))
            msg = bot.send_message(message.chat.id, user_message.replace(' ', '') + ' = ' + answer)
                
        except SyntaxError:
            msg = bot.send_message(message.chat.id, 'ERROR \nИсравьте ошибку и повторите снова')
        except NameError:
            msg = bot.send_message(message.chat.id, 'Переменная мне не известно. \nИсравьте ошибку и повторите снова')
        except TypeError:
            msg = bot.send_message(message.chat.id, 'Вы ошиблись в типах. \nИсравьте ошибку и повторите снова')
        except ZeroDivisionError:
            msg = bot.send_message(message.chat.id, 'На 0 делить НЕЛЬЗЯ!!!. \nИсравьте ошибку и повторите снова')

    if (msg):
        print('Ботий: %s'%msg.text)
        
        
@bot.inline_handler(func=lambda query: True)
def inline_answer_to_user(inline_query):
    answer = 0
    answer_list = []
    try:
        answer = str(eval(inline_query.query.lower().replace(' ', '')))
        answer_to_send = answer.replace('*', '\*')
        query_to_send = inline_query.query.replace('*', '\*').lower().replace(' ', '')

        answer_list.append(types.InlineQueryResultArticle(
            id = 0,
            title = 'Отправить с выражением',
            description='%s = %s' % (inline_query.query, answer),
            input_message_content = types.InputTextMessageContent(
                message_text = '%s = *%s*' % (query_to_send, answer_to_send),
                parse_mode = 'markdown'),
            thumb_url = icon
        ))

        answer_list.append(types.InlineQueryResultArticle(
            id = 1,
            title = 'Отправить без выражения',
            description='%s' % (answer),
            input_message_content = types.InputTextMessageContent(
                message_text = '*%s*' % (answer_to_send),
                parse_mode = 'markdown'),
            thumb_url = nicon
        ))
            
    except SyntaxError: answer = False
    except NameError: answer = False
    except TypeError: answer = False
    except ZeroDivisionError: answer = False
    
    if (not answer):    
        answer_list = []
        answer_list.append(types.InlineQueryResultArticle(
            id = 0,
            title = 'Балкулятор',
            description='Введите выражение\nДля справки \"/inf\"',
            input_message_content = types.InputTextMessageContent(message_text = 'Что-то здесь не так...')
        ))
    
    bot.answer_inline_query(inline_query.id, answer_list)
    
    
if (__name__ == '__main__'):
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print ('Настройка сети. Ожидайте... %s сек.'%time)
            time.sleep(time)
