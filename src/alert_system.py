from .user import User
from .topic import Topic
from .alert_scheduler import AlertScheduler

class AlertSystem:

    def __init__(self):
        #Clase principal, encargada de mantener la información sobre los usuarios, los tópicos, y las alertas,
        #coordinando las interacciones entre estos.
        self.users = {}
        self.topics = {}
        self.alerts = AlertScheduler()
        
    def register_user(self, user_name):
        #Agrega un usuario al sistema de alertas
        if user_name in self.users:
            raise Exception("User name already registered.")
        
        self.users[user_name] = User(user_name)
        return self.users[user_name]

    #Se entiende que un tópico debe existir en la Red Social para que un usuario pueda suscribirse.
    def register_topic(self, topic_name):
        #Agrega un tópico al sistema de alertas
        if topic_name not in self.topics:
            self.topics[topic_name] = Topic(topic_name)    
    
    def get_topic(self, topic_name):
        #Devuelve un objeto Topic a partir del nombre
        return self.topics[topic_name]
    
    def add_users_to_topic(self, topic_name, *users):
        #Registra un usuario como interesado en un tópico
        if topic_name not in self.topics:
            raise Exception("Unregistered Topic")
        
        for user_name in users:
            try:
                user = self.users[user_name]
            except:
                raise Exception("Unregistered User")
            
            self.topics[topic_name].add_user(user)
            user.add_topic(topic_name)

    def get_interested_users_in_topic(self, topic_name):
        return self.topics[topic_name].get_users()
    
    def send_alert(self, alert, user_name=None):
        #Envía una alerta a un usuario específico, 
        # o a todos aquellos que se hayan suscrito a un tópico.
        user_list = []
        
        if not user_name:
            user_list = self.get_interested_users_in_topic(alert.get_topic())
        else:
            user_list = [self.users[user_name]]
            if alert.topic not in user_list[0].get_topics():
                return None
        
        for user in user_list:
            user.receive_alert(alert)

        alert.add_receivers(user_list)

        self.alerts.add_alert(alert)

    def __get_unread_alerts(self, user_name=None, topic=None):
        #Consigue todas las alertas no leídas, por tópico o por usuario. 
        # No indica qué usuario recibió cada alerta, solo se espera que lo utilice el sistema internamente.
        if user_name:
            user = self.users[user_name]
            return user.get_unread_alerts()
        if topic:
            return self.alerts.get_unread_alerts(topic)
        
        return None
    
    def get_unread_alerts(self, user_name=None, topic=None):
        #Consigue todas las alertas no leídas de un usuario o de un tópico, 
        # aclarando en el segundo caso qué usuarios la recibieron.
        #Se entiende que es mejor aclarar a qué usuarios fue enviada en vez de si fue enviada a un usuario específico
        # ya que se asume que una notificación puede ser enviada a todos los usuarios, a uno solo específico
        #  o a varios usuarios de forma separada.
        if user_name and user_name not in self.users:
            raise Exception("Unregisted User")
        
        if topic and topic not in self.topics:
            raise Exception("Unregistered Topic")
        
        unread_alerts = self.__get_unread_alerts(user_name=user_name, topic=topic)

        if user_name:
            return unread_alerts
        
        alerts_with_receivers = []
        for unread_alert in unread_alerts:
            receivers_string = [receiver.name for receiver in unread_alert.sent_to]
            alerts_with_receivers.append((unread_alert, receivers_string))
        
        return alerts_with_receivers
