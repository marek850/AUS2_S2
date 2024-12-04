from Data.Customer import Customer, CustomerByECV, CustomerByID, CustomerGUI
from DataGeneration.Generator import KeyGenerator
from DataStructure.HashFile import HashFile
from DataStructure.HeapFile import HeapFile


class CarShop:
    def __init__(self):
        self.__customers = HeapFile(800, Customer())
        self.__cust_by_id = HashFile(100, CustomerByID())
        self.__cust_by_ecv = HashFile(100, CustomerByECV())
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
        customer_gui = CustomerGUI()
        customer_gui.from_customer(found_customer)
        return customer_gui
            
    def add_visit():
        pass
    def update_vehicle():
        pass