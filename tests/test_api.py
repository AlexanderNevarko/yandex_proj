import random
import requests


base_url = 'http://0.0.0.0:8080'


def test_create_valid():
    citizens = list()
    for i in range(1, 100):
        birth_year = 1950 + i % 50
        citizens.append(
            dict(citizen_id=i,
                 town='Moscow',
                 street='street_name',
                 building='building_name',
                 apartment=10,
                 name='test_name',
                 birth_date=f'03.02.{birth_year}',
                 gender='male',
                 relatives=[]
                 )
        )
    payload = dict(citizens=citizens)

    response = requests.post(url=f'{base_url}/imports', json=payload)
    assert response.status_code == 201
    import_id = response.json()['data']['import_id']

    response = requests.get(url=f'{base_url}/imports/{import_id}/citizens')
    assert response.status_code == 200


def test_create_invalid_id():
    citizens = list()
    for i in range(1, 4):
        citizens.append(
            dict(citizen_id='WRONG_CITIZEN_ID',  # invalid
                 town='Moscow',
                 street='street_name',
                 building='building_name',
                 apartment=10,
                 name='test_name',
                 birth_date='03.02.1998',
                 gender='male',
                 relatives=[]
                 )
        )
    payload = dict(citizens=citizens)

    response = requests.post(url=f'{base_url}/imports', json=payload)
    assert response.status_code == 400


def test_create_invalid_name():
    citizens = list()
    for i in range(1, 4):
        citizens.append(
            dict(citizen_id=i,
                 town='Moscow',
                 street='---',  # invalid
                 building='building_name',
                 apartment=10,
                 name='test_name',
                 birth_date='03.02.1998',
                 gender='male',
                 relatives=[]
                 )
        )
    payload = dict(citizens=citizens)

    response = requests.post(url=f'{base_url}/imports', json=payload)
    assert response.status_code == 400


def test_create_invalid_relatives():
    citizens = list()
    for i in range(1, 4):
        citizens.append(
            dict(citizen_id=i,
                 town='Moscow',
                 street='street_name',
                 building='building_name',
                 apartment=10,
                 name='test_name',
                 birth_date='03.02.1998',
                 gender='male',
                 relatives=[1]  # invalid
                 )
        )
    payload = dict(citizens=citizens)

    response = requests.post(url=f'{base_url}/imports', json=payload)
    assert response.status_code == 400


def test_update_valid(created_import):
    response = requests.get(url=f'{base_url}/imports/{created_import}/citizens')
    assert response.status_code == 200
    citizen_ids = [item['citizen_id'] for item in response.json()['data']]

    citizen_id = random.choice(citizen_ids)
    response = requests.patch(url=f'{base_url}/imports/'
                                  f'{created_import}/citizens/{citizen_id}',
                              json=dict(name='new_name'))
    assert response.status_code == 200


def test_update_invalid_birthdate(created_import):
    response = requests.get(url=f'{base_url}/imports/{created_import}/citizens')
    assert response.status_code == 200
    citizen_ids = [item['citizen_id'] for item in response.json()['data']]

    citizen_id = random.choice(citizen_ids)
    response = requests.patch(url=f'{base_url}/imports/'
                                  f'{created_import}/citizens/{citizen_id}',
                              json=dict(birth_date='31.02.1998'))
    assert response.status_code == 400
