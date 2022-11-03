import pymysql
from easygui import *

try:
    connection = pymysql.connect(
        host='Localhost',
        port=3306,
        user="",
        password='',
        database="",
        cursorclass=pymysql.cursors.DictCursor
    )
    print('ok')
    start_meny = buttonbox('Що бажаєте робити?','FILES',['Вхід','Реєстрація'],image='1.gif')
    if start_meny == 'Вхід':
        table = multpasswordbox("Зайдіть в свій акаунт", "Table", ["Логін", "Пароль"])
        try:
            with connection.cursor() as cursor:
                login = f"select * FROM `clients` where login = '{table[0]}' and parol = '{table[1]}'"
                if cursor.execute(login):
                    cursor.execute(login)
                    connection.commit()
                    msgbox('Ви успішно зайшли у свій акаунт','Welcome','Перейти до кошика',"2.gif")
                    while True:
                        next_step = buttonbox('Що далі бажаєте робити?', "FILE",
                                         ["Додати товар у кошик", "Видалити товар з кошика", "Замінити товар у кошику",
                                          "Очищення кошика", "Перегляд кошика"],'cart.gif')
                        if next_step == "Додати товар у кошик":
                            with connection.cursor() as cursor:
                                cursor.execute(f"SELECT * FROM `products`")
                                all_products = cursor.fetchall()
                            nice_menu = "\n".join([f"{element.get('ProductName')} = {element.get('ProductPrice')}грн" for element in all_products])
                            menu_for_choice = ([f"{element.get('ProductName')}" for element in all_products])
                            choice = choicebox(nice_menu,'SHOP',menu_for_choice)
                            with connection.cursor() as cursor:
                                insert = f'INSERT INTO `shopcart` (ProductName,login) VALUES ("{choice}","{table[0]}")'
                                cursor.execute(insert)
                                connection.commit()
                            msgbox(f"{choice} доданий в корзину",image='8.gif')
                        elif next_step == "Видалити товар з кошика":
                            with connection.cursor() as cursor:
                                cursor.execute(f"SELECT * FROM `shopcart`")
                                all_products = cursor.fetchall()
                            nice_menu = "\n".join(
                                [f"{element.get('ProductName')}" for element in
                                 all_products])
                            menu_for_choice = ([f"{element.get('ProductName')}" for element in all_products])
                            choice = choicebox(f'У вас в корзині: \n \n{nice_menu} \n \nЩо бажаєте видалити?', 'SHOP', menu_for_choice)
                            with connection.cursor() as cursor:
                                delete_table = f"DELETE FROM `shopcart` WHERE ProductName='{choice}';"
                                cursor.execute(delete_table)
                                connection.commit()
                                msgbox(f"{choice} було видалено з кошика", image='6.gif')
                        elif next_step == "Замінити товар у кошику":
                            with connection.cursor() as cursor:
                                cursor.execute(f"SELECT * FROM `shopcart` where login = '{table[0]}';")
                                shopcart_all = cursor.fetchall()
                                shopcart_menu = "\n".join([f"{element.get('ProductName')}" for element in shopcart_all])
                                parametr = enterbox(f"У вашому кошику: \n \n{shopcart_menu} \n \nЩо саме ви хочете в корзині замінити?")
                            with connection.cursor() as cursor:
                                cursor.execute(f"SELECT * FROM `products`")
                                all_products = cursor.fetchall()
                            nice_menu = "\n".join([f"{element.get('ProductName')} = {element.get('ProductPrice')}грн" for element in all_products])
                            new_parametr = enterbox(f'{nice_menu} \n \nВведіть назву товару для додавання в кошик','SHOP')
                            with connection.cursor() as cursor:
                                    change_info = f"UPDATE `shopcart` SET ProductName = '{new_parametr}' WHERE ProductName = '{parametr}'"
                                    cursor.execute(change_info)
                                    connection.commit()
                                    msgbox(f"Ви успішно оновили корзину", image='7.gif')
                        elif next_step == "Очищення кошика":
                            with connection.cursor() as cursor:
                                delete_table = f"DELETE FROM `shopcart` WHERE login='{table[0]}';"
                                cursor.execute(delete_table)
                                connection.commit()
                                msgbox("Кошик було очищено", image='6.gif')
                        elif next_step == "Перегляд кошика":
                            with connection.cursor() as cursor:
                                cursor.execute(f"SELECT * FROM `shopcart` where login = '{table[0]}';")
                                shopCart = cursor.fetchall()
                            nice_menu = "\n".join([f"{element.get('ProductName')}" for element in shopCart])
                            msgbox(nice_menu,image='8.gif')
                        else:
                            break
                else:
                    msgbox('Такого акаунта нема','giphy.gif',image='giphy.gif')
        finally:
            connection.close()

    elif start_meny == "Реєстрація":
        try:
            with connection.cursor() as cursor:
                login = multpasswordbox("Enter login and password:", "Enter", ["Login:", "Pass:"])
                registration = f"INSERT INTO `clients`(login,parol) VALUES ('{login[0]}', '{login[1]}');"
                cursor.execute(registration)
                connection.commit()
                msgbox('Регістрація успішна',image='2.gif')
            while True:
                next_step = buttonbox('Що далі бажаєте робити?', "FILE",
                                      ["Додати товар у кошик", "Видалити товар з кошика", "Замінити товар у кошику",
                                       "Очищення кошика", "Перегляд кошика"], 'cart.gif')
                if next_step == "Додати товар у кошик":
                    with connection.cursor() as cursor:
                        cursor.execute(f"SELECT * FROM `products`")
                        all_products = cursor.fetchall()
                    nice_menu = "\n".join(
                        [f"{element.get('ProductName')} = {element.get('ProductPrice')}грн" for element in
                         all_products])
                    menu_for_choice = ([f"{element.get('ProductName')}" for element in all_products])
                    choice = choicebox(nice_menu, 'SHOP', menu_for_choice)
                    with connection.cursor() as cursor:
                        insert = f'INSERT INTO `shopcart` (ProductName,login) VALUES ("{choice}","{login[0]}")'
                        cursor.execute(insert)
                        connection.commit()
                    msgbox(f"{choice} доданий в корзину", image='8.gif')
                elif next_step == "Видалити товар з кошика":
                    with connection.cursor() as cursor:
                        cursor.execute(f"SELECT * FROM `shopcart`")
                        all_products = cursor.fetchall()
                    nice_menu = "\n".join(
                        [f"{element.get('ProductName')}" for element in
                         all_products])
                    menu_for_choice = ([f"{element.get('ProductName')}" for element in all_products])
                    choice = choicebox(f'У вас в корзині: \n \n{nice_menu} \n \nЩо бажаєте видалити?', 'SHOP',
                                       menu_for_choice)
                    with connection.cursor() as cursor:
                        delete_table = f"DELETE FROM `shopcart` WHERE ProductName='{choice}';"
                        cursor.execute(delete_table)
                        connection.commit()
                        msgbox(f"{choice} було видалено з кошика", image='6.gif')
                elif next_step == "Замінити товар у кошику":
                    with connection.cursor() as cursor:
                        cursor.execute(f"SELECT * FROM `shopcart` where login = '{login[0]}';")
                        shopcart_all = cursor.fetchall()
                        shopcart_menu = "\n".join([f"{element.get('ProductName')}" for element in shopcart_all])
                        parametr = enterbox(
                            f"У вашому кошику: \n \n{shopcart_menu} \n \nЩо саме ви хочете в корзині замінити?")
                    with connection.cursor() as cursor:
                        cursor.execute(f"SELECT * FROM `products`")
                        all_products = cursor.fetchall()
                    nice_menu = "\n".join(
                        [f"{element.get('ProductName')} = {element.get('ProductPrice')}грн" for element in
                         all_products])
                    new_parametr = enterbox(f'{nice_menu} \n \nВведіть назву товару для додавання в кошик', 'SHOP')
                    with connection.cursor() as cursor:
                        change_info = f"UPDATE `shopcart` SET ProductName = '{new_parametr}' WHERE ProductName = '{parametr}'"
                        cursor.execute(change_info)
                        connection.commit()
                        msgbox(f"Ви успішно оновили корзину", image='7.gif')
                elif next_step == "Очищення кошика":
                    with connection.cursor() as cursor:
                        delete_table = f"DELETE FROM `shopcart` WHERE login='{login[0]}';"
                        cursor.execute(delete_table)
                        connection.commit()
                        msgbox("Кошик було очищено", image='6.gif')
                elif next_step == "Перегляд кошика":
                    with connection.cursor() as cursor:
                        cursor.execute(f"SELECT * FROM `shopcart` where login = '{login[0]}';")
                        shopCart = cursor.fetchall()
                    nice_menu = "\n".join([f"{element.get('ProductName')}" for element in shopCart])
                    msgbox(nice_menu, image='8.gif')
                else:
                    break
        finally:
            connection.close()

except:
    msgbox('Користувач з таким іменем і паролем вже зареєстровані, виберіть інше',image='giphy.gif')
