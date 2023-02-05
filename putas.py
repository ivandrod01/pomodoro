import time
from tkinter import *
import math
import pygame
import threading
import tkinter.ttk as ttk

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None
pygame.init()
pygame.mixer.init()
pause = False
restart = False
time_val = None


# ---------------------------- TIMER RESET/PAUSE ------------------------------- #
def pause_timer():
    global pause
    pause = not pause


def restart_timer():
    global restart
    restart = not restart


def reset_timer():
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Timer")
    check_marks.config(text="")
    global reps
    reps = 0


# ---------------------------- TIMER MECHANISM ------------------------------- #
def play_sound(wav_sound):
    sound = pygame.mixer.Sound(wav_sound)
    sound.play()

    while pygame.mixer.get_busy():
        pygame.time.delay(100)


def start_timer():
    global reps, time_val

    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        time_val = long_break_sec
        count_down(time_val)
        title_label.config(text="Break", fg=RED)
        threading.Thread(target=play_sound, args=("20min_break.wav",)).start()
    elif reps % 2 == 0:
        time_val = short_break_sec
        count_down(time_val)
        title_label.config(text="Break", fg=PINK)
        threading.Thread(target=play_sound, args=("5min_break.wav",)).start()
    else:
        time_val = work_sec
        threading.Thread(target=play_sound, args=("work.wav",)).start()
        threading.Thread(target=count_down, args=(time_val,)).start()
        title_label.config(text="Work", fg=GREEN)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    global restart
    print(count)
    while pause:
        window.update()
        time.sleep(0.1)

    if restart:
        count = time_val
        restart = False
    window.update()
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")

    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        marks = ""
        work_sessions = math.floor(reps / 2)
        for _ in range(work_sessions):
            marks += "✔"
        check_marks.config(text=marks)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

title_label = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 50))
title_label.grid(column=1, row=0)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

style = ttk.Style()
style.configure('My.TButton', foreground='black', font=('Calibri', 12, 'bold'))

start_button = ttk.Button(text="Start", command=start_timer, style='aqua.TButton')
start_button.grid(column=0, row=2)

reset_button = ttk.Button(text="Reset", command=reset_timer, style='aqua.TButton')
reset_button.grid(column=2, row=2)

pause_button = ttk.Button(text="Pause", command=pause_timer, style='aqua.TButton')
pause_button.grid(column=1, row=4)

restart_button = ttk.Button(text="Restart", command=restart_timer, style='aqua.TButton')
restart_button.grid(column=1, row=5)

check_marks = Label(fg=GREEN, bg=YELLOW)
check_marks.grid(column=1, row=3)

window.mainloop()
