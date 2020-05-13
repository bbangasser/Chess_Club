import tkinter as tk
import math
import sqlite3

LARGE_FONT = ("Verdana", 15)
BOLD_FONT = ("Verdana", 7, "bold underline")

''' This program is created to be used by chess clubs. 
    This program uses the ELO rating system to determine 
    the skill level of players as well as rate the members 
    after each match. This program also stores player data in an SQL file 
    so that the data can be updated and is easily accessible. The users are able to 
    enter in their personal information, record a match, delete their information,
    as well as look up chess Matches and current members.
'''


class ChessProgram(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)

    # Switch Frames
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
        tk.Label(self, text="Chess Club Program", font=LARGE_FONT).pack(side="top", fill="x", pady=20)

        tk.Button(self, text="Record a Match",
                  command=lambda: master.switch_frame(RecordMatch)).pack(fill="both", pady=10)
        tk.Button(self, text="Add a Player",
                  command=lambda: master.switch_frame(AddPlayer)).pack(fill="both", pady=10)
        tk.Button(self, text="Delete Player",
                  command=lambda: master.switch_frame(DeletePlayer)).pack(fill="both", pady=10)
        tk.Button(self, text="Member List",
                  command=lambda: master.switch_frame(LeaderBoard)).pack(fill="both", pady=10)
        tk.Button(self, text='Match History',
                  command=lambda: master.switch_frame(MatchHistory)).pack(fill='both', pady=10)
        tk.Button(self, text="Exit",
                  command=lambda: master.delete_frame()).pack(fill="both", pady=8)


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

    # Enters the match results into the database
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
                self.winnerID = 0
                RecordMatch.appendMatch(self)
                RecordMatch.CalculateNewRating(self, new_rating1, new_rating2, 50, .5)

            else:
                # Player 1 Wins
                self.winnerID = 1
                RecordMatch.appendMatch(self)
                RecordMatch.CalculateNewRating(self, new_rating1, new_rating2, 50, 1)
        else:
            # Player 2 Wins
            self.winnerID = 2
            RecordMatch.appendMatch(self)
            RecordMatch.CalculateNewRating(self, new_rating1, new_rating2, 50, 0)

        self.player1ID.set("")
        self.player2ID.set("")
        self.player1winner.set(0)
        self.player2winner.set(0)

    # Function to calculate new (Elo system) rating
    # K is a constant.
    # d denotes whether Player A wins or Player B or the match ended in a tie.
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

        elif d == .5:
            Ra = Ra + (K * (1 - Pa) + K * (0 - Pa)) / 2
            Rb = Rb + (K * (0 - Pb) + K * (1 - Pb)) / 2

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
        winnerID_new = self.winnerID
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

    # Create player table and add players to the database
    def appendPlayer(self):
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

    # Deletes player from database(Sets his active status to False)
    def delete(self):
        # Get player ID and set active to false
        id = int(self.deletePlayerID.get())
        active = False

        # Update database to set active to False
        sql = '''UPDATE chess_players SET active = ? WHERE playerID =?'''
        c.execute(sql, (active, id))
        conn.commit()

        self.deletePlayerID.set("")


# LeaderBoard(lists active members of the chess club and their ratings)
class LeaderBoard(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Member List").grid(column=3, row=0)

        # Select players who are active
        query = "SELECT * FROM chess_players WHERE active = ?"
        c.execute(query, (True,))
        database = c.fetchall()

        # Create Labels
        tk.Label(self, text='ID', font=BOLD_FONT).grid(column=0, row=1)
        tk.Label(self, text='First Name', font=BOLD_FONT).grid(column=1, row=1)
        tk.Label(self, text='Last Name', font=BOLD_FONT).grid(column=2, row=1)
        tk.Label(self, text='Address', font=BOLD_FONT).grid(column=3, row=1)
        tk.Label(self, text='Phone', font=BOLD_FONT).grid(column=4, row=1)
        tk.Label(self, text='Rating', font=BOLD_FONT).grid(column=5, row=1)

        print_id = ''
        print_fName = ''
        print_lName = ''
        print_addreses = ''
        print_phone = ''
        print_rating = ''

        # print data
        for data in database:
            print_id += str(data[0]) + '\n'
            print_fName += str(data[1]) + '\n'
            print_lName += str(data[2]) + '\n'
            print_addreses += str(data[3]) + '\n'
            print_phone += str(data[4]) + '\n'
            print_rating += str(data[5]) + '\n'

        tk.Label(self, text=print_id).grid(column=0, row=2)
        tk.Label(self, text=print_fName).grid(column=1, row=2)
        tk.Label(self, text=print_lName).grid(column=2, row=2)
        tk.Label(self, text=print_addreses).grid(column=3, row=2)
        tk.Label(self, text=print_phone).grid(column=4, row=2)
        tk.Label(self, text=print_rating).grid(column=5, row=2)

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=3)

        # Return to home Menu
        tk.Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(StartPage)).grid(column=3, row=3)

# Match record (Keeps record of the chess matches and whether they won, lost or tied)
class MatchHistory(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Match History").grid(column=2, row=0)

        # Select data from SQL
        query = 'SELECT * FROM chess_matches'

        co.execute(query, )
        database = co.fetchall()

        # Create Labels
        tk.Label(self, text='Match Number', font=BOLD_FONT).grid(column=0, row=1)
        tk.Label(self, text='Player 1 ID', font=BOLD_FONT).grid(column=1, row=1)
        tk.Label(self, text='Player 2 ID', font=BOLD_FONT).grid(column=2, row=1)
        tk.Label(self, text='Winner', font=BOLD_FONT).grid(column=3, row=1)

        print_match_id = ''
        print_player1 = ''
        print_player2 = ''
        print_winner = ''

        # Print Match Data
        for data in database:
            print_match_id += str(data[0]) + '\n'
            print_player1 += str(data[1]) + '\n'
            print_player2 += str(data[2]) + '\n'
            print_winner += str(data[3]) + '\n'

        tk.Label(self, text=print_match_id).grid(column=0, row=2)
        tk.Label(self, text=print_player1).grid(column=1, row=2)
        tk.Label(self, text=print_player2).grid(column=2, row=2)
        tk.Label(self, text=print_winner).grid(column=3, row=2)

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=3)

        # Return to Menu
        tk.Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(StartPage)).grid(column=2, sticky=tk.S, row=3)


if __name__ == "__main__":
    # Open databases
    conn = sqlite3.connect("chess_players.db")
    match_conn = sqlite3.connect("chess_matches.db")
    c = conn.cursor()
    co = match_conn.cursor()

    app = ChessProgram()
    app.title("Chess Program")
    app.geometry('650x400')
    app.mainloop()

    # close player database
    c.close()
    conn.close()

    # close the match database
    co.close()
    match_conn.close()
