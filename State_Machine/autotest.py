import unittest
from statemachine import StateMachine
from event import Event
from state import State
from output import Output

test_machine = StateMachine("blah")
test_machine.load()


class SmUnitTests(unittest.TestCase):

    def test_States_is_state(self):
        for i in range(len(test_machine.states)):
            self.assertIsInstance(test_machine.states[i],State)


    def test_Events_is_events(self):
        for i in range(len(test_machine.events)):
            self.assertIsInstance(test_machine.events[i],Event)

    def test_statedata_is_int(self):
        for i in range(len(test_machine.states)):
            for j in test_machine.states[i].data:
                self.assertIsInstance(test_machine.states[i].data[j],int)

    def test_eventdata_is_int(self):
        for i in range(len(test_machine.events)):
            for j in test_machine.events[i].data:
                self.assertIsInstance(test_machine.events[i].data[j],int)

    def test_outputdata_is_int(self):
        for i in range(len(test_machine.outputs)):
            for j in test_machine.outputs[i].data:
                self.assertIsInstance(test_machine.outputs[i].data[j],int)

    def test_trans_table_is_good(self):
        x = len(test_machine.states)
        y = len(test_machine.events)
        for i in range(x):
            for j in range(y):
                self.assertTrue(isinstance(test_machine.transitions[i][j],int) or isinstance(test_machine.transitions[i][j],State))

    def test_out_table_is_good(self):
        x = len(test_machine.states)
        y = len(test_machine.events)
        for i in range(x):
            for j in range(y):
                self.assertTrue(isinstance(test_machine.output_table[i][j],int) or isinstance(test_machine.output_table[i][j],Output))
