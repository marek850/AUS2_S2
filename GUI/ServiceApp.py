import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import Calendar  # Date picker widget
from datetime import date, datetime

from Data.JobDescription import JobDescription
from Data.Visit import Visit
class ServiceApp(ctk.CTk):
    def __init__(self, app=None):
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
        self.grid_rowconfigure(0, weight=1)

        self.frames = {}
        for F in (AddVehicle, VehicleSearch, HeapFile, HashFileID, HashFileECV, GenerateData):
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

        vehicle_search_button = ctk.CTkButton(self, text="Vyhľadát vozidlo", command=lambda: self.show_frame_callback(VehicleSearch))
        vehicle_search_button.pack(pady=10, padx=10)

        heapfile_button = ctk.CTkButton(self, text="HeapFile - Výpis", command=lambda: self.show_frame_callback(HeapFile))
        heapfile_button.pack(pady=10, padx=10)

        hashfile_id_button = ctk.CTkButton(self, text="HashFile ID - Výpis", command=lambda: self.show_frame_callback(HashFileID))
        hashfile_id_button.pack(pady=10, padx=10)

        hashfile_ecv_button = ctk.CTkButton(self, text="HashFile ECV - Výpis", command=lambda: self.show_frame_callback(HashFileECV))
        hashfile_ecv_button.pack(pady=10, padx=10)

        generate_data_button = ctk.CTkButton(self, text="Generovanie Dát", command=lambda: self.show_frame_callback(GenerateData))
        generate_data_button.pack(pady=10, padx=10)
        
        save_button = ctk.CTkButton(self, text="Uložiť", command=lambda: self.save())
        save_button.pack(pady=10, padx=10)
    def save(self):
        self.app.save()
        messagebox.showinfo("Úspech", "Zmeny boli úspešne uložené.")

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
        if selected_option == "ID Zákazníka":
            self.input_label.configure(text="Zadaj ID Zákazníka:")
            self.search_type.set("ID Zákazníka")
        elif selected_option == "EČV Vozidla":
            self.input_label.configure(text="Zadaj EČV Vozidla:")
            self.search_type.set("EČV Vozidla")

    def perform_search(self):
        search_type = self.search_type.get().strip()
        search_value = self.input_entry.get().strip()

        if not search_value:
            messagebox.showinfo("Chyba", "Zadaj hodnotu")
            return
        result = None
        if search_type == "ID Zákazníka":
            # Logic to search by Customer ID
            result = self.app.find_vehicle(customer_id=int(search_value), ecv=None)
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

        
        vehicle_label = ctk.CTkLabel(self.results_frame, text=str(results),wraplength=500)
        vehicle_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        edit_button = ctk.CTkButton(self.results_frame, text="Upravit", command=lambda v=results: self.edit_vehicle(v))
        edit_button.grid(row=0, column=1, padx=5, pady=5)

        add_visit = ctk.CTkButton(self.results_frame, text="Pridat navstevu", command=lambda v=results: self.add_visit(v))
        add_visit.grid(row=0, column=2, padx=5, pady=5)
    def edit_vehicle(self, vehicle):
       
        edit_window = EditCustomerForm(self, vehicle, self.app)
        edit_window.grab_set()
        
    def add_visit(self, vehicle):
        add_visit_window = AddVisitWindow(self, vehicle, self.app)
        add_visit_window.grab_set()
    def show_alert(self, message): 
        messagebox.showerror("Chyba", message)


class AddVisitWindow(ctk.CTkToplevel):
    def __init__(self, parent, vehicle, app):
        super().__init__(parent)
        self.vehicle = vehicle
        self.app = app
        self.title("Pridať Novú Návštevu")
        self.geometry("600x800")

        # Price Label and Entry
        self.price_label = ctk.CTkLabel(self, text="Cena návštevy:")
        self.price_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.price_entry = ctk.CTkEntry(self)
        self.price_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Date Picker Label and Calendar
        self.date_label = ctk.CTkLabel(self, text="Vyberte dátum:")
        self.date_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.calendar = Calendar(self, selectmode='day', year=date.today().year, month=date.today().month, day=date.today().day)
        self.calendar.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Job Descriptions
        self.job_descriptions = []
        self.job_description_labels = []
        self.job_description_entries = []
        for i in range(10):
            label = ctk.CTkLabel(self, text=f"Popis práce {i + 1}:")
            label.grid(row=2 + i, column=0, padx=10, pady=5, sticky="w")
            entry = ctk.CTkEntry(self)
            entry.grid(row=2 + i, column=1, padx=10, pady=5, sticky="w")
            self.job_descriptions.append(entry)

        # Add Visit Button
        self.add_visit_button = ctk.CTkButton(self, text="Pridať návštevu", command=self.add_visit)
        self.add_visit_button.grid(row=13, column=0, columnspan=2, pady=20)

    def add_visit(self):
        # Get price
        price = self.price_entry.get().strip()
        if not price:
            messagebox.showerror("Chyba", "Prosím zadajte cenu návštevy.")
            return

        try:
            price = float(price)
        except ValueError:
            messagebox.showerror("Chyba", "Cena musí byť číslo.")
            return

        # Get date
        visit_date_str = self.calendar.get_date()
        try:
            visit_date = datetime.strptime(visit_date_str, "%m/%d/%y").date()
        except ValueError:
            messagebox.showerror("Chyba", "Neplatný formát dátumu.")
            return

        # Get job descriptions
        descriptions = [entry.get().strip() for entry in self.job_descriptions if entry.get().strip()]

        # Create Visit instance
        visit = Visit(price=price, date=visit_date)
        for desc in descriptions:
            visit.add_description(desc)
        
        # Add visit to the vehicle via app logic
        self.app.add_visit_to_vehicle(self.vehicle, visit)

        # Show success message
        messagebox.showinfo("Úspech", "Návšteva bola úspešne pridaná.")
        self.destroy()
class HeapFile(ctk.CTkFrame):
    def __init__(self, parent, controller, app):
        super().__init__(parent)
        self.app = app
        self.controller = controller
        self.label = ctk.CTkLabel(self, text="HeapFile - Výpis všetkých blokov", font=("Arial", 20))
        self.label.grid(row=0, column=0, columnspan=4, pady=20, sticky="w")

        self.refresh_button = ctk.CTkButton(self, text="Obnoviť", command=self.refresh)
        self.refresh_button.grid(row=0, column=4, padx=10, pady=10)

        # Create a scrollable CTkTextbox for blocks
        self.blocks_textbox = ctk.CTkTextbox(self, width=800, height=500)
        self.blocks_textbox.grid(row=1, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")
        self.blocks_textbox.configure(state="disabled")

        # Logic to get all blocks from the heap file
        blocks = self.app.get_all_blocks("ALL")
        self.display_blocks(blocks)

    def display_blocks(self, blocks):
        self.blocks_textbox.configure(state="normal")
        self.blocks_textbox.delete(1.0, "end")
        self.blocks_textbox.insert("end", "\n".join(str(block) for block in blocks))
        self.blocks_textbox.configure(state="disabled")

    def refresh(self):
        blocks = self.app.get_all_blocks("ALL")
        self.display_blocks(blocks)

class HashFileID(ctk.CTkFrame):
    def __init__(self, parent, controller, app):
        super().__init__(parent)
        self.app = app
        self.controller = controller
        self.label = ctk.CTkLabel(self, text="HashFile ID - Výpis všetkých blokov", font=("Arial", 20))
        self.label.grid(row=0, column=0, columnspan=4, pady=20, sticky="w")

        self.refresh_button = ctk.CTkButton(self, text="Obnoviť", command=self.refresh)
        self.refresh_button.grid(row=0, column=4, padx=10, pady=10)

        # Create a scrollable CTkTextbox for blocks
        self.blocks_textbox = ctk.CTkTextbox(self, width=800, height=500)
        self.blocks_textbox.grid(row=1, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")
        self.blocks_textbox.configure(state="disabled")

        # Logic to get all blocks from the hash file by ID
        blocks = self.app.get_all_blocks("ID")
        self.display_blocks(blocks)

    def display_blocks(self, blocks):
        self.blocks_textbox.configure(state="normal")
        self.blocks_textbox.delete(1.0, "end")
        self.blocks_textbox.insert("end", "\n".join(str(block) for block in blocks))
        self.blocks_textbox.configure(state="disabled")

    def refresh(self):
        blocks = self.app.get_all_blocks("ID")
        self.display_blocks(blocks)

class HashFileECV(ctk.CTkFrame):
    def __init__(self, parent, controller, app):
        super().__init__(parent)
        self.app = app
        self.controller = controller
        self.label = ctk.CTkLabel(self, text="HashFile ECV - Výpis všetkých blokov", font=("Arial", 20))
        self.label.grid(row=0, column=0, columnspan=4, pady=20, sticky="w")

        self.refresh_button = ctk.CTkButton(self, text="Obnoviť", command=self.refresh)
        self.refresh_button.grid(row=0, column=4, padx=10, pady=10)

        # Create a scrollable CTkTextbox for blocks
        self.blocks_textbox = ctk.CTkTextbox(self, width=800, height=500)
        self.blocks_textbox.grid(row=1, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")
        self.blocks_textbox.configure(state="disabled")

        # Logic to get all blocks from the hash file by ECV
        blocks = self.app.get_all_blocks("ECV")
        self.display_blocks(blocks)

    def display_blocks(self, blocks):
        self.blocks_textbox.configure(state="normal")
        self.blocks_textbox.delete(1.0, "end")
        self.blocks_textbox.insert("end", "\n".join(str(block) for block in blocks))
        self.blocks_textbox.configure(state="disabled")

    def refresh(self):
        blocks = self.app.get_all_blocks("ECV")
        self.display_blocks(blocks)


class GenerateData(ctk.CTkFrame):
    def __init__(self, parent, controller, app):
        super().__init__(parent)
        self.app = app
        self.controller = controller

        label = ctk.CTkLabel(self, text="Generovanie Dát", font=("Arial", 20))
        label.grid(row=0, column=0, columnspan=2, pady=20, sticky="w")

        self.records_label = ctk.CTkLabel(self, text="Počet záznamov na generovanie:")
        self.records_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.records_entry = ctk.CTkEntry(self)
        self.records_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        generate_button = ctk.CTkButton(self, text="Generovať", command=self.generate_data)
        generate_button.grid(row=2, column=0, columnspan=2, pady=20)

    def generate_data(self):
        records_str = self.records_entry.get().strip()
        if not records_str.isdigit():
            messagebox.showerror("Chyba", "Prosím zadajte platný počet záznamov.")
            return

        records = int(records_str)
        if records <= 0:
            messagebox.showerror("Chyba", "Počet záznamov musí byť väčší ako 0.")
            return

        # Call the app logic to generate the data
        self.app.generate_data(records)
        messagebox.showinfo("Uspech", f"{records} záznamov bolo úspešne generovaných.")
class EditCustomerForm(ctk.CTkToplevel):
    def __init__(self, parent, customer, app):
        super().__init__(parent)
        self.customer = customer
        self.title("Upraviť zákazníka")
        self.geometry("700x800")
        self.app = app

        # Create a scrollable frame
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=680, height=550)
        self.scrollable_frame.grid(row=0, column=0, padx=10, pady=10, columnspan=2, sticky="nsew")

        # Labels and entry fields for customer's name and surname
        self.name_label = ctk.CTkLabel(self.scrollable_frame, text="Meno:", font=("Arial", 14))
        self.name_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.name_entry = ctk.CTkEntry(self.scrollable_frame, width=300)
        self.name_entry.insert(0, customer.name)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        self.surname_label = ctk.CTkLabel(self.scrollable_frame, text="Priezvisko:", font=("Arial", 14))
        self.surname_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.surname_entry = ctk.CTkEntry(self.scrollable_frame, width=300)
        self.surname_entry.insert(0, customer.surname)
        self.surname_entry.grid(row=1, column=1, padx=10, pady=10)

        # Visits fields
        self.visits_label = ctk.CTkLabel(self.scrollable_frame, text="Návštevy:", font=("Arial", 14))
        self.visits_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.visit_widgets = []
        row_idx = 3
        for idx, visit in enumerate(customer.visits[:customer.valid_visits]):
            # Visit Price
            visit_price_label = ctk.CTkLabel(self.scrollable_frame, text=f"Cena návštevy {idx + 1}:")
            visit_price_label.grid(row=row_idx, column=0, padx=10, pady=10, sticky="w")
            visit_price_entry = ctk.CTkEntry(self.scrollable_frame)
            visit_price_entry.insert(0, str(visit.price if hasattr(visit, 'price') else ''))
            visit_price_entry.grid(row=row_idx, column=1, padx=10, pady=10, sticky="w")

            # Date Picker Label and Calendar
            visit_date_label = ctk.CTkLabel(self.scrollable_frame, text=f"Dátum návštevy {idx + 1}:")
            visit_date_label.grid(row=row_idx + 1, column=0, padx=10, pady=10, sticky="w")
            visit_calendar = Calendar(self.scrollable_frame, selectmode='day', year=visit.date.year, month=visit.date.month, day=visit.date.day)
            visit_calendar.grid(row=row_idx + 1, column=1, padx=10, pady=10, sticky="w")
            if hasattr(visit, 'date') and visit.date:
                visit_calendar.selection_set(visit.date) if visit.date else None

            # Job Descriptions
            job_descriptions = []
            for i in range(10):
                job_desc_label = ctk.CTkLabel(self.scrollable_frame, text=f"Popis práce {idx + 1}.{i + 1}:")
                job_desc_label.grid(row=row_idx + 2 + i, column=0, padx=10, pady=5, sticky="w")
                job_desc_entry = ctk.CTkEntry(self.scrollable_frame)
                job_desc_entry.insert(0, visit.description[i].description)
                job_desc_entry.grid(row=row_idx + 2 + i, column=1, padx=10, pady=5, sticky="w")
                job_descriptions.append(job_desc_entry)

            self.visit_widgets.append((visit_price_entry, visit_calendar, job_descriptions))
            row_idx += 13

        # Buttons to save or cancel
        self.save_button = ctk.CTkButton(self, text="Uložiť", command=self.save_customer)
        self.save_button.grid(row=1, column=0, padx=10, pady=20, sticky="e")
        
        self.cancel_button = ctk.CTkButton(self, text="Zrušiť", command=self.destroy)
        self.cancel_button.grid(row=1, column=1, padx=10, pady=20, sticky="w")

    def save_customer(self):
        # Get values from entry fields
        new_name = self.name_entry.get().strip()
        new_surname = self.surname_entry.get().strip()

        # Validate fields
        if not new_name or not new_surname:
            messagebox.showerror("Chyba", "Meno a priezvisko musia byť vyplnené.")
            return

        # Update customer details
        self.customer.name = new_name
        self.customer.surname = new_surname

        new_visits = []
        for visit_price_entry, visit_calendar, job_desc_entries in self.visit_widgets:
            
            price = visit_price_entry.get().strip()
            if not price:
                messagebox.showerror("Chyba", "Prosím zadajte cenu návštevy.")
                return
            try:
                price = float(price)
            except ValueError:
                messagebox.showerror("Chyba", "Cena musí byť číslo.")
                return

            
            visit_date_str = visit_calendar.get_date()
            try:
                visit_date = datetime.strptime(visit_date_str, "%m/%d/%y").date()
            except ValueError:
                messagebox.showerror("Chyba", "Neplatný formát dátumu.")
                return

            descriptions = [entry.get().strip() for entry in job_desc_entries]
            valid_job_descriptions = []
            for desc in descriptions:
                if desc != "Unknown" and desc != "":
                    valid_job_descriptions.append(desc)
            
            # Create Visit instance
            visit = Visit(price=price, date=visit_date)
            for desc in valid_job_descriptions:
                visit.add_description(desc)

            new_visits.append(visit)
        for _ in self.customer.visits:
            self.customer.remove_visit(_)
        for _ in new_visits:
            self.customer.add_visit(_)
        self.app.update_customer(self.customer)
        self.destroy()
