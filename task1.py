class NameRequiredError(ValueError):
    pass


class NameAndPhoneRequiredError(NameRequiredError):
    pass


class TooLongNameOrPhoneError(ValueError):
    pass


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NameAndPhoneRequiredError:
            return 'Error: namely 2 args (Name & Phone Number) are required.'
        except NameRequiredError:
            return 'Error: namely 1 argument (Name) is required.'
        except TooLongNameOrPhoneError:
            return 'Error: args shouldn\'t contain more than 20 symbols each.'
        except KeyError:
            return 'Error: Contact is not found.'

    return inner


def validate_contact_args(args):
    # seems like validation of the phone number is out of the scope
    if len(args) != 2:
        raise NameAndPhoneRequiredError

    name, phone = args
    if (len(name) > 20 or len(phone) > 20):
        raise TooLongNameOrPhoneError


@input_error
def handle_add_contact(args, contacts):
    validate_contact_args(args)
    name, phone = args
    contacts[name] = phone
    return 'Contact is added.'


@input_error
def handle_change_contact(args, contacts):
    validate_contact_args(args)
    name, phone = args

    if name not in contacts:
        raise KeyError

    contacts[name] = phone
    return 'Contact is updated.'


@input_error
def handle_show_contact(args, contacts):
    if len(args) != 1:
        raise NameRequiredError

    name = args[0]
    return contacts[name]


def handle_get_all(contacts):
    format_str = '{:<21}  {:<21}'
    lines = [format_str.format(name, contacts[name]) for name in contacts]
    output = ['=' * 42, format_str.format('Name:', 'Phone Number: ')]
    output = output + lines + ['=' * 42]

    return '\n'.join(output)


def main():
    contacts = {}
    print('Welcome to the assistant bot!')
    while True:
        user_input = input('Enter a command: ')
        command, *args = parse_input(user_input)

        if command in ['close', 'exit']:
            print('Good bye!')
            break
        elif command == '':
            continue
        elif command == 'hello':
            print('How can I help you?')
        elif command == 'add':
            print(handle_add_contact(args, contacts))
        elif command == 'change':
            print(handle_change_contact(args, contacts))
        elif command == 'phone':
            print(handle_show_contact(args, contacts))
        elif command == 'all':
            print(handle_get_all(contacts))
        else:
            print('Invalid command.')


if __name__ == '__main__':
    main()
