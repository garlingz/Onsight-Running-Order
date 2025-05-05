import tkinter as tk
from tkinter import ttk, messagebox

class App(tk.Tk):
    """Base level window that holds the other frames"""
    def __init__(self):
        super().__init__()
        self.title("Scoring App")
        container = tk.Frame(self)
        container.pack(fill= "both", expand= True)
        self.frames = {}
        for F in (StartingWindow, ScoringUSAC, ScoringOlympic, ScoringIFSC25):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartingWindow")

    def show_frame(self, name):
        self.frames[name].tkraise()
        titles = {
            "StartingWindow": "Home",
            "ScoringUSAC": "USAC Zone Style Scoring",
            "ScoringOlympic": "Olympic Points Scoring",
            "ScoringIFSC25": "IFSC 2025 Points Scoring"
        }
        self.title(titles.get(name, "Scoring App"))

class StartingWindow(tk.Frame):
    """First window where the type of scoring is selected"""
    def __init__(self, parent, controller):
        super().__init__(parent)
        controller.title("Home Window")

        # Window
        self.starting_frame = ttk.Frame(self)
        self.starting_frame.grid(column= 0, row= 0, padx= 20, pady= 20, sticky= 'nsew')
        self.grid_columnconfigure(0, weight= 1)
        self.grid_rowconfigure(0, weight= 1)

        # Text
        self.choice_text = ttk.Label(self.starting_frame, text= "Please select your Scoring Style!")
        self.choice_text.grid(column= 0, row= 0, padx= 20, pady= 20, columnspan= 2)
        self.starting_frame.columnconfigure((0, 1), weight= 1)
        self.starting_frame.rowconfigure(1, weight= 1)

        # Buttons
        self.button_USAC = ttk.Button(self.starting_frame, text= "USAC Zone Style", command= lambda: controller.show_frame("ScoringUSAC"))
        self.button_USAC.grid(column= 0, row= 1, ipadx= 20, ipady= 20, sticky= 'ew')

        self.button_Olympic = ttk.Button(self.starting_frame, text= "Olympic Style", command= lambda: controller.show_frame("ScoringOlympic"))
        self.button_Olympic.grid(column= 1, row= 1, ipadx= 20, ipady= 20, sticky= 'ew')

        self.button_IFSC = ttk.Button(self.starting_frame, text= "IFSC 2025 Style", command= lambda: controller.show_frame("ScoringIFSC25"))
        self.button_IFSC.grid(column= 0, row= 2, ipadx= 20, ipady= 20, sticky= 'ew')

        self.button_OldUSAC = ttk.Button(self.starting_frame, text= "Old USAC Style", command= lambda: messagebox.showinfo(message="Not available yet"))
        self.button_OldUSAC.grid(column= 1, row= 2, ipadx= 20, ipady= 20, sticky= 'ew')

class ScoringUSAC(tk.Frame):
    """The classic scoring window layout for USAC and IFSC events"""
    class Boulder:
        def __init__(self, attempts, level):
            self.attempts = attempts
            self.level = level if level else "0"
            self.top = 0
            self.zone = 0
            self.lowzone = 0
            self.top_attempts = 0
            self.zone_attempts = 0
            self.lowzone_attempts = 0
            self.score = self.calculate_score()
        
        def calculate_score(self):
            if self.level == "T":
                self.top = self.zone = self.lowzone = 1
                self.top_attempts = self.zone_attempts = self.lowzone_attempts = self.attempts
            elif self.level == "Z":
                self.zone = self.lowzone = 1
                self.zone_attempts = self.lowzone_attempts = self.attempts
            elif self.level == "LZ":
                self.lowzone = 1
                self.lowzone_attempts = self.attempts
            else:
                return # Nothing is scored

    class Climber:
        def __init__(self, name):
            self.name = name
            self.boulder_list = []
            self.rank = None

        def add_boulder(self, attempts, level):
            """Adds level and attempts of the boulder to the boulder_list"""
            self.boulder_list.append(ScoringUSAC.Boulder(attempts, level))

        def total_score(self):
            total_tops = sum(boulder.top for boulder in self.boulder_list)
            total_zones = sum(boulder.zone for boulder in self.boulder_list)
            total_lowzones = sum(boulder.lowzone for boulder in self.boulder_list)
            total_top_attempts = sum(boulder.top_attempts for boulder in self.boulder_list)
            total_zone_attempts = sum(boulder.zone_attempts for boulder in self.boulder_list)
            total_lowzone_attempts = sum(boulder.lowzone_attempts for boulder in self.boulder_list)
            
            return (f"Levels= T:{total_tops}, Z:{total_zones}, LZ:{total_lowzones}\nAttempts= T:{total_top_attempts}, Z:{total_zone_attempts}, LZ:{total_lowzone_attempts} ")

        def delete(self, leaderboard):
            """Deletes the climber from the leaderboard."""
            leaderboard.climbers.remove(self)

        def __str__(self):
            return f"Name: {self.name}\nLevels= T:{self.total_tops}, Z:{self.total_zones}, LZ:{self.total_lowzones}\nAttempts= T:{self.total_top_attempts}, Z:{self.total_zone_attempts}, LZ:{self.total_lowzone_attempts}"
    
    class Leaderboard:
        def __init__(self):
            self.climbers = []
            self.toggle_score_breakdown = False

        def add_climber(self, climber):
            self.climbers.append(climber)

        def toggle_score_breakdown(self):
            """Toggles score breakdowns"""
            self.toggle_score_breakdown = not self.toggle_score_breakdown

        def rank_climbers(self):
            """Ranks climbers by the specified key"""
            self.climbers.sort(key= lambda c: (
                -sum(boulder.top for boulder in c.boulder_list), #decending, c for climber and b for boulder
                -sum(boulder.zone for boulder in c.boulder_list), #decending
                -sum(boulder.lowzone for boulder in c.boulder_list), #decending
                sum(boulder.top_attempts for boulder in c.boulder_list), #ascending
                sum(boulder.zone_attempts for boulder in c.boulder_list), #ascending
                sum(boulder.lowzone_attempts for boulder in c.boulder_list) #ascending
            ))
            # Not dealing with tie's in this format
            for i, climber in enumerate(self.climbers, start= 1):
                climber.rank = i

        def __str__(self):
            result = []
            for climber in self.climbers:
                breakdown = ""
                if self.toggle_score_breakdown:
                    # totals for each scoring type
                    total_tops = sum(boulder.top for boulder in climber.boulder_list)
                    total_zones = sum(boulder.zone for boulder in climber.boulder_list)
                    total_lowzones = sum(boulder.lowzone for boulder in climber.boulder_list)
                    total_top_attempts = sum(boulder.top_attempts for boulder in climber.boulder_list)
                    total_zone_attempts = sum(boulder.zone_attempts for boulder in climber.boulder_list)
                    total_lowzone_attempts = sum(boulder.lowzone_attempts for boulder in climber.boulder_list)
                    breakdown = (
                        f"    {total_tops} Tops, {total_top_attempts} attempts.\n"
                        f"    {total_zones} Zones, {total_zone_attempts} attempts.\n"
                        f"    {total_lowzones} LowZones, {total_lowzone_attempts} attempts."
                    )
                result.append(f"{climber.rank}. {climber.name}\n{breakdown}")
            return "\n".join(result)

    def __init__(self, parent, controller):
        super().__init__(parent)

        # Main frame
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(column= 0, row= 0, padx= 20, pady= 20, sticky= "nsew")
        self.main_frame.rowconfigure(0, weight= 1)
        self.main_frame.columnconfigure(0, weight= 1)
        self.main_frame.columnconfigure(1, weight= 1)
        self.leaderboard = self.Leaderboard()

        self.max_boulders = 11
        self.boulder_widgets = []
        self.scoretype_vars = []

        self.create_left()
        self.create_right()

        backbutton = ttk.Button(self, text= "Back", command= lambda: self.backbutton_popup(controller))
        backbutton.grid(column= 0, row= 1, columnspan= 2, sticky= 's')

    def backbutton_popup(self, controller):
        if messagebox.askyesno("Warning!", "Are you sure you want to go back?\nData isn't shared between scoring styles."):
            controller.show_frame("StartingWindow")
        else:
            pass 

    def create_left(self):
        """Left side creation where labels and entry fields exist to gather information from the user."""
        self.left_frame = ttk.Frame(self.main_frame)
        self.left_frame.grid(row=0, column=0, padx=10, pady= 5, sticky= 'nw')

        # Resizing parameters
        for i in range(0, 3):
            self.left_frame.columnconfigure(i, weight= 1)

        for i in range(0, 20):
            self.left_frame.rowconfigure(i, weight= 1)

        # Name Label and Entry
        self.name_label = ttk.Label(self.left_frame, text= "Climber Name : ")
        self.name_label.grid(column= 0, row= 1, padx=5, pady=5, sticky="e")
        self.name_entry = ttk.Entry(self.left_frame, justify= tk.CENTER)
        self.name_entry.grid(column= 1, row= 1, padx=5, pady=5, sticky="w")

        # Dropdown Menu for Number of Boulders
        self.boulder_count_var = tk.StringVar()
        self.boulder_count_select = ttk.Combobox(
            self.left_frame, textvariable= self.boulder_count_var, state= "readonly",
            values= [str(i) for i in range(1, self.max_boulders)], takefocus= 0
        )
        self.boulder_count_select.set("Number of Boulders")
        self.boulder_count_select.bind("<<ComboboxSelected>>", self.update_boulder_fields)
        self.boulder_count_select.grid(column= 1, row= 0, columnspan= 1, pady= 10)

        # Label, entry, and radiobutton fields
        radio_options = ["T", "Z", "LZ", "None"]
        for i in range(self.max_boulders):
            label = ttk.Label(self.left_frame, text=f"Boulder {i + 1} Attempts:")
            entry = ttk.Entry(self.left_frame, width=20, justify=tk.CENTER)

            score_var = tk.StringVar()
            self.scoretype_vars.append(score_var)

            # radiobutton frame
            rb_frame = ttk.Frame(self.left_frame)
            for optn in radio_options:
                rb = ttk.Radiobutton(
                    rb_frame,
                    text= optn,
                    variable= score_var,
                    value= optn,
                    takefocus= False
                )
                rb.pack(side= "left", padx= 2)

            # Putting label, entry, and radiobuttons all in 1 row each
            label.grid(column= 0, row= i + 2, padx= 5, pady= 5)
            entry.grid(column= 1, row= i + 2, padx= 5, pady= 5, sticky= "w")
            rb_frame.grid(column= 2, row= i + 2, padx= 5, pady= 5, sticky= "w")

            # Hide until called
            label.grid_remove()
            entry.grid_remove()
            rb_frame.grid_remove()

            self.boulder_widgets.append((label, entry, rb_frame))

        # Grey text for entry instructions
        self.instruction_label = ttk.Label(
            self.left_frame, 
            foreground= "gray",  
            text= "Enter attempts to the highest scored level. \nNext, select the highest scored level\n"
        )
        self.instruction_label.grid(column= 0, columnspan= 2, row= self.max_boulders + 1)
        
        # Leftside Buttons
        self.add_climber_button = ttk.Button(self.left_frame, text= "Add Climber", command= lambda: self.add_climber())
        self.add_climber_button.grid(row= self.max_boulders + 2, column= 0, columnspan= 2, pady= 10)

        self.edit_climber_button = ttk.Button(self.left_frame, text= "Edit Climber", command= lambda: self.edit_climber())
        self.edit_climber_button.grid(column= 0, row= self.max_boulders + 3, sticky= 'w', padx=5, pady=5)

        self.remove_climber_button = ttk.Button(self.left_frame, text= "Remove Climber", command= lambda: self.remove_climber())
        self.remove_climber_button.grid(column= 1, row= self.max_boulders + 3, sticky= 'e', padx=5, pady=5)

    def create_right(self):
        """Create the right frame for the leaderboard display and associated buttons"""
        self.right_frame = ttk.Frame(self.main_frame)
        self.right_frame.grid(row=0, column=1, padx=10, sticky= 'nsew')

        #letting right frame expand to fill the space
        for i in range(0, 3):
            self.right_frame.columnconfigure(i, weight= 1)

        for i in range(0, 12):
            self.right_frame.rowconfigure(i, weight= 1)

        # Leaderboard Display
        self.leaderboard_text = tk.Text(self.right_frame, height=20, width=30)
        self.leaderboard_text.grid(row=0, column=0, columnspan= 2, pady=10, sticky= "nsew")
        self.disable_edits()

        # Rightside Buttons
        self.leaderboard_buttons = ttk.Frame(self.right_frame)
        self.leaderboard_buttons.grid(row=1, column=0, columnspan=2, pady=10)
        ttk.Button(self.leaderboard_buttons, text="Clear Leaderboard", command= lambda: self.clear_leaderboard_ask()).grid(row= 0, column= 0, columnspan= 2, padx= 10, pady= 10) 

        breakdown_toggle_var = tk.BooleanVar(value= False)
        self.score_breakdown_checkbutton = ttk.Checkbutton(
            self.leaderboard_buttons, 
            text= "Show breakdown of Scores", 
            variable= breakdown_toggle_var, 
            command= lambda: self.toggle_score_breakdown(breakdown_toggle_var.get()),
            state= "disabled"
            )
        self.score_breakdown_checkbutton.grid(row= 1, column= 0, padx= 10, pady= 10)

    # Data Entry and creation functions
    def update_boulder_fields(self, event= None):
        """Show/Hide boulder label/entry fields based on selected number of boulders."""
        selected_count = int(self.boulder_count_var.get())
        # Show the required number of boulder fields
        for i, (label, entry, radio) in enumerate(self.boulder_widgets):
            if i < selected_count:
                label.grid()
                entry.grid()
                radio.grid()
            else:
                label.grid_remove()
                entry.grid_remove()
                radio.grid_remove()
        self.left_frame.update_idletasks()   

    def clear_entries(self):
        selected_boulders = int(self.boulder_count_var.get())
        for i in range(selected_boulders):
            self.boulder_widgets[i][1].delete(0, tk.END)
            try:
                self.scoretype_vars[i].set('')  #set each button to '' in every iteration
            except Exception as e:
                print(f"{e}")
                messagebox.showwarning("", "Something didn't work")
        self.name_entry.delete(0, tk.END)

    # Manipulating Climbers and Leaderboard classes
    def add_climber(self):
        self.enable_edits()
        try:
            climber_name = self.name_entry.get().strip()
            if not climber_name:
                raise ValueError(f"Climber name cannot be empty")
            
            if any (climber.name == climber_name for climber in self.leaderboard.climbers):
                raise ValueError(f"{climber_name} already exists in the leaderboard.\nPlease add another identifier")
            
            try:
                selected_boulders = int(self.boulder_count_var.get())
            except:
                raise ValueError(f"You must select a valid number of boulders to score.")
            self.validate_scores() 

            boulder_list = []
            for i in range(selected_boulders):
                attempts_str = self.boulder_widgets[i][1].get().strip()
                level_str = self.scoretype_vars[i].get()

                attempts = int(attempts_str) if attempts_str else "0"
                boulder_list.append(self.Boulder(attempts, level_str))
            
            climber = self.Climber(climber_name)
            climber.boulder_list = boulder_list
            self.leaderboard.add_climber(climber)

            messagebox.showinfo("Success", f"Scores for {climber_name} added!")
            self.update_leaderboard()
        except Exception as e:
            messagebox.showerror("Error", f"{e}")

    def edit_climber(self):
        try:
            name = self.name_entry.get().strip()
            if not name:
                raise ValueError("Climber name cannot be empty.")
            self.validate_scores()
            selected_boulders = int(self.boulder_count_var.get())

            # find the climber
            climber = next((c for c in self.leaderboard.climbers if c.name == name), None)
            if climber is None:
                raise ValueError(f"Climber '{name}' not found in the leaderboard.")
            
            # Update/Append boulders based on selected data entry fields
            for i in range(selected_boulders):
                attempts_str = self.boulder_widgets[i][1].get().strip()
                level_str = self.scoretype_vars[i].get() 
                attempts = int(attempts_str) if attempts_str else "0"

                boulder = self.Boulder(attempts, level_str)
                if i < len(climber.boulder_list):
                    climber.boulder_list[i] = boulder
                else:
                    climber.boulder_list.append(boulder)
    
            if len(climber.boulder_list) > selected_boulders:
                climber.boulder_list = climber.boulder_list[:selected_boulders]
            self.update_leaderboard()
            messagebox.showinfo("Success", f"Scores for '{name}' were updated.")

        except Exception as e:
            messagebox.showerror("Error", f"Error updating climber '{name}':\n{str(e)}")    

    def remove_climber(self):
        try:
            name = self.name_entry.get()
            if not name:
                raise ValueError(f"Climber name cannot be empty")
            found = False
            for climber in self.leaderboard.climbers[:]:
                if climber.name == name:
                    self.leaderboard.climbers.remove(climber)
                    found = True
            if found:
                messagebox.showinfo("Success", f"'{name}' has been removed." )
                self.update_leaderboard()
            else:
                raise ValueError(f"Climber {name} not found in the leaderboard.")
        except Exception as e:
            messagebox.showerror("Error", f"{e}")

    # Edits to the Leaderboard
    def update_leaderboard(self):
        """Clears the leaderboard, re-ranks climbers, and re-prints the leaderboard. 
        After changes have been made, the entry fields are erased."""
        self.enable_edits()
        self.leaderboard.rank_climbers()
        self.leaderboard_text.delete(1.0, tk.END)
        self.leaderboard_text.insert(tk.END, str(self.leaderboard))
        self.clear_entries()
        self.status_checkbutton()
        self.disable_edits()
        

    def status_checkbutton(self):
        if len(self.leaderboard.climbers) > 0:
            self.score_breakdown_checkbutton.config(state= "normal")
        else:
            self.score_breakdown_checkbutton.config(state= "disabled")

    def validate_scores(self):
        """Validates data entered by user prior to processing. Raises error if formatting is not accepted."""
        try:
            selected_boulders = int(self.boulder_count_var.get())
        except ValueError:
            raise ValueError("Please select the number of boulders to score.")
        
        for i in range(selected_boulders):
            attempts = self.boulder_widgets[i][1].get().strip()
            level_str = self.scoretype_vars[i].get().lower()
            if not level_str:
                raise ValueError(f"Please select a score type of Boulder {i + 1}")
            if not attempts:
                if level_str in ("0", "none"):
                    continue
                else:
                    raise ValueError(f"Missing attempts on Boulder {i + 1} with score '{level_str}'.")
            try:
                attempts_check = int(attempts)
                if attempts_check < 1:
                    raise ValueError
            except ValueError:
                raise ValueError(f"'{attempts}' in Boulder {i + 1} invalid.\nAttempts must be a positive whole number greater than 0.")
            

            
    def clear_leaderboard_ask(self):
        """Asks for confirmation before clearing the entries."""
        response = messagebox.askyesno("Clear Leaderboard", "Are you sure you want to clear the leaderboard?")
        if response:
            self.leaderboard.climbers = []
            self.enable_edits()
            self.leaderboard_text.delete(1.0, tk.END)
            self.disable_edits()
            self.status_checkbutton()
            messagebox.showinfo("Success", "Leaderboard has been cleared.")
               
    def toggle_score_breakdown(self, show_breakdown):
        """Toggle on/off the score breakdown printing in the Leaderboard."""
        self.leaderboard.toggle_score_breakdown = show_breakdown
        self.update_leaderboard()

    def enable_edits(self):
        """Enables editing of the leaderboard."""
        self.leaderboard_text.config(state= tk.NORMAL)

    def disable_edits(self):
        """Disables editing of the leaderboard."""
        self.leaderboard_text.config(state= tk.DISABLED)


class ScoringOlympic(tk.Frame):
    """Olympic Style scoring that is more points focused rather than zone focused"""
    class Boulder:
        """Represents a single boulder and the attempts to a scoring level, as well as the calculated score.
            * attempts: Number of attempts made to highest scored space.
            * level: Highest achieved scoring space (T for top, Z for zone, 0 for no score)"""

        def __init__(self, attempts, level):
            self.attempts = attempts
            self.level = level if level else "0"
            self.score = self.calculate_score()

        def calculate_score(self):
            """Calculates the score for the boulder based on the highest scored level and attempts to that level.
                * return: calculated score."""
            if self.level == "25":
                return round(25 - ((self.attempts - 1) * 0.1), 5) # using attempts -1 because the score technically only subtracts .1 per "failed" attempt
            elif self.level == "10":
                return round(10 - ((self.attempts - 1) * 0.1), 5)
            elif self.level == "5":
                return round(5 - ((self.attempts - 1) * 0.1), 5)
            elif self.level == "" or self.level == "0":
                return 0

    class Climber:
        def __init__(self, name):
            self.name = name
            self.boulder_list = []
            self.rank = None    # Adding rankings rather than just listing order

        def add_boulder(self, attempts, level):
            """Adds the score of a boulder to the climber's scorecard."""
            self.boulder_list.append(ScoringOlympic.Boulder(attempts, level))

        def total_score(self):
            """Calculates the total score of the climber. Used for ranking on the leaderboard."""
            total = round(sum(boulder.score for boulder in self.boulder_list), 5)
            return total
        
        def delete(self, leaderboard):
            """Deletes the climber from the leaderboard."""
            leaderboard.climbers.remove(self)
        
        def __str__(self):
            return f"{self.name}: {self.total_score():.1f} total points."
        
    class Leaderboard:
        """Leaderboard class that will visualize ranking of climbers based on their scores."""
        def __init__(self):
            self.climbers = []
            self.toggle_score_breakdown = False #Default state

        def add_climber(self, climber):
            """Adds a climber to the leaderboard."""
            self.climbers.append(climber)
            
        def rank_climbers(self):
            """Sorts climbers by total score, in descending order."""
            self.climbers.sort(key= lambda climber: climber.total_score(), reverse= True)
            tie_count = 0
            previous_score = None
            current_rank = 1
            tolerance = 1e-5

            for climber in self.climbers:
                current_score = round(climber.total_score(), 5)

                if previous_score is not None and abs(current_score - previous_score) < tolerance:
                    climber.rank = current_rank
                    tie_count += 1
                else:
                    current_rank = current_rank + tie_count
                    climber.rank = current_rank
                    tie_count = 1
                previous_score = current_score

        def toggle_score_breakdown(self):
            """Toggle score breakdown"""
            self.toggle_score_breakdown = not self.toggle_score_breakdown

        def __str__(self):
            """Generate a string representation of the leaderboard."""
            result = []
            for climber in self.climbers:
                breakdown = ""
                if self.toggle_score_breakdown:
                    breakdown = ", ".join(
                        [f"B{i + 1}: {boulder.score:.1f}" for i, boulder in enumerate(climber.boulder_list)]
                    )
                    breakdown = f" ({breakdown})"
                result.append(f"{climber.rank}. {climber.name}: {climber.total_score():.1f} total points\n{breakdown}")
            return "\n".join(result)


    def __init__(self, parent, controller):
        super().__init__(parent)
                # Main Frame
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(column= 0, row= 0, padx= 20, pady= 20, sticky= "nsew")
        self.main_frame.rowconfigure(0, weight= 1)
        self.main_frame.columnconfigure(0, weight= 1)
        self.main_frame.columnconfigure(1, weight= 1)
        self.leaderboard = self.Leaderboard()

        self.max_boulders = 11
        self.boulder_widgets = []
        self.scoretype_vars = []

        self.create_left_frame()
        self.create_right_frame()

        backbutton = ttk.Button(self, text= "Back", command= lambda: self.backbutton_popup(controller))
        backbutton.grid(column= 0, row= 1, columnspan= 2, sticky= "s")

    def create_left_frame(self):
        """Create left frame where labels and entry fields exist to gather information from the user."""
        self.left_frame = ttk.Frame(self.main_frame)
        self.left_frame.grid(row=0, column=0, padx= 10, pady= 5, sticky= 'nw')

        # Resizing parameters
        for i in range(0, 3):
            self.left_frame.columnconfigure(i, weight= 1)

        for i in range(0, 20):
            self.left_frame.rowconfigure(i, weight= 1)

        # Name Label and Entry
        self.name_label = ttk.Label(self.left_frame, text= "Climber Name : ")
        self.name_label.grid(column= 0, row= 1, padx=5, pady=5, sticky="e")
        self.name_entry = ttk.Entry(self.left_frame, justify= tk.CENTER)
        self.name_entry.grid(column= 1, row= 1, padx=5, pady=5, sticky="w")

        # Dropdown Menu for Number of Boulders
        self.boulder_count_var = tk.StringVar()
        self.boulder_count_select = ttk.Combobox(
            self.left_frame, textvariable= self.boulder_count_var, state= "readonly",
            values= [str(i) for i in range(1, self.max_boulders)], takefocus= 0
        )
        self.boulder_count_select.set("Number of Boulders")
        self.boulder_count_select.bind("<<ComboboxSelected>>", self.update_boulder_fields)
        self.boulder_count_select.grid(column= 1, row= 0, columnspan= 2, pady= 10)

        score_radio_options = ['25', '10', '5', '0']
        # Creating all widgets as if max number of boulders is selected
        for i in range(self.max_boulders):
            label = ttk.Label(self.left_frame, text=f"Boulder {i + 1} Attempts:")
            entry = ttk.Entry(self.left_frame, width=20, justify=tk.CENTER)

            score_var = tk.StringVar()
            self.scoretype_vars.append(score_var)

            # radiobutton frame
            rb_frame = ttk.Frame(self.left_frame)
            for optn in score_radio_options:
                rb = ttk.Radiobutton(
                    rb_frame,
                    text= optn,
                    variable= score_var,
                    value= optn,
                    takefocus= False
                )
                rb.pack(side= "left", padx= 2)
            # Putting label, entry, and radiobuttons all in 1 row each
            label.grid(column= 0, row= i + 2, padx= 5, pady= 5)
            entry.grid(column= 1, row= i + 2, padx= 5, pady= 5, sticky= "w")
            rb_frame.grid(column= 2, row= i + 2, padx= 5, pady= 5, sticky= "w")

            # Hide until called
            label.grid_remove()
            entry.grid_remove()
            rb_frame.grid_remove()

            self.boulder_widgets.append((label, entry, rb_frame))

        # Grey text for entry instructions
        self.instruction_label = ttk.Label(
            self.left_frame, 
            foreground= "gray",  
            text= "Enter attempts to the highest scored level. \nIn the second box, select the highest scored level"
        )
        self.instruction_label.grid(column= 0, columnspan= 2, row= self.max_boulders + 1)
        
        # Left Frame buttons
        self.add_climber_button = ttk.Button(self.left_frame, text= "Add Climber", command= lambda: self.add_climber())
        self.add_climber_button.grid(column= 0, columnspan= 2, row= self.max_boulders + 2, padx=5, pady=5)

        self.edit_climber_button = ttk.Button(self.left_frame, text= "Edit Climber", command= lambda: self.edit_climber())
        self.edit_climber_button.grid(column= 0, row= self.max_boulders + 3, sticky= 'w', padx=5, pady=5)

        self.remove_climber_button = ttk.Button(self.left_frame, text= "Remove Climber", command= lambda: self.remove_climber())
        self.remove_climber_button.grid(column= 1, row= self.max_boulders + 3, sticky= 'e', padx=5, pady=5)

    def create_right_frame(self):
        """Create the right frame for the leaderboard display and associated buttons.
        Should be the same for all scoring types."""
        self.right_frame = ttk.Frame(self.main_frame)
        self.right_frame.grid(row= 0, column= 1, padx= 10, sticky= 'nsew')

        # Resizing parameters
        for i in range(0, 3):
            self.right_frame.columnconfigure(i, weight= 1)

        for i in range(0, 12):
            self.right_frame.rowconfigure(i, weight= 1)

        # Leaderboard Display
        self.leaderboard_text = tk.Text(self.right_frame, height= 20, width= 40)
        self.leaderboard_text.grid(row=0, column=0, columnspan= 2, pady= 10, sticky= "nse")
        self.disable_edits()

        # Rightside Buttons
        self.leaderboard_buttons = ttk.Frame(self.right_frame)
        self.leaderboard_buttons.grid(row=1, column=0, columnspan=2, pady=10)
        ttk.Button(self.leaderboard_buttons, text="Clear Leaderboard", command= lambda: self.clear_leaderboard_ask()).grid(row= 0, column= 0, columnspan= 2, padx= 10, pady= 10)

        breakdown_toggle_var = tk.BooleanVar(value= False)
        self.score_breakdown_checkbutton = ttk.Checkbutton(
            self.leaderboard_buttons, 
            text= "Show breakdown of Scores", 
            variable= breakdown_toggle_var, 
            command= lambda: self.toggle_score_breakdown(breakdown_toggle_var.get()),
            state= "disabled"
            )
        self.score_breakdown_checkbutton.grid(row= 1, column= 0, padx= 10, pady= 10)

    def update_boulder_fields(self, event= None):
        """Show/Hide boulder label/entry fields based on selected number of boulders."""
        selected_count = int(self.boulder_count_var.get())
        # Show the required number of boulder fields
        for i, (label, entry, combobox) in enumerate(self.boulder_widgets):
            if i < selected_count:
                label.grid()
                entry.grid()
                combobox.grid()
            else:
                label.grid_remove()
                entry.grid_remove()
                combobox.grid_remove()
        self.left_frame.update_idletasks()

    def status_checkbutton(self):
        if len(self.leaderboard.climbers) > 0:
            self.score_breakdown_checkbutton.config(state= "normal")
        else:
            self.score_breakdown_checkbutton.config(state= "disabled")

    def clear_entries(self):
        """Clears the entry fields, saves the number of boulders selected."""
        selected_boulders = int(self.boulder_count_var.get())
        for i in range(selected_boulders):
            self.boulder_widgets[i][1].delete(0, tk.END)
            try:
                self.scoretype_vars[i].set('')  #set each button to '' in every iteration
            except Exception as e:
                raise RuntimeError("Something has gone wrong")
        self.name_entry.delete(0, tk.END)
    
    # Manipulating the Climbers and Leaderboards classes
    def add_climber(self):
        """Collects entered information (entry fields). Tries to parse attempts/levels from entry fields and then assigns correct score.
            Updates the leaderboard ranking with the climbers name and their total score."""
        self.enable_edits()
        try:
            climber_name = self.name_entry.get().strip()
            if not climber_name:
                messagebox.showerror("Name Error", "Climber name field cannot be empty.")
                return

            # Checks if the name already exists in the leaderboard
            for climber in self.leaderboard.climbers:
                if climber.name == climber_name:
                    messagebox.showerror("Error", f"{climber_name} already exists in the leaderboard.\nPlease add another identifier.")
                    return

            try:      # check to see if number selected for boulder_count      
                selected_boulders = int(self.boulder_count_var.get())
            except ValueError:
                messagebox.showerror("Error", "You must select a valid number of boulders to score.")
                return
            # Input validation
            self.validate_scores() 
            boulder_list = []
            for i in range(selected_boulders):
                attempts_str = self.boulder_widgets[i][1].get()
                level_str = self.scoretype_vars[i].get()
                if attempts_str in ["0"]:
                    attempts = 0.0
                    level = "0"
                else:
                    attempts = int(attempts_str) if attempts_str else "0"
                    level = level_str if level_str else "0"
                boulder_list.append(self.Boulder(attempts, level))
            climber = self.Climber(climber_name)
            climber.boulder_list = boulder_list
            self.leaderboard.add_climber(climber)
            messagebox.showinfo("Success", f"Scores for {climber_name} added!")
            self.update_leaderboard()
        except Exception as e:
            messagebox.showerror("Validation Error", str(e))

    def remove_climber(self):
        """Removes a climber from the Leaderboard"""
        try:
            name = self.name_entry.get()
            if not name:
                raise ValueError(f"Climber name cannot be empty")
            found = False
            for climber in self.leaderboard.climbers[:]:
                if climber.name == name:
                    self.leaderboard.climbers.remove(climber)
                    found = True
                    break
            if found:
                messagebox.showinfo("Success", f"{name} has been removed.")
                self.update_leaderboard()
            else:
                raise ValueError(f"Climber {name} not found in the leaderboard.")
        except Exception as e:
            messagebox.showerror("Error", f"{e}")

    def edit_climber(self):
        try:
            name = self.name_entry.get().strip()
            if not name:
                raise ValueError("Climber name cannot be empty")

            self.validate_scores() 
            selected_boulders = int(self.boulder_count_var.get())
            # Finding the climber
            climber = next((c for c in self.leaderboard.climbers if c.name == name), None)
            if climber is None:
                raise ValueError(f"Climber '{name}' not found in the leaderboard.")
            
            # Update/Append boulders based on selected entry fields
            for i in range(selected_boulders):
                attempts_entry = self.boulder_widgets[i][1]
                attempts_str = attempts_entry.get()
                level_str = self.scoretype_vars[i].get()

                if not attempts_str or level_str in ["", "0"]:
                    continue

                try:
                    attempts = int(attempts_str)
                    level_str in ["25", "10", "5"]
                except(ValueError, IndexError):
                    messagebox.showerror("Value Error", f"Invalid input in Boulder {i + 1}: '{attempts_entry}'")
                    return
                
                boulder = self.Boulder(attempts, level_str)
                if i < len(climber.boulder_list):
                    climber.boulder_list[i] = boulder
                else:
                    climber.boulder_list.append(boulder)
            
            if len(climber.boulder_list) > selected_boulders:
                climber.boulder_list = climber.boulder_list[:selected_boulders]

            self.update_leaderboard()
            messagebox.showinfo("Success", f"Scores for '{name}' were updated sucessfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error updating climber '{name}':\n{str(e)}")

    # Edits to leaderboard
    def update_leaderboard(self):
        """Clears the leaderboard, re-ranks climbers, and re-prints the leaderboard."""
        self.enable_edits()
        self.leaderboard.rank_climbers()
        self.leaderboard_text.delete(1.0, tk.END)
        self.leaderboard_text.insert(tk.END, str(self.leaderboard))
        self.clear_entries()
        self.status_checkbutton()
        self.disable_edits()        

    def validate_scores(self):
        """Validates the scores in the entry fields, making sure formats are acceptable before submission.
            Specifically does NOT edit or save any information.
            Raises errors if formatting is not accepted."""
        try: 
            selected_boulders = int(self.boulder_count_var.get())       # Check if the variable is an integer.
        except:
            raise ValueError("Please select the number of boulders to score.")
        
        for i in range(selected_boulders):
            # Check that there is a selection for each radio button frame.
            level_str = self.scoretype_vars[i].get().lower()
            attempts = self.boulder_widgets[i][1].get().strip()
            if not level_str:
                raise ValueError(f"Please select a score type on Boulder {i + 1}.")
            if not attempts:
                if level_str in ("0", "none"):
                    continue
                else:
                    raise ValueError(f"Missing attempts on Boulder {i + 1} with score '{level_str}'.")
            try:
                attempts_check = int(attempts)
                if attempts_check < 1:
                    raise ValueError
            except ValueError:
                raise ValueError(f"'{attempts}' in Boulder {i + 1} invalid.\nAttempts must be a positive whole number greater than 0.")

    def clear_leaderboard_ask(self):
        """Asks for confirmation before clearing the entries."""
        response = messagebox.askyesno("Clear Leaderboard", "Are you sure you want to clear the leaderboard?")
        if response:
            self.leaderboard.climbers = []
            self.enable_edits()
            self.leaderboard_text.delete(1.0, tk.END)
            self.disable_edits()
            self.status_checkbutton()
            messagebox.showinfo("Success", "Leaderboard has been cleared.")

    def toggle_score_breakdown(self, show_breakdown):
        self.leaderboard.toggle_score_breakdown = show_breakdown
        self.update_leaderboard()

    def backbutton_popup(self, controller):
        """Reminds the user that data isn't shared, then brings the StartingWindow frame to the top."""
        if messagebox.askyesno("Warning!", "Are you sure you want to go back?\nData isn't shared between scoring styles."):
            controller.show_frame("StartingWindow")
        else:
            pass

    def enable_edits(self):
        """Enables editing of the leaderboard."""
        self.leaderboard_text.config(state= tk.NORMAL)

    def disable_edits(self):
        """Disables editing of the leaderboard."""
        self.leaderboard_text.config(state= tk.DISABLED)


class ScoringIFSC25(tk.Frame):
    """New 2025 IFSC scoring that uses two different levels (top worth 25 points and zone worth 10 points) - ((attempts - 1) * 0.1)"""
    class Boulder:
        """Represents a single boulder and the attempts to a scoring level, as well as the calculated score.
            * attempts: Number of attempts made to highest scored space.
            * level: Highest achieved scoring space (T for top, Z for zone, 0 for no score)"""
    
        def __init__(self, attempts, level):
            self.attempts = attempts
            self.level = level.upper() if level else "0"
            self.score = self.calculate_score()

        def calculate_score(self):
            """Calculates the score for the boulder based on the highest scored level and attempts to that level.
                * return: calculated score."""
            if self.level == "25":
                return round(25 - ((self.attempts - 1) * 0.1), 5) # using attempts -1 because the score technically only subtracts .1 per "failed" attempt
            elif self.level == "10":
                return round(10 - ((self.attempts - 1) * 0.1), 5)
            else:
                return 0    # Anything selected that isn't "25" or "10" will result in a 0 score

    class Climber:
        def __init__(self, name):
            self.name = name
            self.boulder_list = []
            self.rank = None    # Adding rankings rather than just listing order

        def add_boulder(self, attempts, level):
            """Adds the score of a boulder to the climber's scorecard.
                * level: Highest scoring level achieved. ("T", "Z", "0")"""
            self.boulder_list.append(ScoringIFSC25.Boulder(attempts, level))

        def total_score(self):
            """Calculates the total score of the climber. Used for ranking on the leaderboard."""
            total = round(sum(boulder.score for boulder in self.boulder_list), 5)
            return total
        
        def delete(self, leaderboard):
            """Deletes the climber from the leaderboard."""
            leaderboard.climbers.remove(self)
        
        def __str__(self):
            return f"{self.name}: {self.total_score():.1f} total points."
        
    class Leaderboard:
        """Leaderboard class that will visualize ranking of climbers based on their scores."""
        def __init__(self):
            self.climbers = []
            self.toggle_score_breakdown = False

        def add_climber(self, climber):
            """Adds a climber to the leaderboard."""
            self.climbers.append(climber)
            
        def rank_climbers(self):
            """Sorts climbers by total score, in descending order."""
            self.climbers.sort(key= lambda climber: climber.total_score(), reverse= True)
            tie_count = 0
            previous_score = None
            current_rank = 1
            tolerance = 1e-5

            for climber in self.climbers:
                current_score = round(climber.total_score(), 5)

                if previous_score is not None and abs(current_score - previous_score) < tolerance:
                    climber.rank = current_rank
                    tie_count += 1
                else:
                    current_rank = current_rank + tie_count
                    climber.rank = current_rank
                    tie_count = 1
                previous_score = current_score

        def toggle_score_breakdown(self):
            self.toggle_score_breakdown = not self.toggle_score_breakdown

        def __str__(self):
            """Generate a string representation of the leaderboard."""
            result = []
            for climber in self.climbers:
                breakdown = ""
                if self.toggle_score_breakdown:
                    breakdown = ", ".join(
                        [f"B{i + 1}: {boulder.score:.1f}" for i, boulder in enumerate(climber.boulder_list)]
                    )
                    breakdown = f" ({breakdown})"
                result.append(f"{climber.rank}. {climber.name}: {climber.total_score():.1f} total points\n{breakdown}")
            return "\n".join(result)

    def __init__(self, parent, controller):
        super().__init__(parent)
        # Main Frame
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(column= 0, row= 0, padx= 20, pady= 20, sticky= "nsew")
        self.main_frame.rowconfigure(0, weight= 1)
        self.main_frame.columnconfigure(0, weight= 1)
        self.main_frame.columnconfigure(1, weight= 1)
        self.leaderboard = self.Leaderboard()

        self.max_boulders = 11
        self.boulder_widgets = []
        self.scoretype_vars = []

        self.create_left_frame()
        self.create_right_frame()

        backbutton = ttk.Button(self, text= "Back", command= lambda: self.backbutton_popup(controller))
        backbutton.grid(column= 0, row= 1, columnspan= 2, sticky= "s")

    def backbutton_popup(self, controller):
        """Reminds the user that data isn't shared, then brings the StartingWindow frame to the top."""
        if messagebox.askyesno("Warning!", "Are you sure you want to go back?\nData isn't shared between scoring styles."):
            controller.show_frame("StartingWindow")
        else:
            pass        

    def create_left_frame(self):
        """Create left frame where labels and entry fields exist to gather information from the user."""
        self.left_frame = ttk.Frame(self.main_frame)
        self.left_frame.grid(row=0, column=0, padx= 10, pady= 5, sticky= 'nw')

        # Resizing parameters
        for i in range(0, 3):
            self.left_frame.columnconfigure(i, weight= 1)

        for i in range(0, 20):
            self.left_frame.rowconfigure(i, weight= 1)

        # Name Label and Entry
        self.name_label = ttk.Label(self.left_frame, text= "Climber Name : ")
        self.name_label.grid(column= 0, row= 1, padx=5, pady=5)
        self.name_entry = ttk.Entry(self.left_frame, justify= tk.CENTER)
        self.name_entry.grid(column= 1, row= 1, padx=5, pady=5, sticky="w")

        # Dropdown Menu for Number of Boulders
        self.boulder_count_var = tk.StringVar()
        self.boulder_count_select = ttk.Combobox(
            self.left_frame, textvariable= self.boulder_count_var, state= "readonly",
            values= [str(i) for i in range(1, self.max_boulders)], takefocus= 0
        )
        self.boulder_count_select.set("Number of Boulders")
        self.boulder_count_select.bind("<<ComboboxSelected>>", self.update_boulder_fields) 
        self.boulder_count_select.grid(column= 1, row= 0, columnspan= 2, pady= 10)

        radio_buttons = ["25", "10", "None"]
        # Creating all widgets as if max number of boulders is selected
        for i in range(self.max_boulders):
            label = ttk.Label(self.left_frame, text=f"Boulder {i + 1} :")
            entry = ttk.Entry(self.left_frame, width= 20, justify= tk.CENTER)

            score_var = tk.StringVar()
            self.scoretype_vars.append(score_var)
            # Radiobutton frame containing radiobuttons
            rb_frame = ttk.Frame(self.left_frame)
            for option in radio_buttons:
                rb = ttk.Radiobutton(
                    rb_frame,
                    text= option,
                    variable= score_var,
                    value= option,
                    takefocus= False
                )
                rb.pack(side= "left", padx= 2)

            label.grid(column=0, row=i + 2, padx=5, pady=5)
            entry.grid(column=1, row=i + 2, padx=5, pady=5, sticky="w")
            rb_frame.grid(column= 2, row= i + 2, padx= 5, pady= 5, sticky= "w")

            # hide until called
            label.grid_remove()  # Hide initially
            entry.grid_remove()  # Hide initially
            rb_frame.grid_remove()
            self.boulder_widgets.append((label, entry, rb_frame))

        # Grey text for entry instructions
        self.instruction_label = ttk.Label(
            self.left_frame, 
            foreground= "gray",  
            text= "Enter attempts to the highest scored level. \nThen select the highest scored zone. 'None' for no score achieved."
        )
        self.instruction_label.grid(column= 0, columnspan= 2, row= self.max_boulders + 1)

        # Left Frame buttons
        self.add_climber_button = ttk.Button(self.left_frame, text= "Add Climber", command= lambda: self.add_climber())
        self.add_climber_button.grid(column= 0, columnspan= 2, row= self.max_boulders + 2, padx=5, pady=5)

        self.edit_climber_button = ttk.Button(self.left_frame, text= "Edit Climber", command= lambda: self.edit_climber())
        self.edit_climber_button.grid(column= 0, row= self.max_boulders + 3, sticky= 'w', padx=5, pady=5)

        self.remove_climber_button = ttk.Button(self.left_frame, text= "Remove Climber", command= lambda: self.remove_climber())
        self.remove_climber_button.grid(column= 1, row= self.max_boulders + 3, sticky= 'e', padx=5, pady=5)

    def create_right_frame(self):
        """Create the right frame for the leaderboard display and associated buttons.
        Should be the same for all scoring types."""
        self.right_frame = ttk.Frame(self.main_frame)
        self.right_frame.grid(row= 0, column= 1, padx= 10, sticky= 'nsew')

        # Resizing parameters
        for i in range(0, 3):
            self.right_frame.columnconfigure(i, weight= 1)

        for i in range(0, 12):
            self.right_frame.rowconfigure(i, weight= 1)

        # Leaderboard Display
        self.leaderboard_text = tk.Text(self.right_frame, height= 20, width= 40)
        self.leaderboard_text.grid(row=0, column=0, columnspan= 2, pady= 10, sticky= "nse")
        self.disable_edits()

        # Rightside Buttons
        self.leaderboard_buttons = ttk.Frame(self.right_frame)
        self.leaderboard_buttons.grid(row=1, column=0, columnspan=2, pady=10)
        ttk.Button(self.leaderboard_buttons, text="Clear Leaderboard", command= self.clear_leaderboard_ask).grid(row= 0, column= 0, columnspan=2, padx= 10, pady= 10)
        # Breakdown Checkbox
        self.breakdown_toggle_var = tk.BooleanVar(value= False)
        self.score_breakdown_checkbutton = ttk.Checkbutton(
            self.leaderboard_buttons, 
            text= "Show breakdown of Scores", 
            variable= self.breakdown_toggle_var, 
            command= lambda: self.toggle_score_breakdown(self.breakdown_toggle_var.get()),
            state= "disabled"
            )
        self.score_breakdown_checkbutton.grid(row= 1, column= 0, padx= 10, pady= 10)

    # Button and Functionality
    def update_boulder_fields(self, event= None):
        """Show/Hide boulder label/entry fields based on selected number of boulders."""
        selected_count = int(self.boulder_count_var.get())
        # Show the required number of boulder fields
        for i, (label, entry, radio) in enumerate(self.boulder_widgets):
            if i < selected_count:
                label.grid()
                entry.grid()
                radio.grid()
            else:
                label.grid_remove()
                entry.grid_remove()
                radio.grid_remove()
        self.left_frame.update_idletasks()

    def clear_entries(self):
        """Clears the entry fields, saves the number of boulders selected."""
        selected_boulders = int(self.boulder_count_var.get())
        for i in range(selected_boulders):
            self.boulder_widgets[i][1].delete(0, tk.END)
            try:
                self.scoretype_vars[i].set('')  #set each button to '' in every iteration
            except Exception as e:
                print(f"{e}") 
                messagebox.showwarning("", "Something didn't work")           
        self.name_entry.delete(0, tk.END)
            
    def add_climber(self):
        """Collects entered information (entry fields). Tries to parse attempts/levels from entry fields and then assigns correct score.
            Updates the leaderboard ranking with the climbers name and their total score."""
        self.enable_edits()
        try:
            climber_name = self.name_entry.get().strip()
            if not climber_name:
                raise ValueError("Climber name field cannot be empty.")
            
            # Checks if the name already exists in the leaderboard
            if any(c.name == climber_name for c in self.leaderboard.climbers):
                raise ValueError(f"{climber_name} already exists in the leaderboard.\nPlease add another identifier.")
            
            self.validate_scores()  # Checking that scores are entered correctly
            selected_boulders = int(self.boulder_count_var.get())

            boulders = []
            for i in range(selected_boulders):
                level = self.scoretype_vars[i].get().strip().lower()
                if level in ["None", "none", "NONE"] or not level:
                    boulders.append(self.Boulder(0, "0"))
                    continue

                attempts = int(self.boulder_widgets[i][1].get().strip())
                boulders.append(self.Boulder(attempts, level))
                   
            climber = self.Climber(climber_name)
            climber.boulder_list = boulders
            self.leaderboard.add_climber(climber)

            messagebox.showinfo("Success", f"Scores for {climber_name} added!")
            self.update_leaderboard()

        except Exception as e:
            messagebox.showerror("Error", f"Error adding climber: {e}")

    def edit_climber(self):
        """Edits the score of an existing climber. Any spaces outside of the name are stripped but the names are not case sensitive.
            If a new value is entered in the field, the leaderboard gets updated."""
        try:
            name = self.name_entry.get().strip()
            if not name:
                raise ValueError("Climber name cannot be empty")
            
            self.validate_scores()
            selected_boulders = int(self.boulder_count_var.get())

            # Find the climber
            climber = next((c for c in self.leaderboard.climbers if c.name == name), None)
            if climber is None:
                raise ValueError(f"Climber '{name}' not found in the leaderboard.")
            
            # Update or append boulders based on selected entry fields
            for i in range(selected_boulders):
                attempts = int(self.boulder_widgets[i][1].get().strip())
                level = self.scoretype_vars[i].get().strip().upper()
                boulder = self.Boulder(attempts, level)
                if i < len(climber.boulder_list):
                    climber.boulder_list[i] = boulder
                else:
                    climber.boulder_list.append(boulder)

            # Matches scored boulders to the current number selected boulders
            if len(climber.boulder_list) > selected_boulders:
                climber.boulder_list = climber.boulder_list[:selected_boulders]
            self.update_leaderboard()
            messagebox.showinfo("Success", f"Scores for '{name}' were updated sucessfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Error updating climber '{name}':\n{str(e)}")    

    def remove_climber(self):
        """Removes a climber from the Leaderboard"""
        try:
            name = self.name_entry.get()

            if not name:
                raise ValueError(f"Climber name cannot be empty")
            found = False
            for climber in self.leaderboard.climbers[:]:
                if climber.name == name:
                    self.leaderboard.climbers.remove(climber)
                    found = True
            if found:
                messagebox.showinfo("Success", f"'{name}' has been removed." )
                self.update_leaderboard()
            else:
                raise ValueError(f"Climber {name} not found in the leaderboard.")

        except Exception as e:
            messagebox.showerror('ValueError', f"Cannot find climber '{name}'. {str(e)}")
            raise ValueError(f"Cannot find climber {name}. {str(e)}")

    # Edits to the Leaderboard
    def clear_leaderboard_ask(self):
        """Asks for confirmation before clearing the entries."""
        response = messagebox.askyesno("Clear Leaderboard", "Are you sure you want to clear the leaderboard?")
        if response:
            self.leaderboard.climbers = []
            self.enable_edits()
            self.leaderboard_text.delete(1.0, tk.END)
            self.disable_edits()
            self.status_checkbutton()
            messagebox.showinfo("Success", "Leaderboard has been cleared.")

    def update_leaderboard(self):
        """Clears the leaderboard, re-ranks climbers, and re-prints the leaderboard."""

        self.enable_edits()
        self.leaderboard.rank_climbers()
        self.leaderboard_text.delete(1.0, tk.END)
        self.leaderboard_text.insert(tk.END, str(self.leaderboard))
        self.clear_entries()
        self.disable_edits()
        self.status_checkbutton()

    def status_checkbutton(self):
        if len(self.leaderboard.climbers) > 0:
            self.score_breakdown_checkbutton.config(state= "normal")
        else:
            self.score_breakdown_checkbutton.config(state= "disabled")

    def validate_scores(self):
        """Validates the scores in the entry fields, making sure formats are acceptable before submission.
            Specifically does NOT edit or save any information.
            Raises errors if formatting is not accepted."""
        try:
            selected_boulders = int(self.boulder_count_var.get()) 
        except:
            messagebox.showerror("Selection Error", "Please select the number of boulders to score.")
            return

        for i in range(selected_boulders):
            level_str = self.scoretype_vars[i].get()
            attempts = self.boulder_widgets[i][1].get().strip()
            if level_str.lower() == "none":         # if None is selected, then don't raise an error
                continue

            if not level_str:
                messagebox.showerror("Scoring Error", f"Please select a score type on Boulder {i + 1}.")
                return
            
            if not attempts:
                attempts = "0"
            try:
                attempts_check = int(attempts)
                if attempts_check < 1:
                    raise ValueError
            except ValueError:
                raise ValueError(f"'{attempts}' in Boulder {i + 1} invalid.\nAttempts must be a positive whole number greater than 0.")
            
    def toggle_score_breakdown(self, show_breakdown):
        """Toggle on/off the score breakdown printing in the Leaderboard."""
        self.leaderboard.toggle_score_breakdown = show_breakdown
        self.update_leaderboard()

    def enable_edits(self):
        """Enables editing of the leaderboard."""
        self.leaderboard_text.config(state= tk.NORMAL)

    def disable_edits(self):
        """Disables editing of the leaderboard."""
        self.leaderboard_text.config(state= tk.DISABLED)

if __name__ == "__main__":
    app = App()
    app.mainloop()