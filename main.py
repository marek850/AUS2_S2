import sys
from DataStructure.Block import Block
from DataStructure.HeapFile import HeapFile
from Person import Person

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
    heap_file = HeapFile(800, Person())

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
    print(heap_file.delete(address4, person4))
if __name__ == "__main__":
    main()
