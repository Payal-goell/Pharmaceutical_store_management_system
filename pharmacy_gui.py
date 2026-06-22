import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import mysql.connector
from datetime import datetime

class PharmacyManagementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Pharmacy Management System")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        
        # Database connection parameters
        self.db_host = "localhost"
        self.db_user = "root"
        self.db_password = "dstvtush04"
        self.db_name = None
        self.table_name = None
        self.connection = None
        
        # Initialize setup
        self.show_setup_screen()
    
    def show_setup_screen(self):
        """Display database and table setup screen"""
        self.setup_frame = ttk.Frame(self.root)
        self.setup_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(self.setup_frame, text="PHARMACY MANAGEMENT SYSTEM", 
                               font=("Arial", 20, "bold"))
        title_label.pack(pady=20)
        
        # Subtitle
        subtitle_label = ttk.Label(self.setup_frame, 
                                  text="Setup Database Connection", 
                                  font=("Arial", 12))
        subtitle_label.pack(pady=10)
        
        # Database Name
        db_frame = ttk.Frame(self.setup_frame)
        db_frame.pack(pady=10)
        ttk.Label(db_frame, text="Database Name:", font=("Arial", 10)).pack(side="left", padx=5)
        self.db_entry = ttk.Entry(db_frame, width=30, font=("Arial", 10))
        self.db_entry.pack(side="left", padx=5)
        
        # Table Name
        table_frame = ttk.Frame(self.setup_frame)
        table_frame.pack(pady=10)
        ttk.Label(table_frame, text="Table Name:", font=("Arial", 10)).pack(side="left", padx=5)
        self.table_entry = ttk.Entry(table_frame, width=30, font=("Arial", 10))
        self.table_entry.pack(side="left", padx=5)
        
        # Connect Button
        connect_btn = ttk.Button(self.setup_frame, text="Connect & Start", 
                                command=self.setup_database)
        connect_btn.pack(pady=20)
        
        # Info Label
        info_label = ttk.Label(self.setup_frame, 
                              text="Note: Database will be created if it doesn't exist.",
                              font=("Arial", 9), foreground="gray")
        info_label.pack(pady=10)
    
    def setup_database(self):
        """Initialize database connection"""
        self.db_name = self.db_entry.get()
        self.table_name = self.table_entry.get()
        
        if not self.db_name or not self.table_name:
            messagebox.showerror("Error", "Please enter both database and table name")
            return
        
        try:
            # Connect to MySQL
            self.connection = mysql.connector.connect(
                host=self.db_host,
                user=self.db_user,
                password=self.db_password
            )
            cursor = self.connection.cursor()
            
            # Create database
            sql = f"CREATE DATABASE IF NOT EXISTS {self.db_name}"
            cursor.execute(sql)
            
            # Use database
            cursor.execute(f"USE {self.db_name}")
            
            # Create table
            create_table_sql = f"""CREATE TABLE IF NOT EXISTS {self.table_name} (
                Customer_ID INT PRIMARY KEY,
                Name VARCHAR(50) NOT NULL,
                Disease VARCHAR(50),
                Medicine VARCHAR(50),
                Balance FLOAT,
                Last_Purchase_Date VARCHAR(15)
            )"""
            cursor.execute(create_table_sql)
            self.connection.commit()
            cursor.close()
            
            messagebox.showinfo("Success", 
                              f"Connected to database '{self.db_name}' with table '{self.table_name}'")
            
            # Show main menu
            self.setup_frame.destroy()
            self.show_main_menu()
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    
    def show_main_menu(self):
        """Display main menu"""
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(self.main_frame, text="PHARMACY MANAGEMENT SYSTEM", 
                               font=("Arial", 18, "bold"))
        title_label.pack(pady=10)
        
        # Database Info
        info_label = ttk.Label(self.main_frame, 
                              text=f"Database: {self.db_name} | Table: {self.table_name}",
                              font=("Arial", 9), foreground="gray")
        info_label.pack(pady=5)
        
        # Button Frame
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(expand=True, fill="both", pady=10)
        
        # Buttons
        buttons = [
            ("Add Customer Record", self.add_customer),
            ("Display All Records", self.display_all_records),
            ("Display Particular Record", self.display_particular_record),
            ("Delete All Records", self.delete_all_records),
            ("Delete Particular Record", self.delete_particular_record),
            ("Modify Customer Record", self.modify_record),
            ("Exit", self.exit_application)
        ]
        
        for i, (text, command) in enumerate(buttons):
            btn = ttk.Button(button_frame, text=text, command=command, width=35)
            btn.pack(pady=8)
    
    def add_customer(self):
        """Add a new customer record"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Customer Record")
        dialog.geometry("400x350")
        
        # Labels and Entries
        fields = [
            ("Customer ID:", "cust_id"),
            ("Name:", "cust_name"),
            ("Disease:", "cust_disease"),
            ("Medicine:", "cust_medicine"),
            ("Balance:", "cust_balance"),
            ("Last Purchase Date (DD/MM/YYYY):", "cust_date")
        ]
        
        entries = {}
        for label_text, key in fields:
            ttk.Label(dialog, text=label_text).pack(pady=5)
            entry = ttk.Entry(dialog, width=40)
            entry.pack(pady=2)
            entries[key] = entry
        
        def save_record():
            try:
                cust_id = int(entries["cust_id"].get())
                cust_name = entries["cust_name"].get()
                cust_disease = entries["cust_disease"].get()
                cust_medicine = entries["cust_medicine"].get()
                cust_balance = float(entries["cust_balance"].get())
                cust_date = entries["cust_date"].get()
                
                if not cust_name:
                    messagebox.showerror("Error", "Customer name is required")
                    return
                
                cursor = self.connection.cursor()
                query = f"INSERT INTO {self.table_name} VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(query, (cust_id, cust_name, cust_disease, cust_medicine, 
                                      cust_balance, cust_date))
                self.connection.commit()
                cursor.close()
                
                messagebox.showinfo("Success", "Record added successfully!")
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid input format")
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
        
        ttk.Button(dialog, text="Save Record", command=save_record).pack(pady=10)
    
    def display_all_records(self):
        """Display all customer records"""
        try:
            cursor = self.connection.cursor()
            query = f"SELECT * FROM {self.table_name}"
            cursor.execute(query)
            records = cursor.fetchall()
            cursor.close()
            
            if not records:
                messagebox.showinfo("Records", "No records found")
                return
            
            # Create display window
            display_window = tk.Toplevel(self.root)
            display_window.title("All Customer Records")
            display_window.geometry("800x500")
            
            # Create Treeview
            columns = ("Customer ID", "Name", "Disease", "Medicine", "Balance", "Last Purchase Date")
            tree = ttk.Treeview(display_window, columns=columns, height=20)
            tree.column("#0", width=0, stretch="no")
            tree.column("Customer ID", anchor="center", width=80)
            tree.column("Name", anchor="w", width=100)
            tree.column("Disease", anchor="w", width=100)
            tree.column("Medicine", anchor="w", width=100)
            tree.column("Balance", anchor="center", width=80)
            tree.column("Last Purchase Date", anchor="center", width=120)
            
            tree.heading("#0", text="", anchor="w")
            for col in columns:
                tree.heading(col, text=col, anchor="w")
            
            # Add data
            for record in records:
                tree.insert(parent="", index="end", text="", values=record)
            
            # Add scrollbar
            scrollbar = ttk.Scrollbar(display_window, orient="vertical", command=tree.yview)
            tree.configure(yscroll=scrollbar.set)
            tree.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    
    def display_particular_record(self):
        """Display a particular customer record"""
        cust_id = simpledialog.askinteger("Search", "Enter Customer ID:")
        if cust_id is None:
            return
        
        try:
            cursor = self.connection.cursor()
            query = f"SELECT * FROM {self.table_name} WHERE Customer_ID = %s"
            cursor.execute(query, (cust_id,))
            record = cursor.fetchone()
            cursor.close()
            
            if not record:
                messagebox.showinfo("Search Result", "No record found for this Customer ID")
                return
            
            # Display record
            display_text = f"""
Customer Record:
─────────────────────────────
Customer ID:         {record[0]}
Name:                {record[1]}
Disease:             {record[2]}
Medicine:            {record[3]}
Balance:             ${record[4]}
Last Purchase Date:  {record[5]}
            """
            messagebox.showinfo("Customer Record", display_text)
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    
    def delete_all_records(self):
        """Delete all customer records"""
        confirm = messagebox.askyesno("Confirm", 
                                     "Are you sure you want to delete ALL records? This cannot be undone.")
        if not confirm:
            return
        
        try:
            cursor = self.connection.cursor()
            query = f"DELETE FROM {self.table_name}"
            cursor.execute(query)
            self.connection.commit()
            cursor.close()
            
            messagebox.showinfo("Success", "All records deleted successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    
    def delete_particular_record(self):
        """Delete a particular customer record"""
        cust_id = simpledialog.askinteger("Delete", "Enter Customer ID to delete:")
        if cust_id is None:
            return
        
        confirm = messagebox.askyesno("Confirm", 
                                     f"Delete record for Customer ID {cust_id}?")
        if not confirm:
            return
        
        try:
            cursor = self.connection.cursor()
            query = f"DELETE FROM {self.table_name} WHERE Customer_ID = %s"
            cursor.execute(query, (cust_id,))
            self.connection.commit()
            
            if cursor.rowcount > 0:
                messagebox.showinfo("Success", "Record deleted successfully!")
            else:
                messagebox.showinfo("Not Found", f"Customer ID {cust_id} not found")
            
            cursor.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    
    def modify_record(self):
        """Modify a customer record"""
        cust_id = simpledialog.askinteger("Modify", "Enter Customer ID to modify:")
        if cust_id is None:
            return
        
        try:
            cursor = self.connection.cursor()
            query = f"SELECT * FROM {self.table_name} WHERE Customer_ID = %s"
            cursor.execute(query, (cust_id,))
            record = cursor.fetchone()
            cursor.close()
            
            if not record:
                messagebox.showinfo("Not Found", "Customer ID not found")
                return
            
            # Create modify window
            modify_window = tk.Toplevel(self.root)
            modify_window.title(f"Modify Record - Customer {cust_id}")
            modify_window.geometry("400x350")
            
            # Display current values
            ttk.Label(modify_window, text=f"Current Record for Customer {cust_id}:", 
                     font=("Arial", 10, "bold")).pack(pady=10)
            
            # Editable fields
            fields = [
                ("Medicine:", record[3], "medicine"),
                ("Balance:", str(record[4]), "balance"),
                ("Last Purchase Date (DD/MM/YYYY):", record[5], "date")
            ]
            
            entries = {}
            for label_text, current_value, key in fields:
                frame = ttk.Frame(modify_window)
                frame.pack(pady=5)
                ttk.Label(frame, text=label_text).pack(side="left", padx=5)
                entry = ttk.Entry(frame, width=30)
                entry.insert(0, current_value)
                entry.pack(side="left", padx=5)
                entries[key] = entry
            
            def update_record():
                try:
                    medicine = entries["medicine"].get()
                    balance = float(entries["balance"].get())
                    date = entries["date"].get()
                    
                    cursor = self.connection.cursor()
                    query = f"UPDATE {self.table_name} SET Medicine=%s, Balance=%s, Last_Purchase_Date=%s WHERE Customer_ID=%s"
                    cursor.execute(query, (medicine, balance, date, cust_id))
                    self.connection.commit()
                    cursor.close()
                    
                    messagebox.showinfo("Success", "Record updated successfully!")
                    modify_window.destroy()
                except ValueError:
                    messagebox.showerror("Error", "Invalid input format")
                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Error: {err}")
            
            ttk.Button(modify_window, text="Update Record", command=update_record).pack(pady=10)
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    
    def exit_application(self):
        """Exit the application"""
        confirm = messagebox.askyesno("Exit", "Are you sure you want to exit?")
        if confirm:
            if self.connection:
                self.connection.close()
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = PharmacyManagementGUI(root)
    root.mainloop()
