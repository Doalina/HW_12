import os
import csv

from classes import Name, Phone, Birthday, Record, AddressBook


def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except KeyError:
            return "Key doesn't exist"
        except ValueError:
            return 'Check the number or name, please'
        except IndexError:
            return 'Element is not present'

    return inner


def hello_message(*args):
    return "Hello! How can I help you?"


@input_error
def add(*args):
    name = Name(args[0][0])
    phone = Phone(args[0][1])
    try:
        birthday = Birthday(args[0][2])
    except:
        birthday = None

    if name.value in address_book.data.keys():
        address_book.data[name.value].add_phone(phone)
    else:
        rec = Record(name, phone=phone, birthday=birthday)
        address_book.add_record(rec)
    return f'Contact for {name.value} was added'


@input_error
def change(*args):
    name = Name(args[0][0])
    phone_to_change = Phone(args[0][1])
    phone_new = Phone(args[0][2])
    if name.value in address_book.data.keys():
        address_book.data[name.value].change_phone(phone_to_change, phone_new)
    else:
        raise ValueError('No person with this name in the address book')
    return f'Phone {phone_to_change.value} of {name.value} was changed to {phone_new.value} '


@input_error
def phone(*args):
    name = Name(args[0][0])
    if name.value in address_book.keys():
        list_of_phones = [ph.value for ph in address_book[name.value].phones]
        return ', '.join(list_of_phones)


def show_all(*args):
    result = ''
    for person in address_book.data.values():
        result += str(person) + '\n'
    return result


def show_block(page_size=10):
    iterator = address_book.iterator()
    current_page = []
    res = ''

    for record in iterator:
        current_page.append(record)

        if len(current_page) == page_size:
            res += ''.join(current_page) + '\n'
            current_page = []

    if current_page:
        res += ''.join(current_page)

    return res


def exit_message(*args):
    return "Good bye!"


def days_to_birthday(*args):
    name = Name(args[0][0])
    if name.value in address_book.keys():
        days = address_book[name.value].days_to_birthday()
        return days


def help_command(*args):
    return ("Please select one of the commands:\n"
            "add user: add 'phone'\n"
            "add user birthday: add 'phone' 'birthday'\n"
            "change user: change\n"
            "show all contacts: show all\n"
            "show user's phone: phone 'name'\n"
            "number of days until your birthday: days 'name'\n"
            "search for entries by characters: find\n")


def find_text(*args):
    search_text = args[0][0]
    matches = []
    for record in address_book.values():
        if search_text in str(record):
            matches.append(str(record))
    if not matches:
        result = f'There are no "{search_text}" characters in the address book'
    else:
        result = '\n'.join(matches)
    return result


HANDLERS = {
    hello_message: ("hello",),
    add: ("add",),
    change: ("change",),
    phone: ("phone",),
    show_all: ("show all",),
    exit_message: ("good bye", "close", "exit"),
    days_to_birthday: ("days",),
    show_block: ("show block",),      # to check the output with pagination
    help_command: ("help_command",),
    find_text: ("find",), # пошук записів за символами
}


def main():
    def processing(user_input):
        for k in HANDLERS:
            for command in HANDLERS[k]:
                if user_input.lower().strip().startswith(command):
                    list_of_data = user_input[len(command):].strip().split(" ")
                    if len(list_of_data) == 1 and list_of_data[0] == '':
                        list_of_data = []
                    return k, list_of_data

    while True:
        user_input = input('Please enter Command: ')
        func, data = processing(user_input)
        print(func(data))
        if func == exit_message:
            break


if __name__ == '__main__':

    address_book = AddressBook()

    if os.path.isfile('my_address_book.csv'):
        with open('my_address_book.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                name = Name(row[0])
                phone = Phone(row[1])
                birthday = Birthday(row[2]) if row[2] else None
                rec = Record(name, phone=phone, birthday=birthday)
                address_book.add_record(rec)

    main()

    with open('my_address_book.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Phone', 'Birthday'])
        for record in address_book.data.values():
            name = record.name.value
            phone = record.phones[0].value if record.phones else ''
            birthday = record.birthday.value if record.birthday else ''
            writer.writerow([name, phone, birthday])


