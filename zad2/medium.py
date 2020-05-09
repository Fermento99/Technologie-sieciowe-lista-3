# Paweł Kajanek


class Medium(object):
    """Object simulating medium"""

    def __init__(self, length):
        """Creates instance of Medium
        Parameters:
        length (int): length of new Medium, < 230
        """

        self.length = min(length + 2, 232)
        self.right_canal = [0] * self.length
        self.left_canal = [0] * self.length
    

    def propagate(self):
        """Makes bits move one step through the medium"""

        temp = [0] * self.length
        for i in range(self.length-1, 1, -1):
            self.right_canal[i] = self.right_canal[i-1]
        for i in range(0, self.length-1, 1):
            self.left_canal[i] = self.left_canal[i+1]
    

    def send(self, bit, joint):
        """Adds new bit, which will move both ways in the medium
        Parameters:
        bit: bit that will be added to medium
        joint (int): place on the medium where bit will be inserted
        """

        if joint <= 0 or joint >= self.length-1:
            raise KeyError('joint is a stopper or doesn\'t exist')
        
        self.left_canal[joint] += bit
        self.right_canal[joint] += bit


    def display(self):
        """Shows the whole medium (evry part of medium)"""

        print('[', end='')
        for i in range(self.length):
            print(self.right_canal[i] + self.left_canal[i],end='')
        print(']')
    
    
    def get_bit(self, joint):
        """Returns the bit that is in certain place in medium
        Parameters:
        joint (int): place on the medium from which bit will be 
                obtained
        """

        if joint < 0 or joint > self.length-1:
            raise KeyError('joint is a stopper or doesn\'t exist')

        return self.right_canal[joint] + self.left_canal[joint]