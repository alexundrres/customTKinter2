from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
import table2 as table2
from sqlite3 import *
import customtkinter
# from openpyxl import Workbook, load_workbook


customtkinter.set_appearance_mode("dark")  # "System", "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # "blue", "green", "dark-blue"


# Получение информации из первой таблицы в бд
def information():
    with connect('database\database.db') as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM table1")
        return cursor.fetchall()


# функция добавления новых записей
def form_submit():
    name = f_name.get() #Entry имя
    insert_inf = (name,)
    with connect('database\database.db') as db:
        cursor = db.cursor()
        query = """ INSERT INTO table1(group_name) VALUES (?)"""
        cursor.execute(query, insert_inf)
        db.commit()
        refresh()


# функция обновления таблицы1
def refresh():
    with connect('database\database.db') as db:
        cursor = db.cursor()
        cursor.execute(''' SELECT * FROM table1 ''')
        [table.delete(i) for i in
         table.get_children()]
        [table.insert('', 'end', values=row) for row in cursor.fetchall()]


# Функция удаления из таблицы1
def delete_user():
    with connect('database\database.db') as db:
        cursor = db.cursor()
        id = id_sel
        cursor.execute('''DELETE FROM table1 WHERE id = ?''', (id,))
        db.commit()
        refresh()


# Функция on_select
# при нажатии по ячейке Treview, создается глобальная переменная с id и column
def on_select(event):
    global id_sel
    global set_col
    id_sel = table.item(table.focus())
    id_sel = id_sel.get('values')[0]
    col = table.identify_column(event.x)
    set_col = table.column(col)
    set_col = set_col.get('id')
    if set_col == 'Группа':
        set_col = 'group_name'


# Функция изменения таблицы1
def changeDB():
    with connect('database\database.db') as db:
        cursor = db.cursor()
        id = id_sel
        whatchange = f_change.get()
        if set_col != 'id':
            cursor.execute("""Update table1 set""" + ' ' + set_col + """ = ? where id = ? """, (whatchange, id))
            db.commit()
            refresh()


# Функция показа справки
def show_info():
    msg = 'Кнопка "Добавить" работает следующим образом: указать имя, платеж, после нажатия создает и добавляет в файл\n\n' \
          'Кнопка "Изменить" работает следующим образом: Сначала надо нажать на изменяемую ячейку, где изменять столбец name, после указать новый name\n\n' \
          'Кнопка "Удалить" работает следующим образом: Сначала надо нажать на изменяемую ячейку, где удалить строку, после нажать кнопку\n\n'\
          'Кнопка "Вхождение в контекстном меню" работает следущющим образом: Сначала надо выбрать какое вхождение будем проверять,' \
          'после по каким столбцам из обеих таблиц, при нажатии кнопки проверка, на Label выдаст результат вхождения в другую таблицу\n\n'\
          'Кнопка "Выгрузка из бд" работает следующим образом: при нажатии "выгрузка в Excel" выгружает всю таблицу в папку database в формате xlsx'

    showinfo("Информация", msg)


# INNER JOIN - возвращает только те строки, которые имеют совпадения в обеих таблицах.
def menu_inner_join():
    # если пользователь откроет новый виджет inner join, то прошлый закроется:
    window.grab_release()
    for widget in window.winfo_children():
        if isinstance(widget, Toplevel):
            widget.destroy()

    def inner_join():

        label_info.config(text="")

        # Установим соединение с базой данных
        with connect('database\database.db') as db:
            # Создание курсора
            cursor = db.cursor()

            if comboExample.get() == 'Имя':
                # SELECT-запрос с INNER JOIN
                query = """SELECT name
                           FROM table1
                           INNER JOIN table2 ON table1.name = table2.names"""

            elif comboExample.get() == 'Расходы':
                # SELECT-запрос с INNER JOIN
                query = """SELECT expenses
                           FROM table1
                           INNER JOIN table2 ON table1.expenses = table2.paid"""
            else:
                print('Пока для программы не корректный запрос')
            # Выполняем запрос
            cursor.execute(query)

            # Получаем результат запроса
            result = cursor.fetchall()

            # распаковка кортежа и запись его в список
            lst = []
            for item in result:
                lst.append(*item, )

            # пустой список для проверки существующих данных о расходах
            isp = []
            for i in range(len(lst)):
                if lst[i] in isp:
                    continue
                else:
                    isp.append(lst[i])
                    new_text = (
                        f' Число вхождений {lst[i] if lst[i - 1] != lst[i] else lst[i - 1]}: {lst.count(lst[i])}')
                    label_info.config(text=label_info.cget('text') + '\n' + new_text)

            # Показываем все на Label

    newWindow = Toplevel(window)
    newWindow.title('Вхождение в обе таблицы')
    newWindow.minsize(300, 200)

    # Комбобокс с выбором вхождений из заголовков первой таблицы
    comboExample = ttk.Combobox(newWindow,
                                values=[
                                    "Имя",
                                    "Расходы", ])
    comboExample.grid(row=5, column=0, columnspan=2, sticky='w', padx=10, pady=10)
    comboExample.current(1)

    # Кнопка проверки вхождения
    btn_new_table = ttk.Button(newWindow, text='Проверка', command=inner_join)
    btn_new_table.grid(row=10, column=0, columnspan=2, sticky='w', padx=10, pady=10)

    # Лейбл с информацией
    label_info = Label(newWindow, text='Что входит из table1 И table2:')
    label_info.grid(row=1, column=0, columnspan=2, sticky='w', padx=10, pady=10)


# INNER JOIN - возвращает только те строки, которые имеют совпадения в обеих таблицах.
def menu_left_join():
    # если пользователь откроет новый виджет inner join, то прошлый закроется:
    window.grab_release()
    for widget in window.winfo_children():
        if isinstance(widget, Toplevel):
            widget.destroy()

    # команда проверки вхождения
    def inner_join():

        label_info.config(text="")

        # Установим соединение с базой данных
        with connect('database\database.db') as db:
            # Создание курсора
            cursor = db.cursor()

            if comboExample.get() == 'Имя':
                # SELECT-запрос с INNER JOIN
                query = """SELECT name
                           FROM table1
                           LEFT JOIN table2 ON table1.name = table2.names"""

            elif comboExample.get() == 'Расходы':
                # SELECT-запрос с INNER JOIN
                query = """SELECT expenses
                           FROM table1
                           LEFT JOIN table2 ON table1.expenses = table2.paid"""
            else:
                print('Пока для программы не корректный запрос')
            # Выполняем запрос
            cursor.execute(query)

            # Получаем результат запроса
            result = cursor.fetchall()

            # распаковка кортежа и запись его в список
            lst = []
            for item in result:
                lst.append(*item, )

            # пустой список для проверки существующих данных о расходах
            isp = []
            for i in range(len(lst)):
                if lst[i] in isp:
                    continue
                else:
                    isp.append(lst[i])
                    new_text = (
                        f'В table1 и table2 есть: {lst[i] if lst[i - 1] != lst[i] else lst[i - 1]}')
                    label_info.config(text=label_info.cget('text') + '\n' + new_text)

            # Показываем все на Label

    newWindow = Toplevel(window)
    newWindow.title('Вхождение в обе таблицы')
    newWindow.minsize(300, 200)

    # Комбобокс с выбором вхождений из заголовков первой таблицы
    comboExample = ttk.Combobox(newWindow,
                                values=[
                                    "Имя",
                                    "Расходы", ])
    comboExample.grid(row=5, column=0, columnspan=2, sticky='w', padx=10, pady=10)
    comboExample.current(1)

    # Кнопка проверки вхождения
    btn_new_table = ttk.Button(newWindow, text='Проверка', command=inner_join)
    btn_new_table.grid(row=10, column=0, columnspan=2, sticky='w', padx=10, pady=10)

    # Лейбл с информацией
    label_info = Label(newWindow, text='Что входит в table1 есть в table2:')
    label_info.grid(row=1, column=0, columnspan=2, sticky='w', padx=10, pady=10)


# функция изменения имени в двух таблицах через внешние ключи/ пока не работает
def menu_change_name():
    def change_name():
        with connect('database\database.db') as db:
            cursor = db.cursor()
            id = id_sel
            whatchange = f_change.get()
            if set_col != 'id':
                cursor.execute("""Update CASCADE table1 set""" + ' ' + set_col + """ = ? where id = ? """,
                               (whatchange, id))
                db.commit()
                refresh()

    window.grab_release()
    for widget in window.winfo_children():
        if isinstance(widget, Toplevel):
            widget.destroy()

    conn = connect('database\database.db')
    cur = conn.cursor()
    cur.execute("SELECT name FROM table1")
    name_table1 = cur.fetchall()

    lst_names = []
    for tables in name_table1:
        lst_names.append(*tables, )

    newWindow = Toplevel(window)
    newWindow.title('Вхождение в обе таблицы')
    newWindow.minsize(300, 200)

    # Комбобокс с выбором вхождений из заголовков первой таблицы
    comboExample = ttk.Combobox(newWindow,
                                values=lst_names)
    comboExample.grid(row=5, column=0, columnspan=2, sticky='w', padx=10, pady=10)
    comboExample.current(0)

    # Кнопка проверки вхождения
    btn_new_table = ttk.Button(newWindow, text='Изменение', command=change_name)
    btn_new_table.grid(row=10, column=0, columnspan=2, sticky='w', padx=10, pady=10)
    # Entry на что изменить имя
    en_change = ttk.Entry(newWindow)
    en_change.grid(row=6, column=0, columnspan=2, sticky='w', padx=10, pady=10)
    # Лейбл с информацией
    label_info = Label(newWindow, text='Выберете которое надо изменить в обеих таблицах')
    label_info.grid(row=1, column=0, columnspan=2, sticky='w', padx=10, pady=10)


# Функция вывода всей бд в excel в папку database
def db_to_excel():
    # Установка соединения с базой данных SQLite
    conn = connect('database\database.db')
    cur = conn.cursor()

    # Получение данных из базы данных в виде списка
    cur.execute("SELECT * FROM table1")
    results = cur.fetchall()

    # Создание объекта Workbook и листа для записи данных
    wb = Workbook()
    del wb['Sheet']

    # создание листов с именами 'table1' и 'table2'
    wb.create_sheet(title='table1')
    wb.create_sheet(title='table2')
    ws = wb.worksheets[0]
    sheet_names = wb.sheetnames
    # Запись заголовков столбцов в первую строку таблицы
    column_names = [description[0] for description in cur.description]
    ws.append(column_names)

    # Запись данных в таблицу Excel
    for row in results:
        ws.append(row)

    # Запись заголовков столбцов в первую строку листа2
    book2 = wb.worksheets[sheet_names.index('table2')]
    wb.active = book2
    ws = wb.active

    cur.execute("SELECT * FROM table2")
    results = cur.fetchall()
    column_names = [description[0] for description in cur.description]
    ws.append(column_names)

    # Запись данных в таблицу Excel
    for row in results:
        ws.append(row)

    # Сохранение таблицы в файл Excel
    wb.save("database.xlsx")

    # Закрытие соединения с базой данных SQLite
    cur.close()
    conn.close()


#  Главное окно
window = customtkinter.CTk()
window.title('subd')
window.minsize(700, 450)

frame_change = customtkinter.CTkFrame(master=window, fg_color="grey")  # блок для функционала субд
frame_change.place(relx=0, rely=0, relwidth=1, relheight=1)
frame_view = customtkinter.CTkFrame(master=window, fg_color="white")  # блок для просмотра базы данных
frame_view.place(relx=0, rely=0.5, relwidth=1, relheight=0.5)

# порядок элементов
heads = ['id', 'Группа']
table = ttk.Treeview(frame_view, show='headings')  # дерево выполняющее свойство таблицы
table['columns'] = heads  # длина таблицы
table.bind('<ButtonRelease-1>', on_select)

# заголовки столбцов и их расположение
for header in heads:
    table.heading(header, text=header, anchor='center')
    table.column(header, anchor='center')

# добавление из бд в таблицу приложения
for row in information():
    table.insert('', END, values=row)
table.pack(expand=YES, fill=BOTH, side=LEFT)

# контекстное меню в Главном окне
mainmenu = Menu(window)
window.config(menu=mainmenu)

# Добавление каскадного меню с командами вхождения в таблице
filemenu = Menu(mainmenu, tearoff=0)
mainmenu.add_cascade(label="Вхождение",menu=filemenu)
filemenu.add_command(label='В обе таблицы', command=menu_inner_join)
filemenu.add_command(label='В Левую таблицу', command=menu_left_join)

frombd_menu = Menu(mainmenu, tearoff=0)

# Добавление кнопки "Выгрузка из бд" в контекстное меню
mainmenu.add_cascade(label="Выгрузка из бд",
                     menu=frombd_menu)
frombd_menu.add_command(label='В Excel', command=db_to_excel)

# добавления новых имен в бд
l_name = customtkinter.CTkLabel(master=frame_change, text="Имя", text_color="black")
f_name = customtkinter.CTkEntry(frame_change, width=130, fg_color="darkgray")
l_name.grid(row=0, column=0, sticky='w', padx=10, pady=10)
f_name.grid(row=0, column=1, sticky='w', padx=10, pady=10)

# добавления новых платежей в бд
l_expenses = customtkinter.CTkLabel(master=frame_change, text="Платеж", text_color="black")
f_expenses = customtkinter.CTkEntry(frame_change, width=130, fg_color="darkgray")
l_expenses.grid(row=1, column=0, sticky='w', padx=10, pady=10)
f_expenses.grid(row=1, column=1, sticky='w', padx=10, pady=10)

#  изменения бд
l_change = customtkinter.CTkLabel(master=frame_change, text="Заменить на:", text_color="black")
f_change = customtkinter.CTkEntry(frame_change, width=130, fg_color="darkgray")
l_change.grid(row=3, column=0, sticky='w', padx=10, pady=10)
f_change.grid(row=3, column=1, sticky='w', padx=10, pady=10)

#  кнопка добавить
btn_submit = customtkinter.CTkButton(master=frame_change, text="Добавить", command=form_submit, text_color="black", fg_color="darkgray")
btn_submit.grid(row=0, column=3, columnspan=2, sticky='w', padx=10, pady=10)

# кнопка удалить
btn_delete = customtkinter.CTkButton(master=frame_change, text="Удалить", command=delete_user, text_color="black", fg_color="darkgray")
btn_delete.grid(row=1, column=3, columnspan=2, sticky='w', padx=10, pady=10)

#  кнопка изменить
but_change = customtkinter.CTkButton(master=frame_change, text='Изменить', command=changeDB, text_color="black", fg_color="darkgray")
but_change.grid(row=3, column=3, columnspan=2, sticky='w', padx=10, pady=10)

#  кнопка вызывающая справку
btn_reference = customtkinter.CTkButton(master=frame_change, text="Справка", command=show_info, text_color="black", fg_color="darkgray")
btn_reference.grid(row=4, column=0, sticky='w', padx=10, pady=10)

# Кнопка вызова таблицы 2
create_new_table = customtkinter.CTkButton(master=frame_change, text='Таблица 2', command=table2.create_table2, text_color="black", fg_color="darkgray")
create_new_table.grid(row=4, column=1, columnspan=2, sticky='w', padx=10, pady=10)

# скроллбар для treview
scrollpanel = ttk.Scrollbar(frame_view, command=table.yview)
table.configure(yscrollcommand=scrollpanel.set)
scrollpanel.pack(side=RIGHT, fill=Y)
table.pack(expand=YES, fill=BOTH)

window.mainloop()
