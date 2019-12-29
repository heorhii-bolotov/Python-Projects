class Value:
    def __init__(self):
        self.amount = 0

    def __get__(self, obj, obj_type=None):
        # if obj is None:
        #     return self
        return int(self.amount * (1 - obj.commission))

    def __set__(self, obj, value):
        # if obj is None:
        #     return self
        self.amount = value


class Account:
    amount = Value()

    def __init__(self, commission):
        self.commission = commission


new_account = Account(0.1)
new_account.amount = 100

print(new_account.amount)
