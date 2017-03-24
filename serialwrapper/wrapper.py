import serial
import time


class MSerial():
    """
        MSerial is wrapper around serial.Serial connector with some basic communication methods
    """
    instance = None

    def __init__(self, device='/dev/ttyUSB0', baud_rate=9600, timeout=1.0):
        if not MSerial.instance:
            MSerial.instance = MSerial.__OnlyOne(device, baud_rate, timeout)
        else:
            self.instance.device = device
            self.instance.baud= baud_rate
            self.instance.timeout = timeout

    def __getattr__(self, item):
        return getattr(self.instance, item)

    class __OnlyOne:
        serial = None
        device = None
        baud = None
        timeout = None
        separator = ';'

        init_sleep = 1.0
        cmd_sleep = 0.3

        r_val = 0
        g_val = 0
        b_val = 0

        def __init__(self, device='/dev/ttyUSB0', baud_rate=9600, timeout=1.0):
            self.baud = baud_rate
            self.device = device
            self.timeout = timeout

            self.connect()

        def connect(self):
            """
            `connect` construct new serial connection and prepare board to work
            :return: None
            """
            self.serial = self._make_connect()
            self.serial.flushInput()
            try:
                self.serial.setDTR(0)
            except IOError as e:
                print('failed to send DTR to device - %s' % e)

            time.sleep(self.init_sleep)

        def disconnect(self):
            """
            `disconnect` destroys current serial connection
            :return: None
            """
            self.serial.close()

        def _make_connect(self):
            """
            `_make_connect` construct new serial connection in order to settings passed via __init__
            :return: serial.Serial
            """
            return serial.Serial(self.device,
                                 self.baud,
                                 bytesize=serial.EIGHTBITS,
                                 parity=serial.PARITY_NONE,
                                 stopbits=serial.STOPBITS_ONE,
                                 timeout=self.timeout,
                                 xonxoff=False)

        def _make_cmd(self, cmd, value):
            return '%s=%s%s' % (cmd, value, self.separator)

        def cmd(self, cmd):
            """
            `cmd` sends command to device via serial port
            :param cmd: command to send
            :return: None
            """
            if not self.serial:
                raise ConnectionError('Connect to port first!')
            if not isinstance(cmd, bytes):
                cmd = str.encode(cmd)

            self.serial.write(cmd)
            time.sleep(self.cmd_sleep)

        def batch_cmd(self, commands):
            """
            `batch_cmd` make commands array joined via `self.separator` char and send to device via serial
            :param commands: array of commands, strings or bytes
            :return: None
            """
            if len(commands) == 0:
                return

            batch = self.separator.join(commands) + self.separator
            self.cmd(batch)

        def set_rgb(self, r=0, g=0, b=0):
            if not all([r, g, b]):
                return

            r_cmd = self._make_cmd('R', r)
            g_cmd = self._make_cmd('G', g)
            b_cmd = self._make_cmd('B', b)

            self.batch_cmd([r_cmd, g_cmd, b_cmd])

            self.r_val = int(r)
            self.g_val = int(g)
            self.b_val = int(b)

        def get_rgb(self):
            return {
                'red': self.r_val,
                'green': self.g_val,
                'blue': self.b_val,
                }


class FakeSerial():
    def __init__(self, device='/dev/ttyUSB0'):
        self.r_val = 0
        self.g_val = 0
        self.b_val = 0
        print('[DEBUG] init fake serial device at {}'.format(device))

    def connect(self):
        print('[DEBUG] connect to fake device')

    def cmd(self, cmd):
        print('[DEBUG] exec command "{}"'.format(cmd))

    def batch_cmd(self, commands):
        print('[DEBUG] exec batch "{}"'.format(commands))

    def set_rgb(self, r=0, g=0, b=0):
        print('[DEBUG] set RGB to r={}, g={}, b={}'.format(r, g, b))
        self.r_val = r
        self.g_val = g
        self.b_val = b

    def get_rgb(self):
        return {
            'red': self.r_val,
            'green': self.g_val,
            'blue': self.b_val,
        }
