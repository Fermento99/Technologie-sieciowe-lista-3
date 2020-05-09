# Paweł Kajanek

import random
from medium import Medium


class Device(object):
    """Object simulating a device connected to a  medium"""
    max_attemps = 16
    jam_sig = '01010101'
    
    def __init__(self, medium, joint):
        """Creates instance of Device
        Parameters:
        medium (Medium): medium to which device will be connected
        joint (int): point on medium where device will be connected
        """

        self.joint = joint
        self.medium = medium
        self.messages = []
        self.m = ''
        self.pointer = 0
        self.counter = 0
        self.attempts = 0
        self.c_flag = False
        self.post_c = True
    

    def add_message(self, message):
        """Adds message to message queue
        Parameters:
        message (iterable): should contain items convertible to integers
        """

        self.messages.append(message)
    

    def send_jam(self):
        """Re-adds jammed message to queue 
        and sets current message to jam signal
        """

        self.post_c = False
        self.messages.insert(0, self.m)
        self.m = self.jam_sig
        self.pointer = 0
    

    def next_message(self):
        """Sets current message to next in queue if such exists"""

        if self.messages:
            self.m = self.messages.pop(0)
        else:
            m = ''
        self.pointer = 0
        self.wait(12)
        
        if self.post_c:
            self.attempts = 0
        else:
            self.post_c = True
    

    def _send_message(self):
        """Sends next bit of current message
        or resets message if whole of it was send
        """

        if self.pointer in range(len(self.m)):
            self.medium.send(int(self.m[self.pointer]), self.joint)
            self.pointer += 1
        else:
            self.m = ''
            self.pointer = 0
    

    def _get_bit(self):
        """Returns the bit on the joint where device
        is connected
        """

        return self.medium.get_bit(self.joint)
    

    def wait(self, cycles):
        """Extends the amount of cycles in which device will be idle
        Parameters:
        cycles (int): number of cycles to be idle for
        """

        if self.counter < cycles:
            self.counter = cycles


    def _check_medium(self):
        """Checks if the medium is unoccupied"""

        if self._get_bit() == 0:
            return True
        else:
            return False

    
    def _check_collision(self):
        """Checks if a collision ocuured
        Note: should be always used after _check_medium returned False
        """

        return self.pointer > 0


    def resolve_collision(self):
        """Handles collisions if such ocuur"""

        self.send_jam()
        self.attempts += 1
        if self.attempts > self.max_attemps:
            print(self, '>> couledn\'t send a message:',
                self.messages.pop(0))
        r = random.randint(0, 2**self.attempts - 1)
        self.wait(r * self.medium.length)
        self.c_flag = False
        print(self, '>> collision detected, waiting for:', r)


    def work(self):
        """Represents transmitting procedure, 
        Decides what a device should do in this cycle 
        """

        if self.c_flag:
            self.resolve_collision()
        elif not self.m:
            self.next_message()
        elif not self._check_medium() and self.post_c:
            if self._check_collision():
                self.c_flag = True
            else:
                self.wait(8)
        elif self.counter > 0 and self.post_c:
            self.counter -= 1
        else:
            self._send_message()