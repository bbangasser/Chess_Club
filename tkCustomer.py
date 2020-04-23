#Programmer: Brock Bangasser
#Program:
#Date: 

import tkinter as tk
from tkinter import ttk
#from builtins import True

class CustomerFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, padding="10 10 10 10")
        self.pack(fill=tk.BOTH, expand=True)
                  
        #Define string variable for the first entry field
        self.customerName = tk.StringVar()
        self.street = tk.StringVar()
        self.city = tk.StringVar()
        self.state = tk.StringVar()
        self.phone = tk.StringVar()
        
        
                  
        #Create a label, entry field, and a button
        ttk.Label(self, text="Customer Name").grid(column=0, row=0, sticky=tk.E)
        ttk.Entry(self, width=25, textvariable=self.customerName).grid(column=1, row=0)
        ttk.Button(self, text="Clear", command=self.clear).grid(column=2, row = 0)
        
        ttk.Label(self, text = 'Street').grid(column=0, row=1, sticky=tk.E)
        ttk.Entry(self, width=25, textvariable=self.street).grid(column=1, row=1)
        ttk.Button(self, text="Clear", command=self.clear).grid(column=2, row = 1)
        
        ttk.Label(self, text = 'City').grid(column=0, row = 2,sticky=tk.E)
        ttk.Entry(self, width = 25, textvariable=self.city).grid(column=1,row=2)
        ttk.Button(self, text="Clear", command=self.clear).grid(column=2, row = 2)
        
        ttk.Label(self, text = 'State').grid(column=0, row = 3,sticky=tk.E)
        ttk.Entry(self, width = 25, textvariable=self.state).grid(column=1,row=3)
        ttk.Button(self, text="Clear", command=self.clear).grid(column=2, row = 3)
        
        ttk.Label(self, text = 'Phone').grid(column=0, row = 4,sticky=tk.E)
        ttk.Entry(self, width = 25, textvariable=self.phone).grid(column=1,row=4)
        ttk.Button(self, text="Clear", command=self.clear).grid(column=2, row = 4)
        
        ttk.Button(self, text='Exit', command = self.destroy).grid(column=1, row = 5)
                  
        #Add padding to all child components
        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=3)
                      
    #Define the event listener for the Clear button
    def clear(self):
        print("Customer Name", self.customerName.get())
        self.customerName.set("")
       
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Customer")
    root.geometry("400x200")
    CustomerFrame(root)
    root.mainloop()