from iss_tracker import find_iss_list, epoch_to_list, find_closest_epoch, calculate_current_speed, calculate_average_speed
import pytest

def test_find_iss_list():
    assert isinstance(find_iss_list(), list) == True
    assert isinstance(find_iss_list()[0], dict) == True

def test_epoch_to_list():
    assert epoch_to_list('2024-047T23:59:00.000Z') == [2024, 47, 23, 59]
    assert epoch_to_list('2024-002T01:01:00.000Z') == [2025, 2, 1, 1]

 def test_find_closest_epoch():
     test_epoch_list = [{'EPOCH': '2024-048T00:07:00.000Z'}, {'EPOCH': '2024-048T00:11:00.000Z'}, {'EPOCH':'2024-048T00:15:00.000Z'}]
     assert find_closest_epoch(test_epoch_list, [2024, 2, 17, 0, 9, 0]) == {'EPOCH': '2024-048T00:07:00.000Z'}

def test_calculate_current_speed():
    assert calculate_current_speed({'X_DOT': -12.01 , 'Y_DOT': -17.85 , 'Z_DOT' : -10}) == pytest.approx(23.7247, .001)
    assert calculate_current_speed({'X_DOT' : 0, 'Y_DOT': 0, 'Z_DOT': 0}) == pytest.approx(0, .001)
    assert calculate_current_speed({'X_DOT' : 57.36, 'Y_DOT': -8.39, 'Z_DOT': 73.8}) == pytest.approx(93.8456, .001)

def test_calculate_average_speed():
    example = [{'X_DOT': -12.01 , 'Y_DOT': -17.85 , 'Z_DOT' : -10}, {'X_DOT' : 0, 'Y_DOT': 0, 'Z_DOT': 0}, {'X_DOT' : 57.36, 'Y_DOT': -8.39, 'Z_DOT': 73.8}]
    assert calculate_average_speed(example) == pytest.approx(39.190, .001)
