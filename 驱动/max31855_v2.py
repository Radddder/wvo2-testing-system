import ustruct


class MAX31855:
    """
    Driver for the MAX31855 thermocouple amplifier.


    MicroPython example::

        import max31855
        from machine import SPI, Pin

        spi = SPI(1, baudrate=1000000)
        cs = Pin(15, Pin.OUT)
        s = max31855.MAX31855(spi, cs)
        print(s.read())

    """
    def __init__(self, spi, cs):
        self.spi = spi
        self.cs = cs
        self.data = bytearray(4)

    def read(self):

        self.cs.off()
        try:
            self.spi.readinto(self.data)
        finally:
            self.cs.on()
        # The data has this format:
        # 00 --> OC fault
        # 01 --> SCG fault
        # 02 --> SCV fault
        # 03 --> reserved
        # 04 -. --> LSB
        # 05  |
        # 06  |
        # 07  |
        #      > reference
        # 08  |
        # 09  |
        # 10  |
        # 11  |
        # 12  |
        # 13  |
        # 14  | --> MSB
        # 15 -' --> sign
        #
        # 16 --> fault
        # 17 --> reserved
        # 18 -.  --> LSB
        # 19   |
        # 20   |
        # 21   |
        # 22   |
        # 23   |
        #       > temp
        # 24   |
        # 25   |
        # 26   |
        # 27   |
        # 28   |
        # 29   |
        # 30   | --> MSB
        # 31  -' --> sign
        judge = 0
        if self.data[3] & 0x01:
            #raise RuntimeError("thermocouple not connected")
            judge = judge + 1
        if self.data[3] & 0x02:
            #raise RuntimeError("short circuit to ground")
            judge = judge + 1
        if self.data[3] & 0x04:
            #raise RuntimeError("short circuit to power")
            judge = judge + 1
        if self.data[1] & 0x01:
            #raise RuntimeError("faulty reading")
            judge = judge + 1
            
        if judge:
            return "error"
        else:
            temp, refer = ustruct.unpack('>hh', self.data)
            refer >>= 4
            temp >>= 2
            return temp / 4

