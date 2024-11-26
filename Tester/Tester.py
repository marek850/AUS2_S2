import random
import sys
from Data.Customer import Customer
from DataStructure.HeapFile import HeapFile


class DataStructureTester:
    def __init__(self,  seed=None):#parcel_tree, property_tree, all_tree,
        self.__max_size = sys.maxsize
        self.__seed = seed if seed is not None else random.randint(1, self.__max_size)
        self.__heap_file = HeapFile(1000, Customer())
        self.__addresses_records = []
        random.seed(self.__seed)
        self.__unique_names = set()
        self.__unique_surnames = set()
        self.__unique_ecvs = set()

    def generate_unique_value(self, max_length, existing_values):
        value = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=random.randint(1, max_length)))
        while value in existing_values:
            value = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=random.randint(1, max_length)))
        existing_values.add(value)
        return value

    def generate_insert(self, operation_num):
        # Generate unique values for the customer
        name = self.generate_unique_value(15, self.__unique_names)
        surname = self.generate_unique_value(20, self.__unique_surnames)
        ecv = self.generate_unique_value(10, self.__unique_ecvs)

        # Create a new Customer instance
        customer = Customer(name=name, surname=surname, ecv=ecv)
        print(f"Inserting record: {customer}")

        # Insert the Customer into the heap file
        address = self.__heap_file.insert(customer)
        print(f"Record {customer} inserted at address: {address}")
        self.__addresses_records.append((address, customer))
        found_record = self.__heap_file.get(address, customer)
        if found_record != customer:
            print(f"Inserted record does not match the retrieved record.Operation {operation_num}")
            return False
        return True
    
    

    def generate_inserts(self, num_customers):
        mistakes = 0
        for _ in range(num_customers):
            if self.generate_insert(_) == False:
                mistakes += 1
        
        if mistakes > 0:
            print(f"Found {mistakes} mistakes in {num_customers} insertions.")
        else:    
            print(f"Successfully inserted {num_customers} records.")
    
    def generate_delete(self, num_oper):
        address, record = random.choice(self.__addresses_records)
        print(f"Deleting record at address {address}")
        print(f"Record: {record}")
        found_record = self.__heap_file.get(address, record)
        if found_record != record:
            print(f"Record not found.Operation {num_oper}")
            return False
        self.__heap_file.delete(address, record)
        self.__addresses_records.remove((address, record))
        found_record = self.__heap_file.get(address, record)
        if found_record is not None:
            print(f"Record not deleted.Operation {num_oper}")
            return False
        blocks = self.__heap_file.get_all_blocks()
        numb_of_records = 0
        for _ in range(len(blocks)):
            numb_of_records += blocks[_].valid_count
        if numb_of_records != len(self.__addresses_records):
            print(f"Number of blocks does not match the number of records.Operation {num_oper}")
            return False
        return True

    def generate_deletes(self, num_deletes):
        mistakes = 0
        for _ in range(num_deletes):                                                                              
            if self.generate_delete(_) == False:                                                                                                                                               
                mistakes += 1                                                                                                                                                                                                                         
        
        if mistakes > 0:
            print(f"Found {mistakes} mistakes in {num_deletes} deletions.")
        else:    
            print(f"Successfully deleted {num_deletes} records.")
    def test(self):
       
            #self.__seed = 8091386027947589026
            print(f"Seed: {self.__seed}")
            self.generate_inserts(1000)
            self.generate_deletes(1000)