class Topic:

    def __init__(self, name):
        #Clase Topico. Tiene un nombre y una lista de aquellos usuarios interesados en el tema.
        self.name = name
        self.interested_users = []
    
    def add_user(self, user):
        self.interested_users.append(user)
    
    def get_users(self):
        return self.interested_users