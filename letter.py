class Letter:

    def __init__(self, name, user, path, l_approved, l_rej1, l_rej2, claimed, date_m):
        self._name = name
        self._user = user
        self._path = path
        self._l_approved = l_approved
        self._l_rej1 = l_rej1
        self._l_rej2 = l_rej2
        self._claimed = claimed
        self._date_m = date_m

    def name(self):
        return self._name

    def user(self):
        return self._user

    def path(self):
        return self._path

    def l_rej1(self):
        return self._l_rej1

    def l_rej2(self):
        return self._l_rej2

    def claimed(self):
        return self._claimed

    def date_m(self):
        return self._date_m

