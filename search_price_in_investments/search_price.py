from decimal import Decimal
import configparser
import os

def breakeven(buy_price:float
            , cnt:int
            , sell_price:float
            , div:float
            , bcom:float
            , tcom:float
            , nsum:float
            , incr_price:float
            , profit_perc:float
            # Облиги
            , bond:bool
            , nominal:float
            , nkd_buy:float
            , nkd_sell:float):

    """Функция расчета затрат и прибыли/убытка на сделку.
    
    Расчет производится по акциям, облигациям, фондам.
    
    Параметры:
    buy_price:float
        цена покупки актива.
    cnt:int
        количество активов.
    bond:bool
        расчет по облигациям.
    div:float
        поступившие купоны/дивы/зачисления по активу.
    sell_price:float
        цена продажи актива.
    nkd_buy:float
        накопленный купонный доход во время покупки.
    nkd_sell:float
        накопленный купонный доход во время продажи.
    nominal:float
        номинал актива, нужен для облигаций.
    bcom:float
        комисиия брокера.
    tcom:float
        комисиия биржи.
    nsum:float
        налоговая ставка.
    incr_price:float
        шаг цены.
    profit_perc:float
        процент заробатка от актива.

    """
    
    cnt_fract = Decimal(str(incr_price)).as_tuple().exponent*(-1)
    profit_perc *= 100

    # Дивиденды на бумагу
    div = div * cnt

    print("----------ПОКУПКА----------")

    if bond:
        buy_price = (buy_price/100) * nominal

    print(f"Цена = {round(buy_price, cnt_fract):,} руб.")

    if bond:
        print(f"НКД = {nkd_buy:,.2f} руб.")

    # Сумма покупки
    if bond:
        bsumm = (buy_price + nkd_buy) * cnt
        print(f"Кол-во = {cnt:,} шт.")
        print(f"Сумма с НКД = {bsumm:,.2f} руб.")
    else:
        bsumm = buy_price * cnt
        print(f"Кол-во = {cnt:,} шт.")
        print(f"Сумма = {bsumm:,.2f} руб.")

    # Расчет комиссий на покупку
    if bool(bcom):
        buy_com_b = bsumm * bcom
    else:
        buy_com_b = 0

    if bool(tcom):
        buy_com_t = bsumm * tcom
    else:
        buy_com_t = 0
        
    buy_comm = buy_com_b + buy_com_t
    print(f"Комиссия брокера = {buy_com_b:,.2f} руб.")
    print(f"Комиссия биржи = {buy_com_t:,.2f} руб.")

    # Всего затрачено на покупку
    total_buy = bsumm + buy_comm    
    print(f"Итого покупка = {total_buy:,.2f} руб.")

    print("----------ПРОДАЖА----------")

    if bool(sell_price):

        # Сумма продажи
        if bond:
            sell_price = (sell_price/100) * nominal

        if bond:
            ssum = (sell_price + nkd_sell) * cnt
        else:
            ssum = sell_price * cnt

        # Расчет комиссии на продажу
        if bool(bcom):
            sell_com_b = ssum * bcom
        else:
            sell_com_b = 0

        if bool(tcom):
            sell_com_t = ssum * tcom
        else:
            sell_com_t = 0

        sell_comm = sell_com_b + sell_com_t
        
        # Будет получено за продажу
        total_sell = ssum - sell_comm

        # Разница от цены покупки/продажи 
        profit_price = ssum - bsumm

        if profit_price > 0:
            nalog = profit_price * nsum
            profit = profit_price - nalog
            profit -= sell_comm + buy_comm
            profit += div
            
        else:
            profit = profit_price + div
            profit -= sell_comm + buy_comm
            nalog = 0

    else:
        # Отправная точка для расчета цены продажи
        sell_price = 0

        # Считаем цену продажи
        while True:

            if bond:
                ssum = (sell_price + nkd_sell) * cnt
            else:
                ssum = sell_price * cnt

            # Расчет комиссии на продажу
            if bool(bcom):
                sell_com_b = ssum * bcom
            else:
                sell_com_b = 0

            if bool(tcom):
                sell_com_t = ssum * tcom
            else:
                sell_com_t = 0
                
            sell_comm = sell_com_b + sell_com_t
            
            # Будет получено за продажу
            total_sell = ssum - sell_comm

            # Разница от цены покупки/продажи 
            profit_price = ssum - bsumm

            if profit_price > 0:
                nalog = profit_price * 0.13
                profit = profit_price - nalog
                profit -= sell_comm + buy_comm
                profit += div
                
            else:
                profit = profit_price + div
                profit -= sell_comm + buy_comm
                nalog = 0
            
            if profit/total_buy*100 >= profit_perc:
                    break
            else:
                sell_price += incr_price

    print(f"Цена = {round(sell_price, cnt_fract):,} руб.")
    if bond:
        print(f"НКД = {nkd_sell:,.2f} руб.")
        print(f"Кол-во = {cnt:,.0f} шт.")
        print(f"Сумма с НКД = {ssum:,.2f} руб.")
    else:
        print(f"Кол-во = {cnt:,.0f} шт.")
        print(f"Сумма = {ssum:,.2f} руб.")
    print(f"Комиссия брокера = {sell_com_b:,.2f} руб.")
    print(f"Комиссия биржи = {sell_com_t:,.2f} руб.")
    print(f"Итого продажа = {total_sell:,.2f} руб.")

    print("----------ИТОГО------------")

    if bond:
        print(f"Профит от покупки/продажи + НКД = {profit_price:,.2f} руб. ({profit_price/total_buy*100:,.2f}%)")
    else:
        print(f"Профит от покупки/продажи = {profit_price:,.2f} руб. ({profit_price/total_buy*100:,.2f}%)")

    print(f"Было получено за время владения = {div:,.2f} руб.")

    print(f"Затрачено на комиссии = {buy_comm + sell_comm:,.2f} руб.")

    print(f"Налог = {nalog:,.2f} руб.")
    
    print(f"Профит итого = {profit:,.2f} руб. ({profit/total_buy*100:,.2f}%)")





# Вывод значения курсивом
def prnt_italic(value):
    # 3 - Курсив
    # 0 - Сброс
    print(f'\033[3m{value}\033[0m')


# Вывод значения ошибки
def prnt_error(value):
    # 1 - Жирный; 31 - Красный цвет
    # 0 - Сброс
    print(f'\033[1;31m{value}\033[0m')


# Вывод значения успешности
def prnt_success(value):
    # 1 - Жирный; 32 - Зеленый цвет
    # 0 - Сброс
    print(f'\033[1;32m{value}\033[0m')


# Проверка вводимого значения на число (+ плавающее)
def isfloat(value):
    # Если отработает функция приведения к float
    # то значение правильное
    try:
        float(value)
        return value
    except ValueError:
        return False

# Проверка необязательного значения на корректность
def valid_dop_value(prnt):
    val = input(prnt)
    if isfloat(val):
        return float(val)
    else:
        return False

# Проверка обязательного значения на корректность
def valid_crit_value(prnt):
    # 3 попытки на ввод значения
    for i in range(1,5):
        # Если попытки не исчерпаны
        if i <= 3:
            # Запрашиваем у пользователя значение
            # Заменяем , на . (под формат float)
            value = input(prnt).replace(',', '.')
            
            # Проверка на числовое значение
            # Если значение числовое, выход из итерации
            if isfloat(value) and float(value) > 0:
                return float(value)
            # Если пользователь ввел не верное значение
            # сообщаем об этом, информируем о нужном формате
            # и повторяем запрос
            else:
                prnt_error('Неверное значение')
                prnt_italic('Введите число в формате (1 или 1.5 или 1,5)\n')
        # Если попытки закончились
        # Сообщаем об этом и возвращаем False
        else:
            prnt_error('Число попыток исчерпано')
            exit()


abspath = os.path.abspath(__file__)
basename = os.path.basename(__file__)
curdir = abspath.replace(basename, '')

prnt_italic('\nЧтение parameters.ini')

# Метод парсинга .ini
config = configparser.ConfigParser()

if config.read(curdir + '/parameters.ini'):
    pass
else:
    print('\nПроблема с чтением parameters.ini, файл не найден')
    exit()

try:

    # Общие параметры
    # Брокерская комиссия (0.1% = 0.001)
    bcom = float(config.get('BASE', 'bcom'))
    # Биржевая комиссия (0.1% = 0.001)
    tcom = float(config.get('BASE', 'tcom'))
    # Налоговая ставка (13% = 0.13)
    nsum = float(config.get('BASE', 'nsum'))
    # Поступившие купоны/дивы/зачисления по активу
    div = float(config.get('BASE', 'div'))
    # Шаг цены в стакане
    incr_price = float(config.get('BASE', 'incr_price'))

    # Для Облигаций
    # Накопленный купонный доход во время покупки
    nkd_buy = float(config.get('BOND', 'nkd_buy'))
    # Накопленный купонный доход во время продажи
    nkd_sell = float(config.get('BOND', 'nkd_sell'))
    # Номинал актива
    nominal = float(config.get('BOND', 'nominal'))

except Exception as err:
    print(f'\nОшибка:{err}')
    exit()

prnt_italic('\nДля пропуска значения нажмите Enter (Оставьте поле пустым)')
prnt_italic('Цена покупки и количество является обязательным для ввода')


# Значения согласия
sucs_list = ['y', 'д']

if input(f'\nРасчет по облигациям? ({sucs_list[0]}|{sucs_list[1]}): '):
    bond = True
else:
    bond = False

if bond:
    prnt_buy_price = '\nВведите цену покупки в % (70 или 60.5): '
else:
    prnt_buy_price = '\nВведите цену покупки: '

# Цена покупки
buy_price = valid_crit_value(prnt_buy_price)

# К-во активов
cnt = valid_crit_value('\nВведите количество бумаг: ')

# Цена продажи или доходность на сделку
prnt_italic('\nДля расчета цены продажи относительно желаемой доходности пропустите ввод значения')
sell_price = valid_dop_value('Введите цену продажи (в формате 100 или 100.5): ')

# Доходность
profit_perc = 0
if not sell_price:
    prnt_italic('\nДля расчета цены безубытка введите 0 или пропустите значение')
    profit_perc = valid_dop_value('Введите желаемую доходность в % (в формате 10 или 10.5): ')/100
    if not profit_perc:
        profit_perc = 0

print('\n\n')

breakeven(
    buy_price = buy_price
    , cnt = cnt
    , sell_price = sell_price
    , bcom= bcom
    , tcom = tcom
    , nsum = nsum
    , div = div
    , bond = bond
    , nominal = nominal
    , nkd_buy = nkd_buy
    , nkd_sell = nkd_sell
    , incr_price = incr_price
    , profit_perc = profit_perc
)

print('\n')