from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not len(value) == 10 or not value.isnumeric():
            msg = 'Phone number should string that consists of 10 digits.'
            raise ValueError(msg)
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone_str):
        if phone_str in self.phones:
            return
        phone = Phone(phone_str)
        self.phones.append(phone)

    def find_phone(self, phone_str):
        for phone in self.phones:
            if phone_str == phone.value:
                return phone
        raise KeyError('Phone number does not exist.')

    def remove_phone(self, phone_str):
        for i in range(len(self.phones)):
            if phone_str == self.phones[i].value:
                del self.phones[i]
                return
        raise KeyError('Phone number does not exist.')

    def edit_phone(self, existing_phone, new_phone):
        for index in range(len(self.phones)):
            if self.phones[index].value == existing_phone:
                self.phones[index] = Phone(new_phone)
                break
        else:
            raise KeyError('Phone number does not exist.')

    def __str__(self):
        phones = '; '.join(p.value for p in self.phones)
        return f'Contact name: {self.name.value}, phones: {phones}'


class AddressBook(UserDict):
    def add_record(self, record_candidate):
        if not type(record_candidate) == Record:
            raise ValueError('Record should instance of corresponfing class.')
        self.data[record_candidate.name.value] = record_candidate

    def delete(self, record_name):
        if record_name not in self.data:
            raise KeyError('Contact with such name does not exist.')
        del self.data[record_name]

    def find(self, record_name):
        if record_name not in self.data:
            raise KeyError('Contact with such name does not exist.')
        return self.data[record_name]


if __name__ == '__main__':
    book = AddressBook()
    # Створення запису для John
    john_record = Record('John')
    john_record.add_phone('1234567890')
    john_record.add_phone('5555555555')

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record('Jane')
    jane_record.add_phone('9876543210')
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find('John')
    john.edit_phone('1234567890', '1112223333')
    # Виведення: Contact name: John, phones: 1112223333; 5555555555
    print(john)
    # Видалення
    john.remove_phone('1112223333')
    print(john)

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone('5555555555')
    print(f'{john.name}: {found_phone}')  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete('Jane')
    print(book)
