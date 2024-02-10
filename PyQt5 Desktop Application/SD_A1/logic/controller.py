from model.user_repository import UserRepository
from model.show_repository import ShowRepository
from model.show import Show
from model.user import User

class Controller:
    def __init__(self):
        self.user_repository = UserRepository()
        self.show_repository = ShowRepository()

    def get_user(self, username):
        return self.user_repository.get_user(username)

    def get_all_shows(self):
        return self.show_repository.get_all_shows()
    
    def get_all_cashiers(self):
        return self.user_repository.get_all_cashiers()

    def add_show(self, name, singer, date, num_tickets, genre):
        show = Show(name, singer, date, num_tickets, genre)
        self.show_repository.add_show(show)

    def add_user(self, username, password, role):
        user = User(username, password, role)
        self.user_repository.add_user(user)

    def update_show(self, name, singer, date, num_tickets, genre):
        show = Show(name, singer, date, num_tickets, genre)
        self.show_repository.update_show(show)

    def delete_show(self, name):
        self.show_repository.delete_show(name)

    def delete_user(self, name):
        self.user_repository.delete_user(name)
