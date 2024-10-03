import cred
from dhanhq import dhanhq
class DhanAPI:
    def __init__(self):
        self.client_id = cred.dhan["client_id"]
        self.access_token = cred.dhan["token"]
        self.__dhan = None

    def get_dhan(self):
        if self.__dhan is None:
            self.__dhan = dhanhq(self.client_id, self.access_token)
        return self.__dhan

dhan = DhanAPI().get_dhan()