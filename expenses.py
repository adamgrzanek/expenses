import sys
import sqlite3
import datetime
import random
import string

connection = sqlite3.connect("expenses.db")  # create database if not exist

def create_table(connection):
    try:
        cur = connection.cursor()
        cur.execute("""CREATE TABLE expenses
                        (amount real, category text, description text, date text)""")
    except:
        pass


create_table(connection)

def show_expenses(connection, category='%', limit=9999999):

    cur = connection.cursor()
    cur.execute(f"""SELECT amount, category, description, date, rowid FROM expenses 
    WHERE category LIKE '{category}' ORDER BY date DESC LIMIT {limit}""")
    result = cur.fetchall()

    # table
    print()
    print('Your expenses:')
    print('  amount  |    category    |               description                |    date    | item number ')
    print('-------------------------------------------------------------------------------------------')
    for row in result:
        year, month, day = row[3].split('-')
        trans_date = f'{day}-{month}-{year}'
        print(f"{str(row[0]):10s}| {row[1]:14s} | {row[2]:40s} | {trans_date:10s} | {str(row[4]):10s}")
    print()


def add_expense(connection):
    cur = connection.cursor()

    # amount
    while True:
        try:
            amount = float(input("Amount [zl]: "))
            if amount < 0:
                raise ValueError
        except ValueError:
            print('Wrong type. Try again.')
            continue
        else:
            break

    # category
    while True:
        cur.execute("""SELECT category FROM expenses""")
        cat = cur.fetchall()
        used_category = []
        for i in cat:
            if i[0] not in used_category:
                used_category.append(i[0])
        print('Used categories: ', sorted(used_category))
        category = input("Category (max 14 char): ").lower()
        if len(category) > 14:
            print('To long category name. Max 14 character.')
            continue
        else:
            break

    # description
    while True:
        description = input("Description (max 40 char): ")
        if len(description) > 40:
            print('To long description. Max 40 character.')
            continue
        else:
            break

    # date
    while True:
        user_date = input('Date [dd-mm-yyyy] or press Enter to use today date: ')
        if user_date == '':
            #user_date = datetime.date.today().strftime('%d-%m-%Y')
            user_date = datetime.date.today()
            break
        else:
            try:
                #day, month, year = (user_date.split('-'))
                day, month, year = (str(user_date).split('-'))
                datetime.date(int(year), int(month), int(day))
                user_date = datetime.date(int(year), int(month), int(day))
            except ValueError:
                print('Not valid date!')
                continue

            else:
                break


    cur.execute(f"""INSERT INTO expenses VALUES ('{amount:10.2f}', '{category}', '{description}', '{user_date}')""")
    connection.commit()
    print('Added to expenses.')


def delete_expense(connection):
    cur = connection.cursor()
    cur.execute(f"""SELECT rowid FROM expenses""")
    result = cur.fetchall()
    row_deleted = str(input('Enter item number to delete: '))

    if row_deleted not in [str(i[0]) for i in result]:
        print('Wrong number. Try again.')
    else:
        cur.execute(f"""DELETE FROM expenses WHERE rowid='{row_deleted}'""")
        connection.commit()
        print('Expense deleted.')


def show_stats(connection):
    cur = connection.cursor()
    cur.execute(f"""SELECT * FROM expenses""")
    result = cur.fetchall()
    all_expenses = 0
    expense_category = {}
    for row in result:
        #print(row)
        if row[1] in expense_category:
            expense_category[row[1]] += int(row[0])
        else:
            expense_category[row[1]] = int(row[0])
        all_expenses += int(row[0])
    print()
    print(f'Value of all expenses: {all_expenses}')
    print('-'*30)
    for k, v in sorted(expense_category.items()):
        print(f'{k} : {v}')


while True:
    used_numbers = [0, 1, 2, 3, 4, 5]
    print()
    print('Choose option:')
    print('1 - Show expenses')
    print('2 - Add expense')
    print('3 - Delete expense')
    print('4 - Show stats')
    print('5 - Clear database')
    print('0 - Exit')
    print()

    try:
        user_choice = int(input('Choose option: '))
    except ValueError:
        print('Wrong type. Try again.')
        continue
    if user_choice not in used_numbers:
        print('Not in options. Try again.')
        continue


    if user_choice == 1:

        while True:
            used_numbers_2 = [0, 1, 2, 3]
            print()
            print('1 - Show last 5 expenses')
            print('2 - Show expenses in a category')
            print('3 - Show all expenses')
            print('0 - Back to main menu')
            print()

            try:
                user_choice_2 = int(input('Chose option: '))
            except ValueError:
                print('Wrong type. Try again.')
                continue
            if user_choice_2 not in used_numbers_2:
                print('Not in options. Try again.')
                continue


            if user_choice_2 == 1:
                show_expenses(connection, limit=5)

            if user_choice_2 == 2:
                cur = connection.cursor()
                cur.execute(f"""SELECT category FROM expenses""")
                result = cur.fetchall()
                category_list = []
                for cat in result:
                    if cat[0] not in category_list:
                        category_list.append(cat[0])
                print(f'Category list: {category_list}')
                user_category = input('Chose category from list: ')
                if user_category not in category_list:
                    print('Error. Try again.')
                else:
                    show_expenses(connection, user_category)

            if user_choice_2 == 3:
                show_expenses(connection)

            if user_choice_2 == 0:
                break

    if user_choice == 2:
        add_expense(connection)

    if user_choice == 3:
        delete_expense(connection)

    if user_choice == 4:
        show_stats(connection)

    if user_choice == 5:
        while True:
            print('Clear database?')
            user_5 = input("If You want to clear all data press 'Y'\nor press any key and accept enter to back to main menu. >>>>").upper()
            if user_5 == 'Y':
                password = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(10)])
                print('Password :', password)
                user_51 = input('Password: ')
                if user_51 == password:
                    cur = connection.cursor()
                    cur.execute(f"""DELETE FROM expenses""")
                    connection.commit()
                    print('All data clear.')
                    break
                else:
                    print('Incorrect password.')
                    break
            else:
                print('Back to main menu.')
                break

    if user_choice == 0:
        break

connection.close()
