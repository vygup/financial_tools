import json

# Проверка вводимого значения на число (+ плавающее)
def isfloat(value):
    # Если отработает функция приведения к float
    # то значение правильное
    try:
        float(value)
        return True
    except ValueError:
        return False


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


# Проверка на правильность ввода значения (размер cashback)
def cashback_input():
    # 3 попытки на ввод значения
    for i in range(1,5):
        # Если попытки не исчерпаны
        if i <= 3:
            # Запрашиваем у пользователя значение
            # Заменяем , на . (под формат float)
            value = input('Размер кешбэка: ').replace(',', '.')    
            
            # Проверка на числовое значение
            # Если значение числовое, выход из итерации
            if isfloat(value):
                return value
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
            return False


# Проверка вводимого значения для подтверждения успешности
def confirm(value=False):
    '''На вход поступает значение,
    которое будет указано
    в начале запроса на подтверждение.

    Чтобы подтвердить действие,
    пользователь должен указать одно из значений
    "Д"-рус или "Y"-англ,
    иное значение (включая пустоту) 
    будет считаться как отказ
    '''

    # Значения согласия
    sucs_list = ['Y', 'Д']

    # Вывод переданной фразы
    if value:
        inp_val = input(f'{value}\n({sucs_list[0]}|{sucs_list[1]}): ')
    # Иначе шаблонная фраза
    else:
        inp_val = input(f'Все верно?\n({sucs_list[0]}|{sucs_list[1]}): ')

    # Возвращаем True если пользователь согласился
    # иначе False
    if inp_val in sucs_list:
        return True
    else:
        return False


# Запрос категории от пользователя
def input_category():
    # Запрашиваем у пользователя нужную информацию
    month_name = input('Название месяца: ')
    bank_name = input('Название банка: ')
    category_name = input('Категория: ')
    bonus_value = cashback_input()

    print('')

    # Проверяем передал ли пользователь все нужные значения
    # и валидируем
    if (month_name and bank_name and 
        category_name and bonus_value):
        # Если пользователь передал все значения - дублируем их
        print(f'В {bank_name} за {month_name} вы выбрали {category_name} = {bonus_value}%')
        
        # Спрашиваем у пользователя все ли корректно
        # Если да - говорим что записали
        if confirm():
            # Готовим возврат значения в определенном формате
            final_value = {
                    "month":month_name,
                    "bank":bank_name,
                    "category":category_name,
                    "cashback":bonus_value,
                    }
            return json.dumps(final_value)
        # Если пользователь не подтвердил
        # считаем условия не выполненными
        else:        
            return False
    
    else:
        prnt_error('Указаны не все значения')
        return False


# Запись переданных данных
if input_category():
    # Записать в БД
    prnt_success('Условия успешно записаны')
else:
    prnt_error('Условия не записаны')



