import customtkinter as ctk
from tkinter import messagebox
class ServiceApp(ctk.CTk):
    def __init__(self, app = None):
        super().__init__()
        self.title("Magula S2")
        self.geometry("1280x720")
        self.app = app

        self.grid_columnconfigure(0, weight=1)  
        self.grid_columnconfigure(1, weight=4)  
        self.grid_rowconfigure(0, weight=1)     
  
        self.menu_frame = MenuFrame(self, self.show_frame, self.app)
        self.menu_frame.grid(row=0, column=0, sticky="nsew")

        self.container = ctk.CTkFrame(self)
        self.container.grid(row=0, column=1, sticky="nsew")
       
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)

        self.frames = {}
        for F in (AddVehicle, VehicleSearch):
            frame = F(parent=self.container, controller=self, app=self.app)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(AddVehicle)
        self.update()
    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()
        
        
class MenuFrame(ctk.CTkFrame):
    def __init__(self, parent, show_frame_callback, app):
        super().__init__(parent)
        self.app = app
        self.show_frame_callback = show_frame_callback
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        
        insert_button = ctk.CTkButton(self, text="Pridať Vozidlo", command=lambda: self.show_frame_callback(AddVehicle))
        insert_button.pack(pady=10, padx=10)
        
        vehicle_search_button = ctk.CTkButton(self, text="Vyhľadať vozidlo", command=lambda: self.show_frame_callback(VehicleSearch))
        vehicle_search_button.pack(pady=10, padx=10)

class AddVehicle(ctk.CTkFrame):
    def __init__(self, parent, controller, app):
        super().__init__(parent)
        self.app = app
        self.controller = controller
        label = ctk.CTkLabel(self, text="Pridanie Vozidla", font=("Arial", 20))
        label.grid(row=0, column=0, columnspan=4, pady=20, sticky="w")

        
        customer_name_label = ctk.CTkLabel(self, text="Meno zákazníka:")
        customer_name_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.customer_name_entry = ctk.CTkEntry(self)
        self.customer_name_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        
        customer_surname_label = ctk.CTkLabel(self, text="Priezvisko zákazníka:")
        customer_surname_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.customer_surname_entry = ctk.CTkEntry(self)
        self.customer_surname_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

       
        ecv_label = ctk.CTkLabel(self, text="ECV vozidla:")
        ecv_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.ecv_entry = ctk.CTkEntry(self)
        self.ecv_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")


        add_vehicle_button = ctk.CTkButton(self, text="Pridat", command=self.add_vehicle)
        add_vehicle_button.grid(row=11, column=0, columnspan=3, pady=20, sticky="w", padx=100)


    def add_vehicle(self):

        customer_name = self.customer_name_entry.get().strip()
        customer_surname = self.customer_surname_entry.get().strip()
        ecv = self.ecv_entry.get().strip()
        
        self.app.add_vehicle(customer_name, customer_surname, ecv)
        self.clear_form()
        self.show_success_message()
        
    def show_success_message(self):
        messagebox.showinfo("Pridane", "Vozidlo uspesne pridane")
    def show_alert(self, message):
        messagebox.showerror("Chyba", message)
    def clear_form(self):
        self.customer_name_entry.delete(0, 'end')
        self.ecv_entry.delete(0, 'end')
        self.customer_surname_entry.delete(0, 'end')
   
class VehicleSearch(ctk.CTkFrame):
    def __init__(self, parent, controller, app):
        super().__init__(parent)
        self.app = app
        self.controller = controller
        # Label for the frame
        self.label = ctk.CTkLabel(self, text="Hladanie vozidla", font=("Arial", 16))
        self.label.grid(row=0, column=0, columnspan=3, pady=10)

        # Dropdown menu for search type
        self.search_type = ctk.StringVar(value="ID Zákazníka")  # Default value
        self.dropdown = ctk.CTkOptionMenu(self, 
                                        values=["ID Zákazníka", "EČV Vozidla"], 
                                        command=self.on_search_type_change)
        self.dropdown.grid(row=1, column=0, columnspan=3, pady=10)

        # Input field for entering search value
        self.input_label = ctk.CTkLabel(self, text="ID Zákazníka:")
        self.input_label.grid(row=2, column=0, columnspan=3, pady=5)

        self.input_entry = ctk.CTkEntry(self, placeholder_text="ID Zákazníka")
        self.input_entry.grid(row=3, column=0, columnspan=3, pady=5)

        # Search button
        self.search_button = ctk.CTkButton(self, text="Nájdi", command=self.perform_search)
        self.search_button.grid(row=4, column=0, columnspan=3, pady=10)

        # Results frame
        self.results_frame = ctk.CTkFrame(self, width=600, height=300)
        self.results_frame.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

    def on_search_type_change(self, selected_option):
        """
        Update the label and placeholder of the input field based on selected search type.
        """
        if selected_option == "ID Zákazníka":
            self.input_label.configure(text="Zadaj ID Zákazníka:")
            self.input_entry.configure(placeholder_text="ID Zákazníka")
            self.search_type.set("ID Zákazníka")
        elif selected_option == "EČV Vozidla":
            self.input_label.configure(text="Zadaj EČV Vozidla:")
            self.input_entry.configure(placeholder_text="EČV Vozidla")
            self.search_type.set("EČV Vozidla")

    def perform_search(self):
        """
        Perform the search based on the selected option and input value.
        """
        search_type = self.search_type.get().strip()
        search_value = self.input_entry.get().strip()

        if not search_value:
            ctk.CTkMessageBox.show_info("Error", "Please enter a value to search.")
            return
        result = None
        if search_type == "ID Zákazníka":
            # Logic to search by Customer ID
            result = self.app.find_vehicle(customer_id=search_value, ecv=None)
            # Add your search logic here
        elif search_type == "EČV Vozidla":
            # Logic to search by Vehicle ECV
            result = self.app.find_vehicle(customer_id=None, ecv=search_value)
            # Add your search logic here
        self.display_results(result)
        
        #self.display_results(results)
    def display_results(self, results):
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        if not results:
            no_results_label = ctk.CTkLabel(self.results_frame, text="Neboli najdene ziadne vozidla.")
            no_results_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
            return

        
        vehicle_label = ctk.CTkLabel(self.results_frame, text=str(property))
        vehicle_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        edit_button = ctk.CTkButton(self.results_frame, text="Edit", command=lambda p=property: self.edit_vehicle(p))
        edit_button.grid(row=0, column=1, padx=5, pady=5)

        """ delete_button = ctk.CTkButton(self.results_frame, text="Delete", command=lambda p=property: self.delete_property(p))
        delete_button.grid(row=0, column=2, padx=5, pady=5) """
    def edit_vehicle(self, vehicle):
        pass
        
    
    def show_alert(self, message): 
        messagebox.showerror("Chyba", message)


