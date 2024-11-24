import sys
from DataStructure.Record import Record

class Person(Record):
    def __init__(self, name=None, age=None, address=None):
        super().__init__()
        if name is not None and age is not None and address is not None:
            self.__name = name
            self.__name_valid_str = len(name)
            self.__age = age
            self.__address = address
            self.__address_valid_str = len(address)
            
        else:
            self.__name = "Unknown"
            self.__name_valid_str = len("Unknown")
            self.__age = 0
            self.__address = "Not specified"
            self.__address_valid_str = len("Not specified")
            
    
    def __str__(self):
        """
        Returns a string representation of the Person object.
        """
        return (
            f"Name: {self.__name}\n"
            f"Name Valid String Length: {self.__name_valid_str}\n"
            f"Age: {self.__age}\n"
            f"Address: {self.__address}\n"
            f"Address Valid String Length: {self.__address_valid_str}"
        )
    @property
    def name_valid_str(self):
        return self.__name_valid_str

    @name_valid_str.setter
    def name_valid_str(self, value):
        self.__name_valid_str = value

    @property
    def address_valid_str(self):
        return self.__address_valid_str

    @address_valid_str.setter
    def address_valid_str(self, value):
        self.__address_valid_str = value
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value
        self.__name_valid_str = len(value)
        self.fill_string(value)

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, value):
        self.__age = value

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, value):
        self.__address = value
        self.__address_valid_str = len(value)
        self.fill_string(value)
    def fill_string(self, string):
        return string.ljust(self.max_str_length, "*")
    def get_size(self):
        """
        Returns the size of the Person in bytes.
        """
        size = len(self.to_byte_array())
        return size

    def __eq__(self, other):
        """
        Overrides the == operator to compare two Person objects.
        """
        if not isinstance(other, Person):
            return False
        return (
            self.__name == other.__name and
            self.__age == other.__age and
            self.__address == other.__address
        )

    def to_byte_array(self):
        """
        Converts the Person to a byte array.
        """
        
        byte_array = bytearray()
        byte_array += (len(self.fill_string(self.__name)).to_bytes(4, 'little'))
       # print(len(byte_array))
        byte_array += bytes(self.fill_string(self.__name), encoding='utf-8') 
        #print(len(byte_array))
        byte_array += self.name_valid_str.to_bytes(4, 'little') 
       # print(len(byte_array))
        byte_array += self.__age.to_bytes(4, 'little') 
       # print(len(byte_array))
        byte_array += (len(self.fill_string(self.address)).to_bytes(4, 'little')) 
       # print(len(byte_array))
        byte_array += bytes(self.fill_string(self.__address), encoding='utf-8') 
       # print(len(byte_array))
        byte_array  += self.address_valid_str.to_bytes(4, 'little')
       # print(len(byte_array))
        return byte_array

    @staticmethod
    def from_byte_array(byte_array):
        """
        Parses a byte array to reconstruct a Person object.
        """
        # Cursor for tracking the position while reading
        cursor = 0
        
        # Read length of name (4 bytes)
        name_length = int.from_bytes(byte_array[cursor:cursor+4], 'little')
        cursor += 4
        
        # Read name
        name = byte_array[cursor:cursor+name_length].decode('utf-8')
        cursor += name_length
        
        # Read name_valid_str (4 bytes)
        name_valid_str = int.from_bytes(byte_array[cursor:cursor+4], 'little')
        cursor += 4

        # Read age (4 bytes)
        age = int.from_bytes(byte_array[cursor:cursor+4], 'little')
        cursor += 4

        # Read length of address (4 bytes)
        address_length = int.from_bytes(byte_array[cursor:cursor+4], 'little')
        cursor += 4

        # Read address
        address = byte_array[cursor:cursor+address_length].decode('utf-8')
        cursor += address_length

        # Read address_valid_str (4 bytes)
        address_valid_str = int.from_bytes(byte_array[cursor:cursor+4], 'little')
        cursor += 4
        
        # Reconstruct and return the Person object
        return Person(name=name[0:name_valid_str], age=age, address=address[0:address_valid_str])

    
        
        
