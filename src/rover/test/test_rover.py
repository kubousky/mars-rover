import pytest
from src.rover.rover import (
    Rover,
    Direction,
    InvalidDirectionError,
    ObstacleEncounteredError
)


@pytest.fixture
def map():
    map = {
        "rock": (0,1),
        "crater": (2,1),
    }
    return map.copy()

def test_upload_map(map):
    rover = Rover([0,0], Direction.NORTH)
    rover.upload_map(map)
    assert rover.map["rock"] == map["rock"]

def test_instance_rover_with_wrong_direction():
    with pytest.raises(InvalidDirectionError):
        Rover([0,0], 'Z')

def test_correct_position_wrapping_north_edge():
    assert Rover.correct_position([0,11]) == [0,0]

def test_correct_position_wrapping_south_edge():
    assert Rover.correct_position([0,-1]) == [0,10]

def test_correct_position_wrapping_east_edge():
    assert Rover.correct_position([-1,0]) == [10,0]

def test_correct_position_wrapping_west_edge():
    assert Rover.correct_position([11,0]) == [0,0]

def test_no_obstacle(map):
    assert Rover.no_obstacle([0,1], map) == False
    assert Rover.no_obstacle([1,1], map) == True

def test_next_forward_position():
    rover = Rover([0,0], Direction.NORTH)
    assert rover.next_forward_position == [0,1]
    rover = Rover([0,0], Direction.EAST)
    assert rover.next_forward_position == [1,0]

def test_next_backward_position():
    rover = Rover([0,1], Direction.NORTH)
    assert rover.next_backward_position == [0,0]
    rover = Rover([1,1], Direction.WEST)
    assert rover.next_backward_position == [2,1]

def test_succeed_to_move_rover_forward(map):
    rover = Rover([0,0], Direction.EAST)
    rover.map = map
    rover.move_forward()
    assert rover.current_position == [1,0]

def test_succeed_to_double_move_rover_forward(map):
    rover = Rover([0,0], Direction.EAST)
    rover.map = map
    rover.move_forward()
    rover.move_forward()
    assert rover.current_position == [2,0]

def test_fail_to_move_rover_forward(map):
    rover = Rover([0,0], Direction.NORTH)
    rover.map = map
    with pytest.raises(ObstacleEncounteredError):
        rover.move_forward()

def test_succeed_to_move_rover_backward(map):
    rover = Rover([0,0], Direction.EAST)
    rover.map = map
    rover.move_backward()
    assert rover.current_position == [10,0]

def test_fail_to_move_rover_backward(map):
    rover = Rover([2,0], Direction.SOUTH)
    rover.map = map
    with pytest.raises(ObstacleEncounteredError):
        rover.move_backward()

def test_turn_right():
    rover = Rover([0,0], Direction.NORTH)
    rover.turn_right()
    assert rover.direction == Direction.EAST

def test_turn_left():
    rover = Rover([0,0], Direction.NORTH)
    rover.turn_left()
    assert rover.direction == Direction.WEST

def test_succeed_with_all_commands(map):
    rover = Rover([0,0],  Direction.EAST)
    rover.map = map
    rover.get_commands(["f","f","f","l","f"])
    assert rover.current_position == [3,1]
    assert rover.direction == Direction.NORTH

def test_fail_to_finish_commands(map):
    rover = Rover([0,0], Direction.EAST)
    rover.map = map
    with pytest.raises(ObstacleEncounteredError):
        rover.get_commands(["f","f","l","f"])

def test_position_when_fail_last_command(map):
    rover = Rover([0,0], Direction.EAST)
    rover.map = map
    with pytest.raises(ObstacleEncounteredError):
        rover.get_commands(["f","f","l","f"])
    assert rover.current_position == [2,0]
    assert rover.direction == Direction.NORTH
