import random
import sys
from Data.Customer import Customer, CustomerByID
from DataStructure.HashFile import HashFile
from DataStructure.HeapFile import HeapFile


class HeapFileTester:
    def __init__(self,  seed=None):
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
    def delete_remaining(self):
        mistakes = 0
        for _ in range(len(self.__addresses_records)):                                                                              
            if self.generate_delete(_) == False:                                                                                                                                               
                mistakes += 1                                                                                                                                                                                                                         
        
        if mistakes > 0:
            print(f"Found {mistakes} mistakes in  deletions.")
        else:    
            print(f"Successfully deleted all records.")
        
    def generate_random_operations(self, num_operations=100):
        print(f"Generating {num_operations} random operations:\n")
        mistakes = 0
        insert_mistakes = 0
        search_mistakes = 0
        delete_mistakes = 0
        for i in range(num_operations):
            operation = random.choice(["insert", "delete", "search"])
            if operation == "insert":
                if self.generate_insert(i) == False:
                    insert_mistakes += 1
            elif operation == "delete":
                if self.generate_delete(i) == False:
                    delete_mistakes += 1
            else:
                if self.generate_search(i) == False:
                    search_mistakes += 1
        mistakes += insert_mistakes + search_mistakes + delete_mistakes
        if mistakes == 0:
            print("All operations were successful")
        else:
            print(f"Number of mistakes during inserts: {insert_mistakes}, searches: {search_mistakes}, deletes: {delete_mistakes}")   
    def generate_inserts(self, num_customers):
        mistakes = 0
        for _ in range(num_customers):
            if self.generate_insert(_) == False:
                mistakes += 1
        
        if mistakes > 0:
            print(f"Found {mistakes} mistakes in {num_customers} insertions.")
        else:    
            print(f"Successfully inserted {num_customers} records.")
    def generate_search(self, num_oper):
        address, record = random.choice(self.__addresses_records)
        print(f"Searching for record at address {address}")
        print(f"Record: {record}")
        found_record = self.__heap_file.get(address, record)
        if found_record != record:
            print(f"Record not found.Operation {num_oper}")
            return False
        return True
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
            """ self.generate_inserts(1000)
            self.generate_deletes(1000) """
            self.generate_inserts(1000)
            self.generate_random_operations(1000)
            self.delete_remaining()
class HashFileTester:
    def __init__(self,  seed=None):#parcel_tree, property_tree, all_tree,
        self.__max_size = sys.maxsize
        self.__seed = seed if seed is not None else random.randint(1, self.__max_size)
        self.__hash_file = HashFile(50, CustomerByID())
        self.__customers = []
        random.seed(self.__seed)
        self.__unique_ids = set()
        self.__unique_addresses = set()
    
    def generate_finds(self):
        mistakes = 0
        for _ in self.__customers:
            id = _.customer_id
            found_element = self.__hash_file.find(id)
            if found_element != _:
                mistakes+=1
        
        if mistakes == 0:
            print("All records have been found successfully")
        else:
            print(f"Number of mistakes during find:{mistakes}")
    def generate_insert(self, operation_num):
        # Generate unique values for the customer
        id = self.generate_unique_value(4, self.__unique_ids)
        address = self.generate_unique_value(5, self.__unique_addresses)
        if operation_num == 109:
            print("tu")
        # Create a new Customer instance
        customer = CustomerByID(id, address)
        print(f"Inserting record: {customer}")
        self.__hash_file.insert(customer)
        print(f"Record {customer} inserted.\n Operation : {operation_num}")
        
        self.__customers.append(customer)
        all_blocks = self.__hash_file.get_all_blocks()
        all_records = []
        mistakes = 0
        for block  in all_blocks:
            all_records += block.records
            
        for customer in self.__customers:
            if customer not in all_records:
                print(f"Record {customer} not found in all records. Operation {operation_num}")
                mistakes += 1
        if mistakes > 0:
            print(f"{mistakes} mistakes found in {operation_num} insertions.")
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
    def generate_unique_value(self, max_length, existing_values):
        value = random.randint(0, 2147483647)
        while value in existing_values:
            value = random.randint(0, 2**max_length - 1)
        existing_values.add(value)
        return value
    def test(self):
       
            #self.__seed = 8091386027947589026
            print(f"Seed: {self.__seed}")
            """ self.generate_inserts(1000)
            self.generate_deletes(1000) """
            self.generate_inserts(1000)
            self.generate_finds()