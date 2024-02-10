from model.database import Database
from model.show import Show

class ShowRepository:
    def __init__(self):
        self.db = Database()

    def get_all_shows(self):
        statement = "SELECT * FROM shows"
        result = self.db.query(statement)
        shows = []
        for row in result:
            name, singer, date, num_tickets, genre = row
            show = Show(name, singer, date, num_tickets, genre)
            shows.append(show)
        return shows
    
    def add_show(self, show):
        statement = "INSERT INTO shows (name, singer, date, num_tickets, genre) VALUES (?, ?, ?, ?, ?)"
        params = (show.name, show.singer, show.date, show.num_tickets, show.genre)
        self.db.execute(statement, params)

    def update_show(self, show):
        statement = "UPDATE shows SET singer = ?, date = ?, num_tickets = ?, genre = ? WHERE name = ?"
        params = (show.singer, show.date, show.num_tickets, show.genre, show.name)
        self.db.execute(statement, params)

    def delete_show(self, name):
        statement = "DELETE FROM shows WHERE name = ?"
        params = (name,)
        self.db.execute(statement, params)

    def get_show_by_name(self, name):
        statement = "SELECT * FROM shows WHERE name = ?"
        params = (name,)
        result = self.db.query(statement, params)
        if len(result) == 0:
            return None
        else:
            name, singer, date, num_tickets, genre = result[0]
            show = Show(name, singer, date, num_tickets, genre)
            return show
