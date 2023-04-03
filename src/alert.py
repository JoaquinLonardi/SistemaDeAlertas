from datetime import datetime

class Alert:
    def __init__(self, title, content, topic, exp_date=None, urgent=False):
        #Clase Alerta, que además del título, contenido, y tópico de la alerta,
        # cuenta con una fecha de expiración opcional y la posibildad de ser marcada como urgente.
        self.title = title
        self.content = content
        self.topic = topic
        self.exp_date = exp_date
        self.urgent = urgent
        self.sent_to = []

    def get_topic(self):
        return self.topic
    
    def is_expired(self):
        if not self.exp_date or self.exp_date > datetime.now():
            return False

        return True
    
    def add_receivers(self, user_list):
        for user in user_list:
            self.sent_to.append(user)
        
