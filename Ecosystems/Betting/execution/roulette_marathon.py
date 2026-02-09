|import sys
import os
from roulette_engine import RouletteEngine

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    engine = RouletteEngine()
    print("=== ROULETTE TESTING MARATHON ACTIVATED ===")
    print("Enter the winning number (0-36) after each spin.")
    print("Type 'exit' to quit.\n")

    while True:
        try:
            user_input = input("Spin Outcome > ").strip().lower()
            if user_input == 'exit':
                break
            
            num = int(user_input)
            if not (0 <= num <= 36):
                print("Invalid number. Must be 0-36.")
                continue

            engine.add_number(num)
            predictions = engine.analyze()
            
            # Display results fast
            print(f"[{len(engine.sequence)}] Last: {num} | Predictions for NEXT: {', '.join(map(str, predictions))}")
            
        except ValueError:
            print("Please enter a valid number.")
        except KeyboardInterrupt:
            break

    print("\nMarathon ended. Sequence summary:", engine.sequence)

if __name__ == "__main__":
    main()
