"""
output.py
==========
The module that holds all of the attributes for an output.
"""

"""Default output descriptions."""
output_descriptions = [['Forward', 'Stop', 'Reverse'],
                       ['Slow', 'Medium', 'Fast'],
                       ['straight', 'left', 'right'],
                       ['No see', 'See'],
                       ['Wait', 'Go', 'Urgent Brake'],
                       ['No trigger', 'Trigger']]


class Output:
    """The output class will be used to represent output sent to the motion controller."""
    name = "Base Output"
    data = [-1]
    descriptions = [[]]

    def __init__(self, data, name):
        """
        Initialize an output instance with the data representation equal to the parameter 'data',
        the name of the state equal to the parameter 'name',
        and the descriptions that correspond to the data equal to the default descriptions.

        Parameters
        ----------
        data
            A list of integers indicating the current output.

        name
            A string indicating the name of the of the output.
        """
        self.data = data
        self.name = name
        self.descriptions = output_descriptions

    def get_data(self):
        """Returns the data representation of an output object."""
        return self.data

    def set_data(self, new_data):
        """
        Sets the local output data of an output object.

        Parameters
        ----------
        new_data
            A list of integers indicating the new representation for a state.

        """
        self.data = new_data

    def get_name(self):
        """Returns the name of an output object."""
        return self.name

    def set_name(self, new_name):
        """
        Sets the local name of an output object.

        Parameters
        ----------
        new_name
            A string indicating the new name of an output object.

        """
        self.name = new_name

    def show_descriptions(self):
        """Displays the default descriptions."""
        for i in range(len(self.descriptions)):
            print(self.descriptions[i])

    def get_output(self):
        """Displays local descriptions indexed by local data."""
        printable_name = '-----Output Name: %s-----\n' % self.name
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
