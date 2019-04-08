import os
from event import Event
from state import State
from output import Output
from menu import begin_menu


def run_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    default_state = State([0, 0, 0, 0, 0, 0], 'Default State')
    default_event = Event([0, 0, 0, 0, 0], 'Default Event')
    default_output = Output([0, 0, 0, 0, 0, 0], 'Default Output')
    begin_menu(default_state, default_event, default_output)


run_menu()
