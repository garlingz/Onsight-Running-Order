import tkinter as tk
from tkinter import ttk, messagebox

# OOP Scoring System logic
class Scores:
    class Top:
        def __init__(self, tops = 0, attempts = 0):
            self.tops = tops
            self.attempts = attempts

        def __str__(self):
            return f"{self.tops} T    {self.attempts} A"
    
    class Zone:
        def __init__(self, zones = 0, attempts = 0):
            self.zones = zones
            self.attempts = attempts

        def __str__(self):
            return f"{self.zones} Z    {self.attempts} A"

    class LowZone:
        def __init__(self, low_zones = 0, attempts = 0):
            self.low_zones = low_zones
            self.attempts = attempts

        def __str__(self):
            return f"{self.low_zones} LZ    {self.attempts} A"

    def __init__(self):
        self.tops = Scores.Top(0, 0)
        self.zones = Scores.Zone(0, 0)
        self.low_zones = Scores.LowZone(0, 0)

class Climber:
    def __init__(self, name, category):
        self.name = name
        self.scores = Scores()
        self.category = category

    def __str__(self):
        return f"{self.name}:\n{self.scores.tops}\n{self.scores.zones}\n{self.scores.low_zones}"
    
    def delete(self, leaderboard):
        """Deletes the climber from the leaderboard"""
        leaderboard.climbers.remove(self)
    
class Leaderboard():
    def __init__(self):
        self.climbers = []

    def add_climber(self, *climbers):
        """Adds a climber to the leaderboard"""
        self.climbers.extend(climbers)
    
    def rank_climbers(self):
        """Sorts climbers by their scores. Key currently matches the USA Climbing Isolation scoring system."""
        def sort_key(climber):
            return (-climber.scores.tops.tops, -climber.scores.zones.zones, -climber.scores.low_zones.low_zones, 
            climber.scores.tops.attempts, climber.scores.zones.attempts, climber.scores.low_zones.attempts)
        self.climbers.sort(key=sort_key)
    
def create_climber(name, category, tops = (0, 0), zones = (0, 0), low_zones = (0, 0)):
    """Creates a climber object with the given name, category, and scores. Scores are taken as tuples.
        If no Score is provided, the name is added to the leaderboard with 0,0"""
    climber = Climber(name, category)
    climber.scores.tops = Scores.Top(*tops)
    climber.scores.zones = Scores.Zone(*zones)
    climber.scores.low_zones = Scores.LowZone(*low_zones)
    return climber

# tkinter window
class ScoringApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Climbing Leaderboard")
        self.leaderboard = Leaderboard()
        
        # Main Frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.grid(column= 0, row= 0, padx= 20, pady= 20, sticky= "nsew")
        self.main_frame.rowconfigure(0, weight= 1)
        self.main_frame.columnconfigure(0, weight= 1)
        self.main_frame.columnconfigure(1, weight= 1)

        # Resizing to fit the frame
        self.root.columnconfigure(0, weight= 1)
        self.root.rowconfigure(0, weight= 1)

        # Creating Left and Right sections
        self.create_left_frame()
        self.create_right_frame()

    def create_left_frame(self):
        """Create the left frame for inputs and buttons"""
        self.left_frame = ttk.Frame(self.main_frame)
        self.left_frame.grid(row=0, column=0, padx=10, pady= 5, sticky= 'nw')

        # Left Frame Resizing
        #self.main_frame.columnconfigure(0, weight= 1)
        self.left_frame.columnconfigure(0, weight= 1)
        self.left_frame.columnconfigure(1, weight= 1)
        self.left_frame.rowconfigure(0, weight= 1)
        self.left_frame.rowconfigure(5, weight= 1)

        # Labels and Entry Fields
        labels = ["Climber Name", "Category", "Tops (count, attempts)", "Zones (count, attempts)", "Low Zones (count, attempts)"]
        self.entries = {}
        for i, label in enumerate(labels):
            ttk.Label(self.left_frame, text= label + ":").grid(row=i, column=0, padx=5, pady=5)
            entry = ttk.Entry(self.left_frame)
            entry.grid(row= i, column= 1, padx=5, pady=5, sticky= "w")
            self.entries[label] = entry #stores in dictionary for easy access
        
        # Leftside Buttons
        ttk.Button(self.left_frame, text="Add Climber", command=self.add_climber).grid(row= 5, column= 0, columnspan= 2, pady= 10)

        # Edit/Remove Climber Buttons
        add_remove_buttons = [
            ("Edit Climber", self.edit_climber),
            ("Remove Climber", self.remove_climber)
        ]
        for i, (text, command) in enumerate(add_remove_buttons):
            ttk.Button(self.left_frame, text= text, command= command).grid(row= 6, column= i, columnspan= 2, padx= 10, pady= 10, sticky= "w")

    def create_right_frame(self):
        """Create the right frame for the leaderboard display and associated buttons"""
        self.right_frame = ttk.Frame(self.main_frame)
        self.right_frame.grid(row=0, column=1, padx=10, sticky= 'nsew')

        #letting right frame expand to fill the space
        self.main_frame.columnconfigure(1, weight= 1)
        self.right_frame.rowconfigure(0, weight= 1)
        self.right_frame.columnconfigure(0, weight= 1)

        # Leaderboard Display
        self.leaderboard_text = tk.Text(self.right_frame, height=20, width=30)
        self.leaderboard_text.grid(row=0, column=0, columnspan= 2, pady=10, sticky= "nsew")
        self.disable_edits()

        # Rightside Buttons
        self.leaderboard_buttons = ttk.Frame(self.right_frame)
        self.leaderboard_buttons.grid(row=1, column=0, columnspan=2, pady=10)
        ttk.Button(self.leaderboard_buttons, text="Clear Leaderboard", command=self.clear_leaderboard_ask).pack(side= "left", padx= 10, pady= 10)
        ttk.Button(self.leaderboard_buttons, text="Show Leaderboard", command=self.show_leaderboard).pack(side= "left", padx= 10, pady= 10)

    # Functions and Logic
    def clear_entries(self):
        """Clears all entry fields"""
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def remove_climber(self):
        """Removes a climber from the Leaderboard"""
        try:
            name = self.entries["Climber Name"].get()
            found = False
            if name == "":
                raise ValueError("Climber Name cannot be empty")
            for climber in self.leaderboard.climbers[:]:
                if climber.name == name:
                    climber.delete(self.leaderboard)
                    found = True
                    break
            if found:
                messagebox.showinfo("Success", f"{name} has been removed.")
                self.clear_entries()
                self.show_leaderboard()
            else:
                raise ValueError(f"Climber {name} not found in the leaderboard.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def validate_scores(self, score_type):
        """Parses and validates the score from the entry field. Raises error an incorrect score is give"""
        entry_value = self.entries[score_type].get()
        scores = tuple(map(int, entry_value.split(',')))
        if not entry_value:
            return (0, 0)
        short_types = score_type.split()[0]
        if scores[0] > scores[1]:
            raise ValueError(f"{short_types}: '{scores[0]}' cannot be larger than attempts '{scores[1]}'")
        return scores

    def add_climber(self):
        """Adds a climber to the current leaderboard. Raises errors if the input is invalid"""
        try:
            name = self.entries["Climber Name"].get()
            if name == "":
                raise ValueError("Name cannot be empty")
            if any(climber.name == name for climber in self.leaderboard.climbers):
                raise ValueError(f"{name} already exists in the leaderboard")
            category = self.entries["Category"].get()
            tops = self.validate_scores("Tops (count, attempts)")
            zones = self.validate_scores("Zones (count, attempts)")
            low_zones = self.validate_scores("Low Zones (count, attempts)") if self.entries["Low Zones (count, attempts)"].get() else (0, 0)
   
            climber = create_climber(name, category, tops, zones, low_zones)
            self.leaderboard.add_climber(climber)
            messagebox.showinfo("Success", f"{name} added to the leaderboard!")
            self.clear_entries()
            self.show_leaderboard()
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def show_leaderboard(self):
        """Displays the current leaderboard, with rankings"""
        self.leaderboard.rank_climbers()
        self.enable_edits()
        self.leaderboard_text.delete(1.0, tk.END)
        for climber in self.leaderboard.climbers:
            self.leaderboard_text.insert(tk.END, f"{climber}\n\n")
        self.disable_edits()

    def edit_climber(self):
        """Edits the score of an existing climber.
            If a new value is entered in the entry field, it is validated and updated"""
        try: 
            name = self.entries["Climber Name"].get()  
            if not name:
                raise ValueError("Climber Name cannot be empty")  
             
            climber = next((c for c in self.leaderboard.climbers if c.name == name), None)
            if not climber:
                raise ValueError(f"Climber {name} not found.")
            
            category = self.entries["Category"].get()
            if category:
                climber.category = category
            
            if self.entries["Tops (count, attempts)"].get():
                tops = self.validate_scores("Tops (count, attempts)")
                climber.scores.tops = Scores.Top(*tops)

            if self.entries["Zones (count, attempts)"].get():
                zones = self.validate_scores("Zones (count, attempts)")
                climber.scores.zones = Scores.Zone(*zones)
        
            if self.entries["Low Zones (count, attempts)"].get():
                low_zones = self.validate_scores("Low Zones (count, attempts)")
                climber.scores.low_zones = Scores.LowZone(*low_zones)

            messagebox.showinfo("Success", f"Climber '{name}' has been updated.")
            self.clear_entries()
            self.show_leaderboard()
        except Exception as e:
            messagebox.showerror("Error", f"Error updating climber '{name}':\n{str(e)}")

    def clear_leaderboard_ask(self):
        """Asks for confirmation before clearing the entries"""
        response = messagebox.askyesno("Clear Leaderboard", "Are you sure you want to clear the leaderboard?")
        if response:
            self.clear_leaderboard()
        
    def clear_leaderboard(self):
        """Clears the leaderboard values"""
        self.leaderboard.climbers = []
        self.enable_edits()
        self.leaderboard_text.delete(1.0, tk.END)
        messagebox.showinfo("Success", "Leaderboard has been cleared.")
        self.disable_edits()

    def enable_edits(self):
        self.leaderboard_text.config(state= tk.NORMAL)

    def disable_edits(self):
        self.leaderboard_text.config(state= tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = ScoringApp(root)
    root.mainloop()