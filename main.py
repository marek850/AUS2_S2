from CarShop import CarShop
from GUI.ServiceApp import ServiceApp

def main():
    appka = ServiceApp(CarShop())
    appka.mainloop()
   
    """ tester = HashFileTester()
    tester.test() """
   # hash_file.get_all_blocks()
if __name__ == "__main__":
    main()
