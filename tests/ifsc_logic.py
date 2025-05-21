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