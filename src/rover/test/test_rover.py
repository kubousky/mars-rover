import pytest
from unittest.mock import patch
from src.rover.rover import (
    Rover, 
    UnexceptedDirection, 
    ObstacleEncountered
)


@pytest.fixture
def moon_map():
    MOON_MAP = {
        "rock": (0,1),
        "crater": (2,1),
    }
    return MOON_MAP.copy() 

def test_upload_map(moon_map):
    rover = Rover([0,0], 'N')
    rover.upload_map(moon_map)
    assert rover.map["rock"] == moon_map["rock"]

def test_instance_rover_with_wrong_direction():
    with pytest.raises(UnexceptedDirection):
        Rover([0,0], 'WRONG')

def test_correct_position_wrapping_north_edge():
    assert Rover.correct_position([0,11]) == [0,0]

def test_correct_position_wrapping_south_edge():
    assert Rover.correct_position([0,-1]) == [0,10]

def test_correct_position_wrapping_east_edge():
    assert Rover.correct_position([-1,0]) == [10,0]

def test_correct_position_wrapping_west_edge():
    assert Rover.correct_position([11,0]) == [0,0]

def test_clear_way(moon_map):
    assert Rover.clear_way([0,1], moon_map) == False
    assert Rover.clear_way([1,1], moon_map) == True

def test_next_forward_position():
    rover = Rover([0,0], 'N')
    assert rover.next_forward_position == [0,1]
    rover = Rover([0,0], 'E')
    assert rover.next_forward_position == [1,0]

def test_next_backward_position():
    rover = Rover([0,1], 'N')
    assert rover.next_backward_position == [0,0]
    rover = Rover([1,1], 'W')
    assert rover.next_backward_position == [2,1]

def test_succeed_to_move_rover_forward(moon_map):
    rover = Rover([0,0], 'E')
    rover.map = moon_map
    rover.move_forward()
    assert rover.current_position == [1,0]

def test_succeed_to_double_move_rover_forward(moon_map):
    rover = Rover([0,0], 'E')
    rover.map = moon_map
    rover.move_forward()
    rover.move_forward()
    assert rover.current_position == [2,0]

def test_fail_to_move_rover_forward(moon_map):
    rover = Rover([0,0], 'N')
    rover.map = moon_map
    with pytest.raises(ObstacleEncountered):
        rover.move_forward()

def test_succeed_to_move_rover_backward(moon_map):
    rover = Rover([0,0], 'E')
    rover.map = moon_map
    rover.move_backward()
    assert rover.current_position == [10,0]

def test_fail_to_move_rover_backward(moon_map):
    rover = Rover([2,0], 'S')
    rover.map = moon_map
    with pytest.raises(ObstacleEncountered):
        rover.move_backward()

def test_turn_right():
    rover = Rover([0,0], 'N')
    rover.turn_right()
    assert rover.direction == "E"

def test_turn_left():
    rover = Rover([0,0], 'N')
    rover.turn_left()
    assert rover.direction == "W"

def test_succeed_with_all_commands(moon_map):
    rover = Rover([0,0], 'E')
    rover.map = moon_map
    rover.get_commands(["f","f","f","l","f"])
    assert rover.current_position == [3,1]
    assert rover.direction == "N"

def test_fail_to_finish_commands(moon_map):
    rover = Rover([0,0], 'N')
    rover.map = moon_map
    with pytest.raises(ObstacleEncountered):
        rover.get_commands(["f","r","f"])
