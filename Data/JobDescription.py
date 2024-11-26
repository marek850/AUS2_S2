class JobDescription:
    def __init__(self, description):
        if description is not None:
            self.__description = description
            self.__valid_str = len(description)
        else:
            self.__description = "Unknown"
            self.__valid_str = len("Unknown")
        
    def fill_string(self, string, length):
        return string.ljust(length, "*")

    def to_byte_array(self):
        byte_array = bytearray()
        filled_desc = self.fill_string(self.__description, 20)
        byte_array += (len(filled_desc).to_bytes(4, 'little'))
        byte_array += bytes(filled_desc, encoding='utf-8') 
        byte_array += self.__valid_str.to_bytes(4, 'little') 
    @staticmethod
    def from_byte_array(byte_array):
        cursor = 0
        desc_length = int.from_bytes(byte_array[cursor:cursor+4], 'little')
        cursor += 4
        desc = byte_array[cursor:cursor+desc_length].decode('utf-8')
        cursor += desc_length
        desc_valid_str = int.from_bytes(byte_array[cursor:cursor+4], 'little')
        return JobDescription(desc[0:desc_valid_str])