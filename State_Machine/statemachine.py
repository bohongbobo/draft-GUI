from event import Event
from state import State
from output import Output
from copy import deepcopy
import sys
import time
sys.path.insert(0,'../MV')
import machineVision as mv
import gui as gg

"""
statemachine.py
=================
The core module of the cognitive state machine.
"""


class StateMachine:
    """The state machine class will be used to hold states, direct inputs, and provide outputs."""
    name = 'My State Machine'
    events = []
    states = []
    outputs = []
    transitions = [[]]
    output_table = [[]]
    current_state = 0
    previous_state = 0
    current_event = 0

    def __init__(self, name):
        """
        Initialize a statemachine instance with the name equal to the parameter 'name'.

        Parameters
        ----------
        name
            A string indicating the name of the state machine.

        """
        self.name = name

    def assign_state(self, cs, ps, ce):
        """
        Assign state machine variables to updated states and updated event.

        Parameters
        ----------
        cs
            A state object indicating the current state of the state machine.

        ps
            A state object indicating the previous state of the machine.

        ce
            An event object indicating the event the state machine just received.

        """
        self.current_state = cs
        self.previous_state = ps
        self.current_event = ce

    def display_events(self):
        """Display all possible events the state machine could receive."""
        for i in range(len(self.events)):
            print(self.events[i].get_event())

    def display_outputs(self):
        """Display all output possibilities for the state machine."""
        for i in range(len(self.outputs)):
            print(self.outputs[i].get_output())

    def reset_transition_table(self):
        """Reset the transition table to default values, e.g. -1"""
        x = len(self.states)
        y = len(self.events)
        self.transitions = []
        for i in range(x):
            self.transitions.append([-1 for i in range(y)])

        self.output_table = deepcopy(self.transitions)

    def reset_transition_table2(self, num_states, num_events):
        """
        Reset the transition table to default values, e.g. -1

        Parameters
        ----------
        num_states
            An integer indicating the number of state objects that are in the self.states list

        num_events
            An integer indicating the number of event objects that are in the self.events list

        """
        self.transitions = []
        for i in range(num_states):
            self.transitions.append([-1 for i in range(num_events)])

        self.output_table = deepcopy(self.transitions)

    def display_machine(self):
        """Display the current status of the state machine."""
        print(self.name)
        print('CURRENT STATE')
        self.current_state.get_state()
        print('PREVIOUS STATE')
        self.previous_state.get_state()
        print('CURRENT EVENT')
        self.current_event.get_event()

    def name_to_state(self, name):
        """
        Return state object in self.states with state name equal to the parameter 'name'.

        Parameters
        ----------
        name
            A string indicating the name of the state being searched for in self.states.

        """
        for i in range(len(self.states)):
            if name.lower() == self.states[i].name.lower():
                return self.states[i]
        error_message = 'State not found in name_to_state(self,%s)' % self.name
        print(error_message)

    def name_to_event(self, name):
        """
        Return event object in self.events with event name equal to the parameter 'name'.

        Parameters
        ----------
        name
            A string indicating the name of the event being searched for in self.events.

        """
        for i in range(len(self.events)):
            if name.lower() == self.events[i].name.lower():
                return self.events[i]
        error_message = 'Event not found in name_to_event(self,%s)' % self.name
        print(error_message)

    def update_transition_table(self):
        """Update the size of the transition table based on the size of self.states
        and self.events sizes after adding a new state or event."""
        x = len(self.states) - 1
        y = len(self.events)
        if len(self.transitions) == 0:
            old = 0
        else:
            old = len(self.transitions[0])
        diff = y - old
        arr = []
        self.transitions.append(arr)
        for i in range(y):
            self.transitions[x].append(-1)
        for i in range(x):
            for difference in range(diff):
                self.transitions[i].append(-1)

    def update_output_table(self):
        """Update the size of the output table based on the size of self.states
        and self.events after adding a new state or event."""
        x = len(self.states) - 1
        y = len(self.events)
        if len(self.output_table) == 0:
            old = 0
        else:
            old = len(self.output_table[0])
        diff = y - old
        arr = []
        self.output_table.append(arr)
        for i in range(y):
            self.output_table[x].append(-1)
        for i in range(x):
            for difference in range(diff):
                self.output_table[i].append(-1)

    def get_event_index(self, event):
        """
        Return an integer that corresponds to the state machine event list when given an event object,
        data specific to a certain event, or a name specific to a certain event.

        Parameters
        ----------
        event
            Either an event object, an integer, or a string indicating which event we are searching for in self.events.

        """
        if isinstance(event, Event):
            for i in range(len(self.events)):
                if self.events[i].data == event.data:
                    return i

        if isinstance(event, int):
            for i in range(len(self.events)):
                if self.events[i].data == event:
                    return i

        if isinstance(event, str):
            if event.isdigit():
                event = [int(data) for data in event]
                for i in range(len(self.events)):
                    if self.events[i].data == event:
                        return i
            else:
                for i in range(len(self.events)):
                    if self.events[i].name == event:
                        return i

        if isinstance(event, str):
            str_to_data_test = ''.join(str(x) for x in event)
            for i in range(len(self.events)):
                if self.events[i].name == str_to_data_test:
                    return i

        return -1

    def get_state_index(self, state):
        """
        Return an integer that corresponds to the state machine state list when given a state object,
        data specific to a certain state, or a name specific to a certain state.

        Parameters
        ----------
        state
            Either a state object, an integer, or a string indicating which event we are searching for in self.states.

        """
        if isinstance(state, State):
            for i in range(len(self.states)):
                if self.states[i].data == state.data:
                    return i

        if isinstance(state, int):
            for i in range(len(self.states)):
                if self.states[i].data == state:
                    return i

        if isinstance(state, str):
            for i in range(len(self.states)):
                if self.states[i].name == state:
                    return i
        print('didnt find state index')

    def get_output_index(self, output):
        """
        Return an integer that corresponds to the state machine output list when given an output object,
        ata specific to a certain output, or a name specific to a certain output.

        Parameters
        ----------
        output
            Either an output object, an integer, or a string
            indicating which output we are searching for in self.outputs.

        """
        if isinstance(output, Output):
            for i in range(len(self.outputs)):
                if self.outputs[i].data == output.data:
                    return i

        if isinstance(output, int):
            for i in range(len(self.outputs)):
                if self.outputs[i].data == output:
                    return i

        if isinstance(output, str):
            for i in range(len(self.outputs)):
                if self.outputs[i].name == output:
                    return i

        return -1

    def add_transition(self):
        """Adds next state data into corresponding transition table starting state's index."""
        transition_data = False
        while not transition_data:
            self.display_states()
            start_state = input('What State would you start in? (State Name): ')
            if self.name_to_state(start_state) in self.states:
                print('POSSIBLE events\n', self.name_to_state(start_state).events)
                input_needed = input('On what Event will you transition? (Binary): ')
                if input_needed in self.name_to_state(start_state).events:
                    end_state = input('What State would you end in? (State Name): ')
                    if self.name_to_state(end_state) in self.states:
                        transition_data = True
                        state1_index = self.get_state_index(start_state.lower())
                        state2_index = self.get_state_index(end_state.lower())
                        event_index = self.get_event_index(
                            input_needed.lower())
                        self.transitions[state1_index][event_index] = self.states[state2_index]
                        self.show_transition_table()
                        output_string = input('Will this cause an output? (Y/N)')
                        if output_string.lower() == 'y':
                            output = self.add_output()
                            self.output_table[state1_index][event_index] = output
                            self.show_output_table()
                        else:
                            print('Okay\n')

    def edit_transition(self):
        """Replaces next state data into corresponding transition table starting state's index."""
        transition_data = False
        while not transition_data:
            start_state = input(
                'Which state\'s transition would you like to change? (State Name): ')
            if self.name_to_state(start_state) in self.states:
                print(self.name_to_state(start_state).events)
                input_needed = input(
                    'Which input would you like to edit? (Binary): ')
                if input_needed in self.name_to_state(start_state).events:
                    state1_index = self.get_state_index(start_state.lower())
                    event_index = self.get_event_index(input_needed.lower())
                    self.transitions[state1_index][event_index] = -1

                    end_state = input('Which state will this input transition to now? '
                                      '(State Name or \'none\' to delete the transition): ')

                    if end_state.lower() == 'none':
                        self.output_table[state1_index][event_index] = -1
                        break

                    elif self.name_to_state(end_state) in self.states:
                        transition_data = True
                        self.transitions[state1_index][event_index] = self.name_to_state(
                            end_state)
                        self.show_transition_table()

                        output_string = input(
                            'Do you want to edit the output caused by this transition? (Y/N)')
                        if output_string.lower() == 'y':
                            output = self.add_output()
                            self.output_table[state1_index][event_index] = output
                            self.show_output_table()

    def add_state(self,State):
        """Prompts user for state data, then creates a state and stores a state object in state machine."""
        if(State != None):
            self.states.append(State)
            self.update_transition_table()
            self.update_output_table()
        check_state = False
        while True:
            try:
                new_state_name = input('New state\'s name: ')
                new_state_data = input('Enter State Data: ')
                if 0 <= int(new_state_data) <= 999999999:
                    new_state_data_array = [int(x) for x in str(new_state_data)]
                    break
                else:
                    print(
                        'General format error. Please provide integers less than 999999999 but greater than 0.')
                    break

            except ValueError:
                print('Make sure you enter integers for data, and strings for names.')
        for i in range(len(self.states)):
            if self.states[i].data == new_state_data_array:
                check_state = True
        if not check_state:
            events = []
            event_string = input(
                'Enter an input or \'quit\' to stop entering events: ')
            while event_string != 'quit':
                if event_string.isdigit():
                    try:
                        event_array = [int(x) for x in event_string]
                        for i in range(len(event_array)):
                            if(event_array[i]!= 0) and (event_array[i]!= 1):
                                    event_array[i] = 2 #Changed here
                        check_event = False
                        event_string = ''.join(str(x) for x in event_array)
                        events.append(event_string)
                        for i in range(len(self.events)):
                            if (self.events[i].data == event_array):
                                check_event = True
                        if not check_event:
                            if len(self.events) == 0:
                                event_name = 'Event1'
                            else:
                                    #print(len(events))
                                i=self.events[-1].name[5:]
                                    #print(i)
                                event_name = 'Event'+ str(int(i) + 1)
                            event_object = Event(event_array, event_name)
                            self.events.append(event_object)
                        else:
                            print("You already added this event")
                    except RuntimeError:

                        print('General format error. Please provide integers less than..... that')
                event_string = input('Enter an input or \'quit\' to stop entering events: ')

            new_state = State(new_state_data_array, new_state_name)
            self.states.append(new_state)
            self.states[-1].events = events
            self.states[-1].get_state()
            self.update_transition_table()
            self.update_output_table()

        else:
            print("The state has already been exist, add state fail")
        if len(self.states) == 1 and len(self.events) != 0:
            self.assign_state(self.states[0], self.states[0], self.events[0])

    def edit_state(self):
        """Prompts user to see which part(s) of a state they would like to
           edit and then changes the attributes of that state object."""
        state_to_edit = input('Which state would you like to edit? (State name): ')
        if self.name_to_state(state_to_edit) in self.states:
            choice = input('Would you like to change the name? (y/n): ')
            choice2 = input('Would you like to change the data? (y/n): ')
            if choice.lower() == 'y' and choice2.lower() == 'y':
                new_name = input('Enter the new name: ')
                new_data = [int(data)
                            for data in input('Enter the new data: ')]
                for i in range(len(self.states)):
                    if self.states[i].name.lower() == state_to_edit.lower():
                        self.states[i].set_name(new_name)
                        self.states[i].set_data(new_data)
                        break

            if choice.lower() == 'y' and choice2.lower() == 'n':
                new_name = input('Enter the new name: ')
                for i in range(len(self.states)):
                    if self.states[i].name.lower() == state_to_edit.lower():
                        self.states[i].set_name(new_name)
                        break

            if choice.lower() == 'n' and choice2.lower() == 'y':
                new_data = [int(data)
                            for data in input('Enter the new data: ')]
                for i in range(len(self.states)):
                    if self.states[i].name.lower() == state_to_edit.lower():
                        self.states[i].set_data(new_data)
                        break

    def del_state(self):
        """Asks a user which state object they would like to delete and then removes
           it from self.states and updates the transition table and output tables accordingly."""
        state_to_del = input('Which state would you like to delete? (State name): ')

        if self.name_to_state(state_to_del) in self.states:
            for i in range(len(self.transitions)):
                for j in range(len(self.transitions[i])):
                    if self.transitions[i][j] == -1:
                        pass
                    elif self.transitions[i][j].name.lower() == state_to_del.lower():
                        self.transitions[i][j] = -1

            for i in range(len(self.states)):
                if self.states[i].name.lower() == state_to_del.lower():
                    if self.current_state == self.states[i]:
                        del self.states[i]
                        del self.transitions[i]
                        del self.output_table[i]
                        if(len(self.states) != 0):
                            self.current_state = self.states[-1]
                        else:
                            print('There is no exist state')
                        break

                    else:
                        del self.states[i]
                        del self.transitions[i]
                        del self.output_table[i]
                        break

    def edit_event(self):
        """Prompts user to see which part(s) of an event they would like to
           edit and then changes the attributes of that event object."""
        event_to_edit = input('Which event would you like to edit? (Event name): ')

        if self.name_to_event(event_to_edit) in self.events:
            choice = input('Would you like to change the name? (y/n): ')
            choice2 = input('Would you like to change the data? (y/n): ')
            if choice.lower() == 'y' and choice2.lower() == 'y':
                new_name = input('Enter the new name: ')
                new_data = [int(data)
                            for data in input('Enter the new data: ')]
                for i in range(len(self.events)):
                    if self.events[i].name.lower() == event_to_edit.lower():
                        self.events[i].set_name(new_name)
                        self.events[i].set_data(new_data)
                        break

            if choice.lower() == 'y' and choice2.lower() == 'n':
                new_name = input('Enter the new name: ')
                for i in range(len(self.events)):
                    if self.events[i].name.lower() == event_to_edit.lower():
                        self.events[i].set_name(new_name)
                        break

            if choice.lower() == 'n' and choice2.lower() == 'y':
                new_data = [int(data)
                            for data in input('Enter the new data: ')]
                for i in range(len(self.events)):
                    if self.events[i].name.lower() == event_to_edit.lower():
                        self.events[i].set_data(new_data)
                        break

    def del_event(self):
        """Asks a user which event object they would like to delete and then removes
           it from self.events and updates the transition table and output tables accordingly."""
        event_to_del = input(
            'Which event would you like to delete? (Event name): ')
        if self.name_to_event(event_to_del) in self.events:
            for i in range(len(self.transitions)):
                for j in range(len(self.transitions[i])):
                    if self.transitions[i][j] == -1:
                        pass
                    elif self.transitions[i][j].name.lower() == event_to_del.lower():
                        self.transitions[i][j] = -1

            for j in range(len(self.events)):
                if self.events[j].name.lower() == event_to_del.lower():
                    if self.current_event == self.events[j]:
                        del self.events[j]
                        for i in range(len(self.states)):
                            del self.transitions[i][j]
                            del self.output_table[i][j]
                        if(len(self.events) != 0):
                            self.current_event = self.events[-1]
                        else:
                            print("There is no event exist")
                        break

                    else:
                        del self.events[j]
                        for i in range(len(self.states)):
                            del self.transitions[i][j]
                            del self.output_table[i][j]
                        break


    def add_output(self):
        """Prompt user for output data. Stores output object into state machine."""
        accept_output = False
        check_exist = False
        self.display_outputs()
        while not accept_output:
            output_data = input('Output Data Sent to Motion Controller: ')
            output_data_list = [int(data) for data in output_data]
            if len(self.outputs) == 0:
                out_name = 'Output1'
            else:
                i = self.outputs[-1].name[6:]
                out_name = 'Output' + str(int(i) + 1)
            output = Output(output_data_list, 'Output'
                            + str(len(self.outputs) + 1))
            for i in range(len(self.outputs)):
                if self.outputs[i].data == output_data_list:
                    output = Output(output_data_list, 'Output' + str(i+1))

                    check_exist = True
                    break

            if not check_exist:
                self.outputs.append(output)
            accept_output = True
        print(self.outputs[-1].get_output())
        return output

    def input_event(self):
        """Prompts user for event input. Function will create event object and pass it into update_state."""
        current_input = input('What Event did TBD2 See? ')
        current_event_array = [int(x) for x in current_input]
        for i in range(len(current_event_array)):
            if(current_event_array[i]!= 0) and (current_event_array[i]!= 1):
                current_event_array[i] = 2 #Changed here
        check_events = False
        for i in range(len(self.current_state.events)):
            check_event = 0
            current_event_array1 = ''.join(str(x) for x in current_event_array)
            if(len(str(current_event_array1)) == len(self.current_state.events[i])):
                for j in range(len(self.current_state.events[i])):
                    if(int(current_event_array[j]) == int(self.current_state.events[i][j]) or int(self.current_state.events[i][j]) == 2 ):
                            check_event = check_event + 1
                            if(check_event == len(self.current_state.events[i])):
                                    check_events = True
        current_input = ''.join(str(x) for x in current_event_array)
        if not check_events:
            print('This does not result in a transition, thus no output.\n')
        else:
            temp_data = [int(x) for x in current_input]
            new_event = Event(temp_data, 'Event TBD2 Saw')
            self.update_state(new_event)

    def show_transition_table(self):
        """Display transition table."""
        print('Transition Table:\n')
        for i in range(len(self.transitions)):
            for j in range(len(self.transitions[i])):
                if isinstance(self.transitions[i][j], int):
                    print(self.transitions[i][j], end=' ')
                else:
                    print(self.transitions[i][j].name, end=' ')
            print('')
        print('\n')

    def show_output_table(self):
        """Display output table."""
        print('Output Table:\n')
        for i in range(len(self.output_table)):
            for j in range(len(self.output_table[i])):
                if isinstance(self.output_table[i][j], int):
                    print(self.output_table[i][j], end=' ')
                else:
                    print(self.output_table[i][j].name, end=' ')
            print('')
        print('\n')

    def display_states(self):
        """Display list of states."""
        for i in range(len(self.states)):
            self.states[i].get_state()

    def save(self):
        """Saves the current state machine along with child data."""
        path = input('Enter file name to save as: ')
        save_file = open(path, 'w')
        lines = [self.name, '\n', str(len(self.states)), '\n',
                 str(len(self.events)), '\n', str(len(self.outputs)), '\n']

        save_file.writelines(lines)

        for i in self.states:
            state_data = ''.join(str(x) for x in i.data)
            lines = [i.name, '\n', state_data, '\n', ]
            save_file.writelines(lines)

            for e in i.events:
                save_file.write(e + ' ')
            save_file.write('\n')

        for i in self.events:
            event_string = ''.join(str(x) for x in i.data)
            lines = [i.name, '\n', event_string, '\n']
            save_file.writelines(lines)

        for i in self.outputs:
            output_string = ''.join(str(x) for x in i.data)
            lines = [i.name, '\n', output_string, '\n']
            save_file.writelines(lines)

        for i in self.transitions:
            for e in i:
                if isinstance(e, int):
                    save_file.write('-1 ')
                else:
                    save_file.write(e.name + ' ')
            save_file.write('\n')

        for i in self.output_table:
            for e in i:
                if isinstance(e, int):
                    save_file.write('-1 ')
                else:
                    save_file.write(e.name + ' ')
            save_file.write('\n')
        save_file.close()

    def reset_machine(self):
        """Resets everything in the state machine to default values."""
        default_state = State([0, 0, 0, 0, 0, 0], 'Default State')
        default_event = Event([0, 0, 0, 0, 0], 'Default Event')
        self.assign_state(default_state, default_state, default_event)
        self.transitions = []
        self.output_table = []
        self.name = 'My State Machine'
        self.events = []
        self.states = []
        self.outputs = []

    def load(self,file):

        """Loads a state machine from a text file."""
        if len(self.states) > 0:
            self.reset_machine()
        if(file == "none"):
            path = input('Enter file name to load State Machine: ')
        else:
            path = file
        load_file = open(path, 'r')

        self.name = load_file.readline().strip()
        print('State Machine Name: {}'.format(self.name))

        num_states = int(load_file.readline().strip())
        print('Number of states: {}'.format(num_states))

        num_events = int(load_file.readline().strip())
        print('Number of events: {}'.format(num_events))

        num_outputs = int(load_file.readline().strip())
        print('Number of outputs: {}\n'.format(num_outputs))

        for i in range(num_states):
            state_name = load_file.readline().strip()
            state_data = [int(data) for data in load_file.readline().strip()]
            self.states.append(State(state_data, state_name))

            event_list = load_file.readline().split()
            self.states[i].events = deepcopy(event_list)

        for i in range(num_events):
            event_name = load_file.readline().strip()
            event_data = [int(data) for data in load_file.readline().strip()]
            self.events.append(Event(event_data, event_name))

        for i in range(num_outputs):
            output_name = load_file.readline().strip()
            output_data = [int(data) for data in load_file.readline().strip()]
            self.outputs.append(Output(output_data, output_name))

        self.reset_transition_table2(num_states, num_events)

        for i in range(num_states):
            transition_list = load_file.readline().split()
            for j in range(len(transition_list)):
                for s in self.states:
                    if transition_list[j] == s.name:
                        self.transitions[i][j] = s

        for i in range(num_states):
            output_list = load_file.readline().split()
            for j in range(len(output_list)):
                for o in self.outputs:
                    if output_list[j] == o.name:
                        self.output_table[i][j] = o

        load_file.close()
        self.assign_state(self.states[0], self.states[0], self.events[0])

    def update_state(self, event):
        """
        Uses current state and new event to index the state machine transitions table,
        assign the new state to the state machine,
        and display/send the corresponding output data to the guidance system.

        Parameters
        ----------
        event
            An event object indicating what event the state machine received form the vision system.

        """
        self.current_event = event
        event_string = ''.join(str(x) for x in event.data)
        current_state_possible_events = self.current_state.events
        output = Output([-1], "No Output")
        check_events = False
        for i in range(len(current_state_possible_events)):
            check_event = 0
            if(len(str(event_string)) == len(str(current_state_possible_events[i]))):
                current_state_possible_events_array = [
                    int(x) for x in str(current_state_possible_events[i])]
                current_event_array = [int(x) for x in event_string]
                for j in range(len(event_string)):
                    if((current_state_possible_events_array[j] == current_event_array[j]) or (current_state_possible_events_array[j] == 2)):
                        check_event = check_event + 1
                        if(check_event == len(event_string)):
                            tem_array = [
                                int(x) for x in current_state_possible_events[i]]
                            event.data = tem_array
                            x = self.get_state_index(self.current_state)
                            y = self.get_event_index(event)
                            new_state = self.transitions[x][y]
                            previous_state = self.current_state
                            self.assign_state(new_state, previous_state, event)
                            if self.output_table[x][y] == -1:
                                output = Output([-1], "No Output")
                            else:
                                output = self.output_table[x][y]
                            self.display_machine()
                            return output

        return output

    def dev_help(self):
        print(self.states, self.events)
        x = len(self.states)
        y = len(self.events)
        for i in range(x):
            for j in range(y):
                if isinstance(self.transitions[i][j], int):
                    print(self.transitions[i][j])
                else:
                    print(self.transitions[i][j].name,
                          ' ', self.transitions[i][j].events)
        message = 'Length of States: %s\nLength of Events: %s' % (
            str(len(self.states)), str(len(self.events)))
        print(message)

    def run(self):
        path1 = input("Enter file name to load inputs: ")
        path2 = input("Enter file name to write outputs: ")
        load_file = open(path1, 'r')
        save_file = open(path2, 'w')
        if len(self.states) < 2:
            self.load('none')
        for line in load_file:
            l = line.rstrip()
            l = [int(x) for x in l]
            e = Event(l, 'Event')
            e.get_event()
            out = self.update_state(e)
            save_file.write(out.name + '\n')

        load_file.close()
        save_file.close()

    def autorun(self):
        gg.sys.stdout = gg.printout()
        if(len(self.states) == 0):
            self.load('none')
       # MV = mv.MachineVision(**mv.video)
       	MV = mv.MachineVision(**mv.options)
        MV.initialize()
        MV.getcolor()
        while(1):
            image,event_string = MV.oneLoop('1111')
            print(event_string)
            MV.gui.display(image)
            temp_data = [int(x) for x in event_string]
            new_event = Event(temp_data, 'Event TBD2 Saw')
            self.update_state(new_event)
            self.current_event.get_event()
