import unittest

class ScoringUSAC():
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

    