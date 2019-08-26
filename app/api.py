from app.models import Import, Citizen
from app import db
from app import validators
from datetime import datetime as dt
import numpy as np


def count_age(citizen):
    today = dt.today()
    correction = 0 if (today.month, today.day) >= (citizen.birth_date.month, citizen.birth_date.day) else 1
    return today.year - citizen.birth_date.year - correction


def create_citizen(*, import_id, data):
    sep = ','
    relatives_str = sep.join(map(str, data['relatives']))
    birth_date = dt.strptime(data['birth_date'], '%d.%m.%Y')
    citizen = Citizen(import_id=import_id,
                      citizen_id=data['citizen_id'],
                      town=data['town'],
                      street=data['street'],
                      building=data['building'],
                      apartment=data['apartment'],
                      name=data['name'],
                      birth_date=birth_date,
                      gender=data['gender'],
                      relatives=relatives_str)
    try:
        db.session.add(citizen)
        db.session.commit()
    except:
        db.session.rollback()


def update_relatives(*, import_, citizen, new_rel):
    sep = ','
    if citizen.relatives:
        old_rel = [int(id_) for id_ in citizen.relatives.split(sep) if id_]
    else:
        old_rel = []
    for relative_id in old_rel:
        if relative_id not in new_rel:
            relative = [rel for rel in import_.citizens if rel.citizen_id == relative_id][0]
            lst = [int(rel) for rel in relative.relatives.split(sep) if rel]
            lst.remove(citizen.citizen_id)
            relative.relatives = sep.join(map(str, lst))

            citizen_rel = [int(rel) for rel in citizen.relatives.split(sep) if rel]
            citizen_rel.remove(relative_id)
            citizen.relatives = sep.join(map(str, citizen_rel))
    db.session.commit()

    for relative_id in new_rel:
        if relative_id not in old_rel:
            relative = [rel for rel in import_.citizens if rel.citizen_id == relative_id][0]
            lst = [int(rel) for rel in relative.relatives.split(sep) if rel]
            lst.append(citizen.citizen_id)
            relative.relatives = sep.join(map(str, lst))
            citizen_rel = [int(rel) for rel in citizen.relatives.split(sep) if rel]
            citizen_rel.append(relative_id)
            citizen.relatives = sep.join(map(str, citizen_rel))
    db.session.commit()



def update_citizen(*, import_, citizen, diff):
    for key, value in diff.items():
        if key == 'town':
            citizen.town = value
        elif key == 'street':
            citizen.street = value
        elif key == 'building':
            citizen.building = value
        elif key == 'name':
            citizen.name = value
        elif key == 'gender':
            citizen.gender = value
        elif key == 'birth_date':
            birth_date = dt.strptime(value, '%d.%m.%Y')
            citizen.birth_date = birth_date
        elif key == 'apartment':
            citizen.apartment = value
        elif key == 'relatives':
            update_relatives(import_=import_, citizen=citizen, new_rel=value)
    
    db.session.commit()
    birth_date = dt.strftime(citizen.birth_date, '%d.%m.%Y')
    sep = ','
    if citizen.relatives:
        relatives = [int(id_) for id_ in citizen.relatives.split(sep) if id_]
    else:
        relatives = []
    return {'citizen_id': citizen.citizen_id,
            'town': citizen.town,
            'street': citizen.street,
            'building': citizen.building,
            'apartment': citizen.apartment,
            'name': citizen.name,
            'gender': citizen.gender,
            'birth_date': birth_date,
            'relatives': relatives}
    
    
def post(data):
    if validators.check_data(data):
        import_rec = Import()
        try:
            db.session.add(import_rec)
            db.session.commit()
        except:
            db.session.rollback()
        import_id = import_rec.import_id
        for citizen in data['citizens']:
            create_citizen(import_id=import_id, data=citizen)
        return import_id, 201
    else:
        return False, 400


def patch(*, import_id, citizen_id, diff):
    if 'citizen_id' in diff.keys():
        return False, 400
    try:
        import_ = db.session.query(Import).filter_by(import_id=import_id).one()
        citizen = db.session.query(Citizen).filter_by(import_id=import_id, 
                                                      citizen_id=citizen_id).one()
    except:
        return False, 400
    if not validators.check_fields(import_=import_, citizen=citizen, diff=diff):
        return False, 400
    new_info = update_citizen(import_=import_, citizen=citizen, diff=diff)
    return new_info, 200    
    

def get(import_id):
    try:
        import_ = db.session.query(Import).filter_by(import_id=import_id).one()
    except:
        return False, 400
    response = []
    for citizen in import_.citizens:
        json_citizen = {'citizen_id': citizen.citizen_id,
                        'town': citizen.town,
                        'street': citizen.street,
                        'building': citizen.building,
                        'apartment': citizen.apartment,
                        'name': citizen.name,
                        'gender': citizen.gender}
        birth_date = dt.strftime(citizen.birth_date, '%d.%m.%Y')
        sep = ','
        if citizen.relatives:
            relatives = [int(id_) for id_ in citizen.relatives.split(sep) if id_]
        else:
            relatives = []
        json_citizen['birth_date'] = birth_date
        json_citizen['relatives'] = relatives
        response.append(json_citizen)
    return response, 200


def get_pres(import_id):
    sep = ','
    try:
        import_ = db.session.query(Import).filter_by(import_id=import_id).one()
    except:
        return False, 400
    response = {str(key): list() for key in range(1, 13)}
    for citizen in import_.citizens:
        relatives = [int(id_) for id_ in citizen.relatives.split(sep) if id_]
        pres_per_month = {key: 0 for key in range(1, 13)}
        for relative_id in relatives:
            relative = [rel for rel in import_.citizens if rel.citizen_id == relative_id][0]
            month = relative.birth_date.month
            pres_per_month[month] += 1
        for key, value in pres_per_month.items():
            if value > 0:
                dct = {'citizen_id': citizen.citizen_id,
                       'presents': value}
                response[str(key)].append(dct)
    return response, 200


def get_stat(import_id):
    try:
        import_ = db.session.query(Import).filter_by(import_id=import_id).one()
    except:
        return False, 400
    cities = {}
    for citizen in import_.citizens:
        if citizen.town not in cities.keys():
            cities[citizen.town] = [count_age(citizen)]
        else:
            cities[citizen.town].append(count_age(citizen))
    response = []
    for city, ages in cities.items():
        dct = {'town': city,
               'p50': round(np.percentile(ages, 50), 2),
               'p75': round(np.percentile(ages, 75), 2),
               'p99': round(np.percentile(ages, 99), 2)}
        response.append(dct)
    return response, 200
                

