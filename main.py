import tkinter
from tkinter import ttk
from tkinter import messagebox
import sqlite3

def delete():
    employee_id_to_delete = employee_id_entry.get()
    
    if employee_id_to_delete:
        conn = sqlite3.connect('employee_data.db')
        cursor = conn.cursor()
        
        delete_query = "DELETE FROM Employee_Data WHERE employee_id = ?"
        cursor.execute(delete_query, (employee_id_to_delete,))
        
        conn.commit()
        conn.close()
    else:
        tkinter.messagebox.showwarning(title="Error", message="Please enter the employee ID to delete.")

def submit():
    employee_id = employee_id_entry.get()
    employee_name = employee_name_entry.get()
        
    if employee_id and employee_name:
        address = address_entry.get()
        contact_no = contact_no_entry.get()
        
        if contact_no and len(contact_no) != 10:
            tkinter.messagebox.showwarning(title="Error", message="Contact number should be 10 digits.")
            return
        
        joining_date = f"{joining_date_day.get()} {joining_date_month.get()} {joining_date_year.get()}"
        salary = salary_entry.get()
            
        print("Employee ID:", employee_id)
        print("Employee Name:", employee_name)
        print("Address:", address)
        print("Contact No:", contact_no)
        print("Joining Date:", joining_date)
        print("Salary:", salary)
        print("------------------------------------------")
            
        conn = sqlite3.connect('employee_data.db')
        table_create_query = '''CREATE TABLE IF NOT EXISTS Employee_Data 
                    (employee_id INTEGER , employee_name TEXT, address TEXT, 
                    contact_no TEXT, joining_date TEXT, salary REAL, primary key(employee_id))
        '''
        conn.execute(table_create_query)
     
        data_insert_query = '''INSERT INTO Employee_Data (employee_id, employee_name, address, 
        contact_no, joining_date, salary) VALUES (?, ?, ?, ?, ?, ?)'''
        data_insert_tuple = (employee_id, employee_name, address, contact_no, joining_date, salary)
        cursor = conn.cursor()
        cursor.execute(data_insert_query, data_insert_tuple)
        conn.commit()
        conn.close()
    else:
        tkinter.messagebox.showwarning(title="Error", message="Employee ID and name are required.")

def show_data():
    conn = sqlite3.connect('employee_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Employee_Data")
    rows = cursor.fetchall()
    conn.close()
    
    if rows:
        display_window = tkinter.Toplevel(window)
        display_window.title("Employee Data")
        
        frame = tkinter.Frame(display_window)
        frame.pack()
        
        for index, row in enumerate(rows):
            for col_index, value in enumerate(row):
                label = tkinter.Label(frame, text=value)
                label.grid(row=index, column=col_index, padx=5, pady=5, sticky="news")
    else:
        tkinter.messagebox.showinfo(title="No Data", message="No data available.")

window = tkinter.Tk()
window.title("Employee Data Management")

frame = tkinter.Frame(window)
frame.pack()

employee_info_frame = tkinter.LabelFrame(frame, text="Employee Information")
employee_info_frame.grid(row=0, column=0, padx=20, pady=10)

employee_id_label = tkinter.Label(employee_info_frame, text="Employee ID")
employee_id_label.grid(row=0, column=0)
employee_name_label = tkinter.Label(employee_info_frame, text="Employee Name")
employee_name_label.grid(row=2, column=0)

employee_id_entry = tkinter.Entry(employee_info_frame)
employee_name_entry = tkinter.Entry(employee_info_frame)
employee_id_entry.grid(row=1, column=0)
employee_name_entry.grid(row=3, column=0)

address_label = tkinter.Label(employee_info_frame, text="Address")
address_entry = tkinter.Entry(employee_info_frame)
address_label.grid(row=4, column=0)
address_entry.grid(row=5, column=0 )

contact_no_label = tkinter.Label(employee_info_frame, text="Contact No")
contact_no_entry = tkinter.Entry(employee_info_frame)
contact_no_label.grid(row=6, column=0)
contact_no_entry.grid(row=7, column=0)

joining_date_label = tkinter.Label(employee_info_frame, text="Joining Date")
joining_date_label.grid(row=8, column=0)

joining_date_day = ttk.Combobox(employee_info_frame, values=[str(i) for i in range(1, 32)])
joining_date_day.grid(row=9, column=0)
joining_date_day.set("Day")

joining_date_month = ttk.Combobox(employee_info_frame, values=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
joining_date_month.grid(row=9, column=1)
joining_date_month.set("Month")

joining_date_year = ttk.Combobox(employee_info_frame, values=[str(i) for i in range(1990, 2051)])
joining_date_year.grid(row=9, column=2)
joining_date_year.set("Year")

salary_label = tkinter.Label(employee_info_frame, text="Salary")
salary_label.grid(row=10, column=0)
salary_entry = tkinter.Entry(employee_info_frame)
salary_entry.grid(row=11, column=0)

for widget in employee_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

but_frame = tkinter.LabelFrame(frame, text=" ")
but_frame.grid(row=3, column=0, sticky="news", padx=20, pady=10)

submit_button = tkinter.Button(but_frame, text="Submit", command=submit)
submit_button.grid(row=3, column=0, sticky="news", padx=20, pady=10)

delete_button = tkinter.Button(but_frame, text="Delete Information", command=delete)
delete_button.grid(row=3, column=1, sticky="news", padx=20, pady=10)

show_button = tkinter.Button(but_frame, text="Show", command=show_data)
show_button.grid(row=3, column=2, sticky="news", padx=20, pady=10)

window.mainloop()
