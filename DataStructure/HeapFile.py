import os
from DataStructure.Block import Block


class HeapFile:
    def __init__(self, block_size, record_type):
        """
        Initializes the HeapFile with the given block size.
        """
        self.__record_type = record_type
        self.__block_size = block_size  # Size of each block in bytes
        self.__file_path = "heapfile.bin"  # Path to the binary file
        self.__partial_free_block = None  # Address of the partially free block, if any
        self.__free_block = None  # Address of a fully free block, if any
        self.__number_of_blocks = 0  # Number of blocks in the file
        # Ensure the file exists
        if not os.path.exists(self.__file_path):
            self.__file = open(self.__file_path, "wb") 
            self.__file.close()
        self.__file =  open(self.__file_path, "r+b")
        
        @property
        def file(self):
            return self.__file
        @property
        def record_type(self):
            return self.__record_type

        @property
        def block_size(self):
            return self.__block_size

        @property
        def file_path(self):
            return self.__file_path

        @property
        def partial_free_block(self):
            return self.__partial_free_block

        @property
        def free_block(self):
            return self.__free_block

        @property
        def number_of_blocks(self):
            return self.__number_of_blocks
        @file.setter
        def file(self, value):
            self.__file = value

        @record_type.setter
        def record_type(self, value):
            self.__record_type = value

        @block_size.setter
        def block_size(self, value):
            self.__block_size = value

        @file_path.setter
        def file_path(self, value):
            self.__file_path = value

        @partial_free_block.setter
        def partial_free_block(self, value):
            self.__partial_free_block = value

        @free_block.setter
        def free_block(self, value):
            self.__free_block = value

        @number_of_blocks.setter
        def number_of_blocks(self, value):
            self.__number_of_blocks = value
    def __get_block_offset(self, block_address):
        """
        Calculates the byte offset of a block in the file based on its address.
        """
        return block_address * self.__block_size

    def read_block(self, block_address):
        """
        Reads a block from the file given its address.
        """
        offset = self.__get_block_offset(block_address)
        #with open(self.file_path, "rb+") as file:
        self.__file.seek(offset)
        block_data = self.__file.read(self.__block_size)
        if not block_data:
            return None
        return Block.from_byte_array(block_data,  type(self.__record_type), self.__block_size)

    def __write_block(self, block_address, block):
        """
        Writes a block to the file at the given address.
        """
        offset = self.__get_block_offset(block_address)
        #with open(self.file_path, "r+b") as file:
        self.__file.seek(offset)
        #print(f"newBlock size: {len(block.to_byte_array())}")
        self.__file.write(block.to_byte_array())

    def __append_block(self, block):
        """
        Appends a new block to the end of the file.
        """
        #with open(self.file_path, "r+b") as file:
        self.__file.seek(0, 2)  # Move to the end of the file
        self.__file.write(block.to_byte_array())

    def __get_file_size(self):
        """
        Returns the size of the file in bytes.
        """
        #with open(self.file_path, "rb+") as file:
        self.__file.seek(0, 2)  # Move to the end of the file
        return self.__file.tell()

    def insert(self, record):
        """
        Inserts a record into the HeapFile and returns the block address.
        """
        # Check if there's a partially free block
        if self.__partial_free_block is not None:
            block_address = self.__partial_free_block
            block = self.read_block(block_address)
            if block.is_full() == False:
                block.add_record(record)
                self.__write_block(block_address, block)
                # If the block is now full, remove it from partially free blocks
                if block.is_full():
                    self.__partial_free_block = block.next_block
                return block_address

        # Check if there's a fully free block
        if self.__free_block is not None:
            block_address = self.__free_block
            block = self.read_block(block_address)
            if not block.is_full():
                block.add_record(record)
                self.__write_block(block_address, block)
                # Move this block to partially free blocks
                self.__partial_free_block = block_address
                self.__free_block = block.next_block
                return block_address

        # Otherwise, create a new block
        block_address = self.__number_of_blocks
        block = Block(self.__block_size, self.__record_type)
        self.__number_of_blocks += 1
        #print(f"Block size: {block.get_current_size()}")
        block.add_record(record)
        self.__append_block(block)
        self.__partial_free_block = block_address
        return block_address

    def get(self, address, record):
        """
        Retrieves a record from a specific block address.
        """
        block = self.read_block(address)
        if block:
            return block.get_record(record)
        return None

    def delete(self, address, record):
        """
        Deletes a record from a specific block address.
        """
        block = self.read_block(address)
        was_full = block.is_full()
        if block:
            block.remove_record(record)
            if block.is_empty():
                #if block is now empty but not the last block
                if address != self.__number_of_blocks - 1:
                    if self.__partial_free_block == address:
                        self.__partial_free_block = block.next_block
                        
                        if block.next_block != None:
                            next = self.read_block(block.next_block)
                            next.previous_block = block.previous_block
                            
                            self.__write_block(block.next_block, next)
                            block.next_block = None
                            block.previous_block = None
                    if block.previous_block != None:
                        previous = self.read_block(block.previous_block)
                        previous.next_block = block.next_block
                        
                        self.__write_block(block.previous_block, previous)
                    if block.next_block != None:
                            next = self.read_block(block.next_block)
                            next.previous_block = block.previous_block
                            
                            self.__write_block(block.next_block, next)
                            block.next_block = None
                            block.previous_block = None    
                    
                    first_free_address = self.__free_block
                    
                    if first_free_address != None:
                        first_free = self.read_block(self.__free_block)
                        first_free.previous_block = address
                        block.next_block = first_free_address
                        self.__write_block(first_free_address, first_free)
                    
                    self.__free_block = address
                    block.previous_block = None
                    self.__write_block(address, block)
                #if block is now empty and is the last block
                elif address == self.__number_of_blocks - 1:
                    current = block
                    current_add = address
                    if self.__number_of_blocks != 0:
                        #previous = self.__read_block(previous_add)
                        while current != None and current.is_empty():
                            if current.previous_block != None:
                                previous = self.read_block(current.previous_block)
                                previous.next_block = current.next_block
                                self.__write_block(current.previous_block, previous)
                               
                            if current.next_block != None:
                                next_block = self.read_block(current.next_block)
                                next_block.previous_block = current.previous_block
                                self.__write_block(current.next_block, next_block)
                               
                            if current_add == self.__free_block:
                                self.__free_block = current.next_block
                            
                            self.trim_file(self.__block_size)
                            current_add -= 1
                            if current_add >= 0:
                                current = self.read_block(current_add)
                            else:
                                current = None
                            self.__number_of_blocks -= 1
            else:
                if was_full:
                    partial_address = self.__partial_free_block 
                    if partial_address != None:
                        partial_block = self.read_block(partial_address)
                        partial_block.previous_block = address
                        self.__write_block(partial_address, partial_block)
                    block.next_block = partial_address
                    self.__partial_free_block = address
                    block.previous_block = None
                    self.__write_block(address, block)
                else:
                    self.__write_block(address, block)
        if self.__number_of_blocks == 0:
            self.__partial_free_block = None
            self.__free_block = None

    def get_all_blocks(self):
        """
        Reads all blocks sequentially from the file and returns them in a list.
        """
        blocks = []
        try:
            #with open(self.file_path, "rb+") as file:
            for block_address in range(self.__number_of_blocks):
                offset = self.__get_block_offset(block_address)
                self.__file.seek(offset)
                block_data = self.__file.read(self.__block_size)
                if block_data:
                    block = Block.from_byte_array(block_data, type(self.__record_type), self.__block_size)
                    print(f"Block {block_address}: {block}")
                    blocks.append(block)
        except Exception as e:
            print(f"An error occurred while reading blocks: {e}")
        return blocks
        
    def trim_file(self, trim_length):
        """
        Trims a specified number of bytes from the end of the file.
        """
        try:
            #with open(self.file_path, 'rb+') as file:
            # Get the current size of the file
            self.__file.seek(0, 2)  # Move to the end of the file
            current_size = self.__file.tell()

            # Calculate the new size
            new_size = max(0, current_size - trim_length)

            # Truncate the file to the new size
            self.__file.truncate(new_size)
            print(f"File trimmed successfully. New size: {new_size} bytes.")
        except Exception as e:
            print(f"An error occurred: {e}")
