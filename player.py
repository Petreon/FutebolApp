from typing import List
from datapoint import DataPoint

class Player():
    
    def __init__(self, name = "") -> None:
        self.name: str = name
        self.data: List[DataPoint] = []
        