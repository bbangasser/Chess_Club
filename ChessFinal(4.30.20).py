  
import tkinter as tk

LARGE_FONT = ("Verdana", 12)


class ChessProgram(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

    # exit frame
    def delete_frame(self):
        self._frame.destroy()
        app.destroy()


# Main Menu
class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Chess Club Program", font=LARGE_FONT).pack(side="top", fill="x", pady=10)

        tk.Button(self, text="Record a Match",
                  command=lambda: master.switch_frame(PageOne)).pack(fill="both", pady=3)
        tk.Button(self, text="Add a Player",
                  command=lambda: master.switch_frame(PageTwo)).pack(fill="both", pady=3)
        tk.Button(self, text="Delete Player",
                  command=lambda: master.switch_frame(PageThree)).pack(fill="both", pady=3)
        tk.Button(self, text="LeaderBoard",
                  command=lambda: master.switch_frame(PageFour)).pack(fill="both", pady=3)
        tk.Button(self, text="Exit",
                  command=lambda: master.delete_frame()).pack(fill="both", pady=3)


# Recording a match
class PageOne(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # defining variables
        self.player1ID = tk.StringVar()
        self.player2ID = tk.StringVar()
        self.player1winner = tk.IntVar()
        self.player2winner = tk.IntVar()

        tk.Label(self, text="Record the Match").grid(column=1, row=0, sticky=tk.N)

        # Create text entries for players
        tk.Label(self, text="Player One ID").grid(column=0, row=1, sticky=tk.E)
        tk.Entry(self, width=25, textvariable=self.player1ID).grid(column=1, row=1)
        tk.Label(self, text="Player Two ID").grid(column=0, row=2, sticky=tk.E)
        tk.Entry(self, width=25, textvariable=self.player2ID).grid(column=1, row=2)
        tk.Label(self,text="Winner?").grid(column=0, row =3, sticky=tk.E)
        tk.Checkbutton(self, text="Player 1", variable=self.player1winner).grid(column=1,row=3, sticky=tk.W)
        tk.Checkbutton(self, text="Player 2", variable=self.player2winner).grid(column=1,row=3 , sticky = tk.E)

        # Create a enterButton
        tk.Button(self, text="Enter", command=self.enter).grid(column=1, row=4)

        # Create ExitButton
        tk.Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(StartPage)).grid(column=0, row=4)

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=3)

    # Enters the values into the database
    def enter(self):
        print(self.player1ID.get(), " was entered!")
        print(self.player2ID.get(), " was entered!")


# Add player
class PageTwo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.firstName = tk.StringVar()
        self.lastName = tk.StringVar()
        self.address = tk.StringVar()
        self.phone = tk.StringVar()
        self.rating=tk.StringVar()
        
        
                  
        #Create label, entry field for new player
        tk.Label(self, text="First Name").grid(column=0, row=0, sticky=tk.E)
        tk.Entry(self, width=25, textvariable=self.firstName).grid(column=1, row=0)
       
        
        tk.Label(self, text = 'Last Name').grid(column=0, row=1, sticky=tk.E)
        tk.Entry(self, width=25, textvariable=self.lastName).grid(column=1, row=1)
       
        
        tk.Label(self, text = 'Address').grid(column=0, row = 2,sticky=tk.E)
        tk.Entry(self, width = 25, textvariable=self.address).grid(column=1,row=2)
     
        tk.Label(self, text = 'Phone Number').grid(column=0, row = 3,sticky=tk.E)
        tk.Entry(self, width = 25, textvariable=self.phone).grid(column=1,row=3)
        
        tk.Label(self, text = 'Rating').grid(column=0, row = 4,sticky=tk.E)
        tk.Entry(self, width = 25, textvariable=self.rating).grid(column=1,row=4)
        
        # Create ExitButton
        tk.Button(self, text="Return",
                  command=lambda: master.switch_frame(StartPage)).grid(column=1, row=5, sticky=tk.W)
                  
        #Create Enter Button
        tk.Button(self, text="Enter").grid(column = 1, row=5, sticky=tk.E)
        
        
        #configure grid
        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=3)
            
        
# Delete player
class PageThree(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Delete Player").grid(column=1, row=0, sticky=tk.N)

        # define variable
        self.deletedPlayerID = tk.StringVar()

        # Create a Label and Text Entry for player ID
        tk.Label(self, text="Player's ID").grid(column=0, row=1, sticky=tk.W, columnspan=1)
        tk.Entry(self, width=25, textvariable=self.deletedPlayerID).grid(column=1, row=1)

        # Create a DeleteButton
        tk.Button(self, text="Enter", command=self.deleted).grid(column=1, row=4)

        # Create ExitButton
        tk.Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(StartPage)).grid(column=0, row=4)

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=3)

    # Deletes player from database
    def deleted(self):
        print(self.deletedPlayerID.get(), "was deleted!")
        self.deletedPlayerID.set("")


# LeaderBoard
class PageFour(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="LeaderBoard").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()


if __name__ == "__main__":
    app = ChessProgram()
    app.title("Chess Program")
    app.geometry('400x200')
    app.mainloop()