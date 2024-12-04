import sys
from CarShop import CarShop
from Data.Customer import Customer, CustomerByID
from DataStructure.Block import Block
from DataStructure.HashBlock import HashBlock
from DataStructure.HashFile import HashFile
from DataStructure.HeapFile import HeapFile
from GUI.ServiceApp import ServiceApp
from Tester.Tester import HeapFileTester
from Tester.Tester import HashFileTester

def main():
    """ string = "safeq"
    print(sys.getsizeof(string))
    print(len(string))
    print(bytes(string, encoding='utf-8'))
    print(len(bytes(string, encoding='utf-8')))
    print((5).to_bytes(4, 'little'))
    print(len((5).to_bytes(4, 'little'))) 
    
    person1 = Person(name="John Doe", age=30, address="123 Main St")
    print(f"Person 1: {person1}")
    print(f"Person 1 size : {person1.get_size()}\n")
    bytePole = person1.to_byte_array()
    person2 = Person.from_byte_array(bytePole)
    print(f"Person 2: {person2}")
    print(f"Person 2 size : {person2.get_size()}\n")
    person3 = Person()
    print(f"Person 3: {person3}")
    print(f"Person 3 size : {person3.get_size()}\n")
    block1 = Block(800, Person())
    block1.add_record(person1)
    block1.add_record(person2)
    print(f"Block 1: {block1}\n")
    print(f"Block 1 curr size : {block1.get_current_size()}\n")
    bytePole = block1.to_byte_array()
    print(f"Block 1 size : {len(bytePole)}\n")
    block2 = Block.from_byte_array(bytePole, Person, 800)
    print(f"Block 2: {block2}\n")
    
    
     """
    #print(bytearray(string, 'utf-8'))
    # Create a HeapFile with a block size of 3 records per block
    """ heap_file = HeapFile(800, Person())

    # Create Person objects
    person1 = Person(name="John Doe", age=30, address="123 Main St")
    person2 = Person(name="Alice Smith", age=25, address="456 Elm St")
    person3 = Person(name="Bob Johnson", age=40, address="789 Oak Ave")
    person4 = Person(name="Diana Prince", age=35, address="321 Pine Rd")

    # Add Persons to the HeapFile
    address1 = heap_file.insert(person1)
    print(f"Person 1 added at address: {address1}")
    print(f"Person 1 size : {person1.get_size()}\n")
    address2 = heap_file.insert(person2)
    print(f"Person 2 added at address: {address2}")

    address3 = heap_file.insert(person3)
    print(f"Person 3 added at address: {address3}")

    address4 = heap_file.insert(person4)
    print(f"Person 4 added at address: {address4}")

    # Retrieve a Person from the HeapFile using its address
    retrieved_person = heap_file.get(address2, person2)
    print(f"Retrieved Person: {retrieved_person.name}, {retrieved_person.age}, {retrieved_person.address}")
    retrieved_person2 = heap_file.get(address1, person1)
    print(f"Retrieved Person: {retrieved_person2.name}, {retrieved_person2.age}, {retrieved_person2.address}")
    retrieved_person3 = heap_file.get(address3, person3)
    print(f"Retrieved Person: {retrieved_person3.name}, {retrieved_person3.age}, {retrieved_person3.address}")
    retrieved_person4 = heap_file.get(address4, person4)
    print(f"Retrieved Person: {retrieved_person4.name}, {retrieved_person4.age}, {retrieved_person4.address}")
    print(heap_file.delete(address1, person1))
    print(heap_file.delete(address2, person2))
    print(heap_file.delete(address3, person3))
    print(heap_file.delete(address4, person4)) """
    """ heap_file = HeapFile(800, Customer())

# Create Customer objects
    customer1 = Customer(name="John", surname="Doe", ecv="AB123CD")
    customer2 = Customer(name="Alice", surname="Smith", ecv="XY456EF")
    customer3 = Customer(name="Bob", surname="Johnson", ecv="GH789IJ")
    customer4 = Customer(name="Diana", surname="Prince", ecv="KL012MN")

    # Add Customers to the HeapFile
    address1 = heap_file.insert(customer1)
    print(f"Customer 1 added at address: {address1}")
    print(f"Customer 1 size: {customer1.get_size()}\n")

    address2 = heap_file.insert(customer2)
    print(f"Customer 2 added at address: {address2}")    print(f"Customer 2 size: {customer2.get_size()}\n")

    address3 = heap_file.insert(customer3)
    print(f"Customer 3 added at address: {address3}")
    print(f"Customer 3 size: {customer3.get_size()}\n")

    address4 = heap_file.insert(customer4)
    print(f"Customer 4 added at address: {address4}")
    print(f"Customer 4 size: {customer4.get_size()}\n")

    # Retrieve Customers from the HeapFile using their addresses
    retrieved_customer1 = heap_file.get(address1, customer1)
    print(f"Retrieved Customer 1: {retrieved_customer1.name}, {retrieved_customer1.surname}, {retrieved_customer1.ecv}")

    retrieved_customer2 = heap_file.get(address2, customer2)
    print(f"Retrieved Customer 2: {retrieved_customer2.name}, {retrieved_customer2.surname}, {retrieved_customer2.ecv}")

    retrieved_customer3 = heap_file.get(address3, customer3)
    print(f"Retrieved Customer 3: {retrieved_customer3.name}, {retrieved_customer3.surname}, {retrieved_customer3.ecv}")

    retrieved_customer4 = heap_file.get(address4, customer4)
    print(f"Retrieved Customer 4: {retrieved_customer4.name}, {retrieved_customer4.surname}, {retrieved_customer4.ecv}")

    # Delete Customers from the HeapFile
    print(heap_file.delete(address1, customer1))  # Expected True if successfully deleted
    print(heap_file.delete(address2, customer2))  # Expected True if successfully deleted
    print(heap_file.delete(address3, customer3))  # Expected True if successfully deleted
    print(heap_file.delete(address4, customer4))  # Expected True if successfully deleted """
    #while True:
    """ tester = DataStructureTester()#9008504728247541526
    
    tester.test() """
    """ appka = ServiceApp()
    appka.mainloop() """
    """ customer1 = Customer(name="John", surname="Doe", ecv="AB123CD")
    customer2 = Customer(name="Alice", surname="Smith", ecv="XY456EF")
    customer3 = Customer(name="Bob", surname="Johnson", ecv="GH789IJ")
    customer4 = Customer(name="Diana", surname="Prince", ecv="KL012MN")
    
    cstmr = CustomerByID(23,4)
    cstmr_bytes = cstmr.to_byte_array()
    print(cstmr)
    cstmr2 = CustomerByID.from_byte_array(cstmr_bytes)
    print(cstmr2)
    if cstmr == cstmr2:
        print("rovnake")
    
    hshblock = HashBlock(800, CustomerByID())
    
    hshblock.add_record(cstmr)
    print(hshblock)
    hash2 = hshblock.to_byte_array()
    asdhas = HashBlock.from_byte_array(hash2, CustomerByID, 800)
    print(asdhas)
    if hshblock == asdhas:
        print("rovnake") """
    """  
    hash_file = HashFile(20, CustomerByID())
    hash_file.insert(CustomerByID(23, 4))
    print(hash_file.find(CustomerByID(23, 4)))
    print("---------------------------------")
    hash_file.insert(CustomerByID(3, 4))
    print(hash_file.find(CustomerByID(23, 4)))
    print(hash_file.find(CustomerByID(3, 4)))
    print("---------------------------------")
    hash_file.insert(CustomerByID(7, 4))
    print(hash_file.find(CustomerByID(23, 4)))
    print(hash_file.find(CustomerByID(3, 4)))
    print(hash_file.find(CustomerByID(7, 4)))
    print("---------------------------------")
    hash_file.insert(CustomerByID(9, 4))
    print(hash_file.find(CustomerByID(23, 4)))
    print(hash_file.find(CustomerByID(3, 4)))
    print(hash_file.find(CustomerByID(7, 4)))
    print(hash_file.find(CustomerByID(9, 4)))
    print("---------------------------------")
    hash_file.insert(CustomerByID(11, 4))
    print(hash_file.find(CustomerByID(23, 4)))
    print(hash_file.find(CustomerByID(3, 4)))
    print(hash_file.find(CustomerByID(7, 4)))
    print(hash_file.find(CustomerByID(9, 4)))
    print(hash_file.find(CustomerByID(11, 4)))
    print("---------------------------------")
    hash_file.get_all_blocks() """
    """  tester = HashFileTester()#9008504728247541526
    
    tester.test() """
    appka = ServiceApp(CarShop())
    appka.mainloop()
   # hash_file.get_all_blocks()
if __name__ == "__main__":
    main()
