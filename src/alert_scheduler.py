from collections import deque

class AlertScheduler:
    def __init__(self):
        #Clase auxiliadora del sistema de alertas y del usuario, 
        # encargada de manejar correctamente el órden de las alertas
        # que se especificó en el punto 11. 
        self.urgent_alerts = deque()   # FIFO = QUEUE
        self.informative_alerts = deque() # LIFO = STACK

    def add_alert(self, alert):
        #Agrega una alerta.
        if alert.urgent:
            if alert not in self.urgent_alerts:
                self.urgent_alerts.append(alert)
        else:
            if alert not in self.informative_alerts:
                self.informative_alerts.append(alert)
    
    def get_next_alert(self):
        #Consigue la siguiente alerta a leer, priorizando las urgentes por sobre las informativas,
        # y utilizando LIFO en el caso de las urgentes, FIFO en el caso de las informativas.
        if len(self.urgent_alerts) > 0:
            return self.urgent_alerts.pop()
        
        if len(self.informative_alerts) > 0:
            return self.informative_alerts.popleft() 

        return None
    
    def get_unread_alerts(self, topic=None):
        #Devuelve una lista de alertas no leídas.
        alert_list = []

        while len(self.urgent_alerts) > 0:
            alert = self.urgent_alerts.pop()
            if not alert.is_expired():
                alert_list.append(alert)
        
        
        aux_alert_list = alert_list.copy()
        aux_alert_list.reverse()

        while len(self.informative_alerts) > 0:
            alert = self.informative_alerts.popleft()

            if not alert.is_expired():
                alert_list.append(alert)
                aux_alert_list.append(alert)

        for alert in aux_alert_list:
            self.add_alert(alert)
        if topic:
            return [alert for alert in alert_list if alert.topic == topic]
        
        return alert_list