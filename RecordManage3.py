import tkinter as tk
from tkinter import messagebox
import sqlite3
import dbs
import random
from tkinter import filedialog
from PIL import Image, ImageTk
import io

class RecordManage:
    def __init__(self, root):
        self.root = root
        self.crimIdentry = tk.StringVar()

    def add_record(self):   
        if dbs.checkEmpty("criminals") or dbs.checkEmpty("crimes"):
            messagebox.showerror("Missing Data", "Either the Criminals or Crimes table is empty. Please add records first.")
        else:
            criminal_list = dbs.getCriminalList()
        
            self.root.withdraw()
            add_window = tk.Toplevel(self.root)
            add_window.title("Add Record")
            add_window.geometry("800x400+600+50")

            
            title_label = tk.Label(add_window, text="ADD RECORD", font=("Arial", 20, "bold"))
            title_label.place(relx=0.38, y=20)
            
            frame = tk.Frame(add_window)
            frame.place(relx=0.20, y=80)
            
            #Name
            criminal_var = tk.StringVar()
            criminal_var.set("Select Criminal")  # Default value
            criminals_list = dbs.getCriminalList()
            tk.Label(frame, text="Criminal:", font=("Arial", 14, "bold")).grid(row=1, column=0, padx=10, pady=10, sticky="w")
            crime_dropdown = tk.OptionMenu(frame, criminal_var, *[f"{id} - {name.title()}" for id, name in criminal_list])
            crime_dropdown.grid(row=1, column=1, padx=10, pady=10)
            crime_dropdown.config(width=30, bd=3)
            
            #Crime
            crime_var = tk.StringVar()
            crime_var.set("Select Crime")
            crime_list = dbs.getCrimeList()
            tk.Label(frame, text="Crime:", font=("Arial", 14, "bold")).grid(row=2, column=0, padx=10, pady=10, sticky="w")
            crime_dropdown = tk.OptionMenu(frame, crime_var, * [f"{id} - {name}" for id, name in crime_list])
            crime_dropdown.grid(row=2, column=1, padx=10, pady=10)
            crime_dropdown.config(width=30, bd=3)
            
            #Location
            tk.Label(frame, text="Location: ", font=("Arial", 14, "bold")).grid(row=3, column=0, padx=5, pady=10, sticky="w")
            criminalLocation = tk.Entry(frame, width=30, bd=3)
            criminalLocation.grid(row=3, column=1, padx=2, pady=10)
            
            #Date
            tk.Label(frame, text="Year of arrest: ", font=("Arial", 14, "bold")).grid(row=4, column=0, padx=5, pady=10, sticky="w")
            recordDate = tk.Entry(frame, width=30, bd=3)
            recordDate.grid(row=4, column=1, padx=2, pady=10)


            date = recordDate.get()
            
            def add_to_db():
                criminal_id = criminal_var.get().strip(" - ")[0] #criminal id
                crime_id = crime_var.get().strip(" - ")[0] # crime id
                location = criminalLocation.get().strip()
                date = recordDate.get().strip()
                
                if criminal_var.get() == "Select Criminal" or crime_var.get() =="Select Crime" or location == "" or date == "":
                    messagebox.showerror("Error", "Please complete the details of the record")
                    return
                
                if not date.isdigit():
                    messagebox.showerror("Invalid date", "Year must be numbers only.")
                
                if (messagebox.askyesno("Confirm Criminal Record Add", "Do you wish to add the criminal record?")):
                    dbs.add_record(criminal_id, crime_id, location, date)
                    messagebox.showinfo("Successful Criminal Record Addition!", "Criminal Record was successfully added!")

                add_window.destroy()

            submit = tk.Button(frame, text="Submit", width=10, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black" ,command=add_to_db)
            submit.grid(row=6, column=1, padx=2, pady=10)

    def delete_record(self):
        if dbs.checkEmpty("records"):
            messagebox.showerror("Missing Data", "No Records to delete.")
        else:
            delRecord = tk.Toplevel(self.root)
            delRecord.title("Delete Record")
            delRecord.geometry("800x800+550+100")
                
            title_label = tk.Label(delRecord, text="DELETE RECORD", font=("Arial", 20, "bold"))                
            title_label.pack(padx=10, pady=20)


            tk.Label(delRecord, text="Select a Record to Delete", font=("Arial", 14, "bold")).pack(pady=10)
            search_entry = tk.Entry(delRecord, font=("Arial", 14), textvariable=self.crimIdentry)
            search_entry.pack(pady=10)
                
            record_list = tk.Listbox(delRecord, font=("Arial", 12), height=6)
            record_list.pack(pady=5, fill=tk.BOTH, expand=True)
                
            def populate_record_list(search_term=""):
                record_list.delete(0, tk.END)  # Clear existing items
                results = dbs.searchRecords(search_term)  # Get all records
                if results:
                    for row in results:
                        record_list.insert(tk.END, f"Record ID: {row[6]} - {row[1].title()} - {row[2].title()} - {row[3].title()} - {row[4]}")
                else:
                    record_list.insert(tk.END, "No records found")

                #call the function to populate the listbox
            populate_record_list()

                # Bind the search entry to the populate_record_list function
            self.crimIdentry.trace_add("write", lambda *args: populate_record_list(self.crimIdentry.get()))
                
            def delete():
                delete_selected = record_list.curselection()
                if not delete_selected:
                    messagebox.showerror("Error", "Please select a record to delete.")
                    return
                        
                delete_selected = record_list.get(delete_selected[0])
                record_id = delete_selected.split()[2]
                    
                if messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this record?"):
                    dbs.deleteRecord(record_id)
                    messagebox.showinfo("Success", "Record deleted successfully!")
                    populate_record_list(self.crimIdentry.get())  # Refresh the list after deletion

            delbtn = tk.Button(delRecord, text="Delete", width=10, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=delete)
            delbtn.pack(pady=10)
    #END#####

    

    def search_criminal_record(self):
        self.root.withdraw()
        self.add_window = tk.Toplevel(self.root)
        self.add_window.title("SEARCH CRIMINAL RECORD")
        self.add_window.geometry("800x600+550+100")
        
        self.record_manager = RecordManage(self.root)

        self.crimIdentry = tk.StringVar(value="")

        self.fram1 = tk.Frame(self.add_window, height=200)
        self.fram1.pack(side=tk.TOP, fill="x")
        self.fram1.pack_propagate(False)
        
        
        self.fram2 = tk.Frame(self.fram1, height=300, width=100, bg="lightgray")
        self.fram2.pack(side=tk.LEFT, fill='both')
        self.lbl = tk.Label(self.fram2)
        self.lbl.pack(side=tk.TOP, anchor="w")
        self.details_label = tk.Label(self.fram2, text="Select a record", font=("Arial", 12), justify="left", anchor="w")
        self.details_label.pack(side=tk.BOTTOM)
        
        self.fram3 = tk.Frame(self.fram1)
        self.fram3.pack()
        self.label = tk.Label(self.fram3, text="SEARCH CRIMINAL RECORD", font=("Arial", 20, "bold"))
        self.label.pack( pady=(30,10))
        self.search_entry = tk.Entry(self.fram3, font=("Arial", 14), textvariable=self.crimIdentry)
        self.search_entry.pack(pady=5 )

        self.crimIdentry.trace_add("write", lambda *args: self.handle_search()) #matic --- changes in the variable calls the function

        header_frame = tk.Frame(self.add_window)
        header_frame.pack(fill=tk.X, padx=10)   
        headers = ["ID", "Name", "Crime", "Location", "Year of Arrest"]
        for idx, text in enumerate(headers):
            tk.Label(header_frame, text=text, font=("Arial", 12, "bold"), width=15, anchor="w").grid(row=0, column=idx)

        self.results_list = tk.Listbox(self.add_window, font=("Arial", 12), height=20)
        self.results_list.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.results_list.bind("<<ListboxSelect>>", self.show_details)
        
        self.handle_search() #populate t he self.results_list

    def handle_search(self):
        """Fetch records from database and update the listbox."""
        criminal_id = self.crimIdentry.get().strip()
        
        try:
            results = dbs.searchRecords(criminal_id)  # Call the function
        except:
            results = criminal_id.isdigit()

        self.results_list.delete(0, tk.END)  # Clear previous results
        self.details_label.config(text='Select a record')

        if results == False:
            print('INVALID ID')
            self.results_list.insert(tk.END, "Invalid ID")
            return
        elif results:
            for row in results:
                self.results_list.insert(tk.END, f"ID: {row[0]} - {row[1].title()} - {row[2].title()} - {row[3].title()} - {row[4]}")  # ID and Name
        else:
            self.results_list.insert(tk.END, "No results found")
        

    def show_details(self, event):
        """Show full details when a record is selected."""
        selected_index = self.results_list.curselection()
        if not selected_index:
            return
        
        selected_text = self.results_list.get(selected_index[0])
        
        split_list = selected_text.split(" - ")

        id_value = split_list[0].replace("ID: ", "").strip()  # Remove "ID: "
        first_name = split_list[1].strip()
        crime = split_list[2].strip()
        location = split_list[3].strip()
        date = split_list[4].strip()

        selected = selected_text.split()
        criminal_id = int(selected[1])  # Extract the ID

        # Fetch full details (assuming dbs.searchRecords returns all columns)
        results = dbs.searchRecords(criminal_id)
        
        if results:
            data = results[0]  # Get first matching record
            details_text = f"ID: {id_value}\nName: {first_name.title()}\nCrime: {crime.title()}\nLocation: {location.title()}\nArrest: {date}\nRelease: {data[5]}\n"
            
            imgresults = dbs.searchCriminal(data[0])
            
            img_data = imgresults[2]  # Get BLOB data
            img = Image.open(io.BytesIO(img_data))  # Convert BLOB to an Image
            img = img.resize((100, 100), Image.LANCZOS)
            img = ImageTk.PhotoImage(img)  # Convert to Tkinter-compatible format

            self.lbl.configure(image=img)  # Update the label
            self.lbl.image = img 
            
            self.details_label.config(text=details_text)













'''
        def delete_criminal_record(self):
        delCriminal = tk.Toplevel(self.root)
        delCriminal.title("Delete Criminal Record")
        delCriminal.geometry("800x800+550+100")

        title_label = tk.Label(delCriminal, text="DELETE CRIMINAL RECORD", font=("Arial", 20, "bold"))
        title_label.pack(padx=10, pady=20)

        frame = tk.Frame(delCriminal)
        frame.place(relx=0.20, y=80)

        tk.Label(frame, text="Enter Criminal ID: ", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=5, pady=10, sticky="e")
        criminal_id_entry = tk.Entry(frame, width=30, bd=3)
        criminal_id_entry.grid(row=0, column=1, padx=2, pady=10)

        def delete():
            criminal_id = criminal_id_entry.get().strip()
            if not criminal_id:
                messagebox.showerror("Error", "Please enter a Criminal ID!")
                return

            if dbs.delete_criminal_record(criminal_id):
                messagebox.showinfo("Success", "Record deleted successfully!")
                delCriminal.destroy()
            else:
                messagebox.showerror("Error", "Failed to delete the record!")

        enter_btn = tk.Button(frame, text="Enter", width=5, bd=5, font=("Arial", 12, "bold"), fg="White", bg="black", command=delete)
        enter_btn.grid(row=0, column=3, columnspan=2, padx=20)
'''
