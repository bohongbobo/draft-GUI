
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
#from tkinter import scrolledtext

from event_states_gui import *

inner_cui = main_wrap()

#initial
newstatename = ''
newmodedata = ''
newturndata = ''
newavoidancedata = ''
newchasedata = ''
newcourseselection = ''
newnumberoflaps = ''
newinputs = ''

fname = ''
lfname = ''

#add state frame
configwin = Tk()
configwin.withdraw()

#save frame
add_window = Tk()
add_window.withdraw()

#load frame
get_window = Tk()
get_window.withdraw()

#entry boxes for save and load function
file_name = Entry(add_window)
get_name = Entry(get_window)

#close all the window
def exitProg():
    get_window.destroy()
    add_window.destroy()
    configwin.destroy()
    root.destroy()
    exit()

#get command
def procComand(event=None):
    str_result = inner_cui.process_cmd(entry1.get(), '', '', '', '', '', '', '', '')
    text.config(text=str_result)
    entry1.delete(0, 'end') #clear the entry box every time after run the command

#command for help button
def procHelp():
    str_result0 = inner_cui.process_cmd("show state template", '', '', '', '', '', '', '', '')
    str_result2 = inner_cui.process_cmd("show event template", '', '', '', '', '', '', '', '')
    str_result3 = inner_cui.process_cmd("show output template", '', '', '', '', '', '', '', '')
    window = Toplevel(root) #pop a window to show the information
    window.geometry("700x530") #size of the frame
    window.title('Event State Template')

    name = Label(window,text="State")
    name.pack()
    fu = Label(window, text=str_result0)
    fu.pack()
    name1 = Label(window,text="Event")
    name1.pack()
    ff = Label(window, text=str_result2)
    ff.pack()
    name2 = Label(window, text="Output")
    name2.pack()
    ffu = Label(window, text=str_result3)
    ffu.pack()

#command to get date from multiple entry boxes
def procAddState():
    global configwin
    global newstatename
    global newmodedata
    global newturndata
    global newavoidancedata
    global newchasedata
    global newcourseselection
    global newnumberoflaps
    global newinputs
    newstatename = eystatename.get()
    newmodedata = eymodedata.get()
    newturndata = eyturndata.get()
    newavoidancedata = eyavoidancedata.get()
    newchasedata = eychasedata.get()
    newcourseselection = eycourseselection.get()
    newnumberoflaps = eynumberoflaps.get()
    newinputs = eyinputs.get()
    str_result = inner_cui.process_cmd("add state", newstatename, newmodedata, newturndata, newavoidancedata,
                                       newchasedata, newcourseselection, newnumberoflaps, newinputs)
    text.config(text=str_result)
    messagebox.showinfo("Succeed", "Your data has been added!")

#creating a new window for user to entry data in order to add states
def procShowConfigWindow():
    configwin = Tk()
    configwin.title('add state')
    configwin.geometry('500x550')
    lbstatename = Label(configwin, text="Add a new state,enter new state's name:")
    lbmodedata = Label(configwin, text='Enter traveling mode data:')
    lbturndata = Label(configwin, text='Enter turning data:')
    lbavoidancedata = Label(configwin, text='Enter avoidance data:')
    lbchasedata = Label(configwin, text='Enter chasing data:')
    lbcourseselection = Label(configwin, text='Enter course selection:')
    lbnumberoflaps = Label(configwin, text='Enter number of laps:')
    lbinputs = Label(configwin, text='Inputs, seperate by space')

    global eystatename
    global eymodedata
    global eyturndata
    global eyavoidancedata
    global eychasedata
    global eycourseselection
    global eynumberoflaps
    global eyinputs

#entry boxes for add state
    eystatename = Entry(configwin,bd=3)
    eymodedata = Entry(configwin,bd=3)
    eyturndata = Entry(configwin,bd=3)
    eyavoidancedata = Entry(configwin,bd=3)
    eychasedata = Entry(configwin,bd=3)
    eycourseselection = Entry(configwin,bd=3)
    eynumberoflaps = Entry(configwin,bd=3)
    eyinputs = Entry(configwin,bd=3)

    btndoneset = ttk.Button(configwin, text='Add', command=procAddState)
    btncloseset = ttk.Button(configwin, text='Cancel', command=configwin.destroy)
    lbstatename.grid(row=0, column=0)
    eystatename.grid(row=0, column=1)
    lbmodedata.grid(row=1, column=0)
    eymodedata.grid(row=1, column=1)
    lbturndata.grid(row=2, column=0)
    eyturndata.grid(row=2, column=1)
    lbavoidancedata.grid(row=3, column=0)
    eyavoidancedata.grid(row=3, column=1)
    lbchasedata.grid(row=4, column=0)
    eychasedata.grid(row=4, column=1)
    lbcourseselection.grid(row=5, column=0)
    eycourseselection.grid(row=5, column=1)
    lbnumberoflaps.grid(row=6, column=0)
    eynumberoflaps.grid(row=6, column=1)
    lbinputs.grid(row=7, column=0)
    eyinputs.grid(row=7, column=1)
    btndoneset.grid(row=8, column=1)
    btncloseset.grid(row=8,column=0)
    configwin.update()

def proinputevent():
    str_result = inner_cui.process_cmd('input event','', '', '', '', '', '', '', '')
    text.config(text=str_result)


#commmand for show input button
def procShowInput():
    str_result = inner_cui.process_cmd('show inputs', '', '', '', '', '', '', '', '')
    text.config(text=str_result)


#command for show state Button
def procShowState():
    str_result = inner_cui.process_cmd('show states', '', '', '', '', '', '', '', '')
    text.config(text=str_result)

#commmand for save button
def procSave():
    global add_window
    global fname
    fname=file_name.get()
    str_result = inner_cui.process_cmd('save', fname, '', '', '', '', '', '', '')
    text.config(text=str_result)
    file_name.delete(0, 'end')

    messagebox.showinfo("Succeed", "Your file has been saved!")

#command for load button
def procLoad():
    global get_window
    global lfname
    lfname=get_name.get()
    str_result = inner_cui.process_cmd('load', lfname, '', '', '', '', '', '', '')
    text.config(text=str_result)
    get_name.delete(0, 'end')

#creating a window for save button
def save_func():
    add_window = Tk() #new window for save function
    add_window.title('Save')
    add_window.geometry('400x80')

    FileName = Label(add_window, text='Please Enter the file name: ')
    global file_name

    file_name = Entry(add_window, bd=3)

    savebtn = ttk.Button(add_window, text='save', command=procSave)
    close_add = ttk.Button(add_window, text='Cancel', command=add_window.destroy)

    FileName.grid(row=0,column=0)
    file_name.grid(row=0,column=1)
    savebtn.grid(row=1,column=1)
    close_add.grid(row=1, column=0)


#creating a window for load button
def load_func():
    get_window = Tk() #new window for load function
    get_window.title('Load')
    get_window.geometry('400x80')

    LFileName = Label(get_window, text='Please Enter the file name: ')
    global get_name

    get_name = Entry(get_window, bd=3)

    loadbtn = ttk.Button(get_window, text='load', command=procLoad)
    close_load = ttk.Button(get_window, text='Cancel', command=get_window.destroy)

    LFileName.grid(row=0,column=0)
    get_name.grid(row=0,column=1)
    loadbtn.grid(row=1,column=1)
    close_load.grid(row=1, column=0)


def protranswin():
    pass

def proedittranswin():
    pass

def proshowtrans():
    pass

def proreset():
    pass

def proShowMachine():
    pass

def proshowoutput():
    pass

def auto_run():
    str_result = inner_cui.process_cmd('auto', '', '', '', '', '', '', '', '')
    text.config(text=str_result)

str_result = inner_cui.start_demonstration()
str_command=""

#main window components
root = Tk()
lb1 = Label(root, text='Type something below')
entry1 = Entry(root,bd=3)
entry1.bind('<Return>', procComand)
btn1 = ttk.Button(root, text='run', width=12, command=procComand)
btnhelp = ttk.Button(root, text='Help', width=12, command=procHelp)

btninputevent = ttk.Button(root, text='Input Event', width=12, command=proinputevent)
btnaddstate = ttk.Button(root, text='Add State', width=12, command=procShowConfigWindow)
btnshowinput = ttk.Button(root, text='Show event', width=12, command=procShowInput)
btnshowstate = ttk.Button(root, text='Show State', width=12, command=procShowState)


btnaddtrans = ttk.Button(root, text='Add Transition',width=12,command=protranswin)
btnedittrans  = ttk.Button(root, text='Edit Transition',width=12,command=proedittranswin)
btnshowtrans = ttk.Button(root, text='Show Transition', width=12,command=proshowtrans)
resettrans = ttk.Button(root, text='Reset Transition', width=12, command=proreset)
showmachine = ttk.Button(root, text='Show Machine', width=12, command=proShowMachine)
showoutput = ttk.Button(root, text='Show Output', width=12, command=proshowoutput)
autorun = ttk.Button(root, text='Autorun', width=12, command=auto_run)


text = Label(root, text=str_result, padx=0, pady=0)

btnsave = ttk.Button(root, text='save', width=12, command=save_func)
btnload = ttk.Button(root, text='load', width=12, command=load_func)
btn3 = ttk.Button(root, text='Exit', width=12, command=exitProg)

#place everything in certain position
class App:
    def __init__(self, master):

        # lay the controls
        lb1.grid(row=0, column=0, columnspan=2)
        entry1.grid(row=1, column=0, columnspan=3)
        btn1.grid(row=2, column=0, columnspan=2)
        btnhelp.grid(row=3, column=0, columnspan=2)

        btninputevent.grid(row=4, column=0, columnspan=2)
        btnaddstate.grid(row=5, column=0, columnspan=2)
        btnshowinput.grid(row=6, column=0, columnspan=2)
        btnshowstate.grid(row=7, column=0, columnspan=2)

        btnaddtrans.grid(row=8, column=0, columnspan=2)
        btnedittrans.grid(row=9, column=0, columnspan=2)
        btnshowtrans.grid(row=10, column=0, columnspan=2)
        resettrans.grid(row=11, column=0, columnspan=2)
        showmachine.grid(row=12, column=0, columnspan=2)
        showoutput.grid(row=13, column=0, columnspan=2)
        autorun.grid(row=14, column=0, columnspan=2)

        text.grid(row=1, column=3, columnspan=2, rowspan=20)

        btnsave.grid(row=25, column=0, columnspan=2)
        btnload.grid(row=26, column=0, columnspan=2)
        btn3.grid(row=27, column=0, columnspan=2)

#main function
if __name__ == '__main__':
    root.title("Event States")
    root.geometry("800x720")
    root.rowconfigure(1, minsize=40)
    root.rowconfigure(2, minsize=40)
    root.rowconfigure(3, minsize=40)
    root.rowconfigure(4, minsize=40)
    root.rowconfigure(5, minsize=40)
    root.rowconfigure(6, minsize=40)
    root.rowconfigure(7, minsize=40)
    root.rowconfigure(8, minsize=40)
    root.rowconfigure(9, minsize=40)
    root.rowconfigure(10, minsize=40)
    root.rowconfigure(11, minsize=40)
    root.rowconfigure(10, minsize=40)
    root.rowconfigure(11, minsize=40)
    root.rowconfigure(12, minsize=40)
    root.rowconfigure(13, minsize=40)
    root.rowconfigure(25, minsize=30)
    root.rowconfigure(26, minsize=30)
    root.rowconfigure(27, minsize=30)
    display = App(root)
    root.mainloop()
