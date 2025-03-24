class Messwert:
    def __init__(self, datum, temperatur, luftfeuchtigkeit, luftdruck, geraetename):
        self.datum = datum
        self.temperatur = temperatur
        self.luftfeuchtigkeit = luftfeuchtigkeit
        self.luftdruck = luftdruck
        self.geraetename = geraetename

    def __str__(self):
        return (f"Messung vom {self.datum}:\n"
                f"Gerät: {self.geraetename}\n"
                f"Temperatur: {self.temperatur}°C\n"
                f"Luftfeuchtigkeit: {self.luftfeuchtigkeit}%\n"
                f"Luftdruck: {self.luftdruck} hPa")
