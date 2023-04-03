import unittest
from src.user import User
from src.alert_system import AlertSystem
from src.alert import Alert
from src.topic import Topic
from datetime import datetime

class AlertsTest(unittest.TestCase):

    def test_user_is_created_with_name(self):
        #Se crea un usuario con un nombre.

        user = User("Name Surname")
        self.assertEqual(user.name, "Name Surname")

    def test_topic_is_registered(self):
        #Se registra un tópico con un título.

        alert_system = AlertSystem()
        alert_system.register_topic("Sports")
        self.assertEqual(alert_system.get_topic("Sports").name, "Sports")

    def test_user_adds_topic(self):
        #Un usuario se suscribe a un tópico.
        alert_system = AlertSystem()
        user = "FootballFan123"
        user_obj = alert_system.register_user(user)
        alert_system.register_topic("Sports")
        alert_system.add_users_to_topic("Sports", user)
        user_topics = user_obj.get_topics()
        
        self.assertEqual("Sports" in user_topics, True)

    def test_user_receives_alert(self):
        #Un usuario se suscribe a un tópico, se envía una alerta para ese tópico, el usuario la recibe.
        alert_system = AlertSystem()
        alert = Alert("Argentina won the World Cup", "Argentina has just become winners of the World Cup after defeating France in penalties.", "Sports")
        user = "FootballFan123"
        user_obj = alert_system.register_user(user)
        alert_system.register_topic("Sports")
        alert_system.add_users_to_topic("Sports", user)
        alert_system.send_alert(alert)
        
        self.assertEqual(alert == user_obj.read_next_alert(), True)

    def test_send_alert_to_all_users(self):
        #Varios usuarios se suscriben a un tópico, se envía una alerta de ese tópico, todos los usuarios la reciben.
        alert_system = AlertSystem()
        alert = Alert("Argentina won the World Cup", "Argentina has just become winners of the World Cup after defeating France in penalties.", "Sports")
        user = "FootballFan123"
        user2 = "I_Love_Football"
        user3 = "FootballLov3r"
        user_obj = alert_system.register_user(user)
        user2_obj = alert_system.register_user(user2)
        user3_obj = alert_system.register_user(user3)

        alert_system.register_topic("Sports")
        alert_system.add_users_to_topic("Sports", user, user2, user3)
        alert_system.send_alert(alert)

        self.assertEqual(alert == user_obj.read_next_alert() and alert == user2_obj.read_next_alert() and alert == user3_obj.read_next_alert(), True)


    def test_send_alert_to_specific_user(self):
        # Si se envía una alerta a un usuario específico, otros usuarios no la reciben 
        # por más que estén suscritos al tópico
        alert_system = AlertSystem()
        alert = Alert("Argentina won the World Cup", "Argentina has just become winners of the World Cup after defeating France in penalties.", "Sports")
        user = "FootballFan123"
        user2 = "I_Love_Football"
        user3 = "FootballLov3r"

        user_obj = alert_system.register_user(user)
        user2_obj = alert_system.register_user(user2)
        user3_obj = alert_system.register_user(user3)
        alert_system.register_topic("Sports")
        alert_system.add_users_to_topic("Sports", user, user2, user3)
        alert_system.send_alert(alert, user)
        
        self.assertEqual(alert == user_obj.read_next_alert() and user2_obj.read_next_alert() == None, True)

    def test_send_alert_to_non_suscribed_user(self):
        # Si se envía una alerta a un usuario específico, pero este no está suscrito al tópico,
        # no la recibe.
        alert_system = AlertSystem()
        alert = Alert("Argentina won the World Cup", "Argentina has just become winners of the World Cup after defeating France in penalties.", "Sports")
        user = "FootballHater123"

        user_obj = alert_system.register_user(user)
        alert_system.register_topic("Sports")
        alert_system.send_alert(alert, user)
        
        self.assertEqual(user_obj.read_next_alert(), None)

    def test_user_reads_alerts_in_specified_order(self):
        # Cuando un usuario recibe varias alertas seguidas, se obtienen en el orden indicado por el punto 11.
        alert_system = AlertSystem()
        urgent_alert_1 = Alert("Argentina won the World Cup", "Argentina has just become winners of the World Cup after defeating France in penalties.", "Sports", urgent=True)
        urgent_alert_2 = Alert("Boca Jrs loses coach", "Boca Juniors announces the firing of their coach.", "Sports", urgent=True)
        informative_alert_1 = Alert("Man City beats Liverpool", "Manchester City beat Liverpool 4-1 today", "Sports")
        informative_alert_2 = Alert("River Plate mantain the top spot", "River Plate confirm their leadership on Liga Argentina, after beating Unión 1-0", "Sports")
        user = "FootballFan123"
        user_obj = alert_system.register_user(user)
        alert_system.register_topic("Sports")
        alert_system.add_users_to_topic("Sports", user)

        alert_system.send_alert(informative_alert_1, user)
        alert_system.send_alert(urgent_alert_2, user)
        alert_system.send_alert(informative_alert_2, user)
        alert_system.send_alert(urgent_alert_1, user)

        should_be_urgent_alert1 = user_obj.read_next_alert()
        should_be_urgent_alert2 = user_obj.read_next_alert()
        should_be_informative_alert1 = user_obj.read_next_alert()
        should_be_informative_alert2 = user_obj.read_next_alert()

        self.assertEqual(should_be_urgent_alert1 == urgent_alert_1 
                    and should_be_urgent_alert2 == urgent_alert_2 
                    and should_be_informative_alert1 == informative_alert_1
                    and should_be_informative_alert2 == informative_alert_2
                    , True)

    def test_getting_all_unread_alerts_from_user(self):
        #Consigo todas las alertas no leídas por un usuario y las recibo en el orden especificado
        alert_system = AlertSystem()
        urgent_alert_1 = Alert("Argentina won the World Cup", "Argentina has just become winners of the World Cup after defeating France in penalties.", "Sports", urgent=True)
        urgent_alert_2 = Alert("Boca Jrs loses coach", "Boca Juniors announces the firing of their coach.", "Sports", urgent=True)
        informative_alert_1 = Alert("Man City beats Liverpool", "Manchester City beat Liverpool 4-1 today", "Sports")
        informative_alert_2 = Alert("River Plate mantain the top spot", "River Plate confirm their leadership on Liga Argentina, after beating Unión 1-0", "Sports")
        user = "FootballFan123"
        
        alert_system.register_user(user)
        alert_system.register_topic("Sports")
        alert_system.add_users_to_topic("Sports", user)

        alert_system.send_alert(informative_alert_1, user)
        alert_system.send_alert(urgent_alert_2, user)
        alert_system.send_alert(informative_alert_2, user)
        alert_system.send_alert(urgent_alert_1, user)

        alerts = [urgent_alert_1, urgent_alert_2, informative_alert_1, informative_alert_2]

        self.assertEqual(alerts, alert_system.get_unread_alerts(user_name=user))

    def test_getting_all_unread_alerts_from_user_twice(self):
        #Consigo todas las alertas no leídas por un usuario dos veces seguidas
        #las dos veces me las devuelve en el mismo orden
        alert_system = AlertSystem()
        urgent_alert_1 = Alert("Argentina won the World Cup", "Argentina has just become winners of the World Cup after defeating France in penalties.", "Sports", urgent=True)
        urgent_alert_2 = Alert("Boca Jrs loses coach", "Boca Juniors announces the firing of their coach.", "Sports", urgent=True)
        informative_alert_1 = Alert("Man City beats Liverpool", "Manchester City beat Liverpool 4-1 today", "Sports")
        informative_alert_2 = Alert("River Plate mantain the top spot", "River Plate confirm their leadership on Liga Argentina, after beating Unión 1-0", "Sports")
        user = "FootballFan123"
        
        alert_system.register_user(user)
        alert_system.register_topic("Sports")
        alert_system.add_users_to_topic("Sports", user)

        alert_system.send_alert(informative_alert_1, user)
        alert_system.send_alert(urgent_alert_2, user)
        alert_system.send_alert(informative_alert_2, user)
        alert_system.send_alert(urgent_alert_1, user)

        #Orden esperado:    
        alerts = [urgent_alert_1, urgent_alert_2, informative_alert_1, informative_alert_2]

        first_try = (alerts == alert_system.get_unread_alerts(user_name=user))
        second_try = (alerts == alert_system.get_unread_alerts(user_name=user))
        self.assertEqual(first_try == True and second_try == True, True)

    def test_getting_all_unread_alerts_from_user_after_reading_one(self):
        #Si un usuario lee una alerta, no debe aparecer en la lista de alertas no leídas.
        alert_system = AlertSystem()
        urgent_alert_1 = Alert("Argentina won the World Cup", "Argentina has just become winners of the World Cup after defeating France in penalties.", "Sports", urgent=True)
        urgent_alert_2 = Alert("Boca Jrs loses coach", "Boca Juniors announces the firing of their coach.", "Sports", urgent=True)
        informative_alert_1 = Alert("Man City beats Liverpool", "Manchester City beat Liverpool 4-1 today", "Sports")
        informative_alert_2 = Alert("River Plate mantain the top spot", "River Plate confirm their leadership on Liga Argentina, after beating Unión 1-0", "Sports")
        user = "FootballFan123"
        
        user_obj = alert_system.register_user(user)
        alert_system.register_topic("Sports")
        alert_system.add_users_to_topic("Sports", user)

        alert_system.send_alert(informative_alert_1, user)
        alert_system.send_alert(urgent_alert_2, user)
        alert_system.send_alert(informative_alert_2, user)
        alert_system.send_alert(urgent_alert_1, user)

        #Lee la alerta
        user_obj.read_next_alert()

        alerts = [urgent_alert_2, informative_alert_1, informative_alert_2]
        self.assertEqual(alerts, alert_system.get_unread_alerts(user_name=user))

    def test_getting_unread_alerts_with_expired_alerts(self):
        #Si se consiguen todas las alertas no leídas, no se inclueyen las expiradas.
        alert_system = AlertSystem()
        urgent_alert_1 = Alert("Argentina won the World Cup", "Argentina has just become winners of the World Cup after defeating France in penalties.", "Sports", urgent=True)
        urgent_alert_2_expired = Alert("France won the World Cup", "France won the World Cup after defeating Brazil in the final", "Sports", urgent=True, exp_date=datetime(1998, 7, 7))
        informative_alert_1_expired = Alert("Diego Maradona retires","Diego Maradona announces he's abandoning professional football", "Sports", exp_date=datetime(1997,10,25))
        informative_alert_2 = Alert("River Plate mantain the top spot", "River Plate confirm their leadership on Liga Argentina, after beating Unión 1-0", "Sports")
        user = "FootballFan123"
        
        user_obj = alert_system.register_user(user)
        alert_system.register_topic("Sports")
        alert_system.add_users_to_topic("Sports", user)

        alert_system.send_alert(informative_alert_1_expired, user)
        alert_system.send_alert(urgent_alert_2_expired, user)
        alert_system.send_alert(informative_alert_2, user)
        alert_system.send_alert(urgent_alert_1, user)


        alerts = [urgent_alert_1, informative_alert_2]
        self.assertEqual(alerts, alert_system.get_unread_alerts(user_name=user))

    def test_getting_all_alerts_from_topic(self):
        #Obtiene todas las alertas de un tópico, por cada una se aclara qué usuarios la recibieron.
        alert_system = AlertSystem()
        urgent_alert_1 = Alert("Argentina won the World Cup", "Argentina has just become winners of the World Cup after defeating France in penalties.", "Sports", urgent=True)
        urgent_alert_2 = Alert("Boca Jrs loses coach", "Boca Juniors announces the firing of their coach.", "Sports", urgent=True)
        informative_alert_1 = Alert("Man City beats Liverpool", "Manchester City beat Liverpool 4-1 today", "Sports")
        informative_alert_2 = Alert("River Plate mantain the top spot", "River Plate confirm their leadership on Liga Argentina, after beating Unión 1-0", "Sports")
        alert1 = Alert("RCHP announce show in argentina", "The Red Hot Chili Peppers will be playing at Argentina", "Music")

        user = "FootballFan123"
        user2 = "FootballLov3r"
        alert_system.register_user(user)
        alert_system.register_user(user2)

        alert_system.register_topic("Sports")
        alert_system.add_users_to_topic("Sports", user)
        alert_system.add_users_to_topic("Sports", user2)

        alert_system.send_alert(informative_alert_1, user)
        alert_system.send_alert(urgent_alert_2)
        alert_system.send_alert(informative_alert_2, user)
        alert_system.send_alert(urgent_alert_1, user)

        expected_alerts = [(urgent_alert_1, [user]), (urgent_alert_2, [user, user2]), (informative_alert_1, [user]), (informative_alert_2, [user])]
        self.assertEqual(expected_alerts, alert_system.get_unread_alerts(topic="Sports"))
    
    def test_alert_with_expiration_date(self):
        alert_system = AlertSystem()
        alert = Alert("Argentina won the World Cup", "Argentina has just become winners of the World Cup after defeating France in penalties.", "Sports", exp_date=datetime(2023, 10, 10))
        expired_alert = Alert("France won the World Cup", "France won the World Cup after defeating Brazil in the final", "Sports", exp_date=datetime(1998, 7, 7))

        self.assertEqual(alert.is_expired() == False and expired_alert.is_expired() == True, True)

    def test_unregistered_user_raises_exception(self):
        alert_system = AlertSystem()
        user = "FootballLov3r"
        alert_system.register_topic("Sports")
        self.assertRaises(Exception, alert_system.add_users_to_topic, "Sports", user)

    def test_unregistered_topic_raises_exception(self):
        alert_system = AlertSystem()
        user = "FootballLov3r"
        alert_system.register_user(user)
        self.assertRaises(Exception, alert_system.add_users_to_topic, "Sports", user)

    def test_registering_user_twice_raises_exception(self):
        alert_system = AlertSystem()
        user = "ILoveFootball123"
        alert_system.register_user(user)
        self.assertRaises(Exception, alert_system.register_user, user)
    
    def test_getting_unread_alerts_from_unregisted_user_raises_exception(self):
        alert_system = AlertSystem()
        user = "ILoveFootball123"
        self.assertRaises(Exception, alert_system.get_unread_alerts, user)

    def test_getting_unread_alerts_from_unregistered_topic_raises_exception(self):
        alert_system = AlertSystem()
        topic = "Sports"
        self.assertRaises(Exception, alert_system.get_unread_alerts, None, topic)
if __name__ == '__main__':
    unittest.main()