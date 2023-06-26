from collections import UserDict
from datetime import datetime


class Field:
    def __init__(self, value: str):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):
    pass


class Phone(Field):

    @Field.value.setter
    def value(self, value):
        if value.isdigit() and 9 <= len(value) <= 13:
            self._value = value
        else:
            print('Wrong phone number format')
            raise ValueError


class Birthday(Field):

    @Field.value.setter
    def value(self, value):
        try:
            self._value = datetime.strptime(value, '%d.%m.%Y').date()
        except ValueError:
            print('Date should be in format dd.mm.YYYY')
            raise ValueError


class Record:

    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None):
        self.name = name
        self.phones = []
        if phone is not None:
            self.phones.append(phone)
        self.birthday = birthday

    def add_phone(self, phohe: Phone):
        self.phones.append(phohe)

    def change_phone(self, phohe: Phone, new_phohe: Phone):
        i = 0
        while i < len(self.phones):
            if self.phones[i] == phohe:
                self.phones[i] = new_phohe
                break
            else:
                i += 1

    def days_to_birthday(self):
        if not self.birthday:
            return None

        now_day = datetime.now().date()

        bd_date = self.birthday.value.replace(year=now_day.year)
        if bd_date < now_day:
            bd_date = bd_date.replace(year=now_day.year + 1)

        delta = bd_date - now_day
        return delta.days

    def __str__(self):
        str_of_phones = [ph.value for ph in self.phones]
        if self.birthday is not None:
            name_str = self.name.value.ljust(10)
            phones_str = ', '.join(str_of_phones)
            birthday_str = f'Birthday is: {self.birthday.value}'
            return f'{name_str}:{phones_str}, {birthday_str}'
        else:
            name_str = self.name.value.ljust(10)
            phones_str = ', '.join(str_of_phones)
            return f'{name_str}:{phones_str}'


class AddressBook(UserDict):

    def add_record(self, rec: Record):
        self.data[rec.name.value] = rec


    def iterator(self, page_size=5):
        records = list(self.data.values())
        for i in range(0, len(records), page_size):
            block = ''.join(str(rec) + '\n' for rec in records[i:i + page_size])
            if i + page_size < len(records):
                block += '-*-' * 10 + '\n'
            yield block


