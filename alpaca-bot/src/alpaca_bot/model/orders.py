from dataclasses import dataclass
from abc import ABC


@dataclass(slots=True)
class Order(ABC):
    symbol: str


@dataclass(slots=True)
class BracketOrder(Order):
    price: float
    shares: int
    stop_loss: float
    take_profit: float

@dataclass(slots=True)
class StopLossUpdate(Order):
    price: float