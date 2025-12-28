import tkinter as tk
from tkinter import ttk, messagebox
import time
import random
from abc import ABC, abstractmethod
from datetime import datetime


class MainWindow:
    """Main window class, creates GUI and directs to user selected algorithm"""
    def __init__(self, root):
        self.root = root
        self.root.title("Algorithm Workshop")
        self.root.geometry("600x500")

        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)

        self.show_main_menu()

    """Clears the window"""
    def clear_window(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_main_menu(self):
        """Creates the main menu, this code is similar across all classes"""
        self.clear_window()

        tk.Label(self.container, text="Algorithm Toolset", font=("Arial", 18, "bold")).pack(pady=10)

        self.algorithm_choice = ttk.Combobox(self.container, values=[
            "RSA Encryption",
            "Fibonacci (DP)",
            "Sorting (Bubble/Selection)",
            "Merge Sort (Divide & Conquer)",
            "Shuffle Deck",
            "Factorial",
            "Search",
            "Palindrome Counter"
        ], width=40)
        self.algorithm_choice.pack(pady=10)

        tk.Frame(self.container, height=2, bd=1, relief="sunken").pack(fill="x", pady=20)
        tk.Label(self.container, text="Global History (Last 5 Runs)", font=("Arial", 10, "bold")).pack()

        """Calls the history function to list previous algorithms"""
        history_list = AlgorithmHistory.get_history()

        if not history_list:
            tk.Label(self.container, text="No algorithms run yet.", fg="gray").pack()
        else:
            for entry in reversed(history_list):
                tk.Label(self.container, text=entry, font=("Courier", 9), anchor="w").pack(fill="x")

        self.run_btn = tk.Button(self.container, text="Select", command=self.handle_execution, bg="green", fg="white")
        self.run_btn.pack(pady=20)

    """Calls design pattern to direct user traffic"""
    def handle_execution(self):
        choice = self.algorithm_choice.get()

        view = AlgorithmSelector.create_view(
            choice,
            self.container,
            self.show_main_menu
        )

        if not view:
            print(f"Error: Logic for {choice} not found.")


class RSAView:
    """RSA Encryption for Requirement 1"""
    def __init__(self, parent, back_callback):
        """Creates RSA Encryption GUI"""
        self.parent = parent
        for widget in self.parent.winfo_children():
            widget.destroy()

        tk.Label(self.parent, text="RSA Encryption Module", font=("Arial", 18, "bold")).pack(pady=10)

        tk.Label(self.parent, text="Enter Message to Encrypt/Decrypt:").pack(pady=5)
        self.user_input = tk.Entry(self.parent, width=50)
        self.user_input.pack(pady=5)

        tk.Label(self.parent, text="Enter 2 Keys to Encrypt/Decrypt Seperated by ',' (leave blank for random Keys):").pack(pady=5)
        self.user_key = tk.Entry(self.parent, width=50)
        self.user_key.pack(pady=5)


        tk.Button(self.parent, text="Encrypt", command=self.get_Keys).pack(pady=5)

        self.cipherText_label = tk.Label(self.parent,text="Encrypted text: ")
        self.cipherText_label.pack(pady=5)
        self.plainText_label = tk.Label(self.parent,text="Decrypted text: ")
        self.plainText_label.pack(pady=5)

        tk.Button(self.parent, text="Back to Menu", command=back_callback).pack(pady=20)

    def is_prime(self, n):
        """Checks if n is prime"""
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True

    def generate_keys(self, start, end):
        """Generates random keys when the user enters none"""
        primes = []

        while len(primes) < 2:
            candidate = random.randint(start, end)
            if self.is_prime(candidate) and candidate not in primes:
                primes.append(candidate)
        return primes

    def get_Keys(self):
        user_key_text = self.user_key.get()

        """Checks if user key is random or selected (and valid)"""
        if user_key_text == "":
            primes = self.generate_keys(10, 1000)
            self.p, self.q = primes[0], primes[1]
        else:
            try:
                keys = list(map(int, user_key_text.split(',')))
                self.p, self.q = keys[0], keys[1]
                if not self.is_prime(self.p) or not self.is_prime(self.q):
                    messagebox.showerror("Error", "Please enter two prime numbers")
                    return
            except:
                messagebox.showerror("Error", "Format must be: prime, prime")
                return

        """Calculates values for RSA Encryption"""
        self.n = self.p * self.q
        self.r = (self.p - 1) * (self.q - 1)

        self.e = 65537
        """Ensures e and r are nor co-primes"""
        if self.r <= self.e: self.e = 3
        try:
            self.d = pow(self.e, -1, self.r)
            self.process_rsa()
        except ValueError:
            messagebox.showerror("Error", "e and r are not coprime. Try different primes.")

    def process_rsa(self):
        message = self.user_input.get()
        if not message: return

        """Runs the RSA Encryption Algorithm"""
        self.ciphertext = [pow(ord(char), self.e, self.n) for char in message]
        self.cipherText_label.config(text=f"Encrypted text: {self.ciphertext}")

        """Runs the RSA Decryption Algorithm"""
        decrypted_chars = [chr(pow(char, self.d, self.n)) for char in self.ciphertext]
        self.message = "".join(decrypted_chars)
        self.plainText_label.config(text=f"Decrypted text: {self.message}")

        """Adds to the history"""
        AlgorithmHistory.add_entry("RSA", f"Encrypted: '{self.message} to {self.ciphertext}'")


class FibonacciAlgorithm:
    """Fibonacci Algorithm for Requirement 2"""
    def __init__(self, parent, back_callback):
        self.parent = parent
        for widget in self.parent.winfo_children():
            widget.destroy()

        tk.Label(self.parent, text="Fibonacci", font=("Arial", 18, "bold")).pack(pady=10)

        tk.Label(self.parent, text="Enter number of steps in sequence").pack(pady=5)
        self.user_input = tk.Entry(self.parent)
        self.user_input.pack(pady=5)

        tk.Button(self.parent, text="Calculate", command=self.solve).pack(pady=5)

        self.result_label = tk.Label(self.parent, text="Result: ", font=("Arial", 12))
        self.result_label.pack(pady=20)


        tk.Button(self.parent, text="Back to Menu", command=back_callback).pack(pady=20)


    def solve(self):
        """Checks the value is entered correctly"""
        if self.user_input.get != '': n = int(self.user_input.get().strip())
        if n < 0:
            return "Invalid Input"
        if n == 0:
            return 0
        if n == 1:
            return 1

        """Creates the table to solve the Fibonacci Algorithm using dynamic programming"""
        fib_table = [0] * (n + 1)
        fib_table[0] = 0
        fib_table[1] = 1

        """Fills in the table and returns the result"""
        for i in range(2, n + 1):
            fib_table[i] = fib_table[i - 1] + fib_table[i - 2]
        result = fib_table[n]

        """Adds to history log"""
        AlgorithmHistory.add_entry("Fibonacci", f"Calculated sequence up to {self.user_input.get()}")
        self.result_label.config(text=f"Result: {result}")


class SortingAlgorithm:
    """Sorting algorithms for Requirement 3"""
    def __init__(self, parent, back_callback):
        self.parent = parent
        for widget in self.parent.winfo_children():
            widget.destroy()

        tk.Label(self.parent, text="Sorting Algorithms", font=("Arial", 18, "bold")).pack(pady=10)

        tk.Label(self.parent, text="Enter Comma seperated list").pack(pady=5)
        self.user_input = tk.Entry(self.parent, width=50)
        self.user_input.pack(pady=5)


        tk.Button(self.parent, text="Bubble", command=self.BubbleAlgorithm).pack(padx=5, pady=5)
        tk.Button(self.parent, text="Selection", command=self.SelectionAlgorithm).pack(padx=10)

        self.sortOrder = ttk.Combobox(self.parent, values=["Ascending", "Descending"])
        self.sortOrder.pack(pady=5)

        self.result_label = tk.Label(self.parent, text="Result: ", font=("Arial", 12))
        self.result_label.pack(pady=20)

        tk.Button(self.parent, text="Back to Menu", command=back_callback).pack(pady=20)

    def BubbleAlgorithm(self):
        """Bubble algorithm for half for Requirement 3"""
        order = self.sortOrder.get()[0]

        """Sets default ofter to Ascending"""
        if order == "": order = "A"
        self.input = [int(x.strip()) for x in self.user_input.get().split(',') if x.strip()]

        if order ==  "A":
            """Bubble sort for ascending order"""
            for j in range(len(self.input)):
                for i in range(len(self.input) - 1):
                    if self.input[i] > self.input[i + 1]:
                        temporaryNumber = int(self.input[i + 1])
                        self.input[i + 1] = self.input[i]
                        self.input[i] = temporaryNumber
        elif order == "D":
            """Bubble sort for descending order"""
            for j in range(len(self.input)):
                for i in range(len(self.input) - 1):
                    if self.input[i] < self.input[i + 1]:
                        temporaryNumber = int(self.input[i + 1])
                        self.input[i + 1] = self.input[i]
                        self.input[i] = temporaryNumber

        self.result_label.config(text=f"Result: {self.input}")
        """Adds to history log"""
        AlgorithmHistory.add_entry(f"Sorted", f"{self.input} with Bubble Algorithm")

    def SelectionAlgorithm(self):
        """Selection algorithm for half of Requirement 3"""
        order = self.sortOrder.get()[0]

        """Sets default order to Ascending"""
        if order == "": order = "A"
        self.input = [int(x.strip()) for x in self.user_input.get().split(',') if x.strip()]
        n = len(self.input)

        for i in range(n):
            extreme_index = i
            for j in range(i + 1, n):
                if order == "A":
                    """Selection sort for ascending order"""
                    if self.input[j] < self.input[extreme_index]:
                        extreme_index = j
                else:
                    """Selection sort for descending order"""
                    if self.input[j] > self.input[extreme_index]:
                        extreme_index = j
            if extreme_index != i:
                self.input[i], self.input[extreme_index] = self.input[extreme_index], self.input[i]

        self.result_label.config(text=f"Result: {self.input}")

        """Adds to history log"""
        AlgorithmHistory.add_entry(f"Sorted", f"{self.input} with Selection Algorithm")


class MergeSort:
    """Merge sort algorithms for Requirement 4"""
    def __init__(self, parent, back_callback):
        self.parent = parent
        for widget in self.parent.winfo_children():
            widget.destroy()

        tk.Label(self.parent, text="Divide and Conquer", font=("Arial", 18, "bold")).pack(pady=10)

        tk.Label(self.parent, text="Enter Comma seperated list").pack(pady=5)
        self.user_input = tk.Entry(self.parent, width=50)
        self.user_input.pack(pady=5)

        self.sortOrder = ttk.Combobox(self.parent, values=["Ascending", "Descending"])
        self.sortOrder.pack(pady=5)
        array = []
        order  = ""

        tk.Button(self.parent, text="Sort", command=lambda: self.sort(array, order)).pack(padx=10)

        self.result_label = tk.Label(self.parent, text="Result: ", font=("Arial", 12))
        self.result_label.pack(pady=20)

        self.timeKeeper = tk.Label(self.parent, text="Time taken: ", font=("Arial", 12))

        tk.Button(self.parent, text="Back to Menu", command=back_callback).pack(pady=20)

        self.decorated_sort = TimeTracker(self.sort_logic)

    def sort_logic(self, array, order):
        n = len(array)
        """Checks is array is length 1"""

        if n <= 1: return array

        """Splits array into two halves"""
        mid = n // 2
        left = self.sort_logic(array[:mid], order)
        right = self.sort_logic(array[mid:], order)
        return self.merge(left, right, order)

    def sort(self, array, order):
        """Code to stop recursive bug from crashing program
         Code from 'is not array:' to 'return' was generated by claude AI"""
        if not array:
            try:
                order = self.sortOrder.get()[0] if self.sortOrder.get() else "A"
                array = [int(x.strip()) for x in self.user_input.get().split(',') if x.strip()]
            except (ValueError, IndexError):
                self.result_label.config(text="Error: Invalid Input")
                return

        final_merge = self.decorated_sort(array, order)

        self.result_label.config(text=f"Result: {final_merge}")

        """Adds to history log"""
        AlgorithmHistory.add_entry(f"Sorted", f"{final_merge} with Merge Algorithm")

        return final_merge

    def merge(self, left, right, order):
        """Merges two sorted arrays"""
        sorted_array = []
        i = 0
        j = 0
        while i < len(left) and j < len(right):
            if order == "A":
                condition = left[i] <= right[j]
            else:
                condition = left[i] >= right[j]

            if condition:
                sorted_array.append(left[i])
                i += 1
            else:
                sorted_array.append(right[j])
                j += 1

        sorted_array.extend(left[i:])
        sorted_array.extend(right[j:])

        return sorted_array


class DeckShuffle:
    """Deck shuffle algorithms for Requirement 5"""
    def __init__(self, parent, back_callback):
        self.parent = parent
        for widget in self.parent.winfo_children():
            widget.destroy()

        tk.Label(self.parent, text="Randomized Deck Shuffle", font=("Arial", 18, "bold")).pack(pady=10)

        tk.Button(self.parent, text="Shuffle New Deck", command=self.display_shuffle, bg="blue", fg="white").pack(
            pady=10)

        # https://www.geeksforgeeks.org/python/python-tkinter-text-widget/
        """Code to create large text box to list results, used above link"""
        self.result_area = tk.Text(self.parent, height=12, width=50)
        self.result_area.pack(pady=10)

        tk.Button(self.parent, text="Back to Menu", command=back_callback).pack(pady=10)

    def create_deck(self):
        """Creates all possible cards in deck"""
        suits = ['H', 'D', 'C', 'S']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        return [f"{v} {s}" for s in suits for v in values]

    def shuffle(self, deck):
        # https://www.geeksforgeeks.org/dsa/shuffle-a-given-array-using-fisher-yates-shuffle-algorithm/
        """Shuffles deck using algorithm from above link"""
        n = len(deck)
        for i in range(n - 1, 0, -1):
            j = random.randint(0, i)
            deck[i], deck[j] = deck[j], deck[i]
        return deck

    def display_shuffle(self):
        """Displays shuffled deck"""
        deck = self.create_deck()
        shuffled_deck = self.shuffle(deck)

        self.result_area.delete('1.0', tk.END)
        for i, card in enumerate(shuffled_deck, 1):
            self.result_area.insert(tk.END, f"{i}. {card}\n")

        """Adds to history log"""
        AlgorithmHistory.add_entry(f"Shuffled a deck of cards", f"{shuffled_deck}")


class FactorialRecursion:
    """Factorial recursion algorithms for Requirement 6"""
    def __init__(self, parent, back_callback):
        self.parent = parent
        for widget in self.parent.winfo_children():
            widget.destroy()

        tk.Label(self.parent, text="Recursive Factorial", font=("Arial", 18, "bold")).pack(pady=10)

        tk.Label(self.parent, text="Enter a non-negative integer:").pack(pady=5)
        self.user_input = tk.Entry(self.parent)
        self.user_input.pack(pady=5)

        tk.Button(self.parent, text="Calculate", command=self.run_factorial, bg="purple", fg="white").pack(pady=10)

        self.result_label = tk.Label(self.parent, text="Result: ", font=("Arial", 12))
        self.result_label.pack(pady=20)

        tk.Button(self.parent, text="Back to Menu", command=back_callback).pack(pady=10)

    def calculate_factorial(self, n):
        """Calculates factorial of n Recursively for Requirement"""
        if n == 0 or n == 1:
            return 1
        else:
            return n * self.calculate_factorial(n - 1)

    def run_factorial(self):
        val = self.user_input.get().strip()
        """Validates that input is both positive and not too large"""
        try:
            n = int(val)
            if n < 0:
                self.result_label.config(text="Error: Enter a positive number")
            elif n > 992:
                self.result_label.config(text="Error: Number too large for recursion")
            else:
                result = self.calculate_factorial(n)
                self.result_label.config(text=f"Result: {result}")

                """Adds to history log"""
                AlgorithmHistory.add_entry(f"Calculated factorial of {val} as: ", result)
        except ValueError:
            self.result_label.config(text="Error: Invalid input")


class SearchStatistics:
    """Search statistics algorithms for Requirement 7"""
    def __init__(self, parent, back_callback):
        self.parent = parent
        for widget in self.parent.winfo_children():
            widget.destroy()

        tk.Label(self.parent, text="Array Statistics", font=("Arial", 18, "bold")).pack(pady=10)

        tk.Label(self.parent, text="Enter numbers separated by commas:").pack()
        self.user_input = tk.Entry(self.parent, width=50)
        self.user_input.pack(pady=5)

        tk.Button(self.parent, text="Calculate Stats", command=self.process_stats).pack(pady=10)

        self.result_box = tk.Label(self.parent, text="", justify="left", font=("Courier", 10))
        self.result_box.pack(pady=10)

        tk.Button(self.parent, text="Back", command=back_callback).pack()

    def calculate_mode(self, arr):
        """Calculates mode of array"""
        counts = {}
        for num in arr:
            counts[num] = counts.get(num, 0) + 1

        max_count = max(counts.values())
        modes = [k for k, v in counts.items() if v == max_count]
        return modes if len(modes) < len(arr) else "No unique mode"

    def get_percentile(self, sorted_arr, percentile):
        """Function to calculate a given percentile"""
        n = len(sorted_arr)
        index = percentile * (n - 1)
        lower = int(index)
        upper = lower + 1

        if upper >= n:
            return sorted_arr[lower]

        weight = index - lower
        return sorted_arr[lower] * (1 - weight) + sorted_arr[upper] * weight

    def process_stats(self):
        """Collects all the data and displays to the user"""
        raw_data = self.user_input.get()
        data = sorted([int(x.strip()) for x in raw_data.split(',') if x.strip()])

        if not data: return

        smallest = data[0]
        largest = data[-1]
        mode = self.calculate_mode(data)
        median = self.get_percentile(data, 0.5)
        q1 = self.get_percentile(data, 0.25)
        q3 = self.get_percentile(data, 0.75)

        res = (f"Smallest: {smallest}\n"
                f"Largest:  {largest}\n"
                f"Mode:     {mode}\n"
                f"Median:   {median:.2f}\n"
                f"1st Q (Q1): {q1:.2f}\n"
                f"3rd Q (Q3): {q3:.2f}")
        self.result_box.config(text=res)

        """Adds to history log"""
        AlgorithmHistory.add_entry(f"Searched {raw_data} and found \n {res}", "")


class PalindromeCounter:
    """Palindrome Counter algorithms for Requirement 8"""
    def __init__(self, parent, back_callback):
        self.parent = parent
        for widget in self.parent.winfo_children():
            widget.destroy()

        tk.Label(self.parent, text="Palindrome Substring Counter", font=("Arial", 18, "bold")).pack(pady=10)

        tk.Label(self.parent, text="Enter a string:").pack(pady=5)
        self.user_input = tk.Entry(self.parent, width=40)
        self.user_input.pack(pady=5)

        tk.Button(self.parent, text="Count Palindromes", command=self.run_logic, bg="teal", fg="white").pack(pady=10)

        self.result_label = tk.Label(self.parent, text="Total Palindromes: ", font=("Arial", 12))
        self.result_label.pack(pady=10)

        self.found_area = tk.Text(self.parent, height=8, width=40)
        self.found_area.pack(pady=10)

        tk.Button(self.parent, text="Back to Menu", command=back_callback).pack(pady=10)

    def run_logic(self):
        s = self.user_input.get().strip()
        if not s: return ""

        """Creates variables needed"""
        n = len(s)
        memo = [[False] * n for _ in range(n)]
        count = 0
        palindromes_found = []

        for i in range(n):
            """Checks all 1 length palindromes,
            All individual characters are palindromes by default"""
            memo[i][i] = True
            count += 1
            palindromes_found.append(s[i])

        for i in range(n - 1):
            """Checks all 2 length palindromes,"""
            if s[i] == s[i + 1]:
                memo[i][i + 1] = True
                count += 1
                palindromes_found.append(s[i:i + 2])

        for k in range(3, n + 1):
            """Checks all 3 or more length palindromes,"""
            for i in range(n - k + 1):
                j = i + k - 1
                if s[i] == s[j] and memo[i + 1][j - 1]:
                    memo[i][j] = True
                    count += 1
                    palindromes_found.append(s[i:j + 1])

        self.result_label.config(text=f"Total Palindromes: {count}")
        self.found_area.delete('1.0', tk.END)
        self.found_area.insert(tk.END, ", ".join(palindromes_found))

        """Adds to history log"""
        AlgorithmHistory.add_entry(f"Looked at", f"{s} and found {count} palindromes")


class Command(ABC):
    @abstractmethod
    def execute(self):
        """Executes the command"""
        pass

class AlgorithmHistory:
    """Behavioural Design Pattern (AlgorithmHistory) for Requirement 9"""
    """Acts as a central registry for algorithm execution logs
        This class uses Class Methods and Class Variables so that history
        is shared globally"""
    _history = []

    @classmethod
    def add_entry(cls, algorithm_name, details):
        """Creates a timestamped log entry and adds it to the global history"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        entry = f"[{timestamp}] {algorithm_name}: {details}"
        cls._history.append(entry)
        """Keep only the last 5 entries"""
        if len(cls._history) > 5:
            cls._history.pop(0)

    @classmethod
    def get_history(cls):
        """Returns the list of stored log entries for the UI to display"""
        return cls._history


class AlgorithmSelector:
    # https://www.geeksforgeeks.org/python/factory-method-python-design-patterns/
    """Creational Design Pattern (AlgorithmSelector) for Requirement 10, used code from above link"""
    @staticmethod
    def create_view(choice, parent, back_callback):
        """Links choices to class that needs to be used"""
        views = {
            "RSA Encryption": RSAView,
            "Fibonacci (DP)": FibonacciAlgorithm,
            "Sorting (Bubble/Selection)": SortingAlgorithm,
            "Merge Sort (Divide & Conquer)": MergeSort,
            "Shuffle Deck": DeckShuffle,
            "Factorial": FactorialRecursion,
            "Search": SearchStatistics,
            "Palindrome Counter": PalindromeCounter
        }

        view_class = views.get(choice)

        """If choice is selected, direct to that choice"""
        if view_class:
            return view_class(parent, back_callback)
        return None


class TimeTracker:
    """Structural Design Pattern (TimeTracker) for Requirement 11"""
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        # https://www.geeksforgeeks.org/python/time-perf_counter-function-in-python/
        """Tracks time taken for algorithm to run, uses code from above link"""
        start_time = time.perf_counter()

        result = self.func(*args, **kwargs)

        end_time = time.perf_counter()
        duration = end_time - start_time

        messagebox.showinfo(title="Time Tracker", message=f"Time taken: {duration:.8f} seconds")
        return result


if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()