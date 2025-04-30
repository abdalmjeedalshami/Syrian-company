from tkinter import *
from tkinter import ttk, messagebox, font, filedialog
from openpyxl import load_workbook, Workbook
from openpyxl.styles import Font
import customtkinter as ctk
import os
import shutil
import pandas as pd
from utils.methods import *


EXCEL_FILE = 'data.xlsx'  # Ensure this file exists
PROFILE_FOLDER = 'images/profile'
cities = ["دمشق", "حلب", "اللاذقية", "حمص", "طرطوس"]


# Update scroll region when adding new widgets
def update_scroll_region(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

# Recalculate centering after resize
def resize_centering(event):
    canvas.coords(content_window, (canvas.winfo_width() // 2, 0))

def get_full_date(day, month, year):
    return f"{day}-{month}-{year}"

def set_profile_path(path):
    global profile_path
    profile_path = path



# Create GUI
root = Tk()
root.iconbitmap("app_icon.ico")
root.title("استبيان إضافة مستفيد")
root.geometry("500x500")

# Maximize window (Windows-specific)
root.wm_state('zoomed')  

# Custom fonts
normal_font = font.Font(family="Segoe UI")
bold_font = font.Font(family="Segoe UI", weight="bold")

# Create a frame for the scrollbar and canvas
scroll_frame = ttk.Frame(root)
scroll_frame.pack(fill="both", expand=True)

# Create canvas to hold the scrollable content
canvas = Canvas(scroll_frame)
canvas.pack(side="left", fill="both", expand=True)

# Add scrollbar
scrollbar = ttk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

# Create a frame inside the canvas to hold the actual content
content_frame = ttk.Frame(canvas)

# Add window to canvas, using `winfo_width()` for dynamic centering
canvas.create_window((canvas.winfo_width() // 2, 0), window=content_frame, anchor="n")

# Configure scrollbar
canvas.configure(yscrollcommand=scrollbar.set)

# Create main frame
# frm = ttk.Frame(root, padding=20)
# frm.pack(fill="both", expand=True, padx=20, pady=20)

# Title
ttk.Label(content_frame, text="استمارة (معتقل - مختفي - ناجي - شاهد)", font=bold_font).pack(pady=10)

first_name_entry = create_labeled_entry(content_frame, "الاسم الأول")
father_name_entry = create_labeled_entry(content_frame, "الاسم الأب")
last_name_entry = create_labeled_entry(content_frame, "الكنية")
mother_name_entry = create_labeled_entry(content_frame, "اسم الأم")

# Gender selection
gender_frame = ttk.Frame(content_frame)
gender_frame.pack(pady=10)
selected_gender = StringVar()
ttk.Label(gender_frame, text="الجنس").pack(side="right", padx=5)
ttk.Radiobutton(gender_frame, text="ذكر", variable=selected_gender, value="ذكر").pack(side="right", padx=5)
ttk.Radiobutton(gender_frame, text="أنثى", variable=selected_gender, value="أنثى").pack(side="right", padx=5)

# Birth date
date_frame = ttk.Frame(content_frame)
date_frame.pack(pady=10)
ttk.Label(date_frame, text="تاريخ الولادة").pack(side="right", padx=5)
ttk.Label(date_frame, text="اليوم").pack(side="right")
selected_day = ttk.Spinbox(date_frame, from_=1, to=31, width=5)
selected_day.pack(side="right", padx=5)
ttk.Label(date_frame, text="الشهر").pack(side="right")
selected_month = ttk.Spinbox(date_frame, from_=1, to=12, width=5)
selected_month.pack(side="right", padx=5)
ttk.Label(date_frame, text="السنة").pack(side="right")
selected_year = ttk.Spinbox(date_frame, width=5)
selected_year.pack(side="right", padx=5)

city_entry = create_labeled_combobox(content_frame, "محل الولادة", ["دمشق", "حلب", "اللاذقية"])
residential_registration_entry = create_labeled_entry(content_frame, "قيد النفوس")
national_number_entry = create_labeled_entry(content_frame, "الرقم الوطني")
full_address_entry = create_labeled_entry(content_frame, "العنوان المفصّل")

# Profile picture button
profile_path = None
create_labeled_button(content_frame, "الصورة الشخصية", "اختر الصورة الشخصية", lambda: file_picker(set_profile_path, title="اختر صورة شخصية", first_name=first_name_entry.get()))

education_entry = create_labeled_combobox(content_frame, "المستوى العلمي", ["أمّي", "ابتدائي", "إعدادي", "ثانوي", "معهد", "جامعة", "ماجستر", "دكتور"])
academic_specialization_entry = create_labeled_entry(content_frame, "الاختصاص")
job_entry = create_labeled_entry(content_frame, "المهنة التي يتقنها")
current_job_entry = create_labeled_entry(content_frame, "المهنة الحالية")

# Height & weight
selected_height = create_labeled_spinbox(content_frame, "الطول (سم)", 0, 300)
selected_weight = create_labeled_spinbox(content_frame, "الوزن (كغ)", 0, 300)

eye_color_entry = create_labeled_combobox(content_frame, "لون العينين", ["أسود", "بني", "أزرق", "أخضر", "عسلي"])
hair_color_entry = create_labeled_combobox(content_frame, "لون الشعر", ["أسود", "بني", "أشقر", "أحمر"])
skin_color_entry = create_labeled_combobox(content_frame, "لون البشرة", ["أبيض", "حنطي", "أسمر", "أسود"])
unique_features_entry = create_labeled_entry(content_frame, "علامات فارقة")

# Social status (correct label)
social_status_entry = create_labeled_combobox(content_frame, "الوضع الاجتماعي", ["أعزب", "متزوج", "مطلق", "أرمل"])

# Children
children_number_entry = create_labeled_entry(content_frame, "عدد الأطفال")

# Frame to hold generated child entry fields
children_frame = ttk.Frame(content_frame)
children_frame.pack(pady=10)

# Button to generate child entries
ttk.Button(children_frame, text="إنشاء حقول الأولاد", command=lambda: generate_entries(children_frame=children_frame, children_number_entry=children_number_entry, children_entries=children_entries)).pack(side="right", pady=5)

# List to store child entry widgets
children_entries = []

from models.form_data import FormData

def on_submit():
    form_data = FormData(
        first_name=first_name_entry.get(),
        father_name=father_name_entry.get(),
        last_name=last_name_entry.get(),
        mother_name=mother_name_entry.get(),
        gender=selected_gender.get(),
        date=f"{selected_day.get()}/{selected_month.get()}/{selected_year.get()}",
        city=city_entry.get(),
        residential_registration=residential_registration_entry.get(),
        national_number=national_number_entry.get(),
        full_address=full_address_entry.get(),
        profile_path=profile_path,  # Make sure this is updated via file_picker
        education=education_entry.get(),
        academic_specialization=academic_specialization_entry.get(),
        job=job_entry.get(),
        current_job=current_job_entry.get(),
        height=selected_height.get(),
        weight=selected_weight.get(),
        eye_color=eye_color_entry.get(),
        hair_color=hair_color_entry.get(),
        skin_color=skin_color_entry.get(),
        unique_features=unique_features_entry.get(),
        social_status=social_status_entry.get(),  # You must have this field
        children_number=children_number_entry.get()
    )
    submit_data(form_data, [(entry.get(), gender.get()) for entry, gender in children_entries])



# Buttons
add_btn_frame = ttk.Frame(content_frame)
add_btn_frame.pack(pady=10)
ttk.Button(
    add_btn_frame,
    text="إضافة", 
    command=on_submit
).pack(pady=10)
# submit_button = ctk.CTkButton(frm, text="إضافة", command=submit_data).grid(row=5, column=0)

content_window = canvas.create_window((canvas.winfo_width() // 2, 0), window=content_frame, anchor="n")
canvas.bind("<Configure>", resize_centering)  # Recenter on window resize
content_frame.bind("<Configure>", update_scroll_region)
root.mainloop()