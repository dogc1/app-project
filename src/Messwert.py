class Messwert:
    """
    Repräsentiert einen Messwert mit Datum, Temperatur, Luftfeuchtigkeit, Luftdruck und Gerätenamen.

    Attribute:
        datum (str): Zeitpunkt der Messung.
        temperatur (float): Temperatur in °C.
        luftfeuchtigkeit (int): Luftfeuchtigkeit in Prozent.
        luftdruck (int): Luftdruck in hPa.
        geraetename (str): Name des verwendeten Geräts.
    """
    def __init__(self, datum, temperatur, luftfeuchtigkeit, luftdruck, geraetename):
        """
        Initialisiert eine neue Instanz der Messwert-Klasse.
        """
        self.datum = datum
        self.temperatur = temperatur
        self.luftfeuchtigkeit = luftfeuchtigkeit
        self.luftdruck = luftdruck
        self.geraetename = geraetename

    def __str__(self):
        """
        Gibt eine lesbare Darstellung des Messwerts zurück.
        """
        return (f"Messung vom {self.datum}:\n"
                f"Gerät: {self.geraetename}\n"
                f"Temperatur: {self.temperatur}°C\n"
                f"Luftfeuchtigkeit: {self.luftfeuchtigkeit}%\n"
                f"Luftdruck: {self.luftdruck} hPa")
