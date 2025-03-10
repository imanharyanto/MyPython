import tkinter as tk
from tkinter import ttk
import math
from functools import partial

class GradientCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Gradient Blue Calculator")
        self.root.geometry("350x500")
        self.root.resizable(False, False)
        
        # Colors - vibrant blue sky to navy blue gradient
        self.colors = {
            "light_blue": "#1E90FF",  # Vibrant blue sky
            "medium_blue": "#4169E1",  # Royal blue
            "dark_blue": "#000080",    # Navy blue
            "text_color": "white",
            "accent": "#87CEEB",       # Sky blue for highlights
            "button_hover": "#00BFFF"  # Deep sky blue for hover
        }
        
        # Initial setup
        self.root.configure(bg=self.colors["medium_blue"])
        self.create_display()
        self.create_buttons()
        
        # Variables
        self.current_expression = ""
        self.current_value = 0
        self.pending_operation = None
        self.update_display("0")

    def create_display(self):
        # Create a gradient frame for the display
        display_frame = tk.Frame(self.root, height=100, bg=self.colors["light_blue"])
        display_frame.pack(fill="x", padx=10, pady=(10, 0))
        
        # Expression display
        self.expression_var = tk.StringVar()
        self.expression_label = tk.Label(
            display_frame, 
            textvariable=self.expression_var,
            font=("Arial", 12),
            bg=self.colors["light_blue"],
            fg=self.colors["text_color"],
            anchor="e",
            padx=10
        )
        self.expression_label.pack(fill="x", pady=(10, 0))
        
        # Result display
        self.display_var = tk.StringVar()
        self.display = tk.Label(
            display_frame, 
            textvariable=self.display_var,
            font=("Arial", 24, "bold"),
            bg=self.colors["light_blue"],
            fg=self.colors["text_color"],
            anchor="e",
            padx=10
        )
        self.display.pack(fill="x", expand=True)

    def create_buttons(self):
        # Create main button frame with gradient background
        button_frame = tk.Frame(self.root, bg=self.colors["medium_blue"])
        button_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configure button styles
        button_style = {
            "font": ("Arial", 16),
            "borderwidth": 0,
            "relief": "flat",
            "padx": 10,
            "pady": 10,
        }
        
        # Define button layout
        button_layout = [
            [("C", self.clear), ("±", self.negate), ("%", self.percent), ("÷", partial(self.operation, "/"))],
            [("7", partial(self.append_digit, "7")), ("8", partial(self.append_digit, "8")), 
             ("9", partial(self.append_digit, "9")), ("×", partial(self.operation, "*"))],
            [("4", partial(self.append_digit, "4")), ("5", partial(self.append_digit, "5")), 
             ("6", partial(self.append_digit, "6")), ("−", partial(self.operation, "-"))],
            [("1", partial(self.append_digit, "1")), ("2", partial(self.append_digit, "2")), 
             ("3", partial(self.append_digit, "3")), ("+", partial(self.operation, "+"))],
            [("0", partial(self.append_digit, "0")), (".", partial(self.append_digit, ".")), 
             ("√", self.square_root), ("=", self.calculate)]
        ]
        
        # Create buttons
        for i, row in enumerate(button_layout):
            for j, (text, command) in enumerate(row):
                # Determine button color based on type
                if text in ["=", "+", "−", "×", "÷"]:
                    bg_color = self.colors["dark_blue"]
                elif text in ["C", "±", "%", "√"]:
                    bg_color = self.colors["medium_blue"]
                else:
                    bg_color = self.colors["light_blue"]
                
                # Create and place button with gradient effect
                btn = tk.Button(
                    button_frame,
                    text=text,
                    command=command,
                    bg=bg_color,
                    fg=self.colors["text_color"],
                    activebackground=self.colors["button_hover"],
                    activeforeground=self.colors["text_color"],
                    **button_style
                )
                
                # Configure button behavior on hover
                btn.bind("<Enter>", lambda e, btn=btn: btn.config(bg=self.colors["accent"]))
                btn.bind("<Leave>", lambda e, btn=btn, bg=bg_color: btn.config(bg=bg))
                
                # Place in grid with some padding for a nicer look
                btn.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")
                
            # Configure row and column weights
            button_frame.grid_rowconfigure(i, weight=1)
            
        for j in range(4):
            button_frame.grid_columnconfigure(j, weight=1)

    def update_display(self, text):
        self.display_var.set(text)

    def update_expression(self, text):
        self.expression_var.set(text)

    def append_digit(self, digit):
        if self.display_var.get() == "0" and digit != ".":
            self.current_expression = digit
            self.update_display(digit)
        else:
            current = self.display_var.get()
            # Prevent multiple decimal points
            if digit == "." and "." in current:
                return
            self.current_expression = current + digit
            self.update_display(self.current_expression)

    def operation(self, op):
        try:
            # Store current value and operation
            self.current_value = float(self.display_var.get())
            self.pending_operation = op
            
            # Update expression display
            display_op = {"*": "×", "/": "÷", "+": "+", "-": "−"}[op]
            self.update_expression(f"{self.current_value} {display_op}")
            
            # Reset display for new input
            self.current_expression = ""
            self.update_display("0")
        except ValueError:
            self.update_display("Error")

    def calculate(self):
        if not self.pending_operation:
            return
            
        try:
            # Get the second operand
            second_operand = float(self.display_var.get())
            
            # Perform the calculation
            if self.pending_operation == "+":
                result = self.current_value + second_operand
            elif self.pending_operation == "-":
                result = self.current_value - second_operand
            elif self.pending_operation == "*":
                result = self.current_value * second_operand
            elif self.pending_operation == "/":
                if second_operand == 0:
                    self.update_display("Error")
                    return
                result = self.current_value / second_operand
                
            # Update display
            # For integer results, show as integers
            if result.is_integer():
                self.update_display(str(int(result)))
            else:
                self.update_display(str(result))
                
            # Update expression
            display_op = {"*": "×", "/": "÷", "+": "+", "-": "−"}[self.pending_operation]
            self.update_expression(f"{self.current_value} {display_op} {second_operand} =")
            
            # Reset for next calculation
            self.current_value = result
            self.pending_operation = None
            self.current_expression = str(result)
            
        except ValueError:
            self.update_display("Error")

    def clear(self):
        self.current_expression = ""
        self.current_value = 0
        self.pending_operation = None
        self.update_display("0")
        self.update_expression("")

    def negate(self):
        try:
            value = float(self.display_var.get())
            value = -value
            
            # For integer results, show as integers
            if value.is_integer():
                self.update_display(str(int(value)))
            else:
                self.update_display(str(value))
                
            self.current_expression = str(value)
        except ValueError:
            self.update_display("Error")

    def percent(self):
        try:
            value = float(self.display_var.get())
            value = value / 100
            
            # For integer results, show as integers
            if value.is_integer():
                self.update_display(str(int(value)))
            else:
                self.update_display(str(value))
                
            self.current_expression = str(value)
        except ValueError:
            self.update_display("Error")

    def square_root(self):
        try:
            value = float(self.display_var.get())
            if value < 0:
                self.update_display("Error")
                return
                
            result = math.sqrt(value)
            
            # For integer results, show as integers
            if result.is_integer():
                self.update_display(str(int(result)))
            else:
                self.update_display(str(result))
                
            self.current_expression = str(result)
        except ValueError:
            self.update_display("Error")

if __name__ == "__main__":
    root = tk.Tk()
    app = GradientCalculator(root)
    root.mainloop()
