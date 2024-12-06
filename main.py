from datetime import date
import random
import string
import sys
from CarShop import CarShop
from Data.Customer import Customer, CustomerByID
from Data.JobDescription import JobDescription
from Data.Visit import Visit
from DataGeneration.Generator import KeyGenerator
from DataStructure.Block import Block
from DataStructure.HashBlock import HashBlock
from DataStructure.HashFile import HashFile
from DataStructure.HeapFile import HeapFile
from GUI.ServiceApp import ServiceApp
from Tester.Tester import HeapFileTester
from Tester.Tester import HashFileTester

def main():
    appka = ServiceApp(CarShop())
    appka.mainloop()
   
    """ jobD1 = JobDescription("Job1")
    print(jobD1)
    bytes = jobD1.to_byte_array()
    job2 = JobDescription.from_byte_array(bytes)
    print(job2)
    visit1 = Visit(2.0, date= date(2024, 11, 23))
    visit1.add_description("Job1")
    print(visit1)
    bytes2 = visit1.to_byte_array()
    print(bytes2)
    visit2 = Visit.from_byte_array(bytes2)
    print(visit2) """
    """ tester = HashFileTester()
    tester.test() """
   # hash_file.get_all_blocks()
if __name__ == "__main__":
    main()
