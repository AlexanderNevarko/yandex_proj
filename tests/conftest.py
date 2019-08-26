import pytest
import requests


base_url = 'http://0.0.0.0:8080'

@pytest.fixture
def created_import():
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
                 relatives=[]
                 )
        )
    payload = dict(citizens=citizens)

    response = requests.post(url=f'{base_url}/imports', json=payload)
    assert response.status_code == 201
    import_id = response.json()['data']['import_id']
    yield import_id
