import hashlib
import random
from DataStructure.HashRecord import HashRecord
from DataStructure.Record import Record
from Data.Visit import Visit
from bitarray import bitarray

class Customer(Record):
    def __init__(self, name=None,  surname=None, ecv=None, id = None):
        super().__init__()
        if name is not None and ecv is not None and surname is not None:
            if id is not None:
                self.__id = id
            else:
                self.__id = random.randint(1, 1000000)
            self.__name = name
            self.__name_valid_str = len(name)
            self.__ecv = ecv
            self.__ecv_valid_str = len(ecv)
            self.__surname = surname
            self.__surname_valid_str = len(surname)
            self.__valid_visits = 0
            self.__visits = [] 
            
        else:
            self.__id = random.randint(1, 1000000)
            self.__name = ""
            self.__name_valid_str = len("Unknown")
            self.__ecv = ""
            self.__ecv_valid_str = len(self.__ecv)
            self.__surname = ""
            self.__surname_valid_str = len("")
            self.__valid_visits = 0
            self.__visits = [] 
        while len(self.__visits) < 5:
            self.__visits.append(Visit())  
            
    def __eq__(self, other):
        if not isinstance(other, Customer):
            return False
        return (
            self.__id == other.__id or self.__ecv == other.__ecv
        )
    def __str__(self):
        visits_str = "\n".join(str(visit) for visit in self.__visits)
        return f"Customer(id={self.__id}, name={self.__name}, surname={self.__surname}, ecv={self.__ecv}, valid_visits={self.__valid_visits}, visits:\n{visits_str}, )"
        

    @property
    def id(self):
        return self.__id
    @id.setter
    def id(self, value):
        self.__id = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value
        self.__name_valid_str = len(value) 

    @property
    def name_valid_str(self):
        return self.__name_valid_str

    @property
    def ecv(self):
        return self.__ecv

    @ecv.setter
    def ecv(self, value):
        self.__ecv = value
        self.__ecv_valid_str = len(value)  
    
    @property
    def ecv_valid_str(self):
        return self.__ecv_valid_str

    @property
    def surname(self):
        return self.__surname

    @surname.setter
    def surname(self, value):
        self.__surname = value
        self.__surname_valid_str = len(value)  

    @property
    def surname_valid_str(self):
        return self.__surname_valid_str

    @property
    def valid_visits(self):
        return self.__valid_visits

    @valid_visits.setter
    def valid_visits(self, value):
        self.__valid_visits = value

    @property
    def visits(self):
        return self.__visits

    @visits.setter
    def visits(self, value):
        self.__visits = value
        
    def is_full(self):
        return self.valid_visits == len(self.visits)
    
    def add_visit(self, visit):
        if  self.is_full() == False:
            if not self.visits:
                self.visits.append(visit)
            else:
                self.visits[self.valid_visits] = visit
            self.valid_visits += 1
            
    def fill_string(self, string, length):
        return string.ljust(length, "*")
    
    def to_byte_array(self):
        byte_array = bytearray()
        byte_array += self.__id.to_bytes(4, 'little')
        filled_name = self.fill_string(self.__name, 15)
        byte_array += (len(filled_name).to_bytes(4, 'little'))
        byte_array += bytes(filled_name, encoding='utf-8') 
        byte_array += self.__name_valid_str.to_bytes(4, 'little')
        filled_ecv = self.fill_string(self.__ecv, 10)
        byte_array += (len(filled_ecv).to_bytes(4, 'little'))
        byte_array += bytes(filled_ecv, encoding='utf-8') 
        byte_array += self.__ecv_valid_str.to_bytes(4, 'little')
        filled_surname = self.fill_string(self.__surname, 20)
        byte_array += (len(filled_surname).to_bytes(4, 'little'))
        byte_array += bytes(filled_surname, encoding='utf-8') 
        byte_array += self.__surname_valid_str.to_bytes(4, 'little')
        byte_array += self.valid_visits.to_bytes(4, 'little')
        for visit in self.visits:
            byte_array += visit.to_byte_array() 
        return byte_array
    
    @staticmethod 
    def from_byte_array(byte_array):
        
        offset = 0  
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
        end_offset = offset + 5 * one_visit_size
        __visits = []
        while offset < end_offset:
            __visits.append(Visit.from_byte_array(byte_array[offset:offset + one_visit_size]))
            offset += one_visit_size
        
        while len(__visits) < 5:
            __visits.append(Visit())
        customer = Customer(__name[0:__name_valid_str], __surname[0:__surname_valid_str], __ecv[0:__ecv_valid_str])
        customer.valid_visits = __valid_visits
        customer.visits = __visits
        customer.__id = __id
        return customer

class CustomerForHash(HashRecord):
    def __init__(self, address = None):
        super().__init__()
        if address is not None:
            self.__address = address
        else:
            self.__address = 53
    
    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, value):
        self.__address = value
    
    @property
    def key(self):
        return self.__key

    @key.setter
    def key(self, value):
        self.__key = value
    def get_hash():
        pass
    def get_hash_by_key(self, key):
        pass
    
class CustomerByID(CustomerForHash):
    def __init__(self, customer_id = None , address = None):
        super().__init__(address)
        if customer_id is not None:
            self.__customer_id = customer_id
        else:
            self.__customer_id = 0
        self.__key = self.__customer_id
  
    @property
    def customer_id(self):
        return self.__customer_id

    @customer_id.setter
    def customer_id(self, value):
        self.__customer_id = value
        self.__key = value  
        
    def __str__(self):
        return f"CustomerByID(customer_id={self.__customer_id}, address={self.address})"
    
    def __eq__(self, other):
        return self.__key == other.__key
    
    def get_hash_by_key(self, key):
        bitset = bitarray(endian='little')
        bitset.frombytes(key.to_bytes((key.bit_length() + 7) // 8, byteorder='little'))
        
        if len(bitset) < 32:
            padding = 32 - len(bitset)
            bitset = bitset+ bitarray('0') * padding 
        return bitset[:32]
    
    def get_hash(self):
        bitset = bitarray(endian='little')
        bitset.frombytes(self.__customer_id.to_bytes((self.__customer_id.bit_length() + 7) // 8, byteorder='little'))
        
        if len(bitset) < 32:
            padding = 32 - len(bitset)
            bitset = bitset+ bitarray('0') * padding 
        return bitset[:32]
    
    def get_size(self):
        return len(self.to_byte_array())
    
    def fill_string(self, string, length):
        return string.ljust(length, "*")
    
    def to_byte_array(self):
        byte_array = bytearray()
        byte_array += super().address.to_bytes(4, 'little')
        byte_array += self.__customer_id.to_bytes(4, 'little')
        return byte_array
    
    @staticmethod 
    def from_byte_array(byte_array):
        offset = 0  
        
        address = int.from_bytes(byte_array[offset:offset + 4], 'little')
        offset += 4

        customer_id = int.from_bytes(byte_array[offset:offset + 4], 'little')
        
        customer = CustomerByID(customer_id, address)
        return customer

    
class CustomerByECV(CustomerForHash):
    def __init__(self, ecv = None, address = None):
        super().__init__(address)
        self.__customer_ecv = None
        if ecv is not None:
            self.__customer_ecv = ecv
            self.__ecv_valid_str = len(self.__customer_ecv)
        else:
            self.__customer_ecv = ""
            self.__ecv_valid_str = len(self.__customer_ecv)
        self.__key = self.__customer_ecv
        
    def __eq__(self, other):
        return self.__key == other.__key
    
    def get_size(self):
        return len(self.to_byte_array())
    
    def __str__(self):
        return f"CustomerByECV(ecv={self.__customer_ecv}, address={self.address})"
    def get_hash(self):
        bitset = bitarray(endian='little')
        bitset.frombytes(self.__customer_ecv.encode('utf-8'))
        if len(bitset) < 32:
            padding = 32 - len(bitset)
            bitset = bitset + bitarray('0') * padding
        
        return bitset[:32]  
    def get_hash_by_key(self, key):
        bitset = bitarray(endian='little')
        bitset.frombytes(key.encode('utf-8'))
        if len(bitset) < 32:
            padding = 32 - len(bitset)
            bitset = bitset + bitarray('0') * padding
        
        return bitset[:32]  
    
    def fill_string(self, string, length):
        return string.ljust(length, "*")
    
    def to_byte_array(self):
        byte_array = bytearray()
        byte_array += super().address.to_bytes(4, 'little')
        filled_ecv = self.fill_string(self.__key, 10)
        byte_array += (len(filled_ecv).to_bytes(4, 'little'))
        byte_array += bytes(filled_ecv, encoding='utf-8') 
        byte_array += self.__ecv_valid_str.to_bytes(4, 'little')
        return byte_array
    
    @staticmethod 
    def from_byte_array(byte_array):
        offset = 0  
        
        address = int.from_bytes(byte_array[offset:offset + 4], 'little')
        offset += 4

        ecv_length = int.from_bytes(byte_array[offset:offset + 4], 'little')
        offset += 4

        __ecv = byte_array[offset:offset + ecv_length].decode('utf-8')
        offset += ecv_length
        
        __ecv_valid_str = int.from_bytes(byte_array[offset:offset + 4], 'little')
        offset += 4
        customer = CustomerByECV(__ecv[0:__ecv_valid_str], address)
        return customer
    
class CustomerGUI:
    def __init__(self, id=None, name=None, surname=None, ecv=None, visits=None):
        self.id = int(id) if id is not None else None
        self.name = name[:15] if name is not None else ""
        self.surname = surname[:20] if surname is not None else ""
        self.ecv = ecv[:10] if ecv is not None else ""
        self.valid_visits = int(0)
        self.visits = visits if visits is not None else []
    def __str__(self):
        visits_str = "\n".join(str(visit) for visit in self.visits[:self.valid_visits])
        return f"Customer(id={self.id}, name={self.name}, surname={self.surname}, ecv={self.ecv}, visits:\n{visits_str}"        
    def add_visit(self, visit):
        if  self.is_full() == False:
            if not self.visits:
                self.visits.append(visit)
            else:
                self.visits[self.valid_visits] = visit
            self.valid_visits += 1
            
    def remove_visit(self, visit):
        self.visits.remove(visit)
        if self.valid_visits > 0:
            self.valid_visits -= 1
        while len(self.visits) < 5:
            self.visits.append(Visit())
            
    def is_full(self):
        return self.valid_visits == len(self.visits) 
       
    def from_customer(self, customer):
        self.id = customer.id
        self.name = customer.name
        self.surname = customer.surname
        self.ecv = customer.ecv
        self.visits = customer.visits
        self.valid_visits = customer.valid_visits

    def to_customer(self):
        cus = Customer(name=self.name, surname=self.surname, ecv=self.ecv, id=self.id)
        cus.valid_visits = self.valid_visits
        cus.visits = self.visits
        return  cus
