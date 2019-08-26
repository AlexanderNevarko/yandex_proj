from datetime import datetime as dt


def check_citizen_ids(data):
    ids = set()
    for citizen in data['citizens']:
        if citizen['citizen_id'] in ids:
            return False
        else: 
            ids.add(citizen['citizen_id'])
    return True


def check_relatives(*, data, citizen):
    for id_ in citizen['relatives']:
        if id_ == citizen['citizen_id']:
            return False
        relative = [person for person in data['citizens'] if
                    person['citizen_id'] == id_][0]
        if not relative:
            return False
        if citizen['citizen_id'] not in relative['relatives']:
            return False
    return True


def check_date(date_str: str):
    try:
        date = dt.strptime(date_str, '%d.%m.%Y')
    except ValueError:
        return False
    if date >= dt.now():
        return False
    else:
        return True


def check_citizen_fields(*, data, citizen):
    str_fields = ('town', 'street', 'building', 'name', 'gender', 'bith_date')
    int_fields = ('citizen_id', 'apartment')
    for key, value in citizen.items():
        if key in str_fields:
            if not isinstance(value, str):
                return False
            elif key in ('town', 'street', 'building'):
                if len(value) < 1 or len(value) > 256:
                    return False
                elif not any(ch.isdigit() for ch in value) and \
                     not any(ch.isalpha for ch in value):
                    return False
            elif key == 'name':
                if not value or len(value) > 256:
                    return False
            elif key == 'gender':
                if value not in ('male', 'female'):
                    return False

        elif key in int_fields:
            if not isinstance(value, int):
                return False
            elif value < 0:
                return False
    if not check_date(citizen['birth_date']):
        return False
    if not check_relatives(data=data, citizen=citizen):
        return False
    return True
        

def check_data(data):
    if not check_citizen_ids(data):
        return False
    for citizen in data['citizens']:
        if not check_citizen_fields(data=data, citizen=citizen):
            return False
    return True


def check_fields(*, import_, citizen, diff):
    str_fields = ('town', 'street', 'building', 'name', 'gender', 'bith_date')
    for key, value in diff.items():
        if key in str_fields:
            if not isinstance(value, str):
                return False
            elif key in ('town', 'street', 'building'):
                if len(value) < 1 or len(value) > 256:
                    return False
                elif not any(ch.isdigit() for ch in value) and \
                     not any(ch.isalpha for ch in value):
                    return False
            elif key == 'name':
                if not value or len(value) > 256:
                    return False
            elif key == 'gender':
                if value not in ('male', 'female'):
                    return False
        elif key == 'apartment':
            if not isinstance(value, int):
                return False
            elif value < 0:
                return False
        elif key == 'relatives':
            if not isinstance(value, list):
                return False
            for id_ in value:
                if id_ == citizen.citizen_id:
                    return False
                relative = [person for person in import_.citizens if \
                            person.citizen_id == id_][0]
                if not relative:
                    return False
    return True