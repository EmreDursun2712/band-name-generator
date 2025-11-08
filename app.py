import tkinter as tk

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Band Name Generator")

        # Header text with clickable "RUN"
        self.header = tk.Text(root, height=2, width=50, borderwidth=0, highlightthickness=0)
        self.header.insert("1.0", "Click ")
        self.header.insert("end", "RUN", "run_tag")
        self.header.insert("end", " to run...")
        self.header.tag_config("run_tag", foreground="blue", underline=True)
        self.header.tag_bind("run_tag", "<Button-1>", lambda e: self.run_program())
        self.header.configure(state="disabled")
        self.header.pack(padx=10, pady=(10, 0), fill="x")

        # Text area for console output
        self.console = tk.Text(root, height=16, width=70)
        self.console.pack(padx=10, pady=10, fill="both", expand=True)

        # Input field + send button
        input_frame = tk.Frame(root)
        input_frame.pack(padx=10, pady=(0,10), fill="x")
        tk.Label(input_frame, text="Input:").pack(side="left")
        self.entry = tk.Entry(input_frame)
        self.entry.pack(side="left", fill="x", expand=True, padx=8)
        self.send_btn = tk.Button(input_frame, text="Send", command=self.on_enter)
        self.send_btn.pack(side="left")

        # State variables
        self.running = False
        self.awaiting_input = False
        self.input_handler = None
        self.city = None
        self.pet = None

        # Pressing Enter submits input
        self.entry.bind("<Return>", self.on_enter)

    # Print a line to the console
    def println(self, text=""):
        self.console.insert(tk.END, text + "\n")
        self.console.see(tk.END)

    # Ask for user input and register a handler for the next response
    def ask(self, prompt, handler):
        self.println(prompt)
        self.input_handler = handler
        self.awaiting_input = True
        self.entry.focus_set()

    # Called when Enter or Send is pressed
    def on_enter(self, event=None):
        val = self.entry.get()
        if val.strip() == "" and not self.awaiting_input:
            return
        # Echo user input to the console
        if self.awaiting_input:
            self.println(val)
        self.entry.delete(0, tk.END)

        if self.awaiting_input and self.input_handler:
            handler = self.input_handler
            # Reset handler before invoking it
            self.input_handler = None
            self.awaiting_input = False
            handler(val)

    # Starts the program when RUN is clicked
    def run_program(self):
        if self.running:
            self.println("Program is already running...")
            return
        # Reset state
        self.running = True
        self.city = None
        self.pet = None

        self.println("Welcome to the Band Name Generator.")

        # Step 1: ask for city
        self.ask("What's the name of the city you grew up in?", self.after_city)

    def after_city(self, city_val):
        self.city = city_val.strip()
        # Step 2: ask for pet
        self.ask("What's your pet's name?", self.after_pet)

    def after_pet(self, pet_val):
        self.pet = pet_val.strip()
        # Step 3: print result
        if self.city and self.pet:
            self.println(f"Your band name could be {self.city} {self.pet}")
        else:
            self.println("Hmmm, some fields were empty 😅 Try again.")
        self.println()  # blank line
        self.running = False  # allow new RUN


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
