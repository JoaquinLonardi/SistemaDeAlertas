from .alert_scheduler import AlertScheduler

class User:

    def __init__(self, name):
        #Clase usuario. Mantiene su nombre y una lista de los tópicos de interés.
        #El manejo de las alertas por leer se lo delega al AlertScheduler.
        self.name = name
        self.topics = []
        self.alerts = AlertScheduler()

    def add_topic(self, topic):
        #Agrega un tópico de interés.
        if topic not in self.topics:
            self.topics.append(topic)

    def get_topics(self):
        #Devuelve los tópicos en los que el usuario está interesado.
        return self.topics

    def receive_alert(self, alert):
        #Recibe una alerta.
        self.alerts.add_alert(alert)

    def read_next_alert(self):
        #Lee la siguiente alerta. 
        # El AlertScheduler se encarga de "marcarla" como leída sacandola de la pila de alertas por leer.
        # Devuelve la alerta leída.
        return self.alerts.get_next_alert()

    def get_unread_alerts(self):
        #Devuelve una lista de todas las alertas no leídas -ni expiradas- del usuario.
        return self.alerts.get_unread_alerts()