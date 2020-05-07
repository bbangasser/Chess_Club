#Stephen Kasahara
#SQL update

import tkinter as tk
import math
import sqlite3
# Import tabulate for the LeaderBoard format
from tabulate import tabulate

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

    # destroy root frame
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

        # Define StringVer object
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
        tk.Button(self, text="Enter", command=self.enter).grid(column=1, row=5)

        # Create ExitButton
        tk.Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(StartPage)).grid(column=0, row=5)

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=3)

    # Enters the values into the database
    def enter(self):

        # Get player ID's
        id1 = self.player1ID.get()
        id2 = self.player2ID.get()

        # Collect player rating
        sql = '''SELECT rating FROM chess_players WHERE playerID = ?'''

        c.execute(sql, (id1,))
        conn.commit()

        # Change ratings into a float variable
        rating1 = c.fetchone()
        x = ''.join(map(str, rating1))
        new_rating1 = float(x)

        c.execute(sql, (id2,))
        conn.commit()

        rating2 = c.fetchone()
        y = ''.join(map(str, rating2))
        new_rating2 = float(y)

        # Calculate Winner
        if self.player1winner.get() == 1:
            if self.player2winner.get() == 1:
                # Calculate Tie
                print("Both players tie!")
            else:
                # Player 1 Wins
                self.winnerID = self.player1ID
                RecordMatch.appendMatch(self)
                RecordMatch.CalculateNewRating(self, new_rating1, new_rating2, 50, 1)
        else:
            # Player 2 Wins
            self.winnerID = self.player2ID
            RecordMatch.appendMatch(self)
            RecordMatch.CalculateNewRating(self, new_rating1, new_rating2, 50, 0)

        self.player1ID.set("")
        self.player2ID.set("")
        self.player1winner.set(0)
        self.player2winner.set(0)

    # Function to calculate Elo rating
    # K is a constant.
    # d determines whether
    # Player A wins or Player B.
    def CalculateNewRating(self, Ra, Rb, K, d):

        # To calculate the Winning
        # Probability of Player B
        Pb = 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (Ra - Rb) / 400))

        # To calculate the Winning
        # Probability of Player A
        Pa = 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (Rb - Ra) / 400))

        # Case 1 When Player A wins
        # Updating the Elo Ratings
        if d == 1:
            Ra = Ra + K * (1 - Pa)
            Rb = Rb + K * (0 - Pb)

        # Case 2 When Player B wins
        # Updating the Elo Ratings
        elif d == 0:
            Ra = Ra + K * (0 - Pa)
            Rb = Rb + K * (1 - Pb)

        # Update SQL with player's ratings
        sql = '''UPDATE chess_players SET rating = ? WHERE playerID =?'''
        # Updating player 1's rating
        c.execute(sql, (round(Ra), self.player1ID.get()))
        conn.commit()
        # Updating player 2's rating
        c.execute(sql, (round(Rb), self.player2ID.get()))
        conn.commit()

    def appendMatch(self):
        # Get player's name and create match table
        co.execute(""" CREATE TABLE IF NOT EXISTS chess_matches (
                                        matchID INTEGER Primary Key,
                                        player1ID character(20) NOT NULL,
                                        player2ID character(20) NOT NULL,
                                        winnerID character(20) NOT NULL
                                    ); """)

        # Get player ID
        player1ID_new = self.player1ID.get()
        player2ID_new = self.player2ID.get()
        winnerID_new = self.winnerID.get()
        # Insert into SQL
        sql = 'INSERT INTO chess_matches (player1ID, player2ID, winnerID) VALUES ( ?, ?, ?) '
        # Execute SQL
        co.execute(sql, (player1ID_new, player2ID_new, winnerID_new))
        match_conn.commit()


# Add player
class AddPlayer(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # Define StringVar objects
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
        # Create player table and add players to the database
        c.execute(""" CREATE TABLE IF NOT EXISTS chess_players (
                                        playerID INTEGER Primary Key,
                                        firstName character(20) NOT NULL,
                                        lastName character(20) NOT NULL,
                                        address character(50) NOT NULL,
                                        phone character(12) NOT NULL,
                                        rating integer(4) NOT NULL,
                                        active boolean NOT NULL
                                    ); """)
        # Get player data
        first_new = self.firstName.get()
        last_new = self.lastName.get()
        address_new = self.address.get()
        phone_new = self.phone.get()
        rating_new = int(self.rating.get())
        active_new = True

        # Insert into the SQL
        sql = 'INSERT INTO chess_players (firstName, lastName, address, phone, rating, active) VALUES (?, ?, ?, ?, ' \
              '                                                                                                 ?, ?) '
        c.execute(sql, (first_new, last_new, address_new, phone_new, rating_new, active_new))
        conn.commit()

        # Reset text boxes
        self.firstName.set("")
        self.lastName.set("")
        self.address.set("")
        self.phone.set("")
        self.rating.set("")


# Delete player
class DeletePlayer(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Delete Player").grid(column=1, row=0, sticky=tk.N)

        # Define StringVar object
        self.deletePlayerID = tk.StringVar()

        # Create a Label and Text Entry for player ID
        tk.Label(self, text="Player's ID").grid(column=0, row=1, sticky=tk.W, columnspan=1)
        tk.Entry(self, width=25, textvariable=self.deletePlayerID).grid(column=1, row=1)

        # Create a DeleteButton
        tk.Button(self, text="Enter", command=self.delete).grid(column=1, row=4)

        # Create ExitButton
        tk.Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(StartPage)).grid(column=0, row=4)

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=3)

    # Deletes player from database
    def delete(self):
        # Get player ID and set active to false
        id = int(self.deletePlayerID.get())
        active = False

        # Update database to set active to False
        sql = '''UPDATE chess_players SET active = ? WHERE playerID =?'''
        c.execute(sql, (active, id))
        conn.commit()

        self.deletePlayerID.set("")

# LeaderBoard
class LeaderBoard(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="LeaderBoard").pack(side="top", fill="x", pady=10)

        # Select players who are active
        query = "SELECT * FROM chess_players WHERE active = ?"
        c.execute(query, (True,))
        database = c.fetchall()

        # Display and format players database
        print(tabulate(database, headers=['ID', 'FirstName', 'LastName', 'Address', 'Phone', 'Rating', 'Active'],
                       tablefmt='psql'))

        tk.Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()


if __name__ == "__main__":
    conn = sqlite3.connect("chess_players.db")
    match_conn = sqlite3.connect("chess_matches.db")
    c = conn.cursor()
    co = match_conn.cursor()

    app = ChessProgram()
    app.title("Chess Program")
    app.geometry('400x200')
    app.mainloop()

    # close player database
    c.close()
    conn.close()

    # close the match database
    co.close()
    match_conn.close()
