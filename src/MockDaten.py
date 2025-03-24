from datetime import datetime, timedelta
import random
from Messwert import Messwert


class MockupDaten: 
    """
    Klasse zur Generierung von Mock-Daten für die Diagramme.
    Methoden:
        greateDatas(): Generiert eine Liste von 30 zufälligen Messwerten.
    """
    def greateDatas(self):
        """
        Generiert 30 zufällige Messwerte mit festen Zeitintervallen.

        Returns:
            tuple: Gerätename und Liste von Messwerten.
        """
        startzeitpunkt = datetime(2025, 3, 23, 8, 0)  # Beginn um 08:00 Uhr
        geraetename = "Sensor A"

        # Liste für die Messungen
        messungen = []

        # Generierung von 30 Datensätzen
        for i in range(30):
            datum = startzeitpunkt + timedelta(minutes=30 * i)
            temperatur = round(random.uniform(15.0, 25.0), 1)  # Zufällige Temperatur zwischen 15 und 25°C
            luftfeuchtigkeit = random.randint(30, 60)          # Zufällige Luftfeuchtigkeit zwischen 30 und 60%
            luftdruck = random.randint(1000, 1020)             # Zufälliger Luftdruck zwischen 1000 und 1020 hPa
            messungen.append(Messwert(datum.strftime("%d.%m.%Y %H:%M"), temperatur, luftfeuchtigkeit, luftdruck, geraetename))

        return geraetename, messungen