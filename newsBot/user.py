class User:
    def __init__(self):
        self.chatId = None
        self.name = None
        self.email = None
        self.age = None
        self.team = None


    def __str__(self) -> str:
        return f'Name: {self.name} - Email: {self.email} - Age: {self.age} - Team: {self.team} - ChatId: {self.chatId}'
