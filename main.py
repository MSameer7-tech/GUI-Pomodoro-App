import os
from tkinter import *

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

# ---------------------------- GLOBAL STATE ---------------------------- #
reps = 0
timer = None
is_paused = False
remaining_seconds = 0


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    """Stops any running timer and resets the app back to its initial state."""
    global timer, reps, is_paused, remaining_seconds

    # Cancel any active countdown tick
    if timer is not None:
        window.after_cancel(timer)
        timer = None

    # Reset tracking variables
    reps = 0
    is_paused = False
    remaining_seconds = 0

    # Reset UI elements
    canvas.itemconfig(timer_text, text="00:00")
    timer_label.config(text="Timer", fg=GREEN)
    checkmark.config(text="")
    start_button.config(text="Start")


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    """Handles starting, pausing, and resuming the Pomodoro timer."""
    global reps, timer, is_paused, remaining_seconds

    # 1. If paused, resume the countdown from where it was paused
    if is_paused:
        is_paused = False
        start_button.config(text="Pause")
        count_down(remaining_seconds)
        return

    # 2. If timer is actively running, pause it (prevents multiple timers!)
    if timer is not None:
        window.after_cancel(timer)
        timer = None
        is_paused = True
        start_button.config(text="Resume")
        return

    # 3. Otherwise, start a new session
    start_button.config(text="Pause")
    if reps == 0:
        checkmark.config(text="")

    reps += 1
    work_sec = int(WORK_MIN * 60)
    short_break_sec = int(SHORT_BREAK_MIN * 60)
    long_break_sec = int(LONG_BREAK_MIN * 60)

    # Every 8th rep is a Long Break (after 4 work sessions)
    if reps % 8 == 0:
        count_down(long_break_sec)
        timer_label.config(text="Break", fg=RED)
    # Even reps are Short Breaks
    elif reps % 2 == 0:
        count_down(short_break_sec)
        timer_label.config(text="Break", fg=PINK)
    # Odd reps are Work sessions
    else:
        count_down(work_sec)
        timer_label.config(text="Work", fg=GREEN)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    """Updates the countdown every second and transitions between sessions."""
    global timer, reps, remaining_seconds
    count = int(count)
    remaining_seconds = count

    count_min = count // 60
    count_sec = count % 60
    # Format to 2 digits with leading zero (e.g. 5 becomes "05")
    canvas.itemconfig(timer_text, text=f"{count_min:02d}:{count_sec:02d}")

    if count > 0:
        timer = window.after(1000, count_down, count - 1)
    else:
        timer = None

        # Play system chime and bring window to front to notify the user
        window.bell()
        window.attributes("-topmost", True)
        window.attributes("-topmost", False)

        # If a long break just finished, the full 4-pomodoro cycle is complete!
        if reps % 8 == 0:
            timer_label.config(text="Done!", fg=GREEN)
            canvas.itemconfig(timer_text, text="00:00")
            start_button.config(text="Start")
            reps = 0
            return

        # Start the next session automatically
        start_timer()

        # Update checkmarks for completed work sessions (max 4 per cycle)
        work_sessions = int((reps % 8) / 2)
        if reps % 8 == 0 and reps > 0:
            work_sessions = 4
        checkmark.config(text="✔" * work_sessions)


# ---------------------------- WINDOW CLEANUP ------------------------------- #
def on_closing():
    """Cancels active timer before closing window to avoid background errors."""
    global timer
    if timer is not None:
        window.after_cancel(timer)
    window.destroy()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(pady=50, padx=100, bg=YELLOW)
window.protocol("WM_DELETE_WINDOW", on_closing)

# Tomato Canvas
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
# Use script directory so tomato.png is found regardless of where python is run
base_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(base_dir, "tomato.png")
tomato_img = PhotoImage(file=image_path)
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(row=1, column=1)

# Timer Label
timer_label = Label(text="Timer", font=(FONT_NAME, 50, "normal"), fg=GREEN, bg=YELLOW)
timer_label.grid(row=0, column=1)

# Start / Pause / Resume Button
start_button = Button(text="Start", highlightthickness=0, borderwidth=0, command=start_timer)
start_button.grid(row=2, column=0)

# Reset Button
reset_button = Button(text="Reset", highlightthickness=0, borderwidth=0, command=reset_timer)
reset_button.grid(row=2, column=2)

# Checkmark Label
checkmark = Label(font=(FONT_NAME, 25), bg=YELLOW, fg=GREEN)
checkmark.grid(row=3, column=1)

if __name__ == "__main__":
    window.mainloop()