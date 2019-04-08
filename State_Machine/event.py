"""
event.py
=========
The module that holds all of the attributes for an event.
"""

"""Default event descriptions."""
event_descriptions = [['light is not active', 'light is active','N/A'],
                      ['red light', 'green light','N/A'],
                      ['lines is not active', 'lines is active','N/A'],
                      ['left line is not detected', 'left line is detected','N/A'],
                      ['right line is not detected', 'right line is detected','N/A'],
                      ['turning is not active', 'turning is active','N/A'],
                      ['turning left','turing right','N/A'],
                      ['finish line is not detected', 'finish line is detected','N/A'],
                      ['obstacle is not detected', 'obstacle is detected','N/A'],
                      ['car is not active', 'car is active','N/A'],
                      ['car is not gaining', 'car is gaining','N/A'],
                      ['arrow is not active', 'arrow is active','N/A'],
                      ['left arrow is not detected', 'left is arrow detected','N/A'],
                      ['right arrow is not detected', 'right is arrow detected','N/A'],
                      ['up arrow is not detected', 'up is arrow detected','N/A']]

                      
                      



class Event:
    """The event class will be used to represent inputs received from the vision system."""
    data = [-1]
    name = 'Base Event'
    descriptions = [[]]

    def __init__(self, data, name):
        """
        Initialize an event instance with the data representation equal to the parameter 'data',
        the name of the state equal to the parameter 'name',
        and the descriptions that correspond to the data equal to the default descriptions.
            
        Parameters
        ----------
        data
            A list of integers indicating an event's data.
            
        name
            A string indicating the name of an event.
            
        """
        self.data = data
        self.name = name
        self.descriptions = event_descriptions

    def get_name(self):
        """Returns the name of an event object."""
        return self.name
    
    def set_name(self, new_name):
        """
        Sets the local event name.
        
        Parameters
        ----------
        new_name
            A string indicating the new name of an event.
        
        """
        self.name = new_name
    
    def get_data(self):
        """Returns the data representation of an event object."""
        return self.data

    def set_data(self, new_data):
        """
        Sets the local event data.
            
        Parameters
        ----------
        new_data
            A list of integers indicating the new representation for an event.
            
        """
        self.data = new_data

    def show_descriptions(self):
        """Displays the default descriptions."""
        for i in range(len(self.descriptions)):
            print(self.descriptions[i])

    def get_event(self):
        """Displays local descriptions indexed by local data."""
        printable_name = '-----Event Name: %s-----\n' % self.name
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
