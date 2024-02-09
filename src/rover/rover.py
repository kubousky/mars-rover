"""
Mars Rover Class able to receive instructions from Earth.
"""
from typing import List, Dict


# Simulates the x-axis and the y-axis
MOON_EDGES = {
    "E": 10,
    "N": 10
}

MOON_MAP = {
    "rock":(1,1),
    "crater": (2,1),
    "crater": (3,1),
}

class UnexceptedDirection(Exception):
    pass

class UploadingError(Exception):
    pass

class ObstacleEncountered(Exception):
    pass


class Rover:
    def __init__(self, current_position, direction):
        self.current_position: List[int] = current_position
        if len(self.current_position) != 2:
            raise ValueError("Position must contain exactly two integers")
        self.direction: str = direction
        if self.direction not in ("N","S","E","W"):
            raise UnexceptedDirection("Introduce correct direction.")
        self.map: Dict[str, tuple] = dict()


    def upload_map(self, new_map: Dict[str, tuple]):
        try:
            self.map.update(new_map)
        except:
            raise UploadingError("An error occured during the map uploading.")

    @staticmethod
    def correct_position(position: List[int]) -> List[int]: 
        """method that implements wrapping at edges"""
        if position[0] > MOON_EDGES["E"]:
            position[0] = 0
        elif position[0] < 0:
            position[0] = MOON_EDGES["E"]

        elif position[1] > MOON_EDGES["N"]:
            position[1] = 0
        elif position[1] < 0:
            position[1] = MOON_EDGES["N"]
        return position

    @staticmethod
    def clear_way(next_position: List[int], map: Dict) -> bool:
        for pos in map.values():
            if list(pos) == next_position:
                return False
        return True
    
    @property
    def next_forward_position(self) -> List[int]:
        next_position = self.current_position
        if self.direction == 'N':
            next_position[1] = self.current_position[1] + 1
        elif self.direction == 'S':
            next_position[1] =  self.current_position[1] - 1
        elif self.direction == 'E':
            next_position[0] = self.current_position[0] + 1
        else:
            next_position[0] = self.current_position[0] - 1
        return next_position
    
    @property
    def next_backward_position(self) -> List[int]:
        next_position = self.current_position
        if self.direction == 'N':
            next_position[1] = self.current_position[1] - 1
        elif self.direction == 'S':
            next_position[1] = self.current_position[1] + 1
        elif self.direction == 'E':
            next_position[0] = self.current_position[0] - 1
        else:
            next_position[0] = self.current_position[0] + 1
        return next_position


    def move_forward(self) -> None:
        next_possible_position = self.correct_position(self.next_forward_position)
        if self.clear_way(next_possible_position, self.map):
            self.current_position = next_possible_position
        else:
            raise ObstacleEncountered("Obstacle encountered, moving back to the last possible point")        


    def move_backward(self) -> None:
        next_possible_position = self.correct_position(self.next_backward_position)
        if self.clear_way(next_possible_position, self.map):
            self.current_position = next_possible_position
        else:
            raise ObstacleEncountered("Obstacle encountered, moving back to the last possible point") 


    def turn_right(self) -> None:
        if self.direction == "N":
            self.direction = "E"
        elif self.direction == "E":
            self.direction = "S"
        elif self.direction == "S":
            self.direction = "W"
        else:
            self.direction = "N"


    def turn_left(self) -> None:
        if self.direction == "N":
            self.direction = "W"
        elif self.direction == "W":
            self.direction = "S"
        elif self.direction == "S":
            self.direction = "E"
        else:
            self.direction = "N"


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
