import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("500x500")

# Frame to hold dynamic children widgets (label, entry, gender, and age)
children_frame = ttk.Frame(root)
children_frame.pack(pady=10)

# List to store dynamic children (each child has label, entry, gender_frame, and age_spinbox)
children_widgets = []

# Spinbox to select number of children
child_count_var = tk.StringVar(value="0")
child_count_spinbox = ttk.Spinbox(
    root, from_=0, to=10, textvariable=child_count_var, width=5, command=lambda: update_children()
)
child_count_spinbox.pack(pady=10)

def update_children():
    count = int(child_count_var.get())

    # Remove extra children widgets if count decreased
    while len(children_widgets) > count:
        label, entry, gender_frame, age_spinbox = children_widgets.pop()
        label.destroy()
        entry.destroy()
        gender_frame.destroy()
        age_spinbox.destroy()

    # Add missing children widgets if count increased
    while len(children_widgets) < count:
        index = len(children_widgets) + 1  # Child index starts at 1
        
        # Create label
        label = ttk.Label(children_frame, text=f"Child {index}")
        label.pack(pady=5)
        
        # Create entry for child name
        entry = ttk.Entry(children_frame)
        entry.pack(pady=5)
        
        # Create gender radio buttons
        gender_frame, gender_variable = create_radio_group(children_frame, "Gender", ["ذكر", "انثى"])
        gender_frame.pack(pady=5)

        # Create age spinbox for each child (from 0 to 18)
        age_spinbox = ttk.Spinbox(children_frame, from_=0, to=18, width=5)
        age_spinbox.pack(pady=5)

        # Store them together in children_widgets
        children_widgets.append((label, entry, gender_frame, age_spinbox))

def create_radio_group(parent, label_text, options, variable=None):
    frame = ttk.Frame(parent)
    frame.pack(pady=10)

    if variable is None:
        variable = tk.StringVar()

    ttk.Label(frame, text=label_text).pack(side="right", padx=5)

    for option in options:
        ttk.Radiobutton(frame, text=option, variable=variable, value=option).pack(
            side="right", padx=5
        )

    return frame, variable  # Return both the frame and the variable

# Function to print the current form data
def print_form_data():
    for index, (label, entry, gender_frame, age_spinbox) in enumerate(children_widgets):
        entry_value = entry.get()  # Get the value of the Entry widget (name)
        gender_value = gender_frame.winfo_children()[1].get()  # Get the selected gender value
        age_value = age_spinbox.get()  # Get the selected age value
        print(f"Child {index + 1}: Name: {entry_value}, Gender: {gender_value}, Age: {age_value}")

# Print Button
print_button = ttk.Button(root, text="Print Form Data", command=print_form_data)
print_button.pack(pady=20)

root.mainloop()
