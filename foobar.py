import json
import os


class FoobarDB(object):
    def __init__(self, location):
        self.location = os.path.expanduser(location)
        self.load(self.location)

    def load(self, location):
        if os.path.exists(location):
            self._load()
        else:
            self.db = []
        return True

    def _load(self):
        self.db = json.load(open(self.location, "r", encoding='utf-8'))

    def authori(self, key):
        naiden = False
        try:
            for i, index in enumerate(self.db):
                if index['_id'] == key:
                    naiden = True
                    return True
                elif i == len(self.db) and not naiden:
                    return False
        except KeyError:
            print("No Value Can Be Found for " + str(key))
            return False

    def authoriEG(self, tel):
        naiden = False
        try:
            for i, index in enumerate(self.db):
                if index['_id'] == tel:
                    naiden = True
                    return True
                elif i == len(self.db) and not naiden:
                    return False
        except KeyError:
            print("No Value Can Be Found telefon " + str(tel))
            return False

    def dumpdb(self):
        try:
            json.dump(self.db, open(self.location, "w",encoding='utf-8'), ensure_ascii=False)
            return True
        except:
            return False

    def append(self, value):
        try:
            self.db.append(value)
            self.dumpdb()
        except Exception as e:
            print("[X] Error Saving Values to Database : " + str(e))
            return False

    def s4etplus(self):
        try:
            abc = int(self.get('0','value'))
            abc += 1
            self.db[0] = {"_id":"0","value": str(abc)}
            self.dumpdb()
            return str(abc)
        except:
            return "0"

    def update_one(self, key, value):
        try:
            self.db.append(value)
            self.dumpdb()
        except Exception as e:
            print("[X] Error Saving Values to Database : " + str(e))
            return False


    def get(self, key, pole):
        try:
            for i, index in enumerate(self.db):
                if index['_id'] == key:
                    return index[pole]
        except KeyError:
            print("No Value Can Be Found for " + str(key))
            return False
    def get_otdel_fio(self, otdel):
        try:
            spisok = []
            for i, index in enumerate(self.db):
                if index['otdel'] == otdel:
                    spisok.append(index['fio'])
            return spisok
        except KeyError:
            print("No Value Can Be Found for " + str(otdel))
            return False

    def delete(self, key):
        if not key in self.db:
            return False
        del self.db[key]
        self.dumpdb()
        return True

    def resetdb(self):
        self.db = []
        self.dumpdb()
        return True


class poles():
    viborka=None
    Dubli        =None
    PComment     =None
    PDDS         =None
    PSumma       =None
    PSummsNDS    =None
    Pcena        =None
    Pcontra      =None
    Pcodcontra = None
    Pdata        =None
    Ped          =None
    Pisto4       =None
    Pkol         =None
    Pmes         =None
    Pnapr        =None
    PnaprPolu4atel =None
    Pcodnapr = None
    Pnds         =None
    PndsVkl      =None
    PndsVsum     =None
    Pno          =None
    Pnomenkl     =None
    Pcodnomenkl = None
    Podrazd      =None
    Porg         =None
    Ppl          =None
    Prs4et       =None
    Psod         =1
    Pus15        =None
    Pval         =None
    Pvn          =None
    Pvx1         =None
    Pvx2         =None
    Reestr       =None
    dubli = None
    inn = None
    raboti       =None
    subconto1    =None
    subconto2    =None
    subconto3    =None
    vidoperAT    =None
    Ident        =None
    idvsmete = None
    idvzayavke = None
    data2 = None
    sklad2 = None
    # idвсмете	#id в заявке
    contragent = {'ООО "НОРД-Инвест"':'НОРД-ИНВЕСТ ООО',
                  'ООО "Бурятпроектреставрация"':'БУРЯТПРОЕКТРЕСТАВРАЦИЯ ООО',
                  'ООО "Байкалкомплект"':'БАЙКАЛКОМПЛЕКТ ООО',
                  'ООО "ДИТАЛ"':'ДИТАЛ ООО','ГК ООО':'ГК ООО',
                  'ООО "ЭЛЬКОТЕК"':'ЭЛЬКОТЕК ООО','ООО "Алмаз"':'АЛМАЗ ООО',
                  'ООО "НБС-Групп"':'НБС-ГРУПП ООО',
                  'ООО "Урбанистик девелопмент"':'Урбанистик девелопмент ООО',
                  'ООО "Камушек"':'Камушек ООО',
                  'ООО "КОНСАЛТИНГПЛЮС"':'КОНСАЛТИНГПЛЮС ООО',
                   'ИП Юлдашев Жахонгир Зарипбаевич' : 'ЮЛДАШЕВ Ж. З. (ИП)',
                  'ООО "Алмаз"':'АЛМАЗ ООО'

    }
    naprKod = {'БП-000106':'База','00-000036':'БРУ','БП-000102':'Выдрино',
               '00-000058':'Инфекционная больница','БП-000097':'Курумкан',
               'БП-000083':'Кабанск','БП-000075':'КЯХТА',
               '00-000052':'Лукодром','00-000037':'Нац. библиотека',
               '00-000057':'Нац. библиотека №2','00-000048':'Общий склад',
               'БП-000099':'Дивизка','БП-000096':'Газета','БП-000103':'БСМП',
               'БП-000095':'Боевая','БП-000077':'Аршан',
               'БП-000072':'Оконный цех','00-000056':'Онкология',
               '00-000031':'Офис','00-000060':'Поликлиника Тарбагатай',
               '00-000033':'Склад Р','00-000042':'Техника',
               'БП-000070':'Автотранспортная','БП-000111':'У К С Детский сад',
               'БП-000108':'ФССП','БП-000107':'Молодежный',
               '00-000051':'Школа Новоселенгинск','БП-000087':'Столярный цех',
               '00-000053':'Школа № 2 гарантийные обязательства',
               'БП-000124':'Онохой','БП-000113':'Максимиха',
               'БП-000128':'Школа Сотниково','БП-000105':'База Содномов М',
               'БП-000114':'ЧИТА театр','БП-000116':'Театр Ульгэр',
               '00-000055':'Онкология инж','БП-000122':'Верхняя Березовка',
               '00-000049':'Лаборатория','БП-000125':'Школа 32','БП-000129':'Гринпарк'}
    sklad = {'00-000034':'БП-000106','00-000039':'00-000057','00-000039':'00-000057','00-000040':'00-000057','00-000040':'00-000057','00-000041':'00-000057','00-000041':'00-000057','00-000049':'БП-000106','00-000055':'00-000056','00-000061':'00-000052','00-000062':'00-000060','00-000063':'00-000057','00-000063':'00-000057','00-000064':'БП-000106','00-000066':'00-000051','00-000067':'00-000051','00-000068':'00-000056','00-000069':'00-000052','БП-000071':'00-000060','БП-000074':'00-000057','БП-000076':'БП-000077','БП-000079':'00-000057','БП-000080':'00-000057','БП-000080':'00-000057','БП-000081':'00-000057','БП-000082':'БП-000083','БП-000084':'БП-000077','БП-000085':'БП-000070','БП-000086':'БП-000070','БП-000087':'БП-000106','БП-000088':'00-000051','БП-000089':'00-000057','БП-000090':'00-000051','БП-000091':'БП-000075','БП-000092':'00-000060','БП-000093':'00-000060','БП-000098':'БП-000096','БП-000101':'БП-000097','БП-000104':'БП-000097','БП-000105':'БП-000106','БП-000109':'БП-000108','БП-000110':'БП-000102','БП-000115':'БП-000107','БП-000120':'БП-000107','БП-000122':'00-000033','БП-000123':'БП-000107','БП-000126':'БП-000125','БП-000127':'БП-000128','БП-000130':'БП-000111','БП-000132':'БП-000107'}

    def __init__(self, matrix):
        for i,index in enumerate(matrix):
            if index == "Дата":
                self.Pdata = i
                continue
            elif index == "N":
                self.Pno = i
                continue
            elif index == "Дубликат":
                self.dubli = i
                continue
            elif index == "#idвсмете":
                self.idvsmete = i
                continue
            elif index == "#id в заявке":
                self.idvzayavke = i
                continue
            elif "Организация" in str(index):
                self.Porg = i
                continue
            elif index == "Поступление (акт, накладная, УПД).Склад" or index == 'Перемещение товаров, материалов.Отправитель' or index == 'Перемещение товаров.Отправитель':
                self.Pnapr = i
                continue
            elif index == "Поступление (акт, накладная, УПД).Контрагент" or index == 'Перемещение товаров.Получатель':
                self.Pcontra = i
                continue
            elif index == "Поступление на расчетный счет.Плательщик" :
                self.Pcontra = i
                continue
            elif 'Контрагент.Код' in index:
                self.Pcodcontra = i
                continue
            elif index == "Номенклатура" :
                self.Pnomenkl = i
                continue
            elif index == "Номенклатура.Код":
                self.Pcodnomenkl = i
                continue
            elif index == "Содержание услуги":
                self.Psod = i
                continue
            elif index == "Единица" or index == 'Вид упаковки' or index == 'Единица измерения':
                self.Ped = i
                continue
            elif index == "Номенклатура.Входит в группу" :
                self.Pvx2 = i
                continue
            elif index == "Номенклатура.Вид номенклатуры" :
                self.Pvx1 = i
                continue
            elif index == "Количество" :
                self.Pkol = i
                continue
            elif index == "Сумма" :
                self.PSumma = i
                continue
            elif index == "НДС" :
                self.Pnds = i
                continue
            elif index == "Цена" :
                self.Pcena = i
                continue
            elif index == "Поступление (акт, накладная, УПД).НДС включен в стоимость" :
                self.PndsVkl = i
                continue
            elif "Сумма включает НДС" in str(index):
                self.PndsVsum = i
                continue
            elif index == "Сумма вкл НДС":
                if self.PSummsNDS == None:
                    self.PSummsNDS = i
                    continue
            elif  index == 'Перемещение товаров, материалов.Организация':
                self.Porg = i
                self.PSummsNDS = i
                self.PSumma = i
                continue
            #elif index == "Поступление (акт, накладная, УПД)" or index == 'Перемещение товаров, материалов':
            #    self.upd = i
            #    continue
            elif index == "Подразделение затрат" :
                self.Podrazd = i
                continue
            elif index == "Субконто 1" :
                self.Pnapr = i
                self.subconto1 = i
                continue
            elif index == "Субконто 2" :
                self.subconto2 = i
                continue
            elif index == "Субконто 3" :
                self.subconto3 = i
                continue
            elif index == "Поступление (акт, накладная, УПД).Комментарий" :
                self.PComment = i
                continue
            elif index == "Реализация (акт, накладная, УПД).Склад" :
                self.Pnapr = i
                continue
            elif index == "Реализация (акт, накладная, УПД).Услуги.Субконто" or index == "Субконто" :
                self.Pnapr = i
                continue
            elif index == "Реализация (акт, накладная, УПД).Контрагент" or index == 'Перемещение товаров, материалов.Получатель':
                self.Pcontra = i
                continue
            elif index == "Реализация (акт, накладная, УПД).Комментарий" :
                self.PComment = i
                continue
            elif index == "Счет" :
                self.Prs4et = i
                continue
            elif index == "Получатель" :
                self.Pcontra = i
                continue
            elif index == 'Перемещение товаров, материалов.Получатель.Код' or index ==  'Поступление (акт, накладная, УПД).Склад.Код' or  index == 'Перемещение товаров.Получатель.Код':
                print(index)
                self.PnaprPolu4atel = i
                continue
            elif index == 'Перемещение товаров, материалов.Отправитель.Код' or index == 'Перемещение товаров.Отправитель.Код':
                self.PnaprOtpr = i
                continue
            elif index == "Статья расходов" :
                self.PDDS = i
                continue
            elif index == "Основание" :
                self.Psod = i
                continue
            elif index == "Комментарий" :
                self.PComment = i
                continue
            elif index == "Договор" :
                self.subconto2 = i
                continue
            elif index == "Вид операции" :
                self.vidoperAT = i
                continue
            elif index == 'дубли':
                self.dubli = i
                continue
            elif 'ИНН' in str(index):
                self.inn = i
                continue
            elif str(index) == 'Идентификатор строки':
                self.Ident = i
                continue
            elif index == 'Дата2':
                self.data2 = i
                continue
            elif index == 'Склад2':
                self.sklad2 = i
                continue

        if self.Psod == 1:
            self.Psod = self.Pnomenkl
        if self.PSummsNDS == None:
            self.PSummsNDS = self.Porg
        if self.PSumma == None:
            self.PSumma = self.Porg
        if self.inn == None:
            self.inn = 3
