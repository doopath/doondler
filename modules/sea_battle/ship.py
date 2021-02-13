""" A module of a ship class. """


class Ship:
    """
        A class of a battle ship.

        Attributes
        ----------
        fields: list
            A list of the Field objects.
        is_destroyed: bool
            Is true if the ship was fully destroyed and false if not.

        Methods
        -------
        destroy_block(field: Field): void
            Destroy a block of the ship.
    """
    def __init__(self, fields: list):
        self.fields = fields
        self.is_destroyed = False

    def destroy(self):
        self.is_destroyed = True
        print(f"The ship at {'(' + '; '.join([f.index for f in self.fields]) + ')'} was destroyed.")



