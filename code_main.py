import pandas as pd
import tkinter as tk
from datetime import datetime
from tkinter import messagebox
from tkinter import filedialog
import io
import pyperclip
import webbrowser
import random

#Main Codeblock for Application
#Competitor Class
class Competitor:
    def __init__(self, name):
        self.name = name
        self.end_time = None

##Category Class
class Category:
    def __init__(self):
        self.competitors = []

    def add_competitor(self, competitor):
        self.competitors.append(competitor)

# global variables
df = pd.DataFrame(columns=['Climber', 'In the chair', 'Starts Climbing', 'Ends Climbing'])

#Creating global functions to convert to and from a Seconds based timescale.
def secondsto_time(input_seconds):      #Turns seconds into a normal display of time
    hours = input_seconds // 3600
    minutes = (input_seconds % 3600) // 60
    seconds = input_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def timeto_seconds(hour = 0, minute = 0, second = 0):   #Turns Normal display of time into seconds
    hourseconds = (hour * 60) * 60
    minuteseconds = minute * 60
    totalseconds = second + minuteseconds + hourseconds
    return totalseconds

#Generating the times for each climber
def generate_startend_times(category):
    global txt_printedinfo
    global df
    current_time = convert_starttime()
    round_length = get_boulderlength()
    transition_length = get_transtime()
    boulders_per_round = get_numofboulders()
    single_round = round_length + transition_length
    info = ""
    for climber in category.competitors:
        end_time = current_time + (single_round * ((boulders_per_round * 2) + 1) - transition_length) #Now accounts for variable boulders in round
        chairtime = current_time - single_round
        #Add row to Dataframe
        df.loc[len(df)] = [climber.name,
                           secondsto_time(chairtime),
                           secondsto_time(current_time),
                           secondsto_time(end_time)]
                        
        info += f"{climber.name} In the chair by {secondsto_time(chairtime)}, starts climbing at {secondsto_time(current_time)}, and ends climbing at {secondsto_time(end_time)}\n"
        #Adds time, loops back through
        current_time += (round_length + transition_length)
    if txt_printedinfo:
        txt_printedinfo.insert(tk.END, info)
    else:
        print("Error: txt_printedinfo is not defined")


#Popup Messages
class PopupMessage:
    @staticmethod
    def starttime_error():
        messagebox.showinfo("Time Error", "Please use military time format\nfor time entries\nExample: 13:45")

    @staticmethod
    def boulderlength_error():
        messagebox.showinfo("Time Error", "Please use MM:SS format\nExample: 4:15 = 4 minutes 15 seconds")

    @staticmethod
    def complist_error():
        messagebox.showinfo("List Error", "Please provide at least one competitor\nin the List of Competitors field")

    @staticmethod
    def sucess_copy():
        messagebox.showinfo('Sucess', 'Text copied to clipboard!')
    
    @staticmethod
    def fail_copy():
        messagebox.showinfo('Warning', 'There was an error and text did not copy')

#Functions to gather information from the user
def create_dataframe():
    df = pd.DataFrame(columns=['Climber', 'In the chair', 'Starts Climbing', 'Ends Climbing'])       

def get_info():
    #Gathering all fields before processing information
    convert_starttime()
    get_boulderlength()
    get_transtime()
    get_numofboulders()
    competitors = get_names()
    category = Category()
    for competitor in competitors:
        category.add_competitor(competitor)

    generate_startend_times(category)

def convert_starttime():
    time_start = ntry_compstart_time.get()
    try:
        time_obj = datetime.strptime(time_start, "%H:%M")
        hour = time_obj.hour
        minute = time_obj.minute
        convert_seconds = int(timeto_seconds(hour, minute))
        #print(f'{hour} hours {minute} minutes, is equal to {convert_seconds} seconds')
        return convert_seconds
    except ValueError:
        PopupMessage.starttime_error()

def get_boulderlength():
    boulderlength = ntry_roundlength.get()
    try:
        time_split = datetime.strptime(boulderlength, "%M:%S")
        hour = 0
        minute = time_split.minute
        second = time_split.second
        converted_seconds = int(timeto_seconds(hour, minute, second))
        return converted_seconds
    except ValueError:
        PopupMessage.boulderlength_error()

def get_transtime(transition_length= 15):
    transition_length = int(spnbx_transtime.get())
    return transition_length

def get_numofboulders(numofboulders= 4):
    numofboulders = int(spnbx_numofboulders.get())
    return numofboulders
    
def get_names():
    #Retrieve text from the Competitorlist text box
    names_fromtext = txt_competlist.get('1.0', 'end').strip()
    names_list = names_fromtext.split('\n')
    names_list = [name.strip() for name in names_list if name.strip()]  #Filters out any empty strings
    if not names_list:
        PopupMessage.complist_error()
    else:
        competitors = [Competitor(name) for name in names_list]
        return competitors
    
#Button functions for the new window
def copy_to_clipboard():
    text_to_copy = txt_printedinfo.get('1.0', 'end-1c')
    if text_to_copy:
        pyperclip.copy(text_to_copy)
        PopupMessage.sucess_copy()
    else:
        PopupMessage.fail_copy()

def saveas_csv():
    file_path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV files', '*.csv')])
    if file_path:
        df.to_csv(file_path, index= False)

def copy_csv():
    csv_data = df.to_csv(index=False)
    pd.read_csv(io.StringIO(csv_data)).to_clipboard(index=False, sep= ',')  #seperated by comma
    if csv_data:
        PopupMessage.sucess_copy()
    else:
        PopupMessage.fail_copy()

def clear_button():
    #Clears entry widgets
    ntry_compstart_time.delete(0, 'end')
    ntry_roundlength.delete(0, 'end')
    txt_competlist.delete('1.0', 'end')

def random_button():
    names_fromtext = txt_competlist.get('1.0', 'end').strip()
    names_list = names_fromtext.split('\n')
    random.shuffle(names_list)
    
    txt_competlist.delete('1.0', 'end')
    for name in names_list:
        txt_competlist.insert('end', name + '\n')

def open_browser():
    url = 'https://www.intervaltimer.com/create/hiit-timer'
    webbrowser.open(url)
    
#Functions for opening new windows, for printed info and CSV info
def open_printed_window():
    global txt_printedinfo
    printed_window = tk.Toplevel(window)
    printed_window.title("Running Order Information")
    printed_window.geometry('800x600')
    #Add widgets to the window here
    fme_printedinfo = tk.Frame(master= printed_window, bg= 'lightgrey')
    fme_printedinfo.pack(expand= True, fill= tk.BOTH, padx= 5, pady= 20)

    txt_printedinfo = tk.Text(master= fme_printedinfo)
    txt_printedinfo.grid(row= 0, column= 0, padx= 5, pady= 20, sticky= 'nsew')

    fme_printedinfo_btns = tk.Frame(master= fme_printedinfo)
    fme_printedinfo_btns.grid(row= 1, column= 0, sticky= 'nsew')

    btn_printedinfo_copy = tk.Button(fme_printedinfo_btns, text='Copy to Clipboard', command= copy_to_clipboard)
    btn_printedinfo_copy.grid(row= 0, column= 0, padx= 5)

    btn_printedinfo_view = tk.Button(fme_printedinfo_btns, text= 'Save as CSV file\n(for exporting to excel/sheets)', command= saveas_csv)
    btn_printedinfo_view.grid(row= 0, column= 1, padx= 5)

    btn_printedinfo_save = tk.Button(fme_printedinfo_btns, text= 'Copy CSV to clipboard', command= copy_csv)
    btn_printedinfo_save.grid(row= 0, column= 2, padx= 5)

    btn_openbrowser = tk.Button(fme_printedinfo_btns, text= 'Create Timer\n(in browser)', command= open_browser)
    btn_openbrowser.grid(row= 1, column= 1)

    fme_printedinfo.rowconfigure(0, weight= 1)
    fme_printedinfo.columnconfigure(0, weight= 1)
    fme_printedinfo_btns.columnconfigure(0, weight= 1)
    fme_printedinfo_btns.columnconfigure(1, weight= 1)
    fme_printedinfo_btns.columnconfigure(2, weight= 1)

#Setting up layout for application
window = tk.Tk()
window.title('Running Order Generator')

fme_main = tk.Frame(master= window, width=1000, height= 600, bg= 'lightgrey')
fme_main.pack(expand= True, fill=tk.BOTH)
txt_printedinfo = None

fme_timeentry = tk.Frame(master= fme_main, relief= 'ridge', borderwidth= 5, padx= 5, pady= 5)
fme_timeentry.grid(row=0, column= 0, sticky= 'nsew')

fme_competitors = tk.Frame(master= fme_main, relief= 'ridge', borderwidth= 5, padx= 10, pady= 10)
fme_competitors.grid(row= 0, column= 2, sticky= 'nsew')

fme_buttons = tk.Frame(master= fme_main, bg= 'lightgrey')
fme_buttons.grid(row= 2, column= 2)

#Column Weights
fme_main.grid_columnconfigure(0, weight= 1, minsize= 50)
fme_main.grid_columnconfigure(1, weight= 2, minsize= 50)

#Start Time Entry
lbl_compstart_time = tk.Label(master= fme_timeentry, text= 'Competition \n Start Time')
lbl_compstart_time.grid(row= 0, column= 0, padx=5, pady=20)

ntry_compstart_time = tk.Entry(master= fme_timeentry, width= 15)
ntry_compstart_time.grid(row= 0, column= 1, padx=5, pady=5)

#Round Length Entry
lbl_roundlength = tk.Label(master= fme_timeentry, text='Time per Boulder')
lbl_roundlength.grid(row= 2, column= 0, padx=5, pady=20)

ntry_roundlength = tk.Entry(master=fme_timeentry, width= 10)
ntry_roundlength.grid(row= 2, column= 1, padx=5, pady=5)

#Transition Time Entry
lbl_transtime = tk.Label(master= fme_timeentry, text= 'Transition Time \n inbetween boulders \n (seconds)')
lbl_transtime.grid(row= 3, column= 0, padx=5, pady=20)

spnbx_transtime = tk.Spinbox(master= fme_timeentry, values= tuple(range(5, 65, 5)), width= 15)
spnbx_transtime.grid(row= 3, column= 1, padx=5, pady=20)

#Number of Boulders Entry
lbl_numofboulders = tk.Label(master= fme_timeentry, text= 'Boulders in the Round')
lbl_numofboulders.grid(row= 4, column= 0, padx=5, pady=20)

spnbx_numofboulders = tk.Spinbox(master= fme_timeentry, values= tuple(range(1, 11)), width= 3)
spnbx_numofboulders.grid(row= 4, column= 1, padx=5, pady=5)

#Competitors Entry
lbl_competlist = tk.Label(master=fme_competitors, text= 'List of Competitors \n (Seperated by new line)')
lbl_competlist.grid(row= 0,column= 0, padx= 5, pady= 20)

txt_competlist = tk.Text(master= fme_competitors, width= 20, height= 20)
txt_competlist.grid(row= 0, column= 1)

#Buttons
btn_clear = tk.Button(fme_buttons, text= 'CLEAR', bg= 'red', fg= 'white', command= clear_button)
btn_clear.grid(row= 0, column= 0, padx=5, pady=20)

btn_enter = tk.Button(fme_buttons, text= 'Submit', command= lambda: [open_printed_window(), get_info()])
btn_enter.grid(row= 0, column= 1, padx=5, pady=20)

btn_randomize = tk.Button(fme_competitors, text= 'Randomize Competitors', command= random_button)
btn_randomize.grid(row= 1, column= 1, padx= 0, pady= 5)

window.mainloop()