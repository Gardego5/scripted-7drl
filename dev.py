from components.inventory import Inventory
from entity import Item

# Hardware Devices
hardware = [
    Item(char=chr(0x25A0), color=(255, 255, 255), name="p1", inventory = Inventory(1)),
    Item(char=chr(0x25A0), color=(255, 255, 255), name="p2", inventory = Inventory(1)),
    Item(char=chr(0x25A0), color=(255, 255, 255), name="p3", inventory = Inventory(1)),
    Item(char=chr(0x25A0), color=(255, 255, 255), name="p4", inventory = Inventory(1)),
    Item(char=chr(0x25A0), color=(255, 255, 255), name="p5", inventory = Inventory(1)),
    Item(char=chr(0x25A0), color=(255, 255, 255), name="p6", inventory = Inventory(1)),

    Item(char=chr(0x25A0), color=(255, 255, 255), name="psu", inventory = Inventory(1)),
    Item(char=chr(0x25A0), color=(255, 255, 255), name="cpu", inventory = Inventory(1)),
    Item(char=chr(0x25A0), color=(255, 255, 255), name="apu", inventory = Inventory(1)),
    Item(char=chr(0x25A0), color=(255, 255, 255), name="gpu", inventory = Inventory(1)),

    Item(char=chr(0x25A0), color=(255, 255, 255), name="d1", inventory = Inventory(1)),
    Item(char=chr(0x25A0), color=(255, 255, 255), name="d2", inventory = Inventory(1)),
    Item(char=chr(0x25A0), color=(255, 255, 255), name="d3", inventory = Inventory(1)),
    Item(char=chr(0x25A0), color=(255, 255, 255), name="d4", inventory = Inventory(1)),
    Item(char=chr(0x25A0), color=(255, 255, 255), name="d5", inventory = Inventory(1)),
    Item(char=chr(0x25A0), color=(255, 255, 255), name="d6", inventory = Inventory(1)),
]

# Software Devices
software = [
    Item(char=chr(0x25A0), color=(255, 255, 255), name="Active", inventory = Inventory(1)),
    Item(char=chr(0x25A0), color=(255, 255, 255), name="Passive", inventory = Inventory(1)),
    Item(char=chr(0x25A0), color=(255, 255, 255), name="Inactive", inventory = Inventory(1)),
]