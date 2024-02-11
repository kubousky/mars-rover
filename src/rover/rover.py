"""
Rover Class able to receive instructions from Earth.
"""
from typing import List, Dict
from enum import Enum
from .errors import (
    InvalidDirectionError,
    UploadingError,
    ObstacleEncounteredError,
    SteeringSystemError
)


EQUATOR_LENGTH = 10
MERIDIAN_LENGTH = 10


class Direction(Enum):
    NORTH = "North"
    SOUTH = "South"
    EAST = "East"
    WEST = "West"


class Rover:
    def __init__(self, current_position, direction):
        if len(current_position) != 2:
            raise ValueError("Position must contain exactly two integers")
        self.current_position: List[int] = current_position
        if direction not in Direction.__members__.values():
            raise InvalidDirectionError("Introduce correct direction.")
        self.direction: Direction = direction
        self.map: Dict[str, tuple] = dict()


    def upload_map(self, new_map: Dict[str, tuple]):
        try:
            self.map.update(new_map)
        except:
            raise UploadingError("An error occured during the map uploading.")

    @staticmethod
    def correct_position(position: List[int]) -> List[int]:
        """method that implements wrapping at edges"""
        if position[0] > EQUATOR_LENGTH:
            position[0] = 0
        elif position[0] < 0:
            position[0] = EQUATOR_LENGTH

        elif position[1] > MERIDIAN_LENGTH:
            position[1] = 0
        elif position[1] < 0:
            position[1] = MERIDIAN_LENGTH
        return position

    @staticmethod
    def no_obstacle(next_position: List[int], map: Dict) -> bool:
        for pos in map.values():
            if list(pos) == next_position:
                return False
        return True

    @property
    def next_forward_position(self) -> List[int]:
        next_position = self.current_position.copy()
        if self.direction == Direction.NORTH:
            next_position[1] = self.current_position[1] + 1
        elif self.direction == Direction.SOUTH:
            next_position[1] =  self.current_position[1] - 1
        elif self.direction == Direction.EAST:
            next_position[0] = self.current_position[0] + 1
        else:
            next_position[0] = self.current_position[0] - 1
        return next_position

    @property
    def next_backward_position(self) -> List[int]:
        next_position = self.current_position.copy()
        if self.direction == Direction.NORTH:
            next_position[1] = self.current_position[1] - 1
        elif self.direction == Direction.SOUTH:
            next_position[1] = self.current_position[1] + 1
        elif self.direction == Direction.EAST:
            next_position[0] = self.current_position[0] - 1
        else:
            next_position[0] = self.current_position[0] + 1
        return next_position


    def move_forward(self) -> None:
        next_possible_position = self.correct_position(self.next_forward_position)
        if self.no_obstacle(next_possible_position, self.map):
            self.current_position = next_possible_position
        else:
            raise ObstacleEncounteredError("Obstacle encountered, moving back to the last possible point")


    def move_backward(self) -> None:
        next_possible_position = self.correct_position(self.next_backward_position)
        if self.no_obstacle(next_possible_position, self.map):
            self.current_position = next_possible_position
        else:
            raise ObstacleEncounteredError("Obstacle encountered, moving back to the last possible point")


    def turn_right(self):
        if self.direction:
            new_direction = {
                Direction.NORTH: Direction.EAST,
                Direction.EAST: Direction.SOUTH,
                Direction.SOUTH: Direction.WEST,
                Direction.WEST: Direction.NORTH,
                }.get(self.direction)
        if new_direction:
            self.direction = new_direction
            return
        raise SteeringSystemError(
            "Invalid steering system. Could not change direction."
        )


    def turn_left(self):
        if self.direction:
            new_direction = {
                Direction.NORTH: Direction.WEST,
                Direction.WEST: Direction.SOUTH,
                Direction.SOUTH: Direction.EAST,
                Direction.EAST: Direction.NORTH,
                }.get(self.direction)
        if new_direction:
            self.direction = new_direction
            return
        raise SteeringSystemError(
            "Invalid steering system. Could not change direction."
        )


    def get_commands(self, commands: List[str]) -> None:
        for c in commands:
            if c == "r":
                self.turn_right()
            elif c == "l":
                self.turn_left()
            elif c == "f":
                self.move_forward()
            elif c == "b":
                self.move_backward()
