# Current Build 3/12/2025
import csv
import tkinter as tk
from datetime import datetime
from tkinter import messagebox
from tkinter import filedialog
import pyperclip
from random import shuffle
from pygame import mixer

class Competitor:
    def __init__(self, name):
        self.name = name
        self.end_time = None

class Category:
    def __init__(self):
        self.competitors = []

    def add_competitor(self, competitor):
        self.competitors.append(competitor)

# global variables
results = []

# Time Conversions and Data Processing Functions
def secondsto_time(input_seconds):
    """Converts seconds into a normal display of time"""
    hours = input_seconds // 3600
    minutes = (input_seconds % 3600) // 60
    seconds = input_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def timeto_seconds(hour = 0, minute = 0, second = 0):
    """Converts Normal display of time into seconds"""
    return (hour * 3600) + (minute * 60) + second

def convert_starttime():
    """Converts the start time to seconds"""
    time_start = ntry_compstart_time.get()
    try:
        time_obj = datetime.strptime(time_start, "%H:%M")
        hour = time_obj.hour
        minute = time_obj.minute
        convert_seconds = int(timeto_seconds(hour, minute))
        #print(f'{hour} hours {minute} minutes, is equal to {convert_seconds} seconds')
        return convert_seconds
    except ValueError:
        PopupMessage.show_error("Time Error", "Please use military time format\nfor time entries\nExample: 13:45")
        return None

def get_boulderlength():
    """Converts the boulder length to seconds"""
    boulderlength = ntry_roundlength.get()
    try:
        minutes, seconds = map(int, boulderlength.split(':'))
        converted_seconds = int(timeto_seconds(0, minutes, seconds))
        return converted_seconds
    except ValueError:
        PopupMessage.show_error("Time Error", "Please use MM:SS format\nExample: 4:15 = 4 minutes 15 seconds")
        return None

def get_transtime():
    """Retrieves the transition time between boulders"""
    return int(spnbx_transtime.get())

def get_numofboulders(numofboulders= 4):
    """Retrieves the number of boulders in the round"""
    return int(spnbx_numofboulders.get())
    
def get_names():
    """Retrieve text from the Competitorlist text box"""
    names = txt_competlist.get('1.0', 'end').strip().split("\n")
    names = [name.strip() for name in names if name.strip()]
    return [Competitor(name) for name in names]

# Competition Logic
def display_results():
    """Displays results in the text box."""
    if txt_printedinfo:
        txt_printedinfo.delete("1.0", tk.END)
        for row in results:
            txt_printedinfo.insert(tk.END, f"{row['Climber']} - Chair Time: {row['Next Up']}, "
                                           f"Climb Time: {row['Start Climbing']}, Ends: {row['End Climbing']}\n")

def generate_startend_times(category):
    """Generates and stores the start and end times for each climber in the category"""
    global results
    results.clear()
    current_time = convert_starttime()
    round_length = get_boulderlength()
    transition_length = get_transtime()
    boulders_per_round = get_numofboulders()
    single_round = round_length + transition_length
    for climber in category.competitors:
        end_time = current_time + (single_round * ((boulders_per_round * 2) + 1) - transition_length) #Now accounts for variable boulders in round
        chairtime = current_time - single_round
        #Add row to Dictionary
        results.append({
            "Climber": climber.name,
            "Next Up": secondsto_time(chairtime),
            "Start Climbing": secondsto_time(current_time),
            "End Climbing": secondsto_time(end_time)
        })              

        current_time += (round_length + transition_length)
    display_results()

def get_info():
    """Gathering all fields before processing information. Also handles error checking."""
    start_time = convert_starttime()
    boulder_length = get_boulderlength()
    if boulder_length is None:
        return
    if boulder_length < 10:
        PopupMessage.show_error("Time Error", "Boulder lengh must be at least 10 seconds")
        return
    
    transition_time = get_transtime()
    if transition_time < 5:
        PopupMessage.show_error("Time Error", "Transition time must be at least 5 seconds")
        return
    
    num_boulders = get_numofboulders()
    if num_boulders <= 0:
        PopupMessage.show_error("Number of Boulders Error", "Number of boulders must be at least 1")
        return
    
    competitors = get_names()
    if not competitors:
        PopupMessage.show_error("List Error", "Please provide at least one competitor")
        return

    # Check if any function raises an error
    if start_time is None or boulder_length <= 5 or transition_time < 5 or num_boulders == 0 or not competitors:
        return
    
    category = Category()
    for competitor in competitors:
        category.add_competitor(competitor)

    open_printed_window()
    generate_startend_times(category)
    set_timer_durations()

# Button/Action Functions
def saveas_csv():
    """Saves the printed info to a CSV file"""
    file_path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV files', '*.csv')])
    if file_path and results:
        with open(file_path, 'w', newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["Climber", "Next Up", "Start Climbing", "End Climbing"])
            writer.writeheader()
            writer.writerows(results)

def clear_button():
    """Clears entry widgets"""
    ntry_compstart_time.delete(0, 'end')
    #ntry_roundlength.delete(0, 'end') # Testing removing this feature, since it's likely to be a constant
    txt_competlist.delete('1.0', 'end')

def random_button():
    """Randomizes the list of competitors"""
    names_fromtext = txt_competlist.get('1.0', 'end').strip()
    names_list = names_fromtext.split('\n')
    shuffle(names_list)
    
    txt_competlist.delete('1.0', 'end')
    for name in names_list:
        txt_competlist.insert('end', name + '\n')

def copy_to_clipboard():
    """Copies text to the clipboard"""
    if results:
        text_to_copy = ""
        for row in results:
            text_to_copy += f"{row['Climber']} - Next: {row['Next Up']}, Start: {row['Start Climbing']}, End: {row['End Climbing']}\n"
        pyperclip.copy(text_to_copy)
        PopupMessage.success('Text was coppied to clipboard!')
    else:
        PopupMessage.show_error('Warning', 'There was an error and text did not copy') 

# UI Management
class PopupMessage:
    @staticmethod
    def show_error(title, message):
        messagebox.showinfo(title, message)

    @staticmethod
    def success(message):
        messagebox.showinfo("Success", message)

def open_printed_window():
    """Opens a new window to display the printed information. Now only triggers in the get_info() function"""
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

    btn_opentimer = tk.Button(fme_printedinfo_btns, text= 'Create Timer', command= open_timer)
    btn_opentimer.grid(row= 0, column= 2)

    fme_printedinfo.rowconfigure(0, weight= 1)
    fme_printedinfo.columnconfigure(0, weight= 1)
    fme_printedinfo_btns.columnconfigure(0, weight= 1)
    fme_printedinfo_btns.columnconfigure(1, weight= 1)
    fme_printedinfo_btns.columnconfigure(2, weight= 1)

def open_timer():
    """Opens a new window containing the TimerApp"""
    timer_window = tk.Toplevel()
    app = TimerApp(timer_window)

def just_timer(): 
    """Opens the TimerApp without needing to open the Running Order Printed window"""
    boulder_length = get_boulderlength()
    if boulder_length is None:
        return
    if boulder_length < 10:
        PopupMessage.show_error("Time Error", "Boulder lengh must be at least 10 seconds")
        return
    
    transition_time = get_transtime()
    if transition_time < 5:
        PopupMessage.show_error("Time Error", "Transition time must be at least 5 seconds")
        return
    
    num_boulders = get_numofboulders()
    if num_boulders <= 0:
        PopupMessage.show_error("Number of Boulders Error", "Number of boulders must be at least 1")
        return
    set_timer_durations()
    open_timer()

#Setting up layout for application Main Window
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

#Main window create timer button
btn_make_timer = tk.Button(master= fme_timeentry, text= 'Create Timer', command= just_timer)
btn_make_timer.grid(row= 5, columnspan= 2, padx= 5, pady= 5)

#Competitors Entry
lbl_competlist = tk.Label(master=fme_competitors, text= 'List of Competitors \n (Seperated by new line)')
lbl_competlist.grid(row= 0,column= 0, padx= 5, pady= 20)

txt_competlist = tk.Text(master= fme_competitors, width= 20, height= 20)
txt_competlist.grid(row= 0, column= 1)

#Buttons
btn_clear = tk.Button(fme_buttons, text= 'CLEAR', bg= 'red', fg= 'white', command= clear_button)
btn_clear.grid(row= 0, column= 0, padx=5, pady=20)

btn_randomize = tk.Button(fme_competitors, text= 'Randomize Competitors', command= random_button)
btn_randomize.grid(row= 1, column= 1, padx= 0, pady= 5)

btn_enter = tk.Button(fme_buttons, text= 'Submit', command= lambda: [get_info()])
btn_enter.grid(row= 0, column= 1, padx=5, pady=20)

def set_timer_durations():
    """Sets the timer durations based on user input."""
    global HIGH_INTENSITY_DURATION, LOW_INTENSITY_DURATION
    boulder_time = get_boulderlength()
    transition_time = int(spnbx_transtime.get())
    HIGH_INTENSITY_DURATION = boulder_time  # seconds
    LOW_INTENSITY_DURATION = transition_time  # seconds

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Climbing Timer")

        # Initialize mixer if not already running
        if not mixer.get_init():
            mixer.init()

        # Start in normal window mode
        self.root.geometry("500x300")  # Ensures it starts in a normal-sized window
        self.root.configure(bg="black")  # Default background color
        self.fullscreen = False  # Fullscreen set to false, can resize later

        # UI setup
        self.label = tk.Label(root, text="00:00", font=("Arial", 250), fg="white", bg="black")
        self.label.pack(expand=True, fill="both")
        # Resize font dynamically
        self.label.bind("<Configure>", self.resize_text)

        # Bind keys for full-screen toggle
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)

        # Timer variables
        self.time_left = int(HIGH_INTENSITY_DURATION)
        self.is_high_intensity = True
        self.running = False  # Timer starts only when the button is clicked

    # Buttons
        # Button Frame
        button_frame = tk.Frame(root, bg= "white")
        button_frame.pack(pady= 10)

        # Start/Resume button
        self.start_button = tk.Button(button_frame, text="Start", font=("Arial", 16), command=self.toggle_timer)
        self.start_button.grid(row= 0, column= 0, padx= 10)

        # Stop Button
        self.stop_button = tk.Button(button_frame, text= 'Pause', font=("Ariel", 16), command= self.pause_timer, state= "disabled")
        self.stop_button.grid(row= 0, column= 1, padx= 10)

        # Reset Button
        self.reset_button = tk.Button(button_frame, text= 'Reset', font=("Ariel", 16), command= self.reset_timer, state= "disabled")
        self.reset_button.grid(row= 0, column= 2, padx= 10)

        self.update_display()

# Commands for the buttons
    def toggle_timer(self):
        """Starts/Resumes the timer depending on which phase its in"""
        if not self.running:
            self.running = True
            self.start_button.config(text="Resume", state="disabled")  # Update button
            self.stop_button.config(state="normal")  # Enable stop button
            self.reset_button.config(state="normal")  # Enable reset button
            self.update_timer()

    def pause_timer(self):
        """Pauses the timer at the current time"""
        if self.running:
            self.running = False
            self.start_button.config(state= "normal")
            self.start_button.config(text= "Resume")    # Changes "Start" to "Resume"

    def reset_timer(self):
        """Stops and/or resets the timer to its intial values"""
        self.running = False
        self.is_high_intensity = True
        self.time_left = HIGH_INTENSITY_DURATION
        self.update_display()
        self.start_button.config(text= "Start", state= "normal")
        self.stop_button.config(state= "disabled")
        self.reset_button.config(state= "disabled")           

    def update_timer(self):
        """Updates the timer display and switches between climbing/transition when time runs out."""
        if not self.running:
            return  # Prevent updating if the timer is stopped
        
        self.time_left = int(self.time_left)
        minutes, seconds = divmod(self.time_left, 60)
        self.label.config(text=f"{minutes:02}:{seconds:02}")
        # Play a beep at 1:00
        if self.is_high_intensity and self.time_left == 60:
            mixer.music.load("440_short.mp3")
            mixer.music.play()

        # Change background color based on conditions. Should reflect USA Climbing's color scheme
        if self.is_high_intensity and self.time_left > 60:
            self.root.configure(bg="black")
            self.label.config(bg="black", fg= "white")
        elif self.is_high_intensity and self.time_left <= 60: 
            self.root.configure(bg="black")
            self.label.config(bg="black", fg= "red")
        elif not self.is_high_intensity:
            self.root.configure(bg="black")
            self.label.config(bg="black", fg= "green")
        else:
            PopupMessage.show_error("Error", "There was an error with the timer")

        if self.time_left <= 5:
            self.short_beeps()

        if self.time_left > 0:
            self.time_left -= 1
            self.root.after(1000, self.update_timer)
        else:
            # play transition sound
            self.play_transition_mp3()

            # Switch intensity
            self.is_high_intensity = not self.is_high_intensity
            self.time_left = int(HIGH_INTENSITY_DURATION if self.is_high_intensity else LOW_INTENSITY_DURATION)
            self.update_timer()

    def update_display(self):
        """Updates the timer display without changing the state."""
        minutes, seconds = divmod(self.time_left, 60)
        self.label.config(text=f"{minutes:02}:{seconds:02}")

    def play_transition_mp3(self):
        """Plays the transition sound at the start of the transition timer and the start of climbing"""
        if self.is_high_intensity:  #plays when switching FROM high intensity
            mixer.music.load("1000_long.mp3")
        else:                       #plays when switching FROM low intensity
            mixer.music.load("short_long.mp3")
        mixer.music.play()
    
    def short_beeps(self):
        """Plays the short beeps each second from 5 seconds remaining"""
        if self.is_high_intensity and self.time_left <= 5:
            mixer.music.load("440_short.mp3")
            mixer.music.play()

    def resize_text(self, event):
        """Dynamically change text size"""
        newfont_size = min(event.width // 4, event.height // 2)
        self.label.config(font= ('Arial', newfont_size))

    def toggle_fullscreen(self, event=None):
        """Toggles full-screen mode."""
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)

    def exit_fullscreen(self, event=None):
        """Exits full-screen mode."""
        self.fullscreen = False
        self.root.attributes("-fullscreen", False)

window.mainloop()