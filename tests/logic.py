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

    
class ScoringOlympic():
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
        
class ScoringIFSC25():
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