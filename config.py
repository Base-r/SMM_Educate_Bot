from environs import Env
from datetime import datetime as dt, timedelta
from foobar import FoobarDB
import datetime
import re

env = Env()
env.read_env()

TOKEN = env.str("TOKEN")
maxChat = int(env.str("ADMIN"))
z_chat = int(env.str("Z_CHAT"))
bodryak = env.str("BODROESLOVO")
adminchat_id = []

cht = env.str("ADMINCHAT").split(',')
for i in cht:
    adminchat_id.append(int(i))

def spreadidfromssylka(ssylka:str):
    sdf = ssylka.split('/')
    return sdf[5]
def name(message):
    name = 'No name'
    try:
        return message.from_user.first_name
    except:
        try:
            return message.from_user.username
        except:
            try:
                return message.from_user.full_name
            except:
                return name
def floatG(st):
    if st == None:
        return 0.0
    if isinstance(st, (int,)):
        return float(st)
    elif isinstance(st, (str,)):
        try:
            if st == ' ' or st == '':
                return 0.0
            return float(st.replace(',', '.').replace(' ', '').replace(' ', ''))
        except:
            return 0.0
            # print(st)
    else:
        return float(st)
def defloatG(st):
    if st == None:
        return '0.0'
    abc = str(st)
    if abc == '':
        return '0.0'
    try:
        abc = abc.replace(' ', '').replace(' ', '').replace(' ', '')
    except:
        print(abc)
    try:
        abc = abc.replace('.', ',')
    except:
        print(abc)
    finally:
        return abc
def undateGoogle(dat):
    # вернет дату из числа 45555 в формате даты ГГГГ-ММ-ЧЧ время
    stData = dt.strptime('30.12.1899', "%d.%m.%Y")
    try:
        stData = dt.strptime(dat, '%d.%m.%Y')
        mgd = 'неверный формат'
    except:
        try:
            stData += timedelta(dat)  # print(stData)
        except:
            mgd = 'формат yt '
    return stData
def undateGoogleStr(dat):
    # вернет дату из числа 45555 в формате строки ГГГГ-ММ-ЧЧ
    stData = dt.strptime('30.12.1899', "%d.%m.%Y")
    try:
        stData = dt.strptime(dat, '%d.%m.%Y')
        mgd = 'неверный формат'
    except:
        try:
            stData += timedelta(dat)  # print(stData)
        except:
            mgd = 'формат yt '
    return stData.strftime("%d.%m.%Y")
def dateGoogle(dat):
    stData = dt.strptime('30.12.1899', "%d.%m.%Y")
    try:
        stt = dt.strptime(dat, '%d.%m.%Y')
        stp = (stt - stData).days  # print(stData)
        return stp
    except:
        mgd = 'формат t'
        return 0
def srokd(datasr):
    vivod = datasr
    if isinstance(datasr, (int,)):
        vivod = (timedelta(int(datasr)) + datetime.date.today()).strftime("%d.%m.%Y")
    try:
        return vivod
    except:
        return datetime.date.today().strftime("%d.%m.%Y")
def poiskdat(dat):
    pattern = r'/(0?[1-9]|[12][0-9]|3[01])[\/\-\.](0?[1-9]|1[012])[ \/\.\-]/'
    dat_txt = r"\d{1,2}\/\d{2}\/20(?:[6-8]\d|9[0-5])"
    poisk = re.search(dat_txt, dat)
    print(poisk.string[poisk.start(0)])
