from tkinter import *
from tkinter import ttk, messagebox, font, filedialog
from openpyxl import load_workbook, Workbook
from openpyxl.styles import Font
import customtkinter as ctk
import os
import shutil


EXCEL_FILE = 'data.xlsx'  # Ensure this file exists
PROFILE_FOLDER = 'images/profile'
cities = ["دمشق", "حلب", "اللاذقية", "حمص", "طرطوس"]

def set_profile_path(path):
    global profile_path
    profile_path = path

def file_picker(on_file_picked, title='اختر ملف'):
    first_name = first_name_entry.get()

    if not first_name:
        messagebox.showwarning("معلومات ناقصة", "يرجى إدخال الاسم أولاً قبل اختيار الصورة")
        return

    # Choose image
    filepath = filedialog.askopenfilename(
         title=title,
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")]
    )

    if filepath:
         on_file_picked(filepath)

def submit_data(first_name, last_name, national_number, city, profile_path, gender):
    print(profile_path)

    if not profile_path:
         messagebox.showwarning('profile error')
         print(f'EEE This is the profile path: {profile_path}')
         return

    if not first_name or not last_name or not national_number or not city or not profile_path or not gender:
        messagebox.showwarning("معلومات مفقودة", "الرجاء تعبئة كل الحقول")
        return
    
    print(f'This is the profile path: {profile_path}')

    try:
        wb = load_workbook(EXCEL_FILE)
    except FileNotFoundError:
        wb = Workbook()
        ws = wb.active
        ws.append(["الاسم الأول", "الاسم الأخير", "الرقم الوطني", "المدينة", "الصورة الشخصية", "الجنس", "تاريخ الولادة"])  # Add headers
    else:
        ws = wb.active

    ws.append([first_name, last_name, national_number, city, "", gender])
    row = ws.max_row

    # Helper to add hyperlink to a cell
    def set_hyperlink(col, label, path):
            cell = ws.cell(row=row, column=col)
            cell.value = label
            cell.hyperlink = path.replace("\\", "/")
            cell.font = Font(color="0000FF", underline="single")

    # Create folder based on first name
    user_folder = os.path.join(PROFILE_FOLDER, first_name)
    os.makedirs(user_folder, exist_ok=True)

    # Copy image to user folder
    filename = os.path.basename(profile_path)
    saved_path = os.path.join(user_folder, filename)
    shutil.copy(profile_path, saved_path)

    # Set hyperlinks
    set_hyperlink(5, "عرض الصورة", saved_path)

    wb.save(EXCEL_FILE)

    first_name_entry.delete(0, END)
    last_name_entry.delete(0, END)
    national_number_entry.delete(0, END)
    # city_entry.delete(0, END)
    city_entry.set("")
    selected_gender.set("")

    messagebox.showinfo("تمت العملية بنجاح", "تم إضافة بيانات المستفيد")

# Create GUI
root = Tk()
root.iconbitmap("app_icon.ico")
root.title("استبيان إضافة مستفيد")

# Maximize window (Windows-specific)
root.wm_state('zoomed')  

# Custom fonts
normal_font = font.Font(family="Segoe UI")
bold_font = font.Font(family="Segoe UI", weight="bold")

# Create main frame
frm = ttk.Frame(root, padding=20)
frm.pack(fill="both", expand=True, padx=20, pady=20)

# Title Label
ttk.Label(frm, text="استمارة (معتقل - مختفي - ناجي - شاهد)", font=bold_font).pack(pady=10)

# Entry fields and labels (side-by-side)


first_name_frame = ttk.Frame(frm)
first_name_frame.pack(pady=10)

ttk.Label(first_name_frame, text="الاسم الأول").pack(side="right", padx=5)
first_name_entry = ttk.Entry(first_name_frame)
first_name_entry.pack(side="right", padx=10)

last_name_frame = ttk.Frame(frm)
last_name_frame.pack(pady=10)

ttk.Label(last_name_frame, text="الاسم الأخير").pack(side="right", padx=5)
first_name_entry = ttk.Entry(last_name_frame)
first_name_entry.pack(side="right", padx=10)

entry_frame = ttk.Frame(frm)
entry_frame.pack(pady=10)

ttk.Label(entry_frame, text="الاسم الأخير").pack(side="left", padx=5)
last_name_entry = ttk.Entry(entry_frame)
last_name_entry.pack(side="left", padx=10)

ttk.Label(entry_frame, text="الرقم الوطني").pack(side="left", padx=5)
national_number_entry = ttk.Entry(entry_frame)
national_number_entry.pack(side="left", padx=10)

ttk.Label(entry_frame, text="المدينة").pack(side="left", padx=5)
city_entry = ttk.Combobox(entry_frame, values=["دمشق", "حلب", "اللاذقية"], state="readonly")
city_entry.pack(side="left", padx=10)

# Profile Picture Selection
profile_path = None
ttk.Button(frm, text="اختر الصورة الشخصية", command=lambda: file_picker(set_profile_path, title="اختر صورة شخصية")).pack(pady=5)

# Gender Selection
gender_frame = ttk.Frame(frm)
gender_frame.pack(pady=5)
selected_gender = StringVar()
ttk.Label(gender_frame, text="الجنس").pack(side="left", padx=5)
ttk.Radiobutton(gender_frame, text="ذكر", variable=selected_gender, value="ذكر").pack(side="left", padx=5)
ttk.Radiobutton(gender_frame, text="أنثى", variable=selected_gender, value="أنثى").pack(side="left", padx=5)

# Date of Birth Selection (Spinboxes)
dob_frame = ttk.Frame(frm)
dob_frame.pack(pady=5)
ttk.Label(dob_frame, text="تاريخ الولادة").pack(side="left", padx=5)
selected_day = ttk.Spinbox(dob_frame, from_=1, to=31, width=5)
selected_day.pack(side="left", padx=5)

selected_month = ttk.Spinbox(dob_frame, from_=1, to=12, width=5)
selected_month.pack(side="left", padx=5)

selected_year = ttk.Spinbox(dob_frame, from_=1950, to=2035, width=5)
selected_year.pack(side="left", padx=5)

# Submit Button
ttk.Button(
    frm,
    text="إضافة", 
    command=lambda: submit_data(
        first_name=first_name_entry.get(),
        last_name=last_name_entry.get(),
        national_number=national_number_entry.get(),
        city=city_entry.get(),
        profile_path=profile_path,
        gender=selected_gender.get()
    )
).pack(pady=10)

root.mainloop()
