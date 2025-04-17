import tkinter as tk
from datetime import datetime, timedelta, timezone
import subprocess
import calendar

from zoneinfo import ZoneInfo
import tzlocal  # pip install tzlocal

# --- Get system timezone ---
local_tz = ZoneInfo(tzlocal.get_localzone_name())

# --- Script paths ---
HAMILTON_DL_PATH = r"C:\BANA7075 Final Project\py Hamilton Montly Sales Downloader\Hamilton_Co_DLer__1_.py"
HAMILTON_SCRAPER_PATH = r"C:\BANA7075 Final Project\py Hamilton Scraper\Hamilton Scraper\Hamilton_Scraper.py"
ZIP_EXTRACTOR_PATH = r"C:\BANA7075 Final Project\py Redfin Median Zip Extractor\PythonApplication1\Zip Extractor.py"
DATA_MERGER_PATH = r"C:\BANA7075 Final Project\py Merger Hamilton and Redfin\PythonApplication1\Data_Merger.py"

# --- Main window setup ---
root = tk.Tk()
root.title("Data Extraction Manager")
root.geometry("800x600")

# --- Clock + Date display ---
clock_label = tk.Label(root, font=("Helvetica", 36), fg="black")
clock_label.pack(pady=(10, 0), anchor="w", padx=20)

date_label = tk.Label(root, font=("Helvetica", 14), fg="gray")
date_label.pack(anchor="w", padx=20)

utc_label = tk.Label(root, font=("Helvetica", 12), fg="gray")
utc_label.pack(anchor="w", padx=20)

# --- Monthly last-day run with offset ---
def get_last_day_of_month_run(hour, minute, offset_minutes=0):
    now = datetime.now(local_tz)
    year, month = now.year, now.month
    last_day = calendar.monthrange(year, month)[1]
    next_run = datetime(year, month, last_day, hour, minute, tzinfo=local_tz)

    if next_run <= now:
        if month == 12:
            year += 1
            month = 1
        else:
            month += 1
        last_day = calendar.monthrange(year, month)[1]
        next_run = datetime(year, month, last_day, hour, minute, tzinfo=local_tz)

    return next_run + timedelta(minutes=offset_minutes)

# --- Script runner ---
def run_script(path, countdown_label, log_label):
    try:
        subprocess.Popen(["python", path], shell=True)
        countdown_label.config(fg="green")
        log_label.config(text=f"Last run: {datetime.now(local_tz).strftime('%Y-%m-%d %H:%M:%S')}")
    except Exception as e:
        countdown_label.config(fg="red")
        log_label.config(text=f"Error: {e}")

# --- Script row builder ---
def create_script_row(label_text, path, next_time_func, log_var):
    frame = tk.Frame(root)
    frame.pack(anchor="w", padx=20, pady=5)

    btn = tk.Button(frame, text=label_text, font=("Helvetica", 14),
                    command=lambda: run_script(path, countdown, log_var))
    btn.pack(side="left", padx=(0, 10))

    countdown = tk.Label(frame, font=("Helvetica", 12), fg="gray")
    countdown.pack(side="left", padx=(0, 15))

    next_label = tk.Label(frame, font=("Helvetica", 12), fg="gray")
    next_label.pack(side="left")

    return {
        "countdown_label": countdown,
        "next_label": next_label,
        "next_time": next_time_func,
    }

# --- Add script rows ---
script_rows = []

last_hamilton_dl_log = tk.Label()
script_rows.append(create_script_row("⬇ DL Hamilton Co. Sales", HAMILTON_DL_PATH,
                                     lambda: get_last_day_of_month_run(14, 0, 0), last_hamilton_dl_log))

last_hamilton_scraper_log = tk.Label()
script_rows.append(create_script_row("▶ Run Hamilton Co. Data Scraper", HAMILTON_SCRAPER_PATH,
                                     lambda: get_last_day_of_month_run(14, 0, 15), last_hamilton_scraper_log))

last_zip_extractor_log = tk.Label()
script_rows.append(create_script_row("▶ Run Redfin Zip Extractor", ZIP_EXTRACTOR_PATH,
                                     lambda: get_last_day_of_month_run(14, 0, 30), last_zip_extractor_log))

last_data_merger_log = tk.Label()
script_rows.append(create_script_row("▶ Run Data Merger", DATA_MERGER_PATH,
                                     lambda: get_last_day_of_month_run(14, 0, 45), last_data_merger_log))

# --- Log section ---
log_frame = tk.Frame(root)
log_frame.pack(pady=20, fill="x", padx=30)

tk.Label(log_frame, text="🕒 Last Run Log", font=("Helvetica", 14, "bold"), anchor="w").pack(fill="x")

for label in [last_hamilton_dl_log, last_hamilton_scraper_log, last_zip_extractor_log, last_data_merger_log]:
    label.config(text="Not yet run", font=("Helvetica", 12), fg="gray", anchor="w", justify="left")
    label.pack(fill="x", padx=10)

# --- Timer update loop ---
def update_timers():
    now = datetime.now(local_tz)
    utc_now = datetime.now(timezone.utc)

    clock_label.config(text=now.strftime("%H:%M:%S"))
    date_label.config(text=now.strftime("%a, %b %d %Y (%Z)"))
    utc_label.config(text="UTC: " + utc_now.strftime("%Y-%m-%d %H:%M"))

    for t in script_rows:
        remaining = t["next_time"]() - now
        t["countdown_label"].config(text=f"Next in: {str(remaining).split('.')[0]}")
        t["next_label"].config(text=f"Next: {t['next_time']().strftime('%a, %b %d %Y @ %I:%M %p')}")

    root.after(1000, update_timers)

# --- Launch the app ---
update_timers()
root.mainloop()