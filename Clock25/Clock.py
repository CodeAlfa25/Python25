import customtkinter as ctk
import time
from datetime import datetime, timedelta
import threading
import pytz

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class ClockApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Clock25 By @CodeAlfa25")
        self.geometry("600x500")

        self.tabview = ctk.CTkTabview(self, width=580, height=480)
        self.tabview.pack(padx=10, pady=10)

        self.local_tab = self.tabview.add("Local Time")
        self.world_tab = self.tabview.add("World Clocks")
        self.stopwatch_tab = self.tabview.add("Stopwatch")
        self.timer_tab = self.tabview.add("Timer")

        self.init_local_time()
        self.init_world_time()
        self.init_stopwatch()
        self.init_timer()

    # -------- Local Time ----------
    def init_local_time(self):
        self.local_label = ctk.CTkLabel(self.local_tab, font=("Consolas", 40))
        self.local_label.pack(pady=100)
        self.update_local_time()

    def update_local_time(self):
        now = datetime.now().strftime('%I:%M:%S %p')
        self.local_label.configure(text=f"Local Time: {now}")
        self.after(1000, self.update_local_time)

    # -------- World Time ----------
    def init_world_time(self):
        self.timezones = ['UTC', 'Asia/Kolkata', 'US/Pacific', 'Europe/London']
        self.labels = []
        for zone in self.timezones:
            lbl = ctk.CTkLabel(self.world_tab, font=("Consolas", 20))
            lbl.pack(pady=5)
            self.labels.append((zone, lbl))
        self.update_world_time()

    def update_world_time(self):
        for zone, lbl in self.labels:
            tz = pytz.timezone(zone)
            now = datetime.now(tz).strftime('%I:%M:%S %p')
            lbl.configure(text=f"{zone}: {now}")
        self.after(1000, self.update_world_time)

    # -------- Stopwatch ----------
    def init_stopwatch(self):
        self.sw_running = False
        self.sw_start_time = 0
        self.sw_elapsed = 0

        self.sw_display = ctk.CTkLabel(self.stopwatch_tab, text="00:00:00", font=("Consolas", 40))
        self.sw_display.pack(pady=20)

        btn_frame = ctk.CTkFrame(self.stopwatch_tab)
        btn_frame.pack()

        self.sw_start_btn = ctk.CTkButton(btn_frame, text="Start", command=self.start_stopwatch)
        self.sw_start_btn.grid(row=0, column=0, padx=10)

        self.sw_pause_btn = ctk.CTkButton(btn_frame, text="Pause", command=self.pause_stopwatch)
        self.sw_pause_btn.grid(row=0, column=1, padx=10)

        self.sw_reset_btn = ctk.CTkButton(btn_frame, text="Reset", command=self.reset_stopwatch)
        self.sw_reset_btn.grid(row=0, column=2, padx=10)

    def update_stopwatch(self):
        while self.sw_running:
            elapsed = time.time() - self.sw_start_time + self.sw_elapsed
            mins, secs = divmod(int(elapsed), 60)
            hrs, mins = divmod(mins, 60)
            self.sw_display.configure(text=f"{hrs:02d}:{mins:02d}:{secs:02d}")
            time.sleep(0.5)

    def start_stopwatch(self):
        if not self.sw_running:
            self.sw_running = True
            self.sw_start_time = time.time()
            threading.Thread(target=self.update_stopwatch, daemon=True).start()

    def pause_stopwatch(self):
        if self.sw_running:
            self.sw_elapsed += time.time() - self.sw_start_time
            self.sw_running = False

    def reset_stopwatch(self):
        self.sw_running = False
        self.sw_elapsed = 0
        self.sw_display.configure(text="00:00:00")

    # -------- Timer ----------
    def init_timer(self):
        self.timer_running = False
        self.timer_seconds = 0

        self.timer_entry = ctk.CTkEntry(self.timer_tab, placeholder_text="Enter seconds")
        self.timer_entry.pack(pady=10)

        self.timer_display = ctk.CTkLabel(self.timer_tab, text="00:00:00", font=("Consolas", 40))
        self.timer_display.pack(pady=20)

        btn_frame = ctk.CTkFrame(self.timer_tab)
        btn_frame.pack()

        self.timer_start_btn = ctk.CTkButton(btn_frame, text="Start", command=self.start_timer)
        self.timer_start_btn.grid(row=0, column=0, padx=10)

        self.timer_pause_btn = ctk.CTkButton(btn_frame, text="Pause", command=self.pause_timer)
        self.timer_pause_btn.grid(row=0, column=1, padx=10)

        self.timer_reset_btn = ctk.CTkButton(btn_frame, text="Reset", command=self.reset_timer)
        self.timer_reset_btn.grid(row=0, column=2, padx=10)

    def update_timer(self):
        while self.timer_running and self.timer_seconds > 0:
            mins, secs = divmod(self.timer_seconds, 60)
            hrs, mins = divmod(mins, 60)
            self.timer_display.configure(text=f"{hrs:02d}:{mins:02d}:{secs:02d}")
            time.sleep(1)
            self.timer_seconds -= 1
        if self.timer_seconds == 0:
            self.timer_display.configure(text="00:00:00")
            self.timer_running = False

    def start_timer(self):
        if not self.timer_running:
            try:
                self.timer_seconds = int(self.timer_entry.get())
                self.timer_running = True
                threading.Thread(target=self.update_timer, daemon=True).start()
            except ValueError:
                self.timer_display.configure(text="Invalid Input")

    def pause_timer(self):
        self.timer_running = False

    def reset_timer(self):
        self.timer_running = False
        self.timer_seconds = 0
        self.timer_display.configure(text="00:00:00")


if __name__ == "__main__":
    app = ClockApp()
    app.mainloop()
