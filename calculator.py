import tkinter as tk
import math


# =========================================================
# COLORS
# =========================================================

BACKGROUND = "#10151d"
DISPLAY_BG = "#171d26"
DISPLAY_BORDER = "#303846"

NUMBER_BG = "#252d39"
NUMBER_HOVER = "#303a48"

OPERATOR_BG = "#0fb9b2"
OPERATOR_HOVER = "#11a9a3"

TEXT_WHITE = "#f5f7fa"
TEXT_SECONDARY = "#8e98a7"


# =========================================================
# MAIN WINDOW
# =========================================================

root = tk.Tk()
root.title("Calculator")
root.geometry("330x500")
root.resizable(False, False)
root.configure(bg=BACKGROUND)


# =========================================================
# TOP SPACING
# =========================================================

top_frame = tk.Frame(
    root,
    bg=BACKGROUND,
    height=38
)

top_frame.pack(
    fill="x",
    padx=20,
    pady=(10, 2)
)

top_frame.pack_propagate(False)


# =========================================================
# CALCULATOR VARIABLES
# =========================================================

first_number = None
operator = None

new_number = True

# Used for repeated "="
last_number = None
last_operator = None


# =========================================================
# DISPLAY AREA
# =========================================================

display_frame = tk.Frame(
    root,
    bg=DISPLAY_BG,
    highlightbackground=DISPLAY_BORDER,
    highlightthickness=1
)

display_frame.pack(
    fill="x",
    padx=20,
    pady=(0, 14)
)

display_frame.pack_propagate(False)

display_frame.configure(height=92)


# Expression shown above the main number
expression_label = tk.Label(
    display_frame,
    text="",
    bg=DISPLAY_BG,
    fg=TEXT_SECONDARY,
    font=("Segoe UI", 10),
    anchor="e"
)

expression_label.pack(
    fill="x",
    padx=16,
    pady=(10, 0)
)


# Main calculator display
display = tk.Entry(
    display_frame,
    bg=DISPLAY_BG,
    fg=TEXT_WHITE,
    insertbackground=TEXT_WHITE,
    relief="flat",
    bd=0,
    justify="right",
    font=("Segoe UI", 28, "bold")
)

display.pack(
    fill="both",
    expand=True,
    padx=16,
    pady=(0, 10)
)

display.insert(0, "0")


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def get_display_value():
    """Return the current display value as float."""

    try:
        return float(display.get())
    except ValueError:
        return None


def format_number(number):
    """Make calculator results look cleaner."""

    if number == int(number):
        return str(int(number))

    return str(round(number, 10))


def set_display(value):
    """Replace the display with a value."""

    display.delete(0, tk.END)
    display.insert(0, value)


def operator_symbol(op):
    """Convert internal operators to calculator symbols."""

    symbols = {
        "+": "+",
        "-": "−",
        "*": "×",
        "/": "÷"
    }

    return symbols.get(op, op)


def calculate(first, second, op):
    """Perform the actual calculation."""

    if op == "+":
        return first + second

    elif op == "-":
        return first - second

    elif op == "*":
        return first * second

    elif op == "/":

        if second == 0:
            return None

        return first / second

    return None


def show_error():
    """Show calculator error."""

    set_display("Error")
    expression_label.config(text="")


# =========================================================
# NUMBER BUTTON
# =========================================================

def number_click(number):

    global new_number
    global last_number
    global last_operator

    # Start fresh after an error
    if display.get() == "Error":
        set_display(number)
        new_number = False

        last_number = None
        last_operator = None

        return

    # Start a new number
    if new_number:

        set_display(number)

        new_number = False

        # Typing a new number cancels repeated "="
        last_number = None
        last_operator = None

        return

    current = display.get()

    # Replace initial zero
    if current == "0":
        set_display(number)

    else:
        set_display(current + number)

    last_number = None
    last_operator = None


# =========================================================
# DECIMAL BUTTON
# =========================================================

def decimal_click():

    global new_number
    global last_number
    global last_operator

    if display.get() == "Error":

        set_display("0.")
        new_number = False

        last_number = None
        last_operator = None

        return

    if new_number:

        set_display("0.")
        new_number = False

        last_number = None
        last_operator = None

        return

    current = display.get()

    if "." not in current:

        set_display(current + ".")

    last_number = None
    last_operator = None


# =========================================================
# OPERATOR BUTTON
# =========================================================

def operator_click(selected_operator):

    global first_number
    global operator
    global new_number
    global last_number
    global last_operator

    current = get_display_value()

    if current is None:
        return

    # If an operator is already waiting and the user
    # enters another operator, calculate the first one.
    if operator is not None and not new_number:

        result = calculate(
            first_number,
            current,
            operator
        )

        if result is None:

            show_error()

            first_number = None
            operator = None
            new_number = True

            return

        first_number = result

        set_display(format_number(result))

    # Start a new calculation
    elif operator is None:

        first_number = current

    operator = selected_operator

    new_number = True

    last_number = None
    last_operator = None

    expression_label.config(
        text=f"{format_number(first_number)} "
             f"{operator_symbol(operator)}"
    )


# =========================================================
# CLEAR BUTTON
# =========================================================

def clear_click():

    global first_number
    global operator
    global new_number
    global last_number
    global last_operator

    first_number = None
    operator = None

    new_number = True

    last_number = None
    last_operator = None

    set_display("0")
    expression_label.config(text="")


# =========================================================
# DELETE BUTTON
# =========================================================

def delete_click():

    global new_number
    global last_number
    global last_operator

    if display.get() == "Error":

        clear_click()
        return

    if new_number:
        return

    current = display.get()

    if len(current) <= 1:

        set_display("0")
        new_number = True

    else:

        set_display(current[:-1])

    last_number = None
    last_operator = None


# =========================================================
# PERCENT BUTTON
# =========================================================

def percent_click():

    global new_number
    global last_number
    global last_operator

    current = get_display_value()

    if current is None:
        return

    result = current / 100

    set_display(format_number(result))

    new_number = False

    last_number = None
    last_operator = None


# =========================================================
# EQUALS BUTTON
# =========================================================

def equals_click():

    global first_number
    global operator
    global new_number
    global last_number
    global last_operator

    current = get_display_value()

    if current is None:
        return

    # -----------------------------------------------------
    # NORMAL CALCULATION
    # -----------------------------------------------------

    if first_number is not None and operator is not None:

        second_number = current

        result = calculate(
            first_number,
            second_number,
            operator
        )

        if result is None:

            show_error()

            first_number = None
            operator = None
            new_number = True

            last_number = None
            last_operator = None

            return

        expression_label.config(
            text=f"{format_number(first_number)} "
                 f"{operator_symbol(operator)} "
                 f"{format_number(second_number)} ="
        )

        set_display(format_number(result))

        # Save information for repeated "="
        last_number = second_number
        last_operator = operator

        first_number = None
        operator = None

        new_number = True

        return

    # -----------------------------------------------------
    # REPEATED "="
    # Example:
    #
    # 5 + 3 = 8
    # =      11
    # =      14
    # -----------------------------------------------------

    if last_number is not None and last_operator is not None:

        first = current

        result = calculate(
            first,
            last_number,
            last_operator
        )

        if result is None:

            show_error()

            last_number = None
            last_operator = None

            return

        expression_label.config(
            text=f"{format_number(first)} "
                 f"{operator_symbol(last_operator)} "
                 f"{format_number(last_number)} ="
        )

        set_display(format_number(result))

        new_number = True


# =========================================================
# ROUNDED BUTTON CLASS
# =========================================================

class RoundedButton(tk.Canvas):

    def __init__(
        self,
        parent,
        text,
        command,
        width=62,
        height=58,
        bg_color=NUMBER_BG,
        hover_color=NUMBER_HOVER,
        text_color=TEXT_WHITE,
        font=("Segoe UI", 16, "bold"),
        radius=18
    ):

        super().__init__(
            parent,
            width=width,
            height=height,
            bg=BACKGROUND,
            highlightthickness=0,
            bd=0
        )

        self.text = text
        self.command = command

        self.width = width
        self.height = height

        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color

        self.font = font
        self.radius = radius

        self.current_color = bg_color

        self.draw_button()

        self.bind(
            "<Enter>",
            self.on_enter
        )

        self.bind(
            "<Leave>",
            self.on_leave
        )

        self.bind(
            "<Button-1>",
            self.on_click
        )


    def rounded_rectangle(
        self,
        x1,
        y1,
        x2,
        y2,
        radius,
        **kwargs
    ):

        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,

            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,

            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,

            x1, y1 + radius,
            x1, y1
        ]

        return self.create_polygon(
            points,
            smooth=True,
            **kwargs
        )


    def draw_button(self):

        self.delete("all")

        self.rounded_rectangle(
            2,
            2,
            self.width - 2,
            self.height - 2,
            self.radius,
            fill=self.current_color,
            outline=""
        )

        self.create_text(
            self.width / 2,
            self.height / 2,
            text=self.text,
            fill=self.text_color,
            font=self.font
        )


    def on_enter(self, event):

        self.current_color = self.hover_color

        self.draw_button()


    def on_leave(self, event):

        self.current_color = self.bg_color

        self.draw_button()


    def on_click(self, event):

        self.command()


# =========================================================
# BUTTON AREA
# =========================================================

button_frame = tk.Frame(
    root,
    bg=BACKGROUND
)

button_frame.pack(
    padx=20,
    pady=(0, 10)
)


# =========================================================
# BUTTON SETTINGS
# =========================================================

BUTTON_WIDTH = 62
BUTTON_HEIGHT = 52

BUTTON_PAD_X = 3
BUTTON_PAD_Y = 4


# =========================================================
# ROW 1
# =========================================================

RoundedButton(
    button_frame,
    "AC",
    clear_click,
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
    NUMBER_BG,
    NUMBER_HOVER,
    TEXT_SECONDARY,
    ("Segoe UI", 14, "bold")
).grid(
    row=0,
    column=0,
    padx=BUTTON_PAD_X,
    pady=BUTTON_PAD_Y
)


RoundedButton(
    button_frame,
    "⌫",
    delete_click,
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
    NUMBER_BG,
    NUMBER_HOVER,
    TEXT_SECONDARY,
    ("Segoe UI", 15, "bold")
).grid(
    row=0,
    column=1,
    padx=BUTTON_PAD_X,
    pady=BUTTON_PAD_Y
)


RoundedButton(
    button_frame,
    "%",
    percent_click,
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
    NUMBER_BG,
    NUMBER_HOVER,
    TEXT_SECONDARY,
    ("Segoe UI", 15, "bold")
).grid(
    row=0,
    column=2,
    padx=BUTTON_PAD_X,
    pady=BUTTON_PAD_Y
)


RoundedButton(
    button_frame,
    "÷",
    lambda: operator_click("/"),
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
    OPERATOR_BG,
    OPERATOR_HOVER,
    TEXT_WHITE,
    ("Segoe UI", 17, "bold")
).grid(
    row=0,
    column=3,
    padx=BUTTON_PAD_X,
    pady=BUTTON_PAD_Y
)


# =========================================================
# ROW 2
# =========================================================

for column, number in enumerate(["7", "8", "9"]):

    RoundedButton(
        button_frame,
        number,
        lambda n=number: number_click(n),
        BUTTON_WIDTH,
        BUTTON_HEIGHT
    ).grid(
        row=1,
        column=column,
        padx=BUTTON_PAD_X,
        pady=BUTTON_PAD_Y
    )


RoundedButton(
    button_frame,
    "×",
    lambda: operator_click("*"),
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
    OPERATOR_BG,
    OPERATOR_HOVER,
    TEXT_WHITE,
    ("Segoe UI", 17, "bold")
).grid(
    row=1,
    column=3,
    padx=BUTTON_PAD_X,
    pady=BUTTON_PAD_Y
)


# =========================================================
# ROW 3
# =========================================================

for column, number in enumerate(["4", "5", "6"]):

    RoundedButton(
        button_frame,
        number,
        lambda n=number: number_click(n),
        BUTTON_WIDTH,
        BUTTON_HEIGHT
    ).grid(
        row=2,
        column=column,
        padx=BUTTON_PAD_X,
        pady=BUTTON_PAD_Y
    )


RoundedButton(
    button_frame,
    "−",
    lambda: operator_click("-"),
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
    OPERATOR_BG,
    OPERATOR_HOVER,
    TEXT_WHITE,
    ("Segoe UI", 17, "bold")
).grid(
    row=2,
    column=3,
    padx=BUTTON_PAD_X,
    pady=BUTTON_PAD_Y
)


# =========================================================
# ROW 4
# =========================================================

for column, number in enumerate(["1", "2", "3"]):

    RoundedButton(
        button_frame,
        number,
        lambda n=number: number_click(n),
        BUTTON_WIDTH,
        BUTTON_HEIGHT
    ).grid(
        row=3,
        column=column,
        padx=BUTTON_PAD_X,
        pady=BUTTON_PAD_Y
    )


RoundedButton(
    button_frame,
    "+",
    lambda: operator_click("+"),
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
    OPERATOR_BG,
    OPERATOR_HOVER,
    TEXT_WHITE,
    ("Segoe UI", 17, "bold")
).grid(
    row=3,
    column=3,
    padx=BUTTON_PAD_X,
    pady=BUTTON_PAD_Y
)

# =========================================================
# LAST ROW
# =========================================================

# Wide ZERO button
RoundedButton(
    button_frame,
    "0",
    lambda: number_click("0"),
    width=130,
    height=52
).grid(
    row=4,
    column=0,
    columnspan=2,
    padx=BUTTON_PAD_X,
    pady=BUTTON_PAD_Y
)


# Decimal button
RoundedButton(
    button_frame,
    ".",
    decimal_click,
    width=62,
    height=52
).grid(
    row=4,
    column=2,
    padx=BUTTON_PAD_X,
    pady=BUTTON_PAD_Y
)


# Equals button
RoundedButton(
    button_frame,
    "=",
    equals_click,
    width=62,
    height=52,
    bg_color=OPERATOR_BG,
    hover_color=OPERATOR_HOVER,
    text_color=TEXT_WHITE,
    font=("Segoe UI", 17, "bold")
).grid(
    row=4,
    column=3,
    padx=BUTTON_PAD_X,
    pady=BUTTON_PAD_Y
)


# =========================================================
# KEYBOARD SUPPORT
# =========================================================

def keyboard_input(event):

    key = event.keysym
    char = event.char

    # -----------------------------------------------------
    # NUMBERS
    # -----------------------------------------------------

    if char in "0123456789":

        number_click(char)

        return "break"


    # -----------------------------------------------------
    # DECIMAL
    # -----------------------------------------------------

    if char == ".":

        decimal_click()

        return "break"


    # -----------------------------------------------------
    # OPERATORS
    # -----------------------------------------------------

    if char == "+":

        operator_click("+")

        return "break"


    if char == "-":

        operator_click("-")

        return "break"


    if char == "*":

        operator_click("*")

        return "break"


    if char == "/":

        operator_click("/")

        return "break"


    # -----------------------------------------------------
    # PERCENT
    # -----------------------------------------------------

    if char == "%":

        percent_click()

        return "break"


    # -----------------------------------------------------
    # ENTER / EQUALS
    # -----------------------------------------------------

    if key in ("Return", "KP_Enter", "equal"):

        equals_click()

        return "break"


    # -----------------------------------------------------
    # BACKSPACE
    # -----------------------------------------------------

    if key == "BackSpace":

        delete_click()

        return "break"


    # -----------------------------------------------------
    # ESCAPE / CLEAR
    # -----------------------------------------------------

    if key == "Escape":

        clear_click()

        return "break"


    # -----------------------------------------------------
    # NUMERIC KEYPAD
    # -----------------------------------------------------

    if key.startswith("KP_"):

        keypad_key = key[3:]

        if keypad_key in "0123456789":

            number_click(keypad_key)

            return "break"

        if keypad_key == "Decimal":

            decimal_click()

            return "break"

        if keypad_key == "Add":

            operator_click("+")

            return "break"

        if keypad_key == "Subtract":

            operator_click("-")

            return "break"

        if keypad_key == "Multiply":

            operator_click("*")

            return "break"

        if keypad_key == "Divide":

            operator_click("/")

            return "break"


# Apply keyboard handler to the whole application
root.bind_all(
    "<KeyPress>",
    keyboard_input
)


# Give the application keyboard focus
root.focus_set()


# =========================================================
# START APPLICATION
# =========================================================

root.mainloop()