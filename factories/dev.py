from components.inventory import Inventory
from entity import Item
import color

# Hardware Devices
hardware = [
    Item(pos=( 8,  6), char=chr(0x3D), color=color.ui_subdued, name="p1", inventory = Inventory(1)),
    Item(pos=(12,  6), char=chr(0x3D), color=color.ui_subdued, name="p2", inventory = Inventory(1)),
    Item(pos=(16,  6), char=chr(0x3D), color=color.ui_subdued, name="p3", inventory = Inventory(1)),
    Item(pos=(22,  6), char=chr(0x3D), color=color.ui_subdued, name="p4", inventory = Inventory(1)),
    Item(pos=(26,  6), char=chr(0x3D), color=color.ui_subdued, name="p5", inventory = Inventory(1)),
    Item(pos=(30,  6), char=chr(0x3D), color=color.ui_subdued, name="p6", inventory = Inventory(1)),

    Item(pos=( 9, 16), char=chr(0x3D), color=color.ui_subdued, name="psu", inventory = Inventory(1)),
    Item(pos=(19, 15), char=chr(0x3D), color=color.ui_subdued, name="cpu", inventory = Inventory(1)),
    Item(pos=(29, 13), char=chr(0x3D), color=color.ui_subdued, name="apu", inventory = Inventory(1)),
    Item(pos=(31, 19), char=chr(0x3D), color=color.ui_subdued, name="gpu", inventory = Inventory(1)),

    Item(pos=(10, 24), char=chr(0x3D), color=color.ui_subdued, name="d1", inventory = Inventory(1)),
    Item(pos=(13, 24), char=chr(0x3D), color=color.ui_subdued, name="d2", inventory = Inventory(1)),
    Item(pos=(16, 24), char=chr(0x3D), color=color.ui_subdued, name="d3", inventory = Inventory(1)),
    Item(pos=(22, 24), char=chr(0x3D), color=color.ui_subdued, name="d4", inventory = Inventory(1)),
    Item(pos=(25, 24), char=chr(0x3D), color=color.ui_subdued, name="d5", inventory = Inventory(1)),
    Item(pos=(28, 24), char=chr(0x3D), color=color.ui_subdued, name="d6", inventory = Inventory(1)),
]
for i in range(6): hardware[i].description = "A peripheral slot. Can be used to attach various devices."
hardware[6].description = "Your Power Supply Unit. Its power output limits the hardware you can install."
hardware[7].description = "Your Central Processing Unit. Its thread count limits the number of active programs you can have running."
hardware[8].description = "Your Auxiliary Processing Unit. Its thread count limits the number of passive programs you can have running."
hardware[9].description = "Your Graphics Processing Unit. Limits your perception of the world surrounding you."
for i in range(10, 16): hardware[i].description = "A data slot. Can be used to expand software storage."

# Software Devices
software = [
    Item(char=chr(0x3D), color=(255, 255, 255), name="Active", inventory = Inventory(1)),
    Item(char=chr(0x3D), color=(255, 255, 255), name="Passive", inventory = Inventory(1)),
    Item(char=chr(0x3D), color=(255, 255, 255), name="Inactive", inventory = Inventory(1)),
]
software[0].description = "Your active programs. Can be activated to create a strong effect. Has limited uses. Number limited by your CPU."
software[1].description = "Your passive programs. Provide continuous effect while running. Number Limited by your APU."
software[2].description = "Inactive programs stored in memory. The number of programs you can store depends on how much software storage you have from your data cards."
