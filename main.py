from src.alert_system import AlertSystem
from src.alert import Alert
from src.user import User
from datetime import datetime

# Para testear, se puede ejecutar por línea de comandos ("python -i main.py")
# y utilizar las siguientes funciones para probar funcionalidades:
# Registrar Usuario: alert_system.register_user("Nombre")
# Registrar Tópico: alert_system.register_topic("Nombre")
# Suscribir usuario a topico: alert_system.add_users_to_topic("Nombre Topico", "Nombre Usuario 1", ..., "Nombre usuario N")
# Crear alerta = Alert("Titulo", "Contenido", "Topico", exp_date=datetime(2022, 7, 7) | None, urgent = True | False) 
# Enviar alerta = alert_system.send_alert(objeto_alerta, nombre_usuario | None) (Si se utiliza None se envía a todos los suscriptores del tópico)
# Leer siguiente alerta (usuario) = user.read_next_alert()
# Obtener alertas no leidas = alert_system.get_unread_alerts(user_name | None, topic | None)
alert_system = AlertSystem()    

user = alert_system.register_user("TestUser")
alert_system.register_topic("TestTopic")
alert_system.add_users_to_topic("TestTopic", "TestUser")
test_alert = Alert("TestAlert", "This is a TestAlert", "TestTopic", datetime(2024,10,10), True)
alert_system.send_alert(test_alert, "TestUser")
user.read_next_alert()

unread_alerts = alert_system.get_unread_alerts(user_name="TestUser")
#unread_alerts debería estar vacía

test_alert1 = Alert("TestAlert1", "This is a TestAlert", "TestTopic", datetime(2024,10,10), True)
test_alert2 = Alert("TestAlert2", "This is a TestAlert", "TestTopic", datetime(2024,10,10), False)
test_alert3 = Alert("TestAlert3", "This is a TestAlert", "TestTopic", datetime(2024,10,10), True)
alert_system.send_alert(test_alert1, "TestUser")
alert_system.send_alert(test_alert2, "TestUser")
alert_system.send_alert(test_alert3, "TestUser")

unread_alerts2 = alert_system.get_unread_alerts(user_name="TestUser")
unread_alerts2 = [unread_alert.title for unread_alert in unread_alerts2]
#unread_alerts2 debería ser [TestAlert3, TestAlert1, TestAlert2]