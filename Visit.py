from datetime import date
import struct

from JobDescription import JobDescription


class Visit:
    def __init__(self, price = 2.0, date = date(2024, 11, 23), description = []):
        self.__price = price
        self.__date = date
        self.__description_valid = 0
        if description:
            self.__description = description
            self.__description_valid = len(description)
        else:
            self.__description = description
        
        while len(self.__description) < 10:
            self.__description.append(JobDescription())
            
            
    def to_byte_array(self):
        """
        Converts the Visit to a byte array.
        """
        byte_array = bytearray()
        byte_array += struct.pack("f", self.__price)
        byte_array += struct.pack("HBB", self.__date.year, self.__date.month, self.__date.day)
        byte_array += self.__description_valid.to_bytes(4, 'little')
        for desc in self.__description:
            byte_array += desc.to_byte_array() 
        return byte_array
    
    @staticmethod
    def from_byte_array(self, byte_array):
        """
        Converts a byte array back into a Visit object.
        """
        offset = 0
        __price = struct.unpack_from("f", byte_array, offset)[0]
        offset += 4
        
        year, month, day = struct.unpack_from("HBB", byte_array, offset)
        __date = date(year, month, day)
        offset += 4
        
        __description_valid = int.from_bytes(byte_array[offset:offset + 4], 'little')
        offset += 4

        # Clear existing description list
        __description = []

        one_desc_size = len(JobDescription().to_byte_array())
        end_offset = offset + __description_valid * one_desc_size
        
        # Deserialize the descriptions
        while offset < end_offset:
            __description.append(JobDescription.from_byte_array(byte_array[offset:offset + one_desc_size]))
            offset += one_desc_size
        
        while len(__description) < 10:
            __description.append(JobDescription())
        
        return Visit(__price, __date, __description)
            
        
    def fill_string(self, string, length):
        return string.ljust(length, "*")