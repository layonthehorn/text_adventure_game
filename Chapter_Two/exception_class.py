class Error(Exception):
    """Base class for exceptions."""

    pass


class ReadOnlyError(Error):
    """Throws error if attempting to set a read only variable."""

    def __init__(self, item, npc):
        super().__init__(f"Failed to set read only variable to {item}, on {npc}")


class LocationError(Error):
    """Throws this error if attempting to move to unknown place."""

    def __init__(self, area):
        super().__init__(f"Failed to find matching area for {area}.")


class ChangeSectionError(Error):
    """Throws this error if attempting to move to unknown section of the map."""

    def __init__(self, area):
        super().__init__(
            f"Failed to find matching section for {area}. Missing map section?"
        )


class NPCLocationError(Error):
    """Throws this error if attempting to start a NPC in an unknown place."""

    def __init__(self, name, area):
        super().__init__(
            f"Failed to find matching area for {area} when setting up {name}."
        )


class ChangeNPCLocationError(Error):
    """An error to tell me that I messed up naming a room correctly when moving a NPC."""

    def __init__(self, name, area):
        super().__init__(f"Failed to find matching area for {area} when moving {name}.")


class RedundantMoveError(Error):
    """For if a NPC or player tries to move to the same room they are in already."""

    def __init__(self, name):
        super().__init__(f"Tried to move {name} to same room as they are in.")


class MapMatchError(Error):
    """If can not find a matching map for player section."""

    def __init__(self, name):
        super().__init__(f"Missing map for {name}.")
