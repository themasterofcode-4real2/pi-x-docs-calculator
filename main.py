import os
import time
from mpmath import mp

PROGRESS_FILE = "progress.txt"
PI_FILE = "pi_digits.txt"  # This will be the single file where all digits are written

def save_progress(digits):
    """Save the current number of digits computed to the progress file."""
    with open(PROGRESS_FILE, "w") as f:
        f.write(str(digits))

def load_progress():
    """Load the number of digits computed from the progress file."""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return int(f.read().strip())
    else:
        return 0  # Start from 0 if the file doesn't exist

def compute_pi_and_save(digits, start_from=0):
    """Compute Pi and save the result to a text file."""
    mp.dps = digits + 2  # Extra digits for precision buffer
    start_time = time.time()

    pi_str = str(mp.pi)[2:]  # Remove leading "3."
    result = "3." + pi_str[start_from:digits]

    # Realtime progress updates in console
    for i in range(start_from + 1, digits + 1):
        print(f"{i}/{digits}", end="\r", flush=True)
        save_progress(i)  # Save progress after each digit
        time.sleep(0.001)  # Optional: simulate visual delay

        # Every 10 digits, append to the single pi_digits.txt file
        if i % 10 == 0:
            with open(PI_FILE, "a") as f:
                f.write(result[i-10:i])  # Append the last 10 digits to the file without new line

    elapsed = time.time() - start_time
    print(f"\nProcess Completed! Digits written to {PI_FILE}.")

def compute_pi_until_interrupt():
    """Compute Pi indefinitely until KeyboardInterrupt (Ctrl+C)."""
    digits = load_progress()  # Start from the last computed digit
    if digits == 0:
        digits = 1000  # Initial digits to start with if nothing is stored

    try:
        while True:
            print(f"\nStarting computation for {digits} digits of Pi...")
            compute_pi_and_save(digits, start_from=digits)
            digits += 10  # Increment digits after each run
    except KeyboardInterrupt:
        print("\nPi calculation stopped by user.")
        print("Goodbye!")

if __name__ == "__main__":
    option = input("How many digits do you want to calculate? (Enter number or type 'F' for infinite calculation until interrupted): ")
    
    if option.lower() == 'f':
        print("You have chosen to calculate Pi until interrupted. Press Ctrl+C to stop.")
        compute_pi_until_interrupt()
    else:
        try:
            digits = int(option)
            compute_pi_and_save(digits)
        except ValueError:
            print("Invalid input. Please enter a valid number of digits.")
