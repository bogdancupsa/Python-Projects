from model.database import Database
from model.user import User

class UserRepository:
    def __init__(self):
        self.db = Database()

    def get_user(self, username):
        statement = "SELECT * FROM users WHERE username = ?"
        params = (username,)
        result = self.db.query(statement, params)
        if len(result) == 0:
            return None
        else:
            id, username, password, role = result[0]
            user = User(username, password, role)
            return user
        
    def get_all_cashiers(self):
        statement = "SELECT * FROM users WHERE role = \"cashier\""
        result = self.db.query(statement)
        cashiers = []
        for row in result:
            id, username, password, role = row
            cashier = User(username, password, role)
            cashiers.append(cashier)
        return cashiers

    def add_user(self, user):
        statement = "INSERT INTO users (username, password, role) VALUES (?, ?, ?)"
        params = (user.username, user.password, user.role)
        self.db.execute(statement, params)

    def update_user(self, user):
        statement = "UPDATE users SET password = ?, role = ? WHERE username = ?"
        params = (user.username, user.password, user.role)
        self.db.execute(statement, params)

    def delete_user(self, username):
        statement = "DELETE FROM users WHERE username = ?"
        params = (username,)
        self.db.execute(statement, params)