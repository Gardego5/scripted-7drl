class Impossible (Exception):
    # Exception raised when an action is impossible to be performed.
    # The reason is given as the exception message.
    pass


class OutOfWindow (Exception):
    # Exception raised when in InventoryEventHandler and a tile is
    # not within the specified window.
    pass


class GenerationException (Exception):
    # Raised when generation takes to long on a step.
    pass
