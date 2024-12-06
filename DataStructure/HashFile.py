from DataStructure.Block import Block
from DataStructure.HashBlock import HashBlock
from DataStructure.HeapFile import HeapFile
import math
import os
from bitarray import bitarray


class HashFile():
    def __init__(self, block_size, record_type, file_name="hashfile.bin"):
        self.__block_size = block_size
        self.__record_type = record_type
        self.__file_depth = 1
        self.__block_depth_dir = [1, 1]
        self.__number_of_blocks = 2
        self.__directory = [0, self.__number_of_blocks - 1]
        self.__blocks = [Block(block_size, record_type), Block(block_size, record_type)]
        self.file_path = file_name
        if not os.path.exists(self.file_path):
            self.__file = open(self.file_path, "wb") 
            self.__file.close()
        
        self.__file =  open(self.file_path, "r+b")
        for i in range(2):
            self.__write_block(self.__directory[i], self.__blocks[i])
    def find(self,key):
        hash = self.__record_type.get_hash_by_key(key)
        dummy = type(self.__record_type)(key)
        target_index = self.hash_to_index(hash)
        target_block_address = self.__directory[target_index]
        target_block = self.read_block(target_block_address)
        if target_block:
            return target_block.get_record(dummy)
        return None
        
    def insert(self, record):
        niejevlozene = True  # Vlajka na indikáciu, či záznam už bol vložený
        inserted_record = record
        while niejevlozene:
            # 1. Vypočítaj hash
            target_index = self.hash_to_index( record.get_hash())
            target_block_address = self.__directory[target_index]
            if target_block_address == -1:
                target_block = Block(self.__block_size, self.__record_type)
                if self.__block_depth_dir[target_index] == self.__file_depth:
                    new_block = Block(self.__block_size, self.__record_type)
                    new_block.add_record(record)
                    split_range = 2 ** (self.__file_depth - self.__block_depth_dir[target_index])
                    start_point = target_index
                    while start_point % split_range != 0:
                        start_point -= 1
                    end_point = start_point + (split_range)
                    split_point = (start_point + end_point) // 2
                    for i in range(start_point, start_point + split_range):
                        self.__directory[i] = self.__number_of_blocks
                    self.__write_block(self.__number_of_blocks, new_block)
                    self.__number_of_blocks += 1
                    niejevlozene = False
                    break;
                else:
                    split_range = 2 ** (self.__file_depth - self.__block_depth_dir[target_index])
                    start_point = target_index
                    while start_point % split_range != 0:
                        start_point -= 1
                    end_point = start_point + (split_range)
                    split_point = (start_point + end_point) // 2
                    #blokom, ktore su obsiahnute v splite sa zvvysi hlbka o 1
                    for i in range(start_point, start_point + split_range):
                        self.__block_depth_dir[i] += 1
                    new_block = Block(self.__block_size, self.__record_type)
                    #ziska vsetky validne zaznamy bloku
                    records_to_insert = target_block.get_valid_records()
                    #odstrani z bloku validne zaznamy
                    for rec in records_to_insert:
                        target_block.remove_record(rec)
                    #do zoznamu zaznamov na pridanie prida zaznam ktory chceme pridat
                    records_to_insert.append(inserted_record)
                    old_block = target_block
                    #vklada zaznamy bud do noveho bloku alebo do povodneho
                    for _ in records_to_insert:
                        #ak je index vkladaneho zaznamu na pravej polovici splitu prida ho do noveho bloku
                        if self.hash_to_index(_.get_hash()) >= split_point:
                            if new_block.add_record(_) == False :
                                niejevlozene = True
                            else:
                                niejevlozene = False
                        # ak je index na lavej strane splitu prida zaznam do povodneho bloku
                        else:
                            if old_block.add_record(_) == False:
                                
                                niejevlozene = True
                            else:
                                niejevlozene = False
                    #Ak novy blok nie je prazdny
                    if new_block.is_empty() == False:
                        #Ak novy blok nie je prazdny a ani povodny blok nie je prazdny
                        if old_block.is_empty() == False:
                            #prepise sa v subore povodny blok
                            self.__write_block(target_block_address, old_block)
                            #v adresari sa vsetkym zaznamom na pravej polke splitu upravi adresa na adresu noveho bloku
                            for i in range (split_point, end_point):
                                self.__directory[i] = self.__number_of_blocks
                            #zapise sa novy blok
                            self.__write_block(self.__number_of_blocks, new_block)
                            #zvysi sa pocet blokov v subore
                            self.__number_of_blocks += 1
                        #ak novy blok nie je prazdny ale stary blok je prazdny
                        else:
                            old_block_add = 0
                            # upravi sa v adresari vsetkym prvkom na lavej strane splitu adresa na -1 a zaroven si ulozim povodnu adresu bloku do old_block_add
                            for i in range (start_point, split_point):
                                old_block_add = self.__directory[i]
                                self.__directory[i] = -1
                            
                            if old_block_add == -1:
                                old_block_add = self.__number_of_blocks
                            for i in range (split_point, end_point):
                                self.__directory[i] = old_block_add
                            #na  povodnu adresu zapisem novy blok
                            self.__write_block(old_block_add, new_block)  
                            self.__number_of_blocks += 1  
                            niejevlozene = False
                            break;
                    #ak je novy blok prazdny
                    else:
                        #upravi sa v adresari prvkom z pravej polovice splitu adresa na -1
                        for i in range (split_point, end_point):
                                self.__directory[i] = - 1
                        for i in range (start_point, split_point):
                                self.__directory[i] = self.__number_of_blocks
                        #prepise sa povodny blok 
                        self.__write_block(self.__number_of_blocks, old_block)
                        self.__number_of_blocks += 1
                        niejevlozene = False
                        break;
                        
            else:
                target_block = self.read_block(target_block_address)
            # 2. Ak je blok plný
            if target_block.is_full():
                # Ak je hloubka bloku rovnaká ako hloubka súboru
                if self.__block_depth_dir[target_index] == self.__file_depth:
                    #tak zdvojnasob adresar
                    self.double_directory()
                #prepocitanie hashu a znovu nacitanie bloku
                new_index = self.hash_to_index(record.get_hash())
                """ target_block_address = self.__directory[new_index]
                target_block = self.read_block(target_block_address) """
                #vypocet co sa bude splitovat
                split_range = 2 ** (self.__file_depth - self.__block_depth_dir[new_index])
                start_point = new_index
                while start_point % split_range != 0:
                    start_point -= 1
                end_point = start_point + (split_range)
                split_point = (start_point + end_point) // 2
                
                #blokom, ktore su obsiahnute v splite sa zvvysi hlbka o 1
                for i in range(start_point, start_point + split_range):
                    self.__block_depth_dir[i] += 1
                    
                new_block = Block(self.__block_size, self.__record_type)
                #ziska vsetky validne zaznamy bloku
                records_to_insert = target_block.get_valid_records()
                #odstrani z bloku validne zaznamy
                for rec in records_to_insert:
                    target_block.remove_record(rec)
                #do zoznamu zaznamov na pridanie prida zaznam ktory chceme pridat
                records_to_insert.append(inserted_record)
                old_block = target_block
                #vklada zaznamy bud do noveho bloku alebo do povodneho
                for _ in records_to_insert:
                    #ak je index vkladaneho zaznamu na pravej polovici splitu prida ho do noveho bloku
                    if self.hash_to_index(_.get_hash()) >= split_point:
                        if new_block.add_record(_) == False :
                            niejevlozene = True
                        else:
                            niejevlozene = False
                    # ak je index na lavej strane splitu prida zaznam do povodneho bloku
                    else:
                        if old_block.add_record(_) == False:
                            
                            niejevlozene = True
                        else:
                            niejevlozene = False
                #Ak novy blok nie je prazdny
                if new_block.is_empty() == False:
                    #Ak novy blok nie je prazdny a ani povodny blok nie je prazdny
                    if old_block.is_empty() == False:
                        #prepise sa v subore povodny blok
                        self.__write_block(target_block_address, old_block)
                        #v adresari sa vsetkym zaznamom na pravej polke splitu upravi adresa na adresu noveho bloku
                        for i in range (split_point, end_point):
                            self.__directory[i] = self.__number_of_blocks
                        #zapise sa novy blok
                        self.__write_block(self.__number_of_blocks, new_block)
                        #zvysi sa pocet blokov v subore
                        self.__number_of_blocks += 1
                    #ak novy blok nie je prazdny ale stary blok je prazdny
                    else:
                        old_block_add = 0
                        # upravi sa v adresari vsetkym prvkom na lavej strane splitu adresa na -1 a zaroven si ulozim povodnu adresu bloku do old_block_add
                        for i in range (start_point, split_point):
                            old_block_add = self.__directory[i]
                            self.__directory[i] = -1
                        #na  povodnu adresu zapisem novy blok
                        self.__write_block(old_block_add, new_block)    
                #ak je novy blok prazdny
                else:
                    #upravi sa v adresari prvkom z pravej polovice splitu adresa na -1
                    for i in range (split_point, end_point):
                            self.__directory[i] = - 1
                    #prepise sa povodny blok 
                    self.__write_block(self.__number_of_blocks, old_block)
            else:
                
                target_block.add_record(inserted_record)
                self.__write_block(target_block_address, target_block)
                self.__directory[target_index] = target_block_address
                niejevlozene = False 
                
    def hash_to_index(self, hash_value):
        hash = hash_value
        #hash.reverse()
        selected_bits = hash[:self.__file_depth]
        return int(selected_bits.to01(), 2)
    def double_directory(self):
        """
        Doubles the size of the directory.
        """
        doubled_list = [item for item in self.__directory for _ in range(2)]
        self.__directory = doubled_list
        doubled_list = [item for item in self.__block_depth_dir for _ in range(2)]
        self.__block_depth_dir = doubled_list
        self.__file_depth += 1
    def __get_block_offset(self, block_address):
        """
        Calculates the byte offset of a block in the file based on its address.
        """
        return block_address * self.__block_size
    def __append_block(self, block):
        """
        Appends a new block to the end of the file.
        """
        #with open(self.file_path, "r+b") as file:
        self.__file.seek(0, 2)  # Move to the end of the file
        self.__file.write(block.to_byte_array())
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
                    """ print(f"Block {block_address}:\n {block}")
                    print(f"--------------------------------------\n") """
                    blocks.append(block)
        except Exception as e:
            print(f"An error occurred while reading blocks: {e}")
        return blocks
