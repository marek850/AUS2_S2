import random
from DataStructure.Record import Record
import Visit


class Customer(Record):
    def __init__(self, name=None,  surname=None, ecv=None):
        super().__init__()
        if name is not None and ecv is not None and surname is not None:
            self.__id = random.randint(1, 1000)
            self.__name = name
            self.__name_valid_str = len(name)
            self.__ecv = ecv
            self.__ecv_valid_str = len(ecv)
            self.__surname = surname
            self.__surname_valid_str = len(surname)
            self.__valid_visits = 0
            self.__visits = []
            
        else:
            self.__id = random.randint(1, 1000)
            self.__name = "Unknown"
            self.__name_valid_str = len("Unknown")
            self.__ecv = "SHGAT621"
            self.__ecv_valid_str = len(self.__ecv)
            self.__surname = "Not specified"
            self.__surname_valid_str = len("Not specified")
            self.__visits = []
        while len(self.__visits) < 5:
            self.__visits.append(Visit())  # Fill with empty instances
    # ID property
    @property
    def id(self):
        return self.__id

    # Name property
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value
        self.__name_valid_str = len(value)  # Update the validity string length automatically

    # Name valid string length property
    @property
    def name_valid_str(self):
        return self.__name_valid_str

    # ECV property
    @property
    def ecv(self):
        return self.__ecv

    @ecv.setter
    def ecv(self, value):
        self.__ecv = value
        self.__ecv_valid_str = len(value)  # Update the validity string length automatically

    # ECV valid string length property
    @property
    def ecv_valid_str(self):
        return self.__ecv_valid_str

    # Surname property
    @property
    def surname(self):
        return self.__surname

    @surname.setter
    def surname(self, value):
        self.__surname = value
        self.__surname_valid_str = len(value)  # Update the validity string length automatically

    # Surname valid string length property
    @property
    def surname_valid_str(self):
        return self.__surname_valid_str

    # Valid visits property
    @property
    def valid_visits(self):
        return self.__valid_visits

    @valid_visits.setter
    def valid_visits(self, value):
        self.__valid_visits = value

    # Visits property
    @property
    def visits(self):
        return self.__visits

    @visits.setter
    def visits(self, value):
        self.__visits = value
    def to_byte_array(self):
        byte_array = bytearray()
        byte_array += self.__id.to_bytes(4, 'little')
        byte_array += (len(self.__name).to_bytes(4, 'little'))
        byte_array += bytes(self.__name, encoding='utf-8') 
        byte_array += self.__name_valid_str.to_bytes(4, 'little')
        byte_array += (len(self.__ecv).to_bytes(4, 'little'))
        byte_array += bytes(self.__ecv, encoding='utf-8') 
        byte_array += self.__ecv_valid_str.to_bytes(4, 'little')
        byte_array += (len(self.__surname).to_bytes(4, 'little'))
        byte_array += bytes(self.__surname, encoding='utf-8') 
        byte_array += self.__surname_valid_str.to_bytes(4, 'little')
        byte_array += self.__valid_visits.to_bytes(4, 'little')
        for visit in self.__visits:
            byte_array += visit.to_byte_array() 
        return byte_array
    @staticmethod 
    def from_byte_array(byte_array):
          # Create an empty Customer object
        offset = 0  # Start at the beginning of the byte array
        
        __id = int.from_bytes(byte_array[offset:offset + 4], 'little')
        offset += 4

        name_length = int.from_bytes(byte_array[offset:offset + 4], 'little')
        offset += 4
        
        __name = byte_array[offset:offset + name_length].decode('utf-8')
        offset += name_length

        __name_valid_str = int.from_bytes(byte_array[offset:offset + 4], 'little')
        offset += 4

        ecv_length = int.from_bytes(byte_array[offset:offset + 4], 'little')
        offset += 4

        __ecv = byte_array[offset:offset + ecv_length].decode('utf-8')
        offset += ecv_length
        
        __ecv_valid_str = int.from_bytes(byte_array[offset:offset + 4], 'little')
        offset += 4

        surname_length = int.from_bytes(byte_array[offset:offset + 4], 'little')
        offset += 4

        __surname = byte_array[offset:offset + surname_length].decode('utf-8')
        offset += surname_length

        __surname_valid_str = int.from_bytes(byte_array[offset:offset + 4], 'little')
        offset += 4

        __valid_visits = int.from_bytes(byte_array[offset:offset + 4], 'little')
        offset += 4


        one_visit_size = len(Visit().to_byte_array())
        end_offset = offset + __valid_visits * one_visit_size
        __visits = []
        # Deserialize the descriptions
        while offset < end_offset:
            __visits.append(Visit.from_byte_array(byte_array[offset:offset + one_visit_size]))
            offset += one_visit_size
        
        while len(__visits) < 5:
            __visits.append(Visit())
        customer = Customer(__name[0:__name_valid_str], __surname[0:__surname_valid_str], __ecv[0:__ecv_valid_str])
        customer.valid_visits = __valid_visits
        customer.visits = __visits
        return customer
    