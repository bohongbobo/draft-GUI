##############################################################
#
#       Authors: Keith Sebald Jordan Ward Shipeng Yang and Bohong Li
#       Team: OUBB
#       Date: 10/13/18
#       Description: Beginning to make event and state classes for
#                    the car
#
#
#
#
##############################################################

import os;

test_descriptions = [["Car is ready", "Car is moving", "Car is finished"],
                     ["Car is not turning", "Car is turning left", "Car is turning right"],
                     ["Car is not avoiding", "Car is avoiding left car", "Car is avoiding right car"],
                     ["Car is not chasing", "Car is chasing"],
                     ["Normal course", "Shortcut Course"]]

event_descriptions = [["Red Light", "Green Light"],
                      ["Start Line", "Both Lines", "Only Left Line", "Only Right line", "Left Line Close",
                       "Right Line Close"],
                      ["No shortcut", "Shortcut Entrance", "Shortcut Exit"],
                      ["Horizontal Line", "Finish Line", "Horizontal Line Right", "Horizontal Line Left"],
                      ["No Other Cars", "Other Car Right", "Other Car Left", "Other Car Front"]]

g_status = "";


class StateMachine:
    name = "My State Machine"
    inputs = []
    states = []
    transitions = [[]]

    def __init__(self, name):
        self.name = name

    def add_state(self, new_state_name, new_state_data1, new_state_data2, new_state_data3, new_state_data4, new_state_data5, new_state_data6, inputs):
        ret = "";
        ret += new_state_name
        new_state_data = [new_state_data1, new_state_data2, new_state_data3, new_state_data4, new_state_data5,
                          new_state_data6]

        inps = inputs.split(' ');
        self.inputs = inps;
        new_state = state(new_state_data, new_state_name, inps)
        self.states.append(new_state)
        str = new_state.get_state()
        return str;
        return 'add state success';

    def add_input(self):
        input1 = input("What input would you like to look for?\n")
        self.inputs.append(input1)

    def display_inputs(self):
        ret = '';
        i = 0
        while i in range(len(self.inputs)):
            #print(self.inputs[i])
            ret += self.inputs[i] + ' ';
            i += 1
        return ret;

    def display_states(self):
        ret = '';
        i = 0
        while i in range(len(self.states)):
            ret += self.states[i].get_state()
            i += 1
        return ret;

    def save(self, path):
        self.inputs = []
        if len(path)==0:
            return 'you should enter the save file at save function';
        if os.path.exists(path):
            return 'the file ' + path + ' has exist on save function';
        with open(path, 'w') as save_file:
            first_line = [self.name, "\n", str(len(self.states))]
            save_file.writelines(first_line)
            save_file.write("\n")

            for z in self.states:
                self.inputs += z.inputs

            save_file.write(str(len(self.inputs)))
            save_file.write("\n")
            str1 = ' '.join(str(e) for e in self.inputs)
            save_file.write(str1 + "\n")

            for i in self.states:
                save_file.write(i.name + "\n")

                str2 = ''.join(str(e) for e in i.data)
                save_file.write(str2 + "\n")

                save_file.write(str(len(i.inputs)) + "\n")

                str3 = '\n'.join(str(e) for e in i.inputs)
                save_file.write(str3 + "\n")

            save_file.close()
            return 'save success to file :' + path;
        return 'open file ' + path + ' at save function failed';
        
    def load(self, path):
        if(len(path)==0):
            return 'you should enter an load file';
        if not os.path.exists(path):
            return 'the file ' + path + ' is not existed in the load function';
        with open(path, 'r') as save_file:
            str = '';
            line = save_file.readline().strip()
            smName = line
            sm = StateMachine(smName)
            str += "\nState Machine Name: " + smName + '\n';

            line = save_file.readline().strip()
            numStates = int(line)
            str += "Number of States: " + line + '\n';

            line = save_file.readline().strip()
            numInputs = int(line)
            str += "Number of Inputs: " + line + '\n';

            line = save_file.readline().strip()
            self.inputs = line.split()
            str += "List of Inputs: " + line + '\n'; #self.inputs;

            i = 0
            while (i < numStates):
                line = save_file.readline().strip()
                state_name = line
                str += "\nState Name: " + state_name + '\n';

                line = save_file.readline().strip()
                state_data = [int(e) for e in line]
                str += "State Data: " + line + '\n';

                line = save_file.readline().strip()
                numInputs = int(line)
                str += "Number of Inputs: " + line + '\n';

                str += "Inputs:";
                tempabc = []
                j = 0
                while (j < numInputs):
                    line = save_file.readline().strip()
                    state_input = line
                    tempabc.append(state_input);
                    str += state_input + ' ' + '\n';
                    self.transitions.append(line)

                    j += 1

                new_state = state(state_data, state_name, tempabc)
                self.states.append(new_state)

                i += 1

            save_file.close()
            str += "\nList of Transitions: ";
            for temp in self.transitions:
                if len(temp)>0:
                    str += temp + ' ';
            return str;
        return 'open file ' + path + 'failed';

class event:
    data = []
    name = "Base Event"
    descriptions = []

    def __init__(self, x, descriptions):
        self.data = x
        self.descriptions = descriptions

    def get_raw_event(self):
        return self.data

    def set_data(self, new_data):
        self.data = new_data

    def get_event(self):
        ret = "";
        i = 0
        printable_name = "-----Event Name: %s-----\n" % (self.name)
        ret += printable_name

        for i in range(len(self.data)):
            ret += self.descriptions[i][self.data[i]] + '\n';

        dashes = (len(printable_name) - 1) * "-"
        ret += dashes
        ret += "\n \n"
        return ret;


class state:
    name = "Base State"
    data = []  # [Traveling mode, Turn, Car avoidance, Chasing, Course Selection, Lap count max]
    descriptions = []
    inputs = []

    def __init__(self, data, name, inp):
        self.data = data
        self.name = name
        self.inputs = inp
        self.descriptions = test_descriptions

    def get_raw_state(self):
        return self.data

    def get_state(self):
        ret = "";
        i = 0
        printable_name = "-----State Name: %s-----\n" % (self.name)
        ret += printable_name
        for i in range(len(self.data) - 1):
            ret += self.descriptions[i][int(self.data[i])] + '\n';
        dashes = (len(printable_name)-1)*"-"
        ret += dashes
        ret += "\n"
        return ret;

    def update_state(self, event):
        string_event = ''.join(str(e) for e in event.data)

        if string_event == "00000":
            self.data = [0, 0, 0, 0, 0, 0]

        elif string_event == "10000":
            self.data = [1, 0, 0, 0, 0, 0]

        elif string_event == "01010":
            self.data = [2, 0, 0, 0, 0, 0]

        else:
            self.data = [0, 0, 0, 0, 0, 0]
machine = StateMachine("Drag Race");

def begin_menu(current_state, current_event, choice, stname, modedata, turndata, avoiddata, chasedata, csdata, noflaps, inputs):
    # choice = "default"
    global machine;
    valid_choices = ["help", "show state template", "show event template",
                     "show inputs", "add new input", "input event", "add state", "show states", "save", "load", "quit"]

    #machine = StateMachine("Drag Race")

    ret = "";
    global g_status;
    if g_status == "need_new_event":
        current_input = choice;
        while len(current_input) != 5 or not current_input.isdigit():
            ret += "New event must be 5 characters long and all characters must be integers, type 'Show Event Template' for help\n";
            ret += "New Event: ";
            return ret
        ret += "\n \n";
        temp_data = []
        i = 0
        while i < len(current_input):
            temp_data.append(int(current_input[i]))
            i += 1
        new_event = event(temp_data, event_descriptions)
        old_event = current_event
        current_event = new_event
        current_state.update_state(current_event)
        ret += current_state.get_state()
        ret += current_event.get_event()
        g_status = "";
        return ret;
    if (choice.lower() == "help"):
        ret = '''Commands: 
                    help 
                    Show State Template
                    Show Event Template 
                    Input Event 
                    add new input | show inputs
                    add state | show states
                    save | load\n'''

    if (choice.lower() == "show event template"):
        i = 0
        while i < len(current_event.descriptions):
            ret += str(current_event.descriptions[i]) + '\n';
            i += 1;
        ret += "\n \n";

    if (choice.lower() == "show state template"):
        i = 0
        while i < len(current_state.descriptions):
            ret += str(current_state.descriptions[i]) + '\n';
            i += 1
        ret += "\n \n";

    if (choice.lower() == "input event"):
        g_status = "need_new_event";
        ret += "New Event: ";

    if (choice.lower() not in valid_choices):
        ret += "Invalid command. Type 'help' to see all available commands.\n";

    if (choice.lower() == "save"):
        ret += machine.save(stname)
    if (choice.lower() == "load"):
        ret += machine.load(stname)

    if (choice.lower() == "add state"):
        if(len(stname)==0 or len(modedata)==0 or len(turndata)==0 or
                len(avoiddata)==0 or len(chasedata)==0 or len(csdata)==0 or
        len(noflaps)==0 ):
            return 'add state parameters invalid';
        try:
            a = int(modedata);
            b = int(turndata);
            c = int(avoiddata);
            d = int(chasedata);
            e = int(csdata);
            f = int(noflaps);
            if( a < 0 or a > 2 or 
                b< 0 or b > 2 or 
                c < 0 or c > 2 or
                d < 0 or d > 1 or 
                e < 0 or e > 1 or 
                f < 0 ):
                return 'Invalid input';
        except:
            return 'Invalid input';
        return machine.add_state(stname, modedata, turndata, avoiddata, chasedata, csdata, noflaps, inputs)
    if (choice.lower() == "add new input"):
        ret += machine.add_input()
    if (choice.lower() == "show inputs"):
        ret += machine.display_inputs()
    if (choice.lower() == "show states"):
        ret += machine.display_states()
    return ret;


def autorun(self):
    self.load()
    # MV = mv.MachineVision(**mv.video)
    MV = mv.MachineVision(**mv.options)
    MV.initialize()
    while(1):
        image,event_string = MV.oneLoop()
        MV.gui.display(image)

        temp_data = [int(x) for x in event_string]
        new_event = Event(temp_data, 'Event TBD2 Saw')
        self.update_state(new_event)
        self.current_event.get_event()

class main_wrap:
    def __init__(self):
        self._fff = "";

    def start_demonstration(self):
        ret = "";
        self.current_state = state([0, 0, 0, 0, 0, 0], "State", [])
        self.current_event = event([0, 0, 0, 0, 0], event_descriptions)

    def process_cmd(self, commandx, stname, modedata, turndata, avoiddata, chasedata, csdata, noflaps, inputs):
        return begin_menu(self.current_state, self.current_event, commandx, stname, modedata, turndata, avoiddata, chasedata, csdata, noflaps, inputs)


if __name__ == "__main__":
    v = main_wrap();
    v.start_demonstration();
    v.process_cmd("add state");

