import random


class KeyGenerator:
    def __init__(self):
        self.__ids = set()
        self.__ecvs = set()

    def generate_id(self):
        return self.generate_unique_value(4, self.__ids)
    def generate_unique_value(self, max_length, existing_values):
        value = random.randint(0, 2147483647)
        while value in existing_values:
            value = random.randint(0, 2**max_length - 1)
        existing_values.add(value)
        return value
    def generate_ecv(self):
        return self.generate_unique_string(self.__ecvs)
    def generate_unique_string(self, existing_strings):
        value = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=10))
        while value in existing_strings:
            value = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=10))
        existing_strings.add(value)
        return value
