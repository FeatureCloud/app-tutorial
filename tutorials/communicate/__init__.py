from enum import Enum


class States(Enum):
    initial = 'initial'
    broadcaster = 'Broadcaster'
    waiter = 'Waiter'
    sender = 'Sender'
    aggregator = 'Aggregator'
    terminal = 'terminal'
