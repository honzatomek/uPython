
# Wemos D1 Mini Pinout
class WemosD1Mini:
    def __init__(self):
        self.A0 = 0
        self.D0 = 16
        self.D1 = 5
        self.D2 = 4
        self.D3 = 0
        self.D4 = 2
        self.D5 = 14
        self.D6 = 12
        self.D7 = 13
        self.D8 = 15
        self.RX = 3
        self.TX = 1

        self.ADC = self.A0
        self.WAKE = self.D0
        self.SCL = self.D1
        self.SDA = self.D2
        self.FLASH = self.D3
        self.LED = self.D4
        self.SCLK = self.D5
        self.MISO = self.D6
        self.MOSI = self.D7
        self.CS = self.D8
