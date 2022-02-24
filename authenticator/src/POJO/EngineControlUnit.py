
class EngineControlUnit(dict):
    def __init__(self, id = None, nonce = 0):
        self["id"] = id
        self["nonce"] = nonce


    @property
    def id(self):
        return self["id"]
    @property
    def nonce(self):
        return self["nonce"]

    def increase_nonce(self):
        self["nonce"] += 1
        if self["nonce"] > 4294967295:
            self["nonce"] = 0
