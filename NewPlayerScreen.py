#Programmer: Brock Bangasser
#Program: Final
#Date: 4/27/20


import tkinter as tk
from tkinter import ttk
#from builtins import True

class PlayerFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, padding="10 10 10 10")
        self.pack(fill=tk.BOTH, expand=True)
                  
        #Define string variable for the first entry field
        self.playerName = tk.StringVar()
        self.firstName = tk.StringVar()
        self.lastName = tk.StringVar()
        self.address = tk.StringVar()
        self.phone = tk.StringVar()
        self.rating=tk.StringVar()
        
        
                  
        #Create a label, entry field, and a button
        ttk.Label(self, text="First Name").grid(column=0, row=0, sticky=tk.E)
        ttk.Entry(self, width=25, textvariable=self.firstName).grid(column=1, row=0)
        ttk.Button(self, text="Clear", command=self.clear).grid(column=2, row = 0)
        
        ttk.Label(self, text = 'Last Name').grid(column=0, row=1, sticky=tk.E)
        ttk.Entry(self, width=25, textvariable=self.lastName).grid(column=1, row=1)
        ttk.Button(self, text="Clear", command=self.clear).grid(column=2, row = 1)
        
        ttk.Label(self, text = 'Address').grid(column=0, row = 2,sticky=tk.E)
        ttk.Entry(self, width = 25, textvariable=self.address).grid(column=1,row=2)
        ttk.Button(self, text="Clear", command=self.clear).grid(column=2, row = 2)
        
        ttk.Label(self, text = 'Phone Number').grid(column=0, row = 3,sticky=tk.E)
        ttk.Entry(self, width = 25, textvariable=self.phone).grid(column=1,row=3)
        ttk.Button(self, text="Clear", command=self.clear).grid(column=2, row = 3)
        
        ttk.Label(self, text = 'Rating').grid(column=0, row = 4,sticky=tk.E)
        ttk.Entry(self, width = 25, textvariable=self.rating).grid(column=1,row=4)
        ttk.Button(self, text="Clear", command=self.clear).grid(column=2, row = 4)
        
        ttk.Button(self, text='Exit', command = self.destroy).grid(column=1, row = 5)
                  
        #Add padding to all child components
        for child in self.winfo_children():
            child.grid_configure(padx=8, pady=6)
                      
    #Define the event listener for the Clear button
    def clear(self):
        print("Player Name", self.firstName.get())
        self.playerName.set("")
       
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Add Player")
    root.geometry("400x200")
    PlayerFrame(root)
    root.mainloop()