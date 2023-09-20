import PySimpleGUI as sg
import sqlite3

#создание бд
conn = sqlite3.connect('db/AddressBook.db')
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS contacts(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, phone TEXT, email TEXT)')
conn.commit()
conn.close()

#функция добавления контакта
def add_contact(name, phone, email):
    conn = sqlite3.connect('db/AddressBook.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)', (name, phone, email))
    conn.commit()
    conn.close()

#Функция поиска контакта (фильтрации)
def hide_contacts(contact_name, contact_phone, contact_mail):
    zapros_default = "SELECT * FROM contacts WHERE"
    zapros = "SELECT * FROM contacts WHERE"
    if contact_name:
        zapros += f" name = '{contact_name}'"
    if contact_phone and zapros != zapros_default:
        zapros += f" AND phone = '{contact_phone}'"
    elif contact_phone:
        zapros += f" phone = '{contact_phone}'"
    if contact_mail and zapros != zapros_default:
        zapros += f" AND email = '{contact_mail}'"
    elif contact_mail:
        zapros += f" email = '{contact_mail}'"

    conn = sqlite3.connect('db/AddressBook.db')
    cursor = conn.cursor()
    cursor.execute(zapros)
    contacts = cursor.fetchall()
    conn.close()
    return contacts


#функция получения контакт
def get_contacts():
    conn = sqlite3.connect('db/AddressBook.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contacts')
    contacts = cursor.fetchall()
    conn.close()
    return contacts

#функция удаления контакта
def delete_contact(contact_id):
    conn = sqlite3.connect('db/AddressBook.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))
    conn.commit()
    conn.close()

# Отображение интерфейса
sg.theme('DarkGrey5')

top = ['id', 'Name', 'Phone', 'Mail']
rows = get_contacts()

layout = [
        [sg.Text('Адресная книга', font=('Arial', 20))],
        [sg.Text('Имя:   '), sg.Input(key='-NAME-', size=(30, 1), expand_x=True)],
        [sg.Text('Номер:'), sg.Input(key='-PHONE-', size=(30, 1), expand_x=True)],
        [sg.Text('Эмэйл:'), sg.Input(key='-MAIL-', size=(30, 1), expand_x=True)],
        [sg.Button('Добавить'), sg.Button('Поиск'), sg.Button('Сброс поиска')],
        [sg.Table(values=rows, headings=top, auto_size_columns=True, display_row_numbers=False, justification='center',
                  key='-TABLE-', select_mode='extended', selected_row_colors='red on yellow', enable_events=True,
                  expand_x=True,
                  expand_y=True, enable_click_events=True)],
        [sg.Button('Удалить')],
]

window = sg.Window('Address Book', layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == 'Добавить':
        name = values['-NAME-']
        phone = values['-PHONE-']
        mail = values['-MAIL-']
        if name or phone or mail:
            add_contact(name, phone, mail)
            window['-TABLE-'].update(values=get_contacts())
            window['-NAME-'].update('')
            window['-PHONE-'].update('')
            window['-MAIL-'].update('')
    # Чтобы удалить запись, нужно ее выбрать. При зажатом ctrl есть возможность удалить сразу несколько записей
    elif event == 'Удалить':
        selected_contacts = values['-TABLE-']
        if selected_contacts:
            for contact in selected_contacts:
                contact_id = rows[contact][0]
                delete_contact(contact_id)
            window['-TABLE-'].update(values=get_contacts())
#Поиск осуществляется через поля "Имя" "Телефон" "эмэил" и поддерживает разные вариации фильтрования. Например:
# "Имя" или "Имя" "эмэил" или "эмэил" или "телефон" или "Имя" "телефон" и т.д. Сброс поиска вернет все записи из БД
    elif event == 'Поиск':
        name = values['-NAME-']
        phone = values['-PHONE-']
        mail = values['-MAIL-']
        if name or phone or mail:
            window['-TABLE-'].update(values=hide_contacts(name, phone, mail))
    elif event == 'Сброс поиска':
        window['-TABLE-'].update(values=get_contacts())

window.close()
