from iss_tracker import get_data, find_header, find_metadata, find_comments, find_iss_list, epoch_to_list, find_closest_epoch, find_matching_epoch, find_matching_speed, calculate_current_speed, calculate_location_astropy, calculate_location_geopy, find_location, find_now
import pytest
import requests

def test_get_data():
    return

response1 = requests.get('http://127.0.0.1:5000/header')
def test_find_header():
    assert response1.status_code == 200
    assert isinstance(response1.json(), dict) == True

response2 = requests.get('http://127.0.0.1:5000/metadata')
def test_find_metadata():
    assert response2.status_code == 200
    assert isinstance(response2.json(), dict) == True

response3 = requests.get('http://127.0.0.1:5000/comment')
def test_find_comments():
    assert response3.status_code == 200
    assert isinstance(response3.json(), list) == True

response4 = requests.get('http://127.0.0.1:5000/epochs')
representative_epoch = response4.json()[0]['EPOCH']
sv_17 = response4.json()[17]
sv_167 = response4.json()[167]
response5 = requests.get('http://127.0.0.1:5000/epochs?limit=150&offset=17')
def test_find_iss_list():
    assert response4.status_code == 200
    assert isinstance(response4.json(), list) == True
    assert isinstance(response5.json(), list) == True
    assert response5.json()[0] == sv_17
    assert response5.json()[-1] == sv_167
    assert len(response5.json()) == 167

def test_epoch_to_list():
    assert epoch_to_list('2024-047T23:59:00.000Z') == [2024, 47, 23, 59]
    assert epoch_to_list('2024-002T01:01:00.000Z') == [2025, 2, 1, 1]

 def test_find_closest_epoch():
     test_epoch_list = [{'EPOCH': '2024-048T00:07:00.000Z'}, {'EPOCH': '2024-048T00:11:00.000Z'}, {'EPOCH':'2024-048T00:15:00.000Z'}]
     assert find_closest_epoch(test_epoch_list, [2024, 2, 17, 0, 9, 0]) == {'EPOCH': '2024-048T00:07:00.000Z'}

response6 = requests.get('http://127.0.0.1:5000/epochs/' + representative_epoch)
def test_find_matching_epoch():
    assert response6.status_code == 200
    assert isinstance(response6.json(), dict) == True
    assert response6.json() == response4.json()[0]

response7 = requests.get('http://127.0.0.1:5000/epochs/' + representative_epoch + '/speed')
def test_find_matching_speed():
    assert response7.status_code == 200
    assert isinstance(response7.json(), dict) == True

example_sv = {}
def test_calculate_current_speed():
    return

def test_calculate_location_astropy():
    return

def test_calculate_location_geopy():
    return

response8 = requests.get(('http://127.0.0.1:5000/epochs/' + representative_epoch + '/location'))
def test_find_location():
    assert response8.status_code == 200
    assert isinstance(response8.json(), dict) == True

response9 = requests.get('http://127.0.0.1:5000/now')
def test_find_now():
    asser response9.status_code == 200
    assert isinstance(response9.json(), dict) == True
