import collections

class RouletteEngine:
    def __init__a (self):
        # European Roulette Wheel (0-36)
        self.wheel_layout = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
        self.sequence = []
        self.num_to_index = {num: i for i, num in enumerate(self.wheel_layout)}

    def add_number(self, number):
        if 0 <= number <= 36:
            self.sequence.append(number)
        else:
            raise ValueError("Number must be between 0 and 36.")

    def get_neighbors(self, number, span=2):
        """Get numbers physically next to a given number on the wheel."""
        if number not in self.num_to_index:
            return []
        idx = self.num_to_index[number]
        neighbors = []
        for i in range(-span, span + 1):
            if i == 0: continue
            neighbors.append(self.wheel_layout[(idx + i) % 37])
        return neighbors

    def analyze(self):
        """Perform statistical analysis on the current sequence."""
        if not self.sequence:
            return [0, 32, 15, 19] # Default starting numbers

        last_num = self.sequence[-1]
        
        # 1. Neighbor Analysis (Physical wheel proximity)
        # Often the wheel hits sectors. We look at neighbors of the last number.
        primary_neighbors = self.get_neighbors(last_num, span=2)
        
        # 2. Sector Frequency
        # Divide wheel into 4 sectors
        # Voisins du Zéro (17 numbers), Tiers du Cylindre (12), Orphelins (8)
        # For simplicity, we'll just use physical neighbors for now.
        
        # 3. "Hot" numbers in the sequence
        counts = collections.Counter(self.sequence)
        hot_numbers = [num for num, count in counts.most_common(4)]
        
        # 4. "Sleeping" numbers (not seen in a while)
        all_nums = set(range(37))
        seen_nums = set(self.sequence[-18:]) # Look at last 18 spins
        sleeping = list(all_nums - seen_nums)[:4]

        # Combine and pick top 4
        # We value physical proximity (neighbors) and recent momentum (hot)
        recommendations = []
        
        # Add primary neighbors of last hit
        recommendations.extend(primary_neighbors)
        
        # Add hot numbers if they aren't already there
        for num in hot_numbers:
            if num not in recommendations:
                recommendations.append(num)
        
        # Limit to 4
        return recommendations[:4]

if __name__ == "__main__":
    engine = RouletteEngine()
    # Quick test
    engine.add_number(32)
    print(f"Predictions after 32: {engine.analyze()}")
