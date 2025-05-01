from tkinter import *
from tkinter import ttk, font
from utils.methods import *
from models.form_data import FormData


EXCEL_FILE = "data.xlsx"  # Ensure this file exists
PROFILE_FOLDER = "images/profile"

def get_full_date(day, month, year):
    return f"{day}/{month}/{year}"


def set_profile_path(path):
    global profile_path
    profile_path = path

# Create GUI
root = Tk()
root.iconbitmap("app_icon.ico")
root.title("استبيان إضافة مستفيد")
root.geometry("500x500")

# Maximize window (Windows-specific)
root.wm_state("zoomed")

# Custom fonts
normal_font = font.Font(family="Segoe UI")
bold_font = font.Font(family="Segoe UI", weight="bold")

# Create a frame for the scrollbar and canvas
main_frame = ttk.Frame(root)
main_frame.pack(fill="both", expand=True)

# Create canvas to hold the scrollable content
canvas = Canvas(main_frame)
canvas.pack(side="left", fill="both", expand=True)

# Add scrollbar
scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

# Configure scrollbar
canvas.configure(yscrollcommand=scrollbar.set)

# Create a frame inside the canvas to hold the actual content
content_frame = ttk.Frame(canvas)

# Add window to canvas, using `winfo_width()` for dynamic centering
canvas.create_window((canvas.winfo_width() // 2, 0), window=content_frame, anchor="n")

# Title
ttk.Label(
    content_frame, text="استمارة (معتقل - مختفي - ناجي - شاهد)", font=bold_font
).pack(pady=10)

first_name_entry = create_labeled_entry(content_frame, "الاسم الأول")
father_name_entry = create_labeled_entry(content_frame, "الاسم الأب")
last_name_entry = create_labeled_entry(content_frame, "الكنية")
mother_name_entry = create_labeled_entry(content_frame, "اسم الأم")

selected_gender = create_radio_group(content_frame, "الجنس", ["ذكر", "أنثى"])

selected_day, selected_month, selected_year = create_date_picker(content_frame, "تاريخ الولادة")

city, city_var, city_entry_var = create_combobox_with_optional_entry(
    content_frame,
    label_text="محل الولادة",
    options=["دمشق", "حلب", "اللاذقية", "(غير ذلك)"],
)

residential_registration_entry = create_labeled_entry(content_frame, "قيد النفوس")
national_number_entry = create_labeled_entry(content_frame, "الرقم الوطني")
full_address_entry = create_labeled_entry(content_frame, "العنوان المفصّل")

# Profile picture button
profile_path = None
create_labeled_button(
    content_frame,
    "الصورة الشخصية",
    "اختر الصورة الشخصية",
    lambda: file_picker(
        set_profile_path, title="اختر صورة شخصية", first_name=first_name_entry.get()
    ),
)

education, education_var, education_entry_var = create_combobox_with_optional_entry(
    content_frame,
    label_text="المستوى العلمي",
    options=["أمّي", "ابتدائي", "إعدادي", "ثانوي", "معهد", "جامعة", "ماجستر", "دكتور"],
)

academic_specialization_entry = create_labeled_entry(content_frame, "الاختصاص")
job_entry = create_labeled_entry(content_frame, "المهنة التي يتقنها")
current_job_entry = create_labeled_entry(content_frame, "المهنة الحالية")

# Height & weight
selected_height = create_labeled_spinbox(content_frame, "الطول (سم)", 0, 300)
selected_weight = create_labeled_spinbox(content_frame, "الوزن (كغ)", 0, 300)

eye_color, eye_color_var, eye_color_entry_var = create_combobox_with_optional_entry(
    content_frame,
    label_text="لون العينين",
    options=["أسود", "بني", "أزرق", "أخضر", "عسلي", "(غير ذلك)"],
)

hair_color, hair_color_var, hair_color_entry_var = create_combobox_with_optional_entry(
    content_frame,
    label_text="لون الشعر",
    options=["أسود", "بني", "أشقر", "أحمر", "(غير ذلك)"],
)

skin_color, skin_color_var, skin_color_entry_var = create_combobox_with_optional_entry(
    content_frame,
    label_text="لون البشرة",
    options=["أبيض", "حنطي", "أسمر", "أسود", "(غير ذلك)"],
)

unique_features_entry = create_labeled_entry(content_frame, "علامات فارقة")

social_status_entry = create_labeled_combobox(
    content_frame, "الوضع الاجتماعي", ["أعزب", "متزوج", "مطلق", "أرمل"]
)

# Children
children_number_entry = create_labeled_entry(content_frame, "عدد الأطفال")

# Frame to hold generated child entry fields
children_frame = ttk.Frame(content_frame)
children_frame.pack(pady=10)


# Button to generate child entries
ttk.Button(
    children_frame,
    text="إنشاء حقول الأولاد",
    command=lambda: generate_entries(
        children_frame=children_frame,
        children_number_entry=children_number_entry,
        children_entries=children_entries,
    ),
).pack(side="right", pady=5)

# List to store child entry widgets
children_entries = []

phone_number_entry = create_labeled_entry(content_frame, "رقم الهاتف")

social_media_entry = create_labeled_entry(content_frame, "التواصل الاجتماعي")

get_nationality, nationality_var, nationality_entry_var = create_combobox_with_optional_entry(
    content_frame,
    label_text="الجنسية",
    options=["سوري", "لبناني", "عراقي", "أردني", "(غير ذلك)"],
)

def on_submit():
    date_entry = (
    ""
    if selected_day.get() == "" or selected_month.get() == "" or selected_year.get() == ""
    else get_full_date(selected_day.get(), selected_month.get(), selected_year.get())
)

    """Handles form submission and clears input fields."""
    form_data = FormData(
        first_name=first_name_entry.get(),
        father_name=father_name_entry.get(),
        last_name=last_name_entry.get(),
        mother_name=mother_name_entry.get(),
        gender=selected_gender.get(),
        date=date_entry,
        city=city(),
        residential_registration=residential_registration_entry.get(),
        national_number=national_number_entry.get(),
        full_address=full_address_entry.get(),
        profile_path=profile_path,  # Ensure this is updated via file_picker
        education=education(),
        academic_specialization=academic_specialization_entry.get(),
        job=job_entry.get(),
        current_job=current_job_entry.get(),
        height=selected_height.get(),
        weight=selected_weight.get(),
        eye_color=eye_color(),
        hair_color=hair_color(),
        skin_color=skin_color(),
        unique_features=unique_features_entry.get(),
        social_status=social_status_entry.get(),
        children_number=children_number_entry.get(),
        children=[(entry.get(), gender.get()) for entry, gender in children_entries],
        phone_number=phone_number_entry.get(),
        social_media=social_media_entry.get(),
        nationality=get_nationality()
    )

    submit_data(form_data)  # Submit the data

    clear_inputs_in_frame(content_frame)

    set_profile_path('')

    # Reset dropdowns and selection fields
    selection_variables = [
        selected_gender,
        city_entry_var,
        city_var,
        education_entry_var,
        education_var,
        eye_color_entry_var,
        hair_color_entry_var,
        skin_color_entry_var,
        eye_color_var,
        skin_color_var,
        hair_color_var,
        social_status_entry,
        nationality_var,
        nationality_entry_var
    ]
    reset_variables(selection_variables)

    # Clear children entries
    for entry, gender in children_entries:
        entry.delete(0, "end")
        gender.set("")

# Buttons
add_btn_frame = ttk.Frame(content_frame)
add_btn_frame.pack(pady=10)
ttk.Button(add_btn_frame, text="إضافة", command=on_submit).pack(pady=10)
# submit_button = ctk.CTkButton(frm, text="إضافة", command=submit_data).grid(row=5, column=0)

content_window = canvas.create_window(
    (canvas.winfo_width() // 2, 0), window=content_frame, anchor="n"
)

# Dynamically adjust width on resize
def resize_canvas(event):
    canvas.itemconfig("inner", width=event.width)

canvas.bind("<Configure>", resize_canvas)  # Recenter on window resize
canvas.itemconfig(canvas.create_window((0, 0), window=content_frame, anchor="n", tags="inner"), width=root.winfo_width())

canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
root.mainloop()
