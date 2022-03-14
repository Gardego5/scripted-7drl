from components.inventory import Inventory, TypedInventory, DynamicInventory
from components.equipable import Equipable
from entity import Item, ItemSlot
import color

# Hardware Devices
hardware = [
    ItemSlot(pos=( 8,  6), name="p1", reqs = {"p1"}, description = "A peripheral slot. Can be used to attach various devices."),
    ItemSlot(pos=(12,  6), name="p2", reqs = {"p2"}, description = "A peripheral slot. Can be used to attach various devices."),
    ItemSlot(pos=(16,  6), name="p3", reqs = {"p3"}, description = "A peripheral slot. Can be used to attach various devices."),
    ItemSlot(pos=(22,  6), name="p4", reqs = {"p4"}, description = "A peripheral slot. Can be used to attach various devices."),
    ItemSlot(pos=(26,  6), name="p5", reqs = {"p5"}, description = "A peripheral slot. Can be used to attach various devices."),
    ItemSlot(pos=(30,  6), name="p6", reqs = {"p6"}, description = "A peripheral slot. Can be used to attach various devices."),

    ItemSlot(pos=( 9, 16), name="psu", reqs = {"psu"}, description = "Your Power Supply Unit. Its power output limits the hardware you can install."),
    ItemSlot(pos=(19, 15), name="cpu", reqs = {"cpu"}, description = "Your Central Processing Unit. Its thread count limits the number of active programs you can have running."),
    ItemSlot(pos=(29, 13), name="apu", reqs = {"apu"}, description = "Your Auxiliary Processing Unit. Its thread count limits the number of passive programs you can have running."),
    ItemSlot(pos=(31, 19), name="gpu", reqs = {"gpu"}, description = "Your Graphics Processing Unit. Limits your perception of the world surrounding you."),

    ItemSlot(pos=(10, 24), name="d1", reqs = {"d1"}, description = "A data slot. Can be used to expand software storage."),
    ItemSlot(pos=(13, 24), name="d2", reqs = {"d2"}, description = "A data slot. Can be used to expand software storage."),
    ItemSlot(pos=(16, 24), name="d3", reqs = {"d3"}, description = "A data slot. Can be used to expand software storage."),
    ItemSlot(pos=(22, 24), name="d4", reqs = {"d4"}, description = "A data slot. Can be used to expand software storage."),
    ItemSlot(pos=(25, 24), name="d5", reqs = {"d5"}, description = "A data slot. Can be used to expand software storage."),
    ItemSlot(pos=(28, 24), name="d6", reqs = {"d6"}, description = "A data slot. Can be used to expand software storage."),
]
