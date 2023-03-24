'''

Точно такой же функционал как и в main, только для второй таблицы

'''
from tkinter import *
from tkinter import ttk
from sqlite3 import *
from tkinter.messagebox import *

def information2():
    with connect('database\database.db') as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM table2")
        return cursor.fetchall()

def information_groups():
    with connect('database\database.db') as db:
        cursor = db.cursor()
        cursor.execute("SELECT group_name FROM table1;")
        return cursor.fetchall()

# функция создания окна второй таблицы
def create_table2():
    def on_select2(event):
        global id_sel2
        global set_col2
        id_sel2 = table2.item(table2.focus())
        id_sel2 = id_sel2.get('values')[0]
        col = table2.identify_column(event.x)
        set_col2 = table2.column(col)
        set_col2 = set_col2.get('id')
        if set_col2 == 'Фио студента':
            set_col2 = 'FIO'
        elif set_col2 == 'Группа':
            set_col2 = 'group_name'

    def delete2():
        with connect('database\database.db') as db:
            cursor = db.cursor()
            id = id_sel2
            cursor.execute('''DELETE FROM  table2 WHERE id = ?''', (id,))
            db.commit()
            refresh2()

    def refresh2():
        with connect('database\database.db') as db:
            cursor = db.cursor()
            cursor.execute(''' SELECT * FROM table2 ''')
            [table2.delete(i) for i in
             table2.get_children()]
            [table2.insert('', 'end', values=row) for row in cursor.fetchall()]

    def form_submit2():
        name = f2_name.get()
        group = comboExample.get()
        insert_inf = (name, group)
        with connect('database\database.db') as db:
            cursor = db.cursor()
            query = """ INSERT INTO table2(FIO, group_name) VALUES (?, ?)"""
            cursor.execute(query, insert_inf)
            db.commit()
            refresh2()

    def changeDB2():
        with connect('database\database.db') as db:
            cursor = db.cursor()
            id = id_sel2
            whatchange = f2_change.get()
            if set_col2 != 'id':
                cursor.execute("""Update table2 set""" + ' ' + set_col2 + """ = ? where id = ? """, (whatchange, id))
                db.commit()
                refresh2()

    def show_info():
        msg = 'Кнопка "Добавить" работает следующим образом: указать имя, платеж, индекс, после нажатия создает и добавляет в файл\n\n' \
              'Кнопка "Изменить" работает следующим образом: Сначала надо указать индекс, где изменять столбец name, после указать новый name\n\n' \
              'Кнопка "Удалить" работает следущющим образом: Сначала надо указать индекс, где удалить строку, после нажать кнопку'
        showinfo("Информация", msg)

    lst_groups = []
    for group in information_groups():
        lst_groups.append(*group,)

    window = Tk()
    window.title('subd')
    window.minsize(700, 450)

    frame2_change = Frame(window, width=150, height=150, bg='white')  # блок для функционала субд
    frame2_view = Frame(window, width=150, height=150, bg='white')  # блок для просмотра базы данных
    frame2_change.place(relx=0, rely=0, relwidth=1, relheight=1)
    frame2_view.place(relx=0, rely=0.5, relwidth=1, relheight=0.5)

    # порядок элементов
    heads2 = ['id', 'Фио студента', 'Группа']
    table2 = ttk.Treeview(frame2_view, show='headings')  # дерево выполняющее свойство таблицы
    table2['columns'] = heads2  # длина таблицы

    table2.bind('<ButtonRelease-1>', on_select2)
    # заголовки столбцов и их расположение
    for header in heads2:
        table2.heading(header, text=header, anchor='center')
        table2.column(header, anchor='center')

    # добавление из бд в таблицу приложения
    for row in information2():
        table2.insert('', END, values=row)
    table2.pack(expand=YES, fill=BOTH, side=LEFT)

    # добавления новых имен в бд
    l2_name = ttk.Label(frame2_change, text="Имя")
    f2_name = ttk.Entry(frame2_change)
    l2_name.grid(row=0, column=0, sticky='w', padx=10, pady=10)
    f2_name.grid(row=0, column=1, sticky='w', padx=10, pady=10)

    # добавления новых групп в бд
    l_groups = ttk.Label(frame2_change, text="Группы")
    comboExample = ttk.Combobox(frame2_change, values=lst_groups)
    l_groups.grid(row=1, column=0, sticky='w', padx=10, pady=10)
    comboExample.grid(row=1, column=1, sticky='w', padx=10, pady=10)
    comboExample.current(0)


    #  изменения бд
    l2_change = ttk.Label(frame2_change, text="Заменить на:")
    f2_change = ttk.Entry(frame2_change)  # entry на что меняем прошлое имя в бд
    l2_change.grid(row=3, column=0, sticky='w', padx=10, pady=10)
    f2_change.grid(row=3, column=1, sticky='w', padx=10, pady=10)

    #  кнопка добавить
    btn2_submit = ttk.Button(frame2_change, text="Добавить", command=form_submit2)
    btn2_submit.grid(row=0, column=3, columnspan=2, sticky='w', padx=10, pady=10)

    #  кнопка удалить
    btn2_delete = ttk.Button(frame2_change, text="Удалить", command=delete2)
    btn2_delete.grid(row=1, column=3, columnspan=2, sticky='w', padx=10, pady=10)

    #  кнопка изменить
    but2_change = ttk.Button(frame2_change, text='Изменить', command=changeDB2)
    but2_change.grid(row=3, column=3, columnspan=2, sticky='w', padx=10, pady=10)

    #  кнопка вызывающая справку
    btn2_reference = ttk.Button(frame2_change, text="Справка", command=show_info)
    btn2_reference.grid(row=4, column=0, sticky='w', padx=10, pady=10)