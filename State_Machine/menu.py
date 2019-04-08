from statemachine import StateMachine


# main menu, check if input is valid, if it is valid, go into different branches
def begin_menu(current_state, current_event, current_output):
    choice = 'default'

    valid_choices = ['help', 'show state template', 'show event template', 'show output template',

                     'show events', 'add new input', 'input event', 'add state', 'add output', 'set output',

                     'show states', 'save', 'load', 'show machine', 'show transitions', 'show output table',

                     'reset transitions', 'add transition', 'edit transition', 'show outputs', 'dev help','delete event',
                     
                     'edit event','edit state','delete state','quit','autorun']

    default_state = current_state
    default_event = current_event
    default_output = current_output

    machine = StateMachine('Your State Machine')

    while choice.lower() != 'quit':

        choice = input('Type a command, Type in "Help" for menu: ')

        print('\n')

        if choice.lower() == 'help':
            print('Commands:  Show State Template  | Show States  | Add State     | Edit State  | delete state |\n') #State
            print('           Show Event Template  | Show Events  | Add New Input | Edit Event  | Input Event  |\n') #Event
            print('           Show Output Template | Show Outputs | Set Output  | \n') #Output
            print('           Show Transitions| Show Output Table | Reset Transitions | Edit Transition   | Delete Transition |\n') #Transition
            print('           Show Machine | Add Transition | Autorun\n')           
            print('           Save | Load | Quit | Help \n')

        if choice.lower() == 'show event template':
            default_event.show_descriptions()

        if choice.lower() == 'show state template':
            default_state.show_descriptions()

        if choice.lower() == 'show output template':
            default_output.show_descriptions()

        if choice.lower() == 'add transition':
            if len(machine.states) >= 2:
                machine.add_transition()
            else:
                print('Please Make 2 states before adding a transition')

        if choice.lower() == 'dev help':
            machine.dev_help()

        if choice.lower() == 'edit transition':
            machine.edit_transition()

        if choice.lower() == 'show transitions':
            machine.show_transition_table()

        if choice.lower() == 'reset transitions':
            machine.reset_transition_table()

        if choice.lower() == 'show machine':
            machine.display_machine()

        if choice.lower() == 'input event':
            machine.display_events()
            machine.input_event()

        if choice.lower() == 'run':
            machine.run()

        if choice.lower() == 'save':
            machine.save()

        if choice.lower() == 'load':
            machine.load()
            machine.assign_state(machine.states[0], machine.states[0], default_event)

        if choice.lower() == 'add state':
            machine.display_states()
            machine.add_state()

        if choice.lower() == 'edit state':
            machine.edit_state()
        
        if choice.lower() == 'delete state':
            machine.del_state()
        
        if choice.lower() == 'edit event':
            machine.edit_event()

        if choice.lower() == 'delete event':
            machine.del_event()

        if choice.lower() == 'show events':
            machine.display_events()

        if choice.lower() == 'show outputs':
            machine.display_outputs()

        if choice.lower() == 'show output table':
            machine.show_output_table()

        if choice.lower() == 'show states':
            machine.display_states()

        if choice.lower() == 'autorun':
            machine.autorun()

        if choice.lower() not in valid_choices:
            print('Invalid command. Type \'help\' to see all available commands.\n')
