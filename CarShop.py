from datetime import date
import random
import string
from Data.Customer import Customer, CustomerByECV, CustomerByID, CustomerGUI
from Data.Visit import Visit
from DataGeneration.Generator import KeyGenerator
from DataStructure.HashFile import HashFile
from DataStructure.HeapFile import HeapFile


class CarShop:
    def __init__(self):
        self.__customers = HeapFile(2000, Customer(), "heap_file.bin", "customers.csv")
        self.__cust_by_id = HashFile(100, CustomerByID(), "hash_file_id.bin", "customers_by_id.csv")
        self.__cust_by_ecv = HashFile(100, CustomerByECV(), "hash_file_ecv.bin", "customers_by_ecv.csv")
        self.__generator = KeyGenerator()
    @property
    def customers(self):
        return self.__customers

    @customers.setter
    def customers(self, value):
        self.__customers = value

    @property
    def cust_by_id(self):
        return self.__cust_by_id

    @cust_by_id.setter
    def cust_by_id(self, value):
        self.__cust_by_id = value

    @property
    def cust_by_ecv(self):
        return self.__cust_by_ecv

    @cust_by_ecv.setter
    def cust_by_ecv(self, value):
        self.__cust_by_ecv = value
    def add_vehicle(self,name, surname, ecv):
        new_record = Customer(name, surname, ecv, self.__generator.generate_id())
        record_address = self.__customers.insert(new_record)
        rec_by_id = CustomerByID(new_record.id, record_address)
        rec_by_ecv = CustomerByECV(new_record.ecv, record_address)
        self.__cust_by_id.insert(rec_by_id)
        self.__cust_by_ecv.insert(rec_by_ecv)
    def find_vehicle(self, customer_id = None, ecv = None):
        customer = None
        dummy_cus = None
        if customer_id is not None:
            customer = self.__cust_by_id.find(customer_id)
            dummy_cus = Customer()
            dummy_cus.id = customer_id
        elif ecv is not None:
            customer = self.__cust_by_ecv.find(ecv)
            dummy_cus = Customer()
            dummy_cus.ecv = ecv
        block = self.__customers.read_block(customer.address)
        found_customer = block.get_record(dummy_cus)
        print(found_customer)
        customer_gui = CustomerGUI()
        customer_gui.from_customer(found_customer)
        return customer_gui
    def add_visit_to_vehicle(self, customer, visit):        
        customer.add_visit(visit)
        cus = customer.to_customer()
        address = self.__cust_by_id.find(cus.id).address
        customer_to_update = self.__customers.get(address, cus)
        customer_to_update.visits = cus.visits
        customer_to_update.valid_visits = cus.valid_visits
        self.__customers.update(address, customer_to_update)
    def get_all_blocks(self, type):
        if type == "ALL":  
            return self.__customers.get_all_blocks()
        elif type == "ID":
            return self.__cust_by_id.get_all_blocks()
        elif type == "ECV":
            return self.__cust_by_ecv.get_all_blocks()
    def generate_data(self, num_records):
        customers = []
        for _ in range(num_records):
           
            name = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
            surname = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
            ecv = self.__generator.generate_ecv()
            id = self.__generator.generate_id()
            customer = Customer(name=name, surname=surname, ecv=ecv, id=id)
            
            num_of_visits = random.randint(2, 5)
            for _ in range(num_of_visits):
                price = random.randint(0, 1000)
                visit_date = date(random.randint(2000, 2023), random.randint(1, 12), random.randint(1, 28))
                visit = Visit(price, visit_date)
                num_of_desc = random.randint(2, 6)
                for _ in range(num_of_desc):
                    desc = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
                    visit.add_description(desc)
                customer.add_visit(visit)
            customers.append(customer)
        for _ in customers:
            self.add_generated_vehicle(_)
            print(f"Inserted record: {_}")
        print(f"Generated {num_records} customers.")
    def add_generated_vehicle(self,record):
        record_address = self.__customers.insert(record)
        rec_by_id = CustomerByID(record.id, record_address)
        rec_by_ecv = CustomerByECV(record.ecv, record_address)
        self.__cust_by_id.insert(rec_by_id)
        self.__cust_by_ecv.insert(rec_by_ecv)  
    def update_customer(self, customer):
        customer_to_update = customer.to_customer()
        address = self.__cust_by_id.find(customer_to_update.id).address
        self.__customers.update(address, customer_to_update)
    def save(self):
        self.__customers.save()
        self.__cust_by_id.save()
        self.__cust_by_ecv.save()