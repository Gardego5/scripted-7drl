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
for i in range(6): hardware[i].description = "A peripheral slot. Can be used to attach various devices."
hardware[6].description = "Your Power Supply Unit. Its power output limits the hardware you can install."
hardware[7].description = "Your Central Processing Unit. Its thread count limits the number of active programs you can have running."
hardware[8].description = "Your Auxiliary Processing Unit. Its thread count limits the number of passive programs you can have running."
hardware[9].description = "Your Graphics Processing Unit. Limits your perception of the world surrounding you."
for i in range(10, 16): hardware[i].description = "A data slot. Can be used to expand software storage."

# Software Devices
software = [
    Item(char=chr(0x25A0), color=(255, 255, 255), name="Active", inventory = Inventory(1)),
    Item(char=chr(0x25A0), color=(255, 255, 255), name="Passive", inventory = Inventory(1)),
    Item(char=chr(0x25A0), color=(255, 255, 255), name="Inactive", inventory = Inventory(1)),
]
software[0].description = "Your active programs. Can be activated to create a strong effect. Has limited uses. Number limited by your CPU."
software[1].description = "Your passive programs. Provide continuous effect while running. Number Limited by your APU."
software[2].description = "Inactive programs stored in memory. The number of programs you can store depends on how much software storage you have from your data cards."
