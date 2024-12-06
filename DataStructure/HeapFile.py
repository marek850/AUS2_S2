import csv
import os
from DataStructure.Block import Block
from DataStructure.FileStructure import FileStructure


class HeapFile(FileStructure):
    def __init__(self, block_size, record_type, file_name, load_file):
        super().__init__(block_size, record_type, file_name, load_file)
        self.__partial_free_block = None  # Address of the partially free block, if any
        self.__free_block = None  # Address of a fully free block, if any
        if  os.path.exists(self.load_file):
            self.load()
    
        
        @property
        def file(self):
            return self.file
        @property
        def record_type(self):
            return self.record_type

        @property
        def block_size(self):
            return self.block_size

        @property
        def file_path(self):
            return self.file_path

        @property
        def partial_free_block(self):
            return self.__partial_free_block

        @property
        def free_block(self):
            return self.__free_block

        @property
        def number_of_blocks(self):
            return self.number_of_blocks
        @file.setter
        def file(self, value):
            self.file = value

        @record_type.setter
        def record_type(self, value):
            self.record_type = value

        @block_size.setter
        def block_size(self, value):
            self.block_size = value

        @file_path.setter
        def file_path(self, value):
            self.file_path = value

        @partial_free_block.setter
        def partial_free_block(self, value):
            self.__partial_free_block = value

        @free_block.setter
        def free_block(self, value):
            self.__free_block = value

        @number_of_blocks.setter
        def number_of_blocks(self, value):
            self.number_of_blocks = value
    def save(self):
        data = {
            "block_size": self.block_size,
            "partial_free_block": self.__partial_free_block,
            "free_block": self.__free_block,
            "number_of_blocks": self.number_of_blocks,
        }

        
        with open(self.load_file, mode='w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=data.keys())
            writer.writeheader()
            writer.writerow(data)
    def load(self):
        try:
            with open(self.load_file, mode='r', newline='') as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    self.block_size = int(row["block_size"]) if row["block_size"] else None
                    self.__partial_free_block = (
                        int(row["partial_free_block"]) if row["partial_free_block"] else None
                    )
                    self.__free_block = int(row["free_block"]) if row["free_block"] else None
                    self.number_of_blocks = (
                        int(row["number_of_blocks"]) if row["number_of_blocks"] else None
                    )
        except FileNotFoundError:
            print(f"Error: File {self.load_file} not found.")
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def insert(self, record):
        # Check if there's a partially free block
        if self.__partial_free_block is not None:
            block_address = self.__partial_free_block
            block = self.read_block(block_address)
            if block.is_full() == False:
                block.add_record(record)
                self.write_block(block_address, block)
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
                self.write_block(block_address, block)
                # Move this block to partially free blocks
                self.__partial_free_block = block_address
                self.__free_block = block.next_block
                return block_address

        # Otherwise, create a new block
        block_address = self.number_of_blocks
        block = Block(self.block_size, self.record_type)
        self.number_of_blocks += 1
        #print(f"Block size: {block.get_current_size()}")
        block.add_record(record)
        self.append_block(block)
        self.__partial_free_block = block_address
        return block_address
    def update(self, address, record):
        block = self.read_block(address)
        rec = block.get_record(record)
        block.remove_record(rec)
        block.add_record(record)
        self.write_block(address, block)
    def get(self, address, record):
        block = self.read_block(address)
        if block:
            return block.get_record(record)
        return None

    def delete(self, address, record):
        block = self.read_block(address)
        was_full = block.is_full()
        if block:
            block.remove_record(record)
            if block.is_empty():
                #if block is now empty but not the last block
                if address != self.number_of_blocks - 1:
                    if self.__partial_free_block == address:
                        self.__partial_free_block = block.next_block
                        
                        if block.next_block != None:
                            next = self.read_block(block.next_block)
                            next.previous_block = block.previous_block
                            
                            self.write_block(block.next_block, next)
                            block.next_block = None
                            block.previous_block = None
                    if block.previous_block != None:
                        previous = self.read_block(block.previous_block)
                        previous.next_block = block.next_block
                        
                        self.write_block(block.previous_block, previous)
                    if block.next_block != None:
                            next = self.read_block(block.next_block)
                            next.previous_block = block.previous_block
                            
                            self.write_block(block.next_block, next)
                            block.next_block = None
                            block.previous_block = None    
                    
                    first_free_address = self.__free_block
                    
                    if first_free_address != None:
                        first_free = self.read_block(self.__free_block)
                        first_free.previous_block = address
                        block.next_block = first_free_address
                        self.write_block(first_free_address, first_free)
                    
                    self.__free_block = address
                    block.previous_block = None
                    self.write_block(address, block)
                #if block is now empty and is the last block
                elif address == self.number_of_blocks - 1:
                    current = block
                    current_add = address
                    if self.number_of_blocks != 0:
                        #previous = self.__read_block(previous_add)
                        while current != None and current.is_empty():
                            if current.previous_block != None:
                                previous = self.read_block(current.previous_block)
                                previous.next_block = current.next_block
                                self.write_block(current.previous_block, previous)
                               
                            if current.next_block != None:
                                next_block = self.read_block(current.next_block)
                                next_block.previous_block = current.previous_block
                                self.write_block(current.next_block, next_block)
                               
                            if current_add == self.__free_block:
                                self.__free_block = current.next_block
                            
                            self.trim_file(self.block_size)
                            current_add -= 1
                            if current_add >= 0:
                                current = self.read_block(current_add)
                            else:
                                current = None
                            self.number_of_blocks -= 1
            else:
                if was_full:
                    partial_address = self.__partial_free_block 
                    if partial_address != None:
                        partial_block = self.read_block(partial_address)
                        partial_block.previous_block = address
                        self.write_block(partial_address, partial_block)
                    block.next_block = partial_address
                    self.__partial_free_block = address
                    block.previous_block = None
                    self.write_block(address, block)
                else:
                    self.write_block(address, block)
        if self.number_of_blocks == 0:
            self.__partial_free_block = None
            self.__free_block = None

    
        
    def trim_file(self, trim_length):
        """
        Trims a specified number of bytes from the end of the file.
        """
        try:
            #with open(self.file_path, 'rb+') as file:
            # Get the current size of the file
            self.file.seek(0, 2)  # Move to the end of the file
            current_size = self.file.tell()

            # Calculate the new size
            new_size = max(0, current_size - trim_length)

            # Truncate the file to the new size
            self.file.truncate(new_size)
            print(f"File trimmed successfully. New size: {new_size} bytes.")
        except Exception as e:
            print(f"An error occurred: {e}")
