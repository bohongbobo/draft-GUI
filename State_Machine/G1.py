from tkinter import *
from tkinter import ttk
import statemachine as SM
import sys
import subprocess
from state import State
from tkinter import simpledialog as SD
from tkinter import messagebox as MB
from tkinter import scrolledtext
sys.path.insert(0,'../MV')
import gui as gg

#inner_cui = main_wrap()
#str_result = inner_cui.start_demonstration()
#str_command=""
root = Tk()

lbtext = scrolledtext.ScrolledText(root)
lbtext.grid(row=1, column=3, columnspan=2, rowspan=30)

normal_out = sys.stdout



class printout():
    def write(self, s):
        lbtext.insert(END, s)

    def flush(self):
        pass

class printin():
    def write(self, s):
        lbtext.insert(END, s)

    def flush(self):
        pass


#sys.stdin = printin()





class Demo1:
    def __init__(self, master):
        self.master = master
        self.master.title("Cognitive State Machine Creator")
        self.master.geometry("1000x600")
        self.sm = SM.StateMachine('')
        self.lb1 = Label(self.master, text='Type a command: ')
        self.lb1.grid(row=0, column=0, columnspan=2)
        self.entry1 = Entry(self.master,bd=3)
        self.entry1.grid(row=1, column=0, columnspan=3)
        self.entry1.bind('<Return>', self.procComand)
        self.canvas = Canvas(self.master,bg='grey')
        self.canvas.grid(row=50, column=50, columnspan=2, rowspan=30)
        #self.entry1.bind('<Return>', self.procComand)
        self.canvas.create_text(100, 100, font=("Courier New", 12), text='test')
        #self.btnrun = Button(self.master, text='Run', width=12, command=self.procComand)
        #self.btnrun.grid(row=2, column=0, columnspan=2)
        #lbtext = Text(root)
        #lbtext.grid(row=1, column=3, rowspan=30)

        self.btnaddstate = Button(self.master, text='Add State', width=12, command = self.new_window)
        self.btnaddstate.grid(row=4, column=0, columnspan=2)
        self.btnshowstate = Button(self.master, text='Show State', width=12, command=self.show_state)
        self.btnshowstate.grid(row=5, column=0, columnspan=2)
        self.btneditstate = Button(self.master, text='Edit State', width=12, command=self.edit_states)
        self.btneditstate.grid(row=6, column=0, columnspan=2)
        self.btndeletestate = Button(self.master, text='Delete State', width=12, command=self.delete_state)
        self.btndeletestate.grid(row=7, column=0, columnspan=2)

        self.btnshowinput = Button(self.master, text='Show Event', width=12, command=self.show_event)
        self.btnshowinput.grid(row=10, column=0, columnspan=2)
        self.btnaddnewevent = Button(self.master, text='Add New Event', width=12, command = self.add_new_event)
        self.btnaddnewevent.grid(row=11, column=0, columnspan=2)
        self.btneditevent = Button(self.master, text='Edit Event', width=12, command=self.edit_events)
        self.btneditevent.grid(row=12, column=0, columnspan=2)
        self.btninputevent = Button(self.master, text='Input Event', width=12, command=self.input_events)
        self.btninputevent.grid(row=13, column=0, columnspan=2)

        self.btnshowouttable = Button(self.master, text='Output Table', width=12, command=self.show_out_table)
        self.btnshowouttable.grid(row=4, column=20, columnspan=2)
        self.btnshowoutput = Button(self.master, text='Show Output', width=12, command=self.show_output)
        self.btnshowoutput.grid(row=5, column=20, columnspan=2)
        self.btnsetoutput = Button(self.master, text='Set Output', width=12, command=self.set_output)
        self.btnsetoutput.grid(row=6, column=20, columnspan=2)


        self.btnaddtrans = Button(self.master, text='Add Transition',width=12, command=self.add_trans)
        self.btnaddtrans.grid(row=10, column=20, columnspan=2)
        self.btnshowtrans = Button(self.master, text='Show Transition', width=12, command=self.show_trans)
        self.btnshowtrans.grid(row=11, column=20, columnspan=2)
        self.btnedittrans  = Button(self.master, text='Edit Transition',width=12, command=self.edit_trans)
        self.btnedittrans.grid(row=12, column=20, columnspan=2)
        self.btnresettrans = Button(self.master, text='Reset Transition', width=12, command=self.reset_trans)
        self.btnresettrans.grid(row=13, column=20, columnspan=2)
        self.btndeletetrans = Button(self.master, text='Delete Transition', width=12, command=self.delete_trans)
        self.btndeletetrans.grid(row=14, column=20, columnspan=2)


        self.showmachine = Button(self.master, text='Show Machine', width=12, command=self.show_machine)
        self.showmachine.grid(row=30, column=20, columnspan=2)

        self.btnsave = Button(self.master, text='save', width=12, command=self.save)
        self.btnsave.grid(row=31, column=20, columnspan=2)
        self.btnload = Button(self.master, text='load', width=12, command=self.load)
        self.btnload.grid(row=32, column=20, columnspan=2)
        self.btnautorun = Button(self.master, text='Run', width=12, command=self.auto_run, highlightbackground='green')
        self.btnautorun.grid(row=33, column=20, columnspan=2)


        self.btnhelp = Button(self.master, text='Help', width=12, command=self.help_btn, highlightbackground='grey')
        self.btnhelp.grid(row=1, column=20, columnspan=2)
        self.quitButton = Button(self.master, text = 'Exit', width=12, command = self.quit, highlightbackground='grey')
        self.quitButton.grid(row=33, column=0, columnspan=2)


    def quit(self):
        sys.stdout = printout()
        answer = SD.askstring("WAIT!","Are you sure you want to quit? (Y/N)")
        if(answer.lower() == "y"):
            self.close_windows()
        else:
            pass
        sys.stdout = normal_out

    def input_events(self):
        self.sm.display_events()
        self.sm.input_event()

    def edit_events(self):
        self.sm.edit_event()

    def procComand(self, event=None):
        #self.sm.run()
        #global lbtext
        t2 = self.entry1.get()
        lbtext.insert(END, t2  + '\n')
        self.entry1.delete(0, END)
        '''
        self.str_result = inner_cui.process_cmd(self.entry1.get())
        self.lbtext.config(text=self.str_result)
        self.entry1.delete(0, 'end')
        '''

    def help_btn(self):
        sys.stdout = printout()
        print('Commands:  Autorun | Add State | Add Transition\n')
        print('           Input Event | Reset Transitions | Show events\n')
        print('           Show State Template | Show Event Template | Show output Template\n')
        print('           Show States | Show Transitions | Show outputs\n')
        print('           Save | Load | Quit | Help \n')
        #self.sm.show_descriptions()
        #self.sm.show_descriptions()
        #self.sm.show_descriptions()
        sys.stdout = normal_out
        """
        self.str_result0 = inner_cui.process_cmd("show state template")
        self.str_result2 = inner_cui.process_cmd("show event template")
        self.window = Toplevel(self.master)
        self.window.geometry("700x450")
        self.window.title('Help')
        self.lf = Label(self.window,
            text='''
            Commands:  Autorun | Add State | Add Transition\n')
                       Input Event | Reset Transitions | Show events\n')
                       Show State Template | Show Event Template | Show output Template\n')
                       Show States | Show Transitions | Show outputs\n')
                       Save | Load | Quit | Help \n''',
            font = ('courier', 13))
        self.lf.pack()
        self.name = Label(self.window,text="State")
        self.name.pack()
        self.fu = Label(self.window, text=self.str_result0)
        self.fu.pack()
        self.name1 = Label(self.window,text="Event")
        self.name1.pack()
        self.ff = Label(self.window, text=self.str_result2)
        self.ff.pack()
        """

    def save(self):
        sys.stdout = printout()
        file = SD.askstring("Save","What name should we save it as?")
        self.sm.save()
        sys.stdout = normal_out

    def load(self):
        sys.stdout = printout()
        file = SD.askstring("Load","What File should we load?")
        self.sm.load(file)
        MB.showinfo('SUCCESS', "File loaded Successfully")
        sys.stdout = normal_out


    def auto_run(self):
        file = SD.askstring("Load","Enter file name to load State Machine:")
        self.sm.load(file)

        self.VisionWindow = Toplevel(self.master)
        self.app = gg.GUI(self.VisionWindow)
        self.VisionWindow.destroy()

        self.sm.autorun()


    def show_event(self):
        sys.stdout = printout()
        self.sm.display_events()
        sys.stdout = normal_out
    def add_new_event(self):
        pass

    def show_state(self):
        sys.stdout = printout()
        self.sm.display_states()
        sys.stdout = normal_out
    def edit_states(self):
        sys.stdout = printout()
        self.sm.edit_state()
        sys.stdout = normal_out
    def delete_state(self):
        self.sm.del_state()

    def show_out_table(self):
        sys.stdout = printout()
        self.sm.show_output_table()
        sys.stdout = normal_out

    def set_output(self):
        pass

    def add_trans(self):
        sys.stdout = printout()
        self.sm.add_transition()
        sys.stdout = normal_out

    def edit_trans(self):
        sys.stdout = printout()
        self.sm.edit_transition()
        sys.stdout = normal_out

    def show_trans(self):
        sys.stdout = printout()
        self.sm.show_transition_table()
        sys.stdout = normal_out
    def reset_trans(self):
        self.sm.reset_transition_table()
        MB.showinfo('Reset', "All transitions reset")
    def delete_trans(self):
        pass

    def show_machine(self):
        sys.stdout = printout()
        self.sm.display_machine()
        sys.stdout = normal_out


    def show_output(self):
        sys.stdout = printout()
        self.sm.display_outputs()
        sys.stdout = normal_out


    def close_windows(self):
        self.master.destroy()

    def new_window(self):
        self.newWindow = Toplevel(self.master)
        self.app = Demo2(self.newWindow)


class Demo2:
    def __init__(self, master):
        self.master = master
        self.master.geometry("500x550")
        self.master.title("add state")

        self.lbA = Label(self.master, text="Add a new state,enter new state's name:  ").grid(row=0, column=0)
        self.entryA = Entry(self.master,bd=3)
        self.entryA.grid(row=0, column=2)

        self.lbB = Label(self.master, text="Enter traveling mode data:").grid(row=1, column=0)
        self.entryB = Entry(self.master,bd=3)
        self.entryB.grid(row=1, column=2)

        self.lbC = Label(self.master, text="Enter turning data: ").grid(row=2, column=0)
        self.entryC = Entry(self.master,bd=3)
        self.entryC.grid(row=2, column=2)

        self.lbD = Label(self.master, text="Enter avoidance data: ").grid(row=3, column=0)
        self.entryD = Entry(self.master,bd=3)
        self.entryD.grid(row=3, column=2)

        self.lbE = Label(self.master, text="Enter chasing data: ").grid(row=4, column=0)
        self.entryE = Entry(self.master,bd=3)
        self.entryE.grid(row=4, column=2)

        self.lbF = Label(self.master, text="Enter course selection: ").grid(row=5, column=0)
        self.entryF = Entry(self.master,bd=3)
        self.entryF.grid(row=5, column=2)

        self.lbG = Label(self.master, text="Enter number of laps: ").grid(row=6, column=0)
        self.entryG = Entry(self.master,bd=3)
        self.entryG.grid(row=6, column=2)

        self.quitButton = Button(self.master, text = 'Done', command = self.command).grid(row=10, column=2, columnspan=4)



    def command(self, event=None):

#        self.str_result = inner_cui.process_cmd(self.entryA.get())
        #self.lbtext.config(text=self.str_result)
        data = (self.entryB,self.entryC,self.entryD,self.entryE,self.entryF,self.entryG)
        name = self.entryA
        new_state = State(name,data)
        self.sm.add_state(new_state)
        self.entryA.delete(0, 'end')
        self.master.destroy()


    #def close_windows(self):
        #self.master.destroy()




def main():
    app = Demo1(root)
    #root.rowconfigure(2, minsize=100)
    root.rowconfigure(1, minsize=10)
    root.rowconfigure(2, minsize=10)
    root.rowconfigure(3, minsize=10)
    root.rowconfigure(4, minsize=10)
    root.rowconfigure(5, minsize=10)
    root.rowconfigure(6, minsize=10)
    root.rowconfigure(7, minsize=10)
    root.rowconfigure(8, minsize=10)
    root.rowconfigure(9, minsize=10)
    root.rowconfigure(10, minsize=10)
    root.rowconfigure(11, minsize=10)
    root.rowconfigure(10, minsize=10)
    root.rowconfigure(11, minsize=10)
    root.rowconfigure(12, minsize=10)
    root.rowconfigure(13, minsize=10)
    root.rowconfigure(14, minsize=10)
    root.rowconfigure(15, minsize=10)
    root.rowconfigure(16, minsize=10)
    root.rowconfigure(17, minsize=10)
    root.rowconfigure(18, minsize=10)
    root.rowconfigure(19, minsize=10)

    root.rowconfigure(25, minsize=10)
    root.rowconfigure(26, minsize=10)
    root.rowconfigure(27, minsize=10)
    root.rowconfigure(28, minsize=10)
    root.rowconfigure(29, minsize=10)
    root.rowconfigure(30, minsize=10)
    root.rowconfigure(31, minsize=10)
    root.rowconfigure(32, minsize=10)
    root.mainloop()

if __name__ == '__main__':
    main()
