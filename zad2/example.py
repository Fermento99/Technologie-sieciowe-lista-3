# Paweł Kajanek

"""Example program
shows simulation of two devices, which are connected to a common medium,
that try to send 3 messages each.
"""

from device import Device
from medium import Medium


def main():
    cord = Medium(100)
    pc1 = Device(cord, 4)
    pc1.add_message('1'*100)
    pc1.add_message('1'*100)
    pc1.add_message('1'*100)
    pc2 = Device(cord, 70)
    pc2.add_message('1'*100)
    pc2.add_message('1'*100)
    pc2.add_message('1'*100)

    for i in range(1000):
        print('iteration {}: '.format(i+1), end='')
        cord.display()
        pc2.work()
        pc1.work()
        cord.propagate()

if __name__ == "__main__":
    main()