import sys
import os
import json
import random
from datetime import date, datetime, timedelta
from PIL import Image, ImageDraw, ImageTk

try:
    import customtkinter as ctk
except ImportError:
    print("Error: 'customtkinter' is required. Install it using 'pip install customtkinter'.")
    sys.exit(1)

# Windows taskbar icon grouping fix
if os.name == 'nt':
    try:
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('universal.backlogtracker.app.1.0')
    except Exception:
        pass

# Returns directory path for packaged resources
def get_bundle_dir():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

# Resolves path to user's icon.ico asset
def get_icon_path():
    bundle_dir = get_bundle_dir()
    path_bundle = os.path.join(bundle_dir, "icon.ico")
    if os.path.exists(path_bundle):
        return path_bundle

    path_cwd = os.path.join(os.getcwd(), "icon.ico")
    if os.path.exists(path_cwd):
        return path_cwd

    script_dir = os.path.dirname(os.path.abspath(__file__))
    path_script = os.path.join(script_dir, "icon.ico")
    if os.path.exists(path_script):
        return path_script

    return None

# Resolves platform-specific safe database file path
def get_data_filepath():
    if os.name == 'nt':
        base_dir = os.environ.get('LOCALAPPDATA', os.path.expanduser('~'))
    else:
        base_dir = os.path.expanduser('~')
    
    app_dir = os.path.join(base_dir, ".backlog_tracker")
    os.makedirs(app_dir, exist_ok=True)
    return os.path.join(app_dir, "backlog_data.json")

SAVE_FILE = get_data_filepath()

# Dark Theme Palette
APP_BG = "#0b0f19"
CARD_BG = "#111827"
SECONDARY_BG = "#1f2937"
ACCENT = "#3b82f6"       
ACCENT_LIGHT = "#60a5fa" 
ACCENT_YELLOW = "#f59e0b"
TEXT_DIM = "#9ca3af"
SUCCESS = "#10b981"
DANGER = "#ef4444"

MOTIVATIONAL_QUOTES = [
    "Anxiety guesses. Mathematics calculates. You can clear this!",
    "12 days of absolute hustle beats 2 months of constant dread.",
    "Don't just reset the clock by changing batches. Fix the daily habit today.",
    "The longer you wait, the worse it snowballs. Neutralize the threat now!",
    "Every single completed lecture is a step towards absolute mental freedom.",
    "Focus on one class at a time. Consistency defeats exponential growth.",
    "Practice from books when the backlog is clear. Clear the foundation first.",
    "Future you is watching your decisions today.",
    "A backlog ignored today becomes panic tomorrow.",
    "One completed lecture daily changes your entire trajectory.",
    "Discipline feels hard until regret feels harder.",
    "Slow progress still destroys zero progress.",
    "You don't need motivation every day. You need systems.",
    "Momentum is built one boring session at a time.",
    "The topper is usually just the most consistent person.",
    "Your competition is studying while you're negotiating with yourself.",
    "Clear today's work before tomorrow arrives.",
    "The fear disappears when the work starts.",
    "Small wins create dangerous confidence.",
    "A single focused hour beats five distracted hours.",
    "Backlog is temporary. Skills are permanent.",
    "If you can survive the boring days, you can win anything.",
    "Stop measuring mood. Start measuring completed lectures.",
    "Every lecture skipped today returns stronger tomorrow.",
    "The best stress relief is finishing pending work.",
    "One chapter completed is better than ten chapters planned.",
    "You are always one productive week away from confidence.",
    "Don't chase motivation. Chase momentum.",
    "Your future rank is hidden inside today's consistency.",
    "The comeback starts with opening the first lecture.",
    "A disciplined student eventually beats a talented procrastinator.",
    "Nobody clears backlog accidentally.",
    "The hardest lecture is usually the one you keep avoiding.",
    "Done imperfectly beats postponed perfectly.",
    "You are not behind forever unless you stop moving.",
    "Finish what your past self abandoned.",
    "Motivation starts after action, not before it.",
    "Pressure becomes power when you finally start working.",
    "Every completed class weakens your anxiety.",
    "Consistency looks small daily but massive yearly.",
    "The pain of studying ends. The pain of regret compounds.",
    "Progress is built quietly, not dramatically.",
    "Backlog doesn't disappear with planning. It disappears with execution.",
    "One more lecture. Then another. That's how people recover.",
    "You don't need a perfect timetable. You need honest effort.",
    "The strongest students are usually the most repetitive.",
    "No reset button will save you. Daily action will.",
    "Your goals require fewer excuses and more completed tasks.",
    "You become confident by keeping promises to yourself.",
    "Results respect repetition.",
    "The best way to reduce stress is to reduce pending work.",
    "Hard days are where serious students are created.",
    "The lecture you're avoiding is probably the most important one.",
    "A calm mind is earned through completed work.",
    "You can either suffer discipline or suffer consequences.",
    "Every day delayed increases the future workload.",
    "Clear the backlog before it controls your life.",
]

PRESET_SUBJECTS = {
    "Physics":      ("⚛️",  "#FF6B35"),
    "Maths":        ("🧮",  "#06b6d4"),
    "Chemistry":    ("🧪",  "#a855f7"),
    "Biology":      ("🧬",  "#10b981"),
    "Computer Sci": ("💻",  "#ec4899"),
    "Electronics":    ("🔌",  "#06b6d4"),
    "AI / ML":        ("🤖",  "#3b82f6"),
    "Robotics":       ("🦾",  "#64748b"),
    "Web Dev":        ("🌐",  "#0f766e"),
    "Programming":    ("⌨️",  "#7c3aed"),
    "Accountancy":    ("📚",  "#14b8a6"),
    "Business Stud.": ("💼",  "#8b5cf6"),
    "Statistics":     ("📊",  "#0ea5e9"),
}

PALETTE = [
    "#FF6B35", "#06b6d4", "#a855f7", "#10b981", "#fbbf24",
    "#f97316", "#0ea5e9", "#ec4899", "#14b8a6", "#ef4444",
    "#3b82f6", "#84cc16", "#6366f1", "#d946ef", "#6b7280"
]

DEFAULT_DATA = {
    "subjects": {},
    "classes_per_day": 4,
    "skip_sunday": True,
    "course_name": "My Course Tracker",
    "last_updated": str(date.today()),
    "setup_done": False,
    "theme": "dark"
}

# Generates fallback app icon dynamically
def create_app_icon(size=64):
    img = Image.new('RGBA', (size, size), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([2, 2, size - 3, size - 3], outline="#3b82f6", width=4)
    draw.rectangle([18, 20, size - 19, size - 20], fill="#f59e0b")
    draw.polygon([(18, 20), (size // 2, 34), (size - 19, 20)], fill="#3b82f6")
    draw.ellipse([size // 2 - 4, size // 2 - 4, size // 2 + 4, size // 2 + 4], fill="#ffffff")
    return img

# Sets cross-platform window icons
def set_window_icon(window):
    try:
        icon_path = get_icon_path()
        if icon_path and os.path.exists(icon_path):
            if os.name == 'nt':
                try:
                    window.iconbitmap(icon_path)
                except Exception:
                    pass
            icon_img = Image.open(icon_path).convert("RGBA")
            resized_img = icon_img.resize((32, 32), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(resized_img)
            window._current_icon_photo = photo
            window.wm_iconphoto(True, photo)
        else:
            fallback_img = create_app_icon(32)
            photo = ImageTk.PhotoImage(fallback_img)
            window._current_icon_photo = photo
            window.wm_iconphoto(True, photo)
    except Exception:
        pass

# Loads state configuration from save file
def load_data():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)
            for k, v in DEFAULT_DATA.items():
                data.setdefault(k, v)
            return data
        except Exception:
            pass
    return dict(DEFAULT_DATA)

# Writes state configuration to save file
def save_data(data):
    try:
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass

# Processes elapsed days and updates backlogs
def advance_days(data):
    if not data.get("subjects"):
        return data

    try:
        last = date.fromisoformat(data["last_updated"])
    except Exception:
        last = date.today()
        
    today = date.today()
    if today <= last:
        return data

    delta = (today - last).days
    incremented_days = 0

    for i in range(delta):
        day = last + timedelta(days=i + 1)
        if data["skip_sunday"] and day.weekday() == 6:
            continue
        for _, s in data["subjects"].items():
            s["backlog"] = s.get("backlog", 0) + s.get("daily_increase", 1)
        incremented_days += 1

    data["last_updated"] = str(today)
    save_data(data)
    if incremented_days > 0:
        data["_sync_notice"] = f"Auto-synced: Added {incremented_days} days of growth."
    return data

def total_backlog(data):
    return sum(s.get("backlog", 0) for s in data["subjects"].values())

def total_growth(data):
    return sum(s.get("daily_increase", 1) for s in data["subjects"].values())

# Simulates daily study plans to compute ETA
def days_to_clear_calendar(data):
    total = total_backlog(data)
    if total <= 0:
        return 0

    cpd = data["classes_per_day"]
    growth = total_growth(data)

    if data["skip_sunday"]:
        weekly_clearance = (cpd * 7) - (growth * 6)
    else:
        weekly_clearance = (cpd - growth) * 7

    if weekly_clearance <= 0:
        return float("inf")

    current_backlog = total
    calendar_days = 0
    current_date = date.today()
    
    while current_backlog > 0 and calendar_days < 10000:
        calendar_days += 1
        target_day = current_date + timedelta(days=calendar_days)
        if data["skip_sunday"] and target_day.weekday() == 6:
            current_backlog -= cpd
        else:
            current_backlog -= (cpd - growth)
            
    return calendar_days

# Generates UI category text breaks
def section(parent, text):
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    frame.pack(fill="x", padx=24, pady=(16, 6))
    ctk.CTkLabel(frame, text=text, font=ctk.CTkFont(size=14, weight="bold"), text_color=ACCENT_LIGHT).pack(side="left")

# Simple warning pop-up window
def popup(parent, text, title="Notice"):
    top = ctk.CTkToplevel(parent)
    top.geometry("360x160")
    top.title(title)
    top.resizable(False, False)
    top.grab_set()
    set_window_icon(top)

    main_frame = ctk.CTkFrame(top, fg_color=APP_BG)
    main_frame.pack(fill="both", expand=True)
    ctk.CTkLabel(main_frame, text=text, wraplength=300, font=ctk.CTkFont(size=13), text_color="white").pack(expand=True, padx=20, pady=(20, 10))
    ctk.CTkButton(main_frame, text="Close", width=100, fg_color=ACCENT, hover_color=ACCENT_LIGHT, command=top.destroy).pack(pady=(0, 15))


class SetupWindow(ctk.CTkToplevel):
    def __init__(self, parent, data, on_done):
        super().__init__(parent)
        self.geometry("780x820")
        self.title("Setup Wizard — Backlog Tracker")
        self.configure(fg_color=APP_BG)
        self.wait_visibility()  
        self.grab_set()        
        set_window_icon(self)

        self.data = data
        self.on_done = on_done
        self.selected_presets = set()
        self.custom_rows = []
        self.preset_backlogs = {}
        self.preset_growths = {}

        # Safe close protocol handling
        self.protocol("WM_DELETE_WINDOW", self.on_close_request)
        self.build()

    # Gracefully intercepts close button actions
    def on_close_request(self):
        if not self.data.get("setup_done") or not self.data.get("subjects"):
            self.master.destroy()
        else:
            self.destroy()

    def build(self):
        scroll = ctk.CTkScrollableFrame(self, fg_color=APP_BG)
        scroll.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(scroll, text="🎓 Set Up Your Dashboard", font=ctk.CTkFont(size=26, weight="bold"), text_color="white").pack(pady=(20, 4))
        ctk.CTkLabel(scroll, text="Set daily targets and structure your active curriculum.", text_color=TEXT_DIM, font=ctk.CTkFont(size=13)).pack(pady=(0, 20))

        section(scroll, "📝 Target Settings")
        info_frame = ctk.CTkFrame(scroll, fg_color=CARD_BG, corner_radius=12)
        info_frame.pack(fill="x", padx=24, pady=6)

        row_batch = ctk.CTkFrame(info_frame, fg_color="transparent")
        row_batch.pack(fill="x", padx=16, pady=(14, 8))
        ctk.CTkLabel(row_batch, text="Target Milestone / Batch Name", font=ctk.CTkFont(size=13, weight="bold"), text_color="white").pack(side="left")
        self.course_var = ctk.StringVar(value=self.data.get("course_name", "JEE 2027"))
        ctk.CTkEntry(row_batch, textvariable=self.course_var, width=220, height=34, placeholder_text="e.g., JEE 2027, UPSC").pack(side="right")

        row_classes = ctk.CTkFrame(info_frame, fg_color="transparent")
        row_classes.pack(fill="x", padx=16, pady=8)
        ctk.CTkLabel(row_classes, text="Daily Class Completion Target (CPD)", font=ctk.CTkFont(size=13, weight="bold"), text_color="white").pack(side="left")
        self.cpd_var = ctk.StringVar(value=str(self.data.get("classes_per_day", 4)))
        ctk.CTkEntry(row_classes, width=80, height=34, justify="center", textvariable=self.cpd_var).pack(side="right")

        row_skip = ctk.CTkFrame(info_frame, fg_color="transparent")
        row_skip.pack(fill="x", padx=16, pady=(8, 14))
        ctk.CTkLabel(row_skip, text="Skip Sunday Live Classes (No growth, study remains active)", font=ctk.CTkFont(size=13, weight="bold"), text_color="white").pack(side="left")
        self.skip_var = ctk.BooleanVar(value=self.data.get("skip_sunday", True))
        ctk.CTkSwitch(row_skip, text="", variable=self.skip_var, progress_color=ACCENT).pack(side="right")

        section(scroll, "📋 Quick Curriculums Presets")
        grid_wrapper = ctk.CTkFrame(scroll, fg_color="transparent")
        grid_wrapper.pack(fill="x", padx=24, pady=6)
        grid_wrapper.grid_columnconfigure((0, 1, 2), weight=1, uniform="equal")

        # Subject presets population
        for i, (name, (emoji, color)) in enumerate(PRESET_SUBJECTS.items()):
            active = name in self.data.get("subjects", {})
            if active:
                self.selected_presets.add(name)

            card = ctk.CTkFrame(grid_wrapper, fg_color=CARD_BG, corner_radius=12)
            card.grid(row=i // 3, column=i % 3, padx=6, pady=6, sticky="nsew")

            btn = ctk.CTkButton(
                card, text=f"{emoji} {name}",
                fg_color=color if active else SECONDARY_BG,
                hover_color=color,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="white" if active else TEXT_DIM,
                height=34,
                command=lambda n=name, c=color: self.toggle_preset(n, c)
            )
            btn.pack(fill="x", padx=10, pady=(10, 6))
            setattr(self, f"preset_btn_{name}", btn)

            sub_frame_backlog = ctk.CTkFrame(card, fg_color="transparent")
            sub_frame_backlog.pack(fill="x", padx=10, pady=(2, 4))
            ctk.CTkLabel(sub_frame_backlog, text="Backlog:", font=ctk.CTkFont(size=11), text_color=TEXT_DIM).pack(side="left")
            curr_backlog = str(self.data.get("subjects", {}).get(name, {}).get("backlog", 0))
            backlog_var = ctk.StringVar(value=curr_backlog)
            self.preset_backlogs[name] = backlog_var
            ctk.CTkEntry(sub_frame_backlog, width=54, height=22, justify="center", font=ctk.CTkFont(size=11), textvariable=backlog_var).pack(side="right")

            sub_frame_growth = ctk.CTkFrame(card, fg_color="transparent")
            sub_frame_growth.pack(fill="x", padx=10, pady=(2, 10))
            ctk.CTkLabel(sub_frame_growth, text="New Rate/day:", font=ctk.CTkFont(size=11), text_color=TEXT_DIM).pack(side="left")
            curr_growth = str(self.data.get("subjects", {}).get(name, {}).get("daily_increase", 1))
            growth_var = ctk.StringVar(value=curr_growth)
            self.preset_growths[name] = growth_var
            ctk.CTkEntry(sub_frame_growth, width=54, height=22, justify="center", font=ctk.CTkFont(size=11), textvariable=growth_var).pack(side="right")

        section(scroll, "➕ Add Customized Modules")
        self.custom_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        self.custom_frame.pack(fill="x", padx=24, pady=4)

        for name, s in self.data.get("subjects", {}).items():
            if name not in PRESET_SUBJECTS:
                self.add_custom_row(name=name, emoji=s.get("emoji", "📚"), color=s.get("color", PALETTE[0]), backlog=s.get("backlog", 0), di=s.get("daily_increase", 1))

        ctk.CTkButton(scroll, text="➕ Append New Custom Subject Row", height=38, fg_color=SECONDARY_BG, hover_color=ACCENT, font=ctk.CTkFont(size=12, weight="bold"), command=self.add_custom_row).pack(fill="x", padx=24, pady=(8, 20))
        save_btn = ctk.CTkButton(scroll, text="🚀 Apply Setup Configuration", height=48, fg_color=SUCCESS, hover_color="#059669", font=ctk.CTkFont(size=15, weight="bold"), command=self.save_setup)
        save_btn.pack(fill="x", padx=24, pady=(10, 20))

    def toggle_preset(self, name, color):
        btn = getattr(self, f"preset_btn_{name}")
        if name in self.selected_presets:
            self.selected_presets.remove(name)
            btn.configure(fg_color=SECONDARY_BG, text_color=TEXT_DIM)
        else:
            self.selected_presets.add(name)
            btn.configure(fg_color=color, text_color="white")

    def add_custom_row(self, name="", emoji="📚", color=None, backlog=0, di=1):
        if color is None:
            color = PALETTE[len(self.custom_rows) % len(PALETTE)]

        row = ctk.CTkFrame(self.custom_frame, fg_color=CARD_BG, corner_radius=10)
        row.pack(fill="x", pady=5)

        name_var = ctk.StringVar(value=name)
        emoji_var = ctk.StringVar(value=emoji)
        color_var = ctk.StringVar(value=color)
        backlog_var = ctk.StringVar(value=str(backlog))
        di_var = ctk.StringVar(value=str(di))

        ctk.CTkEntry(row, width=150, height=32, textvariable=name_var, placeholder_text="Module Name...").pack(side="left", padx=(10, 5), pady=8)
        ctk.CTkEntry(row, width=42, height=32, justify="center", textvariable=emoji_var).pack(side="left", padx=5)

        color_index = {"idx": PALETTE.index(color) if color in PALETTE else 0}

        def cycle_color():
            color_index["idx"] = (color_index["idx"] + 1) % len(PALETTE)
            new_col = PALETTE[color_index["idx"]]
            color_var.set(new_col)
            color_btn.configure(fg_color=new_col)

        color_btn = ctk.CTkButton(row, text="🎨", width=36, height=32, fg_color=color, hover_color="#ffffff", command=cycle_color)
        color_btn.pack(side="left", padx=5)

        b_frame = ctk.CTkFrame(row, fg_color="transparent")
        b_frame.pack(side="left", padx=5)
        ctk.CTkLabel(b_frame, text="Backlog", font=ctk.CTkFont(size=9), text_color=TEXT_DIM).pack()
        ctk.CTkEntry(b_frame, width=54, height=22, justify="center", textvariable=backlog_var).pack()

        g_frame = ctk.CTkFrame(row, fg_color="transparent")
        g_frame.pack(side="left", padx=5)
        ctk.CTkLabel(g_frame, text="Growth/d", font=ctk.CTkFont(size=9), text_color=TEXT_DIM).pack()
        ctk.CTkEntry(g_frame, width=54, height=22, justify="center", textvariable=di_var).pack()

        def remove_self():
            row.destroy()
            self.custom_rows = [x for x in self.custom_rows if x[-1] != row]

        ctk.CTkButton(row, text="✕", width=32, height=32, fg_color="transparent", text_color=DANGER, hover_color=SECONDARY_BG, command=remove_self).pack(side="right", padx=10)
        self.custom_rows.append((name_var, emoji_var, color_var, backlog_var, di_var, row))

    def save_setup(self):
        subjects = {}

        for name in self.selected_presets:
            emoji, color = PRESET_SUBJECTS[name]
            try:
                backlog = max(0, int(self.preset_backlogs[name].get().strip()))
            except ValueError:
                backlog = 0
            try:
                di = max(0, int(self.preset_growths[name].get().strip()))
            except ValueError:
                di = 1
            subjects[name] = {"backlog": backlog, "emoji": emoji, "color": color, "daily_increase": di}

        for name_var, emoji_var, color_var, backlog_var, di_var, _ in self.custom_rows:
            raw_name = name_var.get().strip()
            if not raw_name:
                continue
            try:
                backlog = max(0, int(backlog_var.get().strip()))
            except ValueError:
                backlog = 0
            try:
                di = max(0, int(di_var.get().strip()))
            except ValueError:
                di = 1
            subjects[raw_name] = {"backlog": backlog, "emoji": emoji_var.get().strip() or "📚", "color": color_var.get(), "daily_increase": di}

        if not subjects:
            popup(self, "Please customize and activate at least one learning subject to begin tracking.", "Warning")
            return

        try:
            cpd = max(1, int(self.cpd_var.get().strip()))
        except ValueError:
            cpd = 4

        self.data["subjects"] = subjects
        self.data["classes_per_day"] = cpd
        self.data["skip_sunday"] = self.skip_var.get()
        self.data["course_name"] = self.course_var.get().strip() or "My Course Tracker"
        self.data["setup_done"] = True

        save_data(self.data)
        self.destroy()
        self.on_done()


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("640x950")
        self.title("Backlog Tracker")
        self.configure(fg_color=APP_BG)
        set_window_icon(self)

        self.data = advance_days(load_data())

        if not self.data.get("setup_done") or not self.data.get("subjects"):
            self.display_onboarding()
        else:
            self.build_dashboard()

    def display_onboarding(self):
        self.onboard_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.onboard_frame.pack(fill="both", expand=True)

        ctk.CTkLabel(self.onboard_frame, text="🎓 BACKLOG TRACKER", font=ctk.CTkFont(size=28, weight="bold"), text_color="white").pack(expand=True, pady=(100, 10))
        start_btn = ctk.CTkButton(
            self.onboard_frame, text="Initialize Setup Wizard ⚙️", height=48, fg_color=ACCENT, hover_color=ACCENT_LIGHT,
            font=ctk.CTkFont(size=14, weight="bold"), command=lambda: SetupWindow(self, self.data, self.finish_onboarding)
        )
        start_btn.pack(expand=True, pady=(0, 100))

    def finish_onboarding(self):
        if hasattr(self, "onboard_frame"):
            self.onboard_frame.destroy()
        self.reload_and_refresh()

    def reload_and_refresh(self):
        self.data = load_data()
        for widget in self.winfo_children():
            widget.destroy()
        self.build_dashboard()

    def build_dashboard(self):
        header_frame = ctk.CTkFrame(self, fg_color=CARD_BG, corner_radius=0)
        header_frame.pack(fill="x")

        title_row = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_row.pack(fill="x", padx=20, pady=(15, 4))
        ctk.CTkLabel(title_row, text=f"🎓 {self.data['course_name']}", font=ctk.CTkFont(size=22, weight="bold"), text_color="white").pack(side="left")

        ctk.CTkButton(
            title_row, text="Configure App ⚙️", width=110, height=28, fg_color=SECONDARY_BG, hover_color=ACCENT,
            font=ctk.CTkFont(size=11, weight="bold"), command=lambda: SetupWindow(self, self.data, self.reload_and_refresh)
        ).pack(side="right")

        motivation_frame = ctk.CTkFrame(header_frame, fg_color=SECONDARY_BG, corner_radius=8)
        motivation_frame.pack(fill="x", padx=20, pady=(4, 12))
        
        selected_quote = random.choice(MOTIVATIONAL_QUOTES)
        self.quote_label = ctk.CTkLabel(motivation_frame, text=f"🔥 \"{selected_quote}\"", text_color=ACCENT_LIGHT, wraplength=540, justify="center", font=ctk.CTkFont(size=12, slant="italic", weight="bold"))
        self.quote_label.pack(fill="x", padx=12, pady=8)

        kpi_frame = ctk.CTkFrame(self, fg_color="transparent")
        kpi_frame.pack(fill="x", padx=16, pady=(10, 6))
        kpi_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="equal")

        self.kpi_total = self.render_kpi_card(kpi_frame, "📦 TOTAL BACKLOG", "0", 0)
        self.kpi_growth = self.render_kpi_card(kpi_frame, "📈 DAILY GROWTH", "0/day", 1)
        self.kpi_eta = self.render_kpi_card(kpi_frame, "⌛ CLEARANCE ETA", "0 days", 2)

        self.status_banner = ctk.CTkFrame(self, fg_color=CARD_BG, corner_radius=10)
        self.status_banner.pack(fill="x", padx=16, pady=(0, 10))
        self.threat_lvl_label = ctk.CTkLabel(self.status_banner, text="THREAT LEVEL: DIAGNOSING...", font=ctk.CTkFont(size=12, weight="bold"), text_color="white")
        self.threat_lvl_label.pack(side="left", padx=16, pady=8)

        sync_txt = self.data.get("_sync_notice", "")
        if not sync_txt:
            sync_txt = f"Last Checked: {self.data.get('last_updated', str(date.today()))}"
            
        self.sync_label = ctk.CTkLabel(self.status_banner, text=sync_txt, font=ctk.CTkFont(size=11), text_color=TEXT_DIM)
        self.sync_label.pack(side="right", padx=16, pady=8)

        controls = ctk.CTkFrame(self, fg_color=CARD_BG, corner_radius=12)
        controls.pack(fill="x", padx=16, pady=(0, 10))

        row_ctrl = ctk.CTkFrame(controls, fg_color="transparent")
        row_ctrl.pack(fill="x", padx=16, pady=10)
        ctk.CTkLabel(row_ctrl, text="Dynamic CPD Capacity Target:", font=ctk.CTkFont(size=12, weight="bold"), text_color="white").pack(side="left")

        self.cpd_input_var = ctk.StringVar(value=str(self.data.get("classes_per_day", 4)))
        target_entry = ctk.CTkEntry(row_ctrl, width=50, height=26, justify="center", textvariable=self.cpd_input_var, font=ctk.CTkFont(size=12, weight="bold"))
        target_entry.pack(side="left", padx=10)
        target_entry.bind("<Return>", lambda e: self.update_global_target())
        target_entry.bind("<FocusOut>", lambda e: self.update_global_target())

        # Configures visual chart canvas
        self.chart_canvas = ctk.CTkCanvas(controls, height=70, bg=CARD_BG, highlightthickness=0)
        self.chart_canvas.pack(fill="x", padx=16, pady=(0, 10))
        
        # Redraws visual weight distribution bar dynamically on window resize
        self.chart_canvas.bind("<Configure>", lambda event: self.draw_visual_insights())

        self.subject_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.subject_scroll.pack(fill="both", expand=True, padx=12)

        self.cards_dict = {}
        for s_name, s_data in self.data["subjects"].items():
            self.append_dashboard_card(s_name, s_data)

        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.pack(fill="x", padx=16, pady=10)

        self.lbl_eta_date = ctk.CTkLabel(footer, text="", font=ctk.CTkFont(size=12, weight="bold"), text_color=ACCENT_LIGHT)
        self.lbl_eta_date.pack(side="left")

        ctk.CTkButton(footer, text="Sync Changes 🔄", width=120, fg_color=SECONDARY_BG, hover_color=ACCENT, command=self.refresh_dashboard).pack(side="right")
        self.refresh_dashboard()

    def render_kpi_card(self, parent, title, val, col_idx):
        card = ctk.CTkFrame(parent, fg_color=CARD_BG, corner_radius=12)
        card.grid(row=0, column=col_idx, padx=4, sticky="nsew")
        lbl_title = ctk.CTkLabel(card, text=title, text_color=TEXT_DIM, font=ctk.CTkFont(size=10, weight="bold"))
        lbl_title.pack(pady=(12, 2))
        lbl_val = ctk.CTkLabel(card, text=val, font=ctk.CTkFont(size=18, weight="bold"), text_color="white")
        lbl_val.pack(pady=(0, 12))
        card.lbl_val = lbl_val
        return card

    # Repaints custom visual insights chart
    def draw_visual_insights(self):
        self.chart_canvas.delete("all")
        width = self.chart_canvas.winfo_width()
        if width <= 1:
            width = 580

        subjects = self.data["subjects"]
        total = total_backlog(self.data)

        if total <= 0:
            self.chart_canvas.create_text(width // 2, 35, text="🎉 ALL CURRICULUMS SECURED & DEFEATED", fill=SUCCESS, font=("Arial", 11, "bold"))
            return

        self.chart_canvas.create_text(10, 10, text="Curriculum Weight Distribution:", fill=TEXT_DIM, font=("Arial", 9, "normal"), anchor="w")

        current_x = 10
        usable_width = width - 20
        bar_y_start = 22
        bar_height = 14

        for name, data in subjects.items():
            backlog = data.get("backlog", 0)
            if backlog <= 0:
                continue
            color = data.get("color", "#ffffff")
            ratio = backlog / total
            segment_width = ratio * usable_width
            if segment_width < 3:
                continue

            self.chart_canvas.create_rectangle(current_x, bar_y_start, current_x + segment_width, bar_y_start + bar_height, fill=color, outline="")
            current_x += segment_width

        active_list = sorted(subjects.items(), key=lambda x: x[1].get("backlog", 0), reverse=True)[:3]
        legend_x = 10
        for name, data in active_list:
            backlog = data.get("backlog", 0)
            if backlog <= 0:
                continue
            color = data.get("color", "#ffffff")
            emoji = data.get("emoji", "📚")
            
            self.chart_canvas.create_oval(legend_x, 48, legend_x + 8, 56, fill=color, outline="")
            self.chart_canvas.create_text(legend_x + 12, 52, text=f"{emoji} {name} ({backlog})", fill="white", font=("Arial", 9, "bold"), anchor="w")
            legend_x += 140

    def append_dashboard_card(self, name, s_data):
        color = s_data.get("color", ACCENT)
        emoji = s_data.get("emoji", "📚")

        card = ctk.CTkFrame(self.subject_scroll, fg_color=CARD_BG, border_width=1, border_color=SECONDARY_BG, corner_radius=14)
        card.pack(fill="x", pady=6)

        container = ctk.CTkFrame(card, fg_color="transparent")
        container.pack(fill="x", padx=16, pady=(12, 10))

        left_box = ctk.CTkFrame(container, fg_color="transparent")
        left_box.pack(side="left", fill="both", expand=True)

        lbl_title = ctk.CTkLabel(left_box, text=f"{emoji} {name}", text_color=color, font=ctk.CTkFont(size=16, weight="bold"))
        lbl_title.pack(anchor="w")

        sub_row = ctk.CTkFrame(left_box, fg_color="transparent")
        sub_row.pack(anchor="w", pady=(2, 0))
        ctk.CTkLabel(sub_row, text="Growth: +", text_color=TEXT_DIM, font=ctk.CTkFont(size=11)).pack(side="left")

        growth_var = ctk.StringVar(value=str(s_data.get("daily_increase", 1)))
        growth_entry = ctk.CTkEntry(sub_row, width=34, height=18, justify="center", font=ctk.CTkFont(size=10, weight="bold"), textvariable=growth_var)
        growth_entry.pack(side="left", padx=2)
        ctk.CTkLabel(sub_row, text="/day", text_color=TEXT_DIM, font=ctk.CTkFont(size=11)).pack(side="left")

        # Direct inline updates handler
        def update_growth_rate(*args):
            try:
                val = max(0, int(growth_var.get().strip()))
                self.data["subjects"][name]["daily_increase"] = val
                save_data(self.data)
                self.refresh_dashboard()
            except ValueError:
                pass

        growth_entry.bind("<Return>", update_growth_rate)
        growth_entry.bind("<FocusOut>", update_growth_rate)

        right_box = ctk.CTkFrame(container, fg_color="transparent")
        right_box.pack(side="right")

        lbl_qty = ctk.CTkLabel(right_box, text="0 Classes", font=ctk.CTkFont(size=16, weight="bold"), text_color="white")
        lbl_qty.pack(anchor="e")

        progress_bar = ctk.CTkProgressBar(card, height=6, progress_color=color, fg_color=SECONDARY_BG)
        progress_bar.pack(fill="x", padx=16, pady=(0, 10))
        progress_bar.set(0)

        interactions = ctk.CTkFrame(card, fg_color="transparent")
        interactions.pack(fill="x", padx=16, pady=(0, 12))

        ctk.CTkButton(interactions, text="➕ Class Added", width=110, height=30, fg_color=SECONDARY_BG, hover_color=DANGER, font=ctk.CTkFont(size=11, weight="bold"), command=lambda: self.tweak_backlog_metric(name, 1)).pack(side="left", padx=(0, 6))
        ctk.CTkButton(
            interactions, text="✅ Completed Class", width=135, height=30, fg_color=color, 
            text_color="#000" if self.get_brightness_is_high(color) else "#fff", hover_color="#ffffff", 
            font=ctk.CTkFont(size=11, weight="bold"), command=lambda: self.tweak_backlog_metric(name, -1)
        ).pack(side="left")

        self.cards_dict[name] = {
            "qty_label": lbl_qty,
            "progress": progress_bar,
            "growth_entry": growth_entry,
            "growth_var": growth_var
        }

    # Custom brightness evaluation to dynamically contrast overlay text
    def get_brightness_is_high(self, hex_color):
        hex_color = hex_color.lstrip('#')
        try:
            r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            brightness = (r * 299 + g * 587 + b * 114) / 1000
            return brightness > 140
        except Exception:
            return True

    def tweak_backlog_metric(self, name, amount):
        curr = self.data["subjects"][name].get("backlog", 0)
        self.data["subjects"][name]["backlog"] = max(0, curr + amount)
        save_data(self.data)
        self.refresh_dashboard()

    def update_global_target(self):
        try:
            val = max(1, int(self.cpd_input_var.get().strip()))
            self.data["classes_per_day"] = val
            save_data(self.data)
        except ValueError:
            pass
        self.refresh_dashboard()

    def refresh_dashboard(self):
        total = total_backlog(self.data)
        growth = total_growth(self.data)
        days = days_to_clear_calendar(self.data)

        self.kpi_total.lbl_val.configure(text=str(total))
        self.kpi_growth.lbl_val.configure(text=f"{growth}/day")

        if total == 0:
            self.threat_lvl_label.configure(text="🔴 STATUS INDEX: SECURED (No Backlog)", text_color=SUCCESS)
        elif days == float("inf"):
            self.threat_lvl_label.configure(text="⚠️ ALERT: CRITICAL (Snowballing Out of Control)", text_color=DANGER)
        elif days > 30:
            self.threat_lvl_label.configure(text="🔸 STATUS INDEX: OVERLOADED (Steady Progress Needed)", text_color=ACCENT_YELLOW)
        else:
            self.threat_lvl_label.configure(text="🔹 STATUS INDEX: STABILIZED (Under Active Clearance)", text_color=ACCENT_LIGHT)

        if days == float("inf"):
            self.kpi_total.lbl_val.configure(text_color=DANGER)
            self.kpi_eta.lbl_val.configure(text="Never", text_color=DANGER)
            self.lbl_eta_date.configure(text="⚠️ Growth rate matches/outpaces daily watch target. Backlog cannot clear.", text_color=DANGER)
        else:
            self.kpi_total.lbl_val.configure(text_color="white")
            self.kpi_eta.lbl_val.configure(text=f"{days} days", text_color=SUCCESS if days == 0 else "white")
            
            if days == 0:
                self.lbl_eta_date.configure(text="🎉 Track Clear: All modules optimized!", text_color=SUCCESS)
            else:
                eta_date = date.today() + timedelta(days=int(days))
                self.lbl_eta_date.configure(text=f"📅 Target Catchup Date: {eta_date.strftime('%A, %d %b %Y')}", text_color=ACCENT_LIGHT)

        max_item_backlog = max([s.get("backlog", 0) for s in self.data["subjects"].values()] + [1])

        for name, widgets in self.cards_dict.items():
            s = self.data["subjects"][name]
            backlog_count = s.get("backlog", 0)
            widgets["qty_label"].configure(text=f"{backlog_count} Lectures")
            
            progress_ratio = 1.0 - (backlog_count / max_item_backlog) if max_item_backlog > 0 else 1.0
            widgets["progress"].set(max(0.02, progress_ratio))
            widgets["growth_var"].set(str(s.get("daily_increase", 1)))

        if total > 0 and random.random() < 0.25:
            self.quote_label.configure(text=f"🔥 \"{random.choice(MOTIVATIONAL_QUOTES)}\"")

        self.draw_visual_insights()


if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    app = App()
    app.mainloop()