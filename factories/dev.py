from components.inventory import Inventory, TypedInventory
from components.equipable import Equipable
from entity import Item, ItemSlot
import color

example_psu = Item(
    char=chr(0x2261),
    name="Example PSU",
    color=color.yellow,
    flags={"psu"},
    equipable=Equipable(max_hp=100),
    description="An example Power Supply."
)

# Hardware Devices
hardware = [
    ItemSlot(pos=( 8,  6), name="p1", reqs = {"p1"}),
    ItemSlot(pos=(12,  6), name="p2", reqs = {"p2"}),
    ItemSlot(pos=(16,  6), name="p3", reqs = {"p3"}),
    ItemSlot(pos=(22,  6), name="p4", reqs = {"p4"}),
    ItemSlot(pos=(26,  6), name="p5", reqs = {"p5"}),
    ItemSlot(pos=(30,  6), name="p6", reqs = {"p6"}),

    ItemSlot(pos=( 9, 16), name="psu", reqs = {"psu"}),
    ItemSlot(pos=(19, 15), name="cpu", reqs = {"cpu"}),
    ItemSlot(pos=(29, 13), name="apu", reqs = {"apu"}),
    ItemSlot(pos=(31, 19), name="gpu", reqs = {"gpu"}),

    ItemSlot(pos=(10, 24), name="d1", reqs = {"d1"}),
    ItemSlot(pos=(13, 24), name="d2", reqs = {"d2"}),
    ItemSlot(pos=(16, 24), name="d3", reqs = {"d3"}),
    ItemSlot(pos=(22, 24), name="d4", reqs = {"d4"}),
    ItemSlot(pos=(25, 24), name="d5", reqs = {"d5"}),
    ItemSlot(pos=(28, 24), name="d6", reqs = {"d6"}),
]
for i in range(6): hardware[i].description = "A peripheral slot. Can be used to attach various devices."
hardware[6].description = "Your Power Supply Unit. Its power output limits the hardware you can install."
hardware[7].description = "Your Central Processing Unit. Its thread count limits the number of active programs you can have running."
hardware[8].description = "Your Auxiliary Processing Unit. Its thread count limits the number of passive programs you can have running."
hardware[9].description = "Your Graphics Processing Unit. Limits your perception of the world surrounding you."
for i in range(10, 16): hardware[i].description = "A data slot. Can be used to expand software storage."

hardware[6].inventory.add(example_psu)

# Software Devices
software = [
    Item(char=chr(0x3D), color=(255, 255, 255), name="Active", inventory = Inventory(1)),
    Item(char=chr(0x3D), color=(255, 255, 255), name="Passive", inventory = Inventory(1)),
    Item(char=chr(0x3D), color=(255, 255, 255), name="Inactive", inventory = Inventory(1)),
]
software[0].description = "Your active programs. Can be activated to create a strong effect. Has limited uses. Number limited by your CPU."
software[1].description = "Your passive programs. Provide continuous effect while running. Number Limited by your APU."
software[2].description = "Inactive programs stored in memory. The number of programs you can store depends on how much software storage you have from your data cards."
