from tkinter import *
from tkinter import messagebox
import os
import sys

# ---------------- WINDOW ----------------
root = Tk()
try:
    root.iconbitmap(r"C:\Users\vivek\applications\logi.ico")
except Exception as e:
    print("Icon error:", e)
root.title("PayPlan")
root.geometry("500x670")
root.iconbitmap(r"C:\Users\vivek\applications\logi.ico")
root.config(bg="#1e1e2f")
root.resizable(True,True)


# -------- ICON FIX --------
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

try:
    icon = PhotoImage(file=resource_path("logi.ico"))
    root.iconphoto(True, icon)
except Exception as e:
    print("Icon loading failed:", e)

# ---------------- PLACEHOLDER FUNCTION ----------------
def add_placeholder(entry, text):

    entry.insert(0, text)
    entry.config(fg="grey")

    def on_focus_in(event):

        if entry.get() == text:
            entry.delete(0, END)
            entry.config(fg="black")

    def on_focus_out(event):

        if entry.get() == "":
            entry.insert(0, text)
            entry.config(fg="grey")

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)


# ---------------- EMI FUNCTION ----------------
def emiCalc():

    try:
        amt = float(entry_amt.get())
        ir = float(entry_ir.get())
        lp = float(entry_lp.get())

        if amt <= 0 or ir <= 0 or lp <= 0:
            messagebox.showerror(
                "Error",
                "All values must be greater than 0"
            )
            return

        months = int(lp * 12)

        # ---------------- FLAT RATE ----------------
        if emi_type.get() == "Flat":

            interest = amt * (ir / 100)
            toti = interest * lp
            tamt = amt + toti
            emi = tamt / months

            result.config(
                text=f"EMI Type : Flat Rate\n\n"
                     f"Monthly EMI : ₹ {emi:,.2f}\n\n"
                     f"Total Interest : ₹ {toti:,.2f}\n\n"
                     f"Total Amount : ₹ {tamt:,.2f}"
            )

        # ---------------- REDUCING BALANCE ----------------
        else:

            monthly_rate = (ir / 12) / 100

            emi = (
                amt * monthly_rate *
                (1 + monthly_rate) ** months
            ) / (
                (1 + monthly_rate) ** months - 1
            )

            tamt = emi * months
            toti = tamt - amt

            result.config(
                text=f"EMI Type : Reducing Balance\n\n"
                     f"Monthly EMI : ₹ {emi:,.2f}\n\n"
                     f"Total Interest : ₹ {toti:,.2f}\n\n"
                     f"Total Amount : ₹ {tamt:,.2f}"
            )

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Please enter valid numbers only"
        )

# ---------------- CLEAR FUNCTION ----------------
def clearFields():

    entry_amt.delete(0, END)
    entry_ir.delete(0, END)
    entry_lp.delete(0, END)

    # Restore placeholders
    add_placeholder(entry_amt, " Loan Amount")
    add_placeholder(entry_ir, " Interest Rate")
    add_placeholder(entry_lp, "Loan Period")
    result.config(text="Your EMI will appear here")
    # ---------------- EMI TYPE ----------------

# ---------------- HEADING ----------------
heading = Label(
    root,
    text="paYPlan",
    font=("Arial", 24, "bold"),
    bg="#1e1e2f",
    fg="green"
)

heading.pack(pady=20)

# ---------------- FRAME ----------------
frame = Frame(
    root,
    bg="#2b2b40",
    bd=5,
    relief=RIDGE
)

frame.pack(
    pady=2,
    padx=2,
    fill="both",
    expand=True
)

# ---------------- LOAN AMOUNT ----------------
Label(
    frame,
    text="Loan Amount (₹)",
    font=("Arial", 14),
    bg="#2b2b40",
    fg="white"
).pack(pady=10)

entry_amt = Entry(
    frame,
    font=("Arial", 16),
    justify="center"
)

entry_amt.pack(
    ipady=8,
    padx=5,
)

# PLACEHOLDER
add_placeholder(entry_amt, " Loan Amount")

# ---------------- INTEREST RATE ----------------
Label(
    frame,
    text="Interest Rate (%)",
    font=("Arial", 14),
    bg="#2b2b40",
    fg="white"
).pack(pady=10)

entry_ir = Entry(
    frame,
    font=("Arial", 16),
    justify="center"
)

entry_ir.pack(
    ipady=8,
    padx=5,
)

# PLACEHOLDER
add_placeholder(entry_ir, " Interest Rate")

# ---------------- LOAN PERIOD ----------------
Label(
    frame,
    text="Loan Period (Years)",
    font=("Arial", 14),
    bg="#2b2b40",
    fg="white"
).pack(pady=10)

entry_lp = Entry(
    frame,
    font=("Arial", 16),
    justify="center"
)

entry_lp.pack(
    ipady=5,
    padx=8,
)

# PLACEHOLDER
add_placeholder(entry_lp, " Loan Period")

emi_type = StringVar()
emi_type.set("Flat")

Label(
    frame,
    text="EMI Calculation Type",
    font=("Arial", 14),
    bg="#2b2b40",
    fg="white"
).pack(pady=3)

from tkinter.ttk import Combobox

emi_type = StringVar()

emi_combo = Combobox(
    frame,
    textvariable=emi_type,
    values=["Flat", "Diminishing"],
    state="readonly"
)

emi_combo.current(0)
emi_combo.pack(pady=2)

# ---------------- BUTTON FRAME ----------------
button_frame = Frame(
    frame,
    bg="#2b2b40"
)

button_frame.pack(pady=5)

# ---------------- MODERN ROUND BUTTON FUNCTION ----------------
def round_button(
        canvas,
        x,
        y,
        width,
        height,
        radius,
        color,
        hover_color,
        text,
        command
):

    left = canvas.create_oval(
        x,
        y,
        x + radius * 2,
        y + height,
        fill=color,
        outline=color
    )

    right = canvas.create_oval(
        x + width - radius * 2,
        y,
        x + width,
        y + height,
        fill=color,
        outline=color
    )

    center = canvas.create_rectangle(
        x + radius,
        y,
        x + width - radius,
        y + height,
        fill=color,
        outline=color
    )

    txt = canvas.create_text(
        x + width / 2,
        y + height / 2,
        text=text,
        fill="white",
        font=("Segoe UI", 12, "bold")
    )

    def on_enter(event):

        canvas.itemconfig(left, fill=hover_color, outline=hover_color)
        canvas.itemconfig(right, fill=hover_color, outline=hover_color)
        canvas.itemconfig(center, fill=hover_color, outline=hover_color)

    def on_leave(event):

        canvas.itemconfig(left, fill=color, outline=color)
        canvas.itemconfig(right, fill=color, outline=color)
        canvas.itemconfig(center, fill=color, outline=color)

    canvas.bind("<Button-1>", lambda event: command())

    canvas.bind("<Enter>", on_enter)
    canvas.bind("<Leave>", on_leave)


# ---------------- GENERATE BUTTON CANVAS ----------------
btn_canvas = Canvas(
    button_frame,
    width=159,
    height=60,
    bg="#2b2b40",
    highlightthickness=0
)

btn_canvas.pack(side=LEFT, padx=3)

# ---------------- GENERATE BUTTON ----------------
round_button(
    btn_canvas,
    x=5,
    y=10,
    width=155,
    height=40,
    radius=18,
    color="#00c896",
    hover_color="#00a67e",
    text="✨CHECK EMI ",
    command=emiCalc
)

# ---------------- CLEAR BUTTON CANVAS ----------------
clear_canvas = Canvas(
    button_frame,
    width=150,
    height=60,
    bg="#2b2b40",
    highlightthickness=0
)

clear_canvas.pack(side=LEFT, padx=3)

# ---------------- CLEAR BUTTON ----------------
round_button(
    clear_canvas,
    x=5,
    y=10,
    width=135,
    height=40,
    radius=18,
    color="#ff7675",
    hover_color="#e74c3c",
    text="✖ CLEAR",
    command=clearFields
)

# ---------------- RESULT ----------------
result = Label(
    frame,
    text="Your EMI will appear here",
    font=("Arial", 15, "bold"),
    bg="#2b2b40",
    fg="#00ffcc",
    justify="center"
)

result.pack(pady=1)

# ---------------- FOOTER ----------------
footer = Label(
    root,
    text="Made with Python Tkinter",
    font=("Arial", 10),
    bg="#1e1e2f",
    fg="#aaaaaa"
)

footer.pack(
    side=BOTTOM,
    pady=1
)

# ---------------- MAIN LOOP ----------------
root.mainloop()