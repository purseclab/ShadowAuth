from . import EngineControlUnit

class Context:
    can_id: int
    ecu: EngineControlUnit.EngineControlUnit
    msg: bytearray
    is_authenticated: bool

    def __init__(self, can_id = None, ecu = None, msg = None, is_authenticated = False):
        self.can_id = can_id
        self.ecu = ecu
        self.msg = msg
        self.is_authenticated = is_authenticated
