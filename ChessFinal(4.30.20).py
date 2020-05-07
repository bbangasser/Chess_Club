import tkinter as tk
import math
import sqlite3

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
                  command=lambda: master.switch_frame(RecordMatch)).pack(fill="both", pady=3)
        tk.Button(self, text="Add a Player",
                  command=lambda: master.switch_frame(AddPlayer)).pack(fill="both", pady=3)
        tk.Button(self, text="Delete Player",
                  command=lambda: master.switch_frame(DeletePlayer)).pack(fill="both", pady=3)
        tk.Button(self, text="LeaderBoard",
                  command=lambda: master.switch_frame(LeaderBoard)).pack(fill="both", pady=3)
        tk.Button(self, text="Exit",
                  command=lambda: master.delete_frame()).pack(fill="both", pady=3)


# Recording a match/Determine player rating
class RecordMatch(tk.Frame):
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
        tk.Label(self, text="Winner?").grid(column=0, row=3, sticky=tk.E)
        tk.Checkbutton(self, text="Player 1", variable=self.player1winner).grid(column=1, row=3, sticky=tk.W)
        tk.Checkbutton(self, text="Player 2", variable=self.player2winner).grid(column=1, row=3, sticky=tk.E)

        # Create a enterButton
        tk.Button(self, text="Enter", command=self.enter).grid(column=1, row=4)

        # Create ExitButton
        tk.Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(StartPage)).grid(column=0, row=4)

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=3)

    # Enters the values into the database
    def enter(self):

        if self.player1winner.get() == 1:
            print("Player", self.player1ID.get(), "won!")
            print("The new ratings are: ", RecordMatch.CalculateNewRating(1000, 1000, 50, 1))
        else:
            print("Player", self.player2ID.get(), "won!")

    # Function to calculate Elo rating
    # K is a constant.
    # d determines whether
    # Player A wins or Player B.
    def CalculateNewRating(Ra, Rb, K, d):

        # To calculate the Winning
        # Probability of Player B
        Pb = 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (Ra - Rb) / 400))

        # To calculate the Winning
        # Probability of Player A
        Pa = 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (Rb - Ra) / 400))

        # Case -1 When Player A wins
        # Updating the Elo Ratings
        if d == 1:
            Ra = Ra + K * (1 - Pa)
            Rb = Rb + K * (0 - Pb)

        # Case -2 When Player B wins
        # Updating the Elo Ratings
        else:
            Ra = Ra + K * (0 - Pa)
            Rb = Rb + K * (1 - Pb)

        # print("Updated Ratings:-")
        # print("Ra =", round(Ra, 6), " Rb =", round(Rb, 6))

        return round(Ra, 6)


# Add player
class AddPlayer(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.firstName = tk.StringVar()
        self.lastName = tk.StringVar()
        self.address = tk.StringVar()
        self.phone = tk.StringVar()
        self.rating = tk.StringVar()

        # Create label, entry field for new player
        tk.Label(self, text="First Name").grid(column=0, row=0, sticky=tk.E)
        tk.Entry(self, width=25, textvariable=self.firstName).grid(column=1, row=0)

        tk.Label(self, text='Last Name').grid(column=0, row=1, sticky=tk.E)
        tk.Entry(self, width=25, textvariable=self.lastName).grid(column=1, row=1)

        tk.Label(self, text='Address').grid(column=0, row=2, sticky=tk.E)
        tk.Entry(self, width=25, textvariable=self.address).grid(column=1, row=2)

        tk.Label(self, text='Phone Number').grid(column=0, row=3, sticky=tk.E)
        tk.Entry(self, width=25, textvariable=self.phone).grid(column=1, row=3)

        tk.Label(self, text='Rating').grid(column=0, row=4, sticky=tk.E)
        tk.Entry(self, width=25, textvariable=self.rating).grid(column=1, row=4)

        # Create ExitButton
        tk.Button(self, text="Return",
                  command=lambda: master.switch_frame(StartPage)).grid(column=1, row=5, sticky=tk.W)

        # Create Enter Button
        tk.Button(self, text="Enter", command=self.appendPlayer).grid(column=1, row=5, sticky=tk.E)

        # configure grid
        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=3)

    def appendPlayer(self):
        # Get player's name and create table
        c.execute("""CREATE TABLE IF NOT EXISTS club_members (playerID INTEGER, firstName TEXT, lastName TEXT, 
                                                                    address TEXT, phone TEXT, rating TEXT); """)

        first_new = self.firstName.get()
        last_new = self.lastName.get()
        address_new = self.address.get()
        phone_new = self.phone.get()
        rating_new = self.rating.get()
        c.execute("SELECT MAX(playerID) FROM club_members;")
        maxPlayerID = c.fetchone()
        print(maxPlayerID)
        print("why")
        maxPlayerID = + 1
        print(maxPlayerID)

        print(first_new, last_new)
        sql = 'INSERT INTO club_members (playerID, firstName, lastName, address, phone, rating) VALUES (?, ?, ?, ?, ' \
              '                                                                                                 ?, ?) '

        c.execute(sql, (maxPlayerID, first_new, last_new, address_new, phone_new, rating_new))
        conn.commit()
        print(first_new)


# Delete player
class DeletePlayer(tk.Frame):
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
class LeaderBoard(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="LeaderBoard").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()


if __name__ == "__main__":
    conn = sqlite3.connect("club_members.db")
    c = conn.cursor()

    app = ChessProgram()
    app.title("Chess Program")
    app.geometry('400x200')
    app.mainloop()

    c.close()
    conn.close()
