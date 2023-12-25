class chain_sum:
    def __init__(self, num):
        self.total = num

    def __call__(self, next_num=0):
        self.total += next_num
        return self

    def __repr__(self):
        return str(self.total)

print(chain_sum(5)())
print(chain_sum(5)(2)())
print(chain_sum(5)(100)(-10)())