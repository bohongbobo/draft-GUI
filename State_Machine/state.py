"""
state.py
=========
The module that holds all of the attributes for a state.
"""

"""Default state descriptions."""
state_descriptions = [['Car is ready', 'Car is moving', 'Car is finished'],
                      ['Car is not turning', 'Car is turning left', 'Car is turning right'],
                      ['Car is not avoiding', 'Car is avoiding left car', 'Car is avoiding right car'],
                      ['Car is not chasing', 'Car is chasing'],
                      ['Normal course', 'Shortcut Course']]


class State:
    """The state class will be used to represent states in a state machine."""
    data = [-1]
    name = 'Base State'
    descriptions = [[]]
    events = []
    start_state = False
    finish_state = False

    def __init__(self, data, name):
        """
        Initialize a state instance with the data representation equal to the parameter 'data',
        the name of the state equal to the parameter 'name',
        and the descriptions that correspond to the data equal to the default descriptions.

        Parameters
        ----------
        data
            A list of integers indicating a state's data.

        name
            A string indicating the name of a state.

        """
        self.data = data
        self.name = name
        self.descriptions = state_descriptions

    def set_data(self, new_data):
        """
        Sets the data of a state object equal to the parameter new_data.

        Parameters
        ----------
        new_data
            A list of integers indicating the new data of a state.

        """
        self.data = new_data

    def get_data(self):
        """Returns the data representation of a state object."""
        return self.data

    def set_name(self, new_name):
        """
        Sets the name of a state object equal to the parameter new_name.

        Parameters
        ----------
        new_name
            A string indicating the new name of a state.
        """
        self.name = new_name

    def get_name(self):
        """Returns the name of a state object."""
        return self.name

    def show_descriptions(self):
        """Displays the default descriptions."""
        for i in range(len(self.descriptions)):
            print(self.descriptions[i])

    def get_state(self):
        """Displays local descriptions indexed by local data."""
        printable_name = '-----State Name: %s-----\n' % self.name
        print(printable_name)
        print(self.data)
        try:
            for i in range(len(self.descriptions)):
                print(self.descriptions[i][int(self.data[i])])
        except IndexError:
            print('-')
        dashes = (len(printable_name) - 1) * '-'
        print(dashes)
        return ''
