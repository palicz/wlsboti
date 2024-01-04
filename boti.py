##############################
#            v5.0            #
#   BOTi Automata Közmunka   #
#                            #
#    zenzty        (c) 2023  #
##############################

__author__ = "zenzty"
__copyright__ = "Copyright (C) 2023, zenzty"
__license__ = "The MIT License (MIT)"
__version__ = "5.0"
__maintainer__ = "zenzty"
__email__ = " - "
__status__ = "Public Beta"

import tkinter as tk
from tkinter import ttk
from PIL import ImageGrab, ImageTk, Image
import threading
import numpy as np
import cv2
import time
from datetime import date
from modules.directkeypress import PressKey, ReleaseKey, W, A, S, D, E
import win32api, win32con
import sys
import urllib.request
import os
import webbrowser

class ConsoleRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)


def create_directory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"'{directory_path}' sikeresen létrehozva.")
    else:
        print(f"'{directory_path}' már létezik.")


directory = "./boti_data"

create_directory(directory)


def straight():
    PressKey(W)


def use():
    PressKey(E)
    ReleaseKey(W)
    ReleaseKey(A)
    ReleaseKey(D)


def left():
    PressKey(A)
    ReleaseKey(W)
    ReleaseKey(D)
    ReleaseKey(E)


def right():
    PressKey(D)
    ReleaseKey(W)
    ReleaseKey(A)
    ReleaseKey(E)


def stop():
    ReleaseKey(W)
    ReleaseKey(A)
    ReleaseKey(D)
    ReleaseKey(E)


def defineOnScreen():
    if x < screen.shape[1] / 2:
        print("bal")
        straight()
        left()
    else:
        print("jobb")
        straight()
        right()

is_running = False
result = None
category_frame = None

def start():
    def countdown():
        global is_running
        for i in range(4, 0, -1):
            countdown_label.config(text=str(i))
            time.sleep(1)
        if (
            is_running
        ):
            countdown_label.config(text="A program fut...")
            t = threading.Thread(target=run_application)
            t.start()
        else:
            countdown_label.config(
                text="A program NEM fut..."
            )

    global is_running
    if start_button["text"] == "Start":
        start_button["text"] = "Stop"
        is_running = True
        threading.Thread(target=countdown).start()
    else:
        start_button["text"] = "Start"
        is_running = False
        countdown_label.config(text="A program NEM fut...")

def exit_application(event=None):
    root.quit()

def run_application():
    global screen, x
    last_time = time.time()
    while start_button["text"] == "Stop":
        screen = np.array(ImageGrab.grab(bbox=(0, 40, 800, 625)))
        new_screen, x = processed_img(screen)
        console_output.insert(
            tk.END, "A generálás {} ideig tartott\n".format(time.time() - last_time)
        )
        last_time = time.time()
        if new_screen is not None and x is not None:
            defineOnScreen()
            straight()
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            exit_application()


def processed_img(original_image):
    processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)
    lower_red = np.array([120, 200, 200])
    upper_red = np.array([120, 255, 255])
    mask = cv2.inRange(processed_img, lower_red, upper_red)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        max_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(max_contour)
        mask = np.zeros_like(mask)
        cv2.drawContours(mask, [max_contour], 0, (255), thickness=cv2.FILLED)
        return mask, x
    else:
        use()
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, -50, 0, 0)
        time.sleep(0.01)
        stop()
        return None, None


root = tk.Tk()
root.title("BOTi automata közmunka")
root.geometry("400x440")
root.resizable(False, False)

style = ttk.Style()
style.configure("Bold.TButton", font=("TkDefaultFont", 12, "bold"))

image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/No_broom_icon.svg/300px-No_broom_icon.svg.png"
urllib.request.urlretrieve(image_url, "./boti_data/nobroom.png")
icon_image = ImageTk.PhotoImage(Image.open("./boti_data/nobroom.png").resize((64, 64)))
root.iconphoto(True, icon_image)
icon_label = ttk.Label(root, image=icon_image)
icon_label.pack(pady=(20, 10))

style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=10)
style.configure("TLabel", font=("Arial", 12), padding=5)

start_button = ttk.Button(
    root, text="Start", command=start, state=tk.NORMAL, style="Bold.TButton"
)
start_button.pack(pady=10)

countdown_label = ttk.Label(root, text="", font=("Arial", 20))
countdown_label.pack(pady=5)

app_status_label = ttk.Label(root, text="", font=("Arial", 16))
app_status_label.pack(pady=5)

def show_category(window, category):
    global category_frame

    if category_frame is not None:
        category_frame.destroy()

    category_frame = tk.Frame(window, width=200, height=200, bg="#f0f0f0")
    category_frame.grid(row=0, column=1, sticky="nsew")

    if category == "Fejlesztés":
        updates = {
            "1.5.0": [
                "Kód optimalizálás",
                "Licensze rendszer eltávolítása",
            ],
            "1.4.2": ["Kisebb hibajavítások"],
            "1.4.1": [
                "Beállítások felület létrehozása",
                "FiveM crash javítva",
                "Teljes UTF-8 támogatás hozzáadva",
            ],
            "1.3.4": ["Bug javítások", "'Használati napló' funkció eltávolítva"],
            "1.3.0": [
                "Beállítások implementálása",
                "Felhasználói felület optimalizálása",
            ],
            "1.2.1": [
                "Konzol hozzáadása a felhasználói felülethez",
                "Kód optimalizálás",
                "Néhány lehetséges memóriaszivárgás javítva",
            ],
            "1.2.0": [
                "Licensz-rendszer implementálása",
                "Backend support",
                "Naplózó működésének javítása",
            ],
            "1.1.2": [
                "Továbbfejlesztett felhasználói felület hozzáadva",
                "Kisebb bug javítások",
            ],
            "1.1.0": [
                "Felhasználói felület hozzáadva",
                "Teljesítmény javítása, észlelés pontosítás",
                "'Használati napló' funkció hozzáadva",
            ],
            "1.0.1": [
                "Hibás képernyő-olvasás javítása",
                "Karaktermozgás implementálása",
                "Különféle hibajavítások",
            ],
            "1.0.0": [
                "Alapvető működési mechanizmus bekalibrálva",
                "Prototípus algoritmus minimalizálása",
            ],
        }

        notes_frame = tk.Frame(category_frame, bg="white")
        notes_frame.pack(pady=20)

        scrollbar = ttk.Scrollbar(notes_frame, orient="vertical")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas = tk.Canvas(notes_frame, bg="white", yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        canvas.bind_all(
            "<MouseWheel>", lambda event: on_mousewheel(event, canvas)
        )

        scrollbar.config(command=canvas.yview)

        update_notes_frame = tk.Frame(canvas, bg="white")
        canvas.create_window((0, 0), window=update_notes_frame, anchor=tk.NW)

        for version, update_list in updates.items():
            version_label = tk.Label(
                update_notes_frame,
                text=version,
                font=("Arial", 14, "bold"),
                bg="white",
                fg="#333333",
                anchor="w",
            )
            version_label.pack(pady=(5, 2), padx=10, anchor="w")

            for item in update_list:
                update_bullet = tk.Label(
                    update_notes_frame,
                    text="• " + item,
                    anchor="w",
                    justify=tk.LEFT,
                    bg="white",
                    fg="#333333",
                )
                update_bullet.pack(anchor="w")

        update_notes_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox(tk.ALL))

    elif category == "Használat":
        usage_box = ttk.Frame(category_frame, style="Usage.TFrame")
        usage_box.pack(fill="both", padx=10, pady=10)

        text_label = ttk.Label(
            usage_box,
            text="- Indítsd el a FiveM-et és lépj fel a WLS szerverre.\n\n- Menj a beállításokba, és állítsd át a felbontást 800x600-ra, illetve ablakos módra.\n\n- Húzd a FiveM ablakot a monitorod BAL-FELSŐ sarkába. Válts belső nézetre, hogy a karaktered ne látszódjon.\n\n- Kattints a 'Start' gombra, majd van 4 másodperced, hogy visszakattints a játékba.",
            wraplength=300,
            justify="left",
            style="UsageMessage.TLabel",
        )
        text_label.grid(
            row=0,
            column=1,
            sticky="w",
            padx=(5, 0),
            pady=5,
        )

        style.configure(
            "Usage.TFrame",
            background="white",
            borderwidth=2,
            relief="groove",
            padding=(20, 10, 10, 10),
        )

        style.configure("UsageMessage.TLabel", background="white", foreground="#333333")
    elif category == "Info":
        warning_box = ttk.Frame(category_frame, style="Warning.TFrame")
        warning_box.pack(fill="both", padx=10, pady=10)

        exclamation_label = ttk.Label(
            warning_box,
            text="!",
            font=("Arial", 60),
            foreground="red",
            style="Exclamation.TLabel",
        )
        exclamation_label.grid(row=0, column=0, sticky="w", padx=(25, 50), pady=10)

        text_label = ttk.Label(
            warning_box,
            text="Az esetleges szankciókért \naz alkalmazás készítője.\nNEM vállal felelősséget!",
            wraplength=300,
            justify="left",
            style="Message.TLabel",
        )
        text_label.grid(row=0, column=1, sticky="w")

        style.configure(
            "Warning.TFrame",
            background="white",
            borderwidth=2,
            relief="groove",
            padding=(20, 10, 10, 10),
        )

        style.configure("Exclamation.TLabel", background="white", foreground="red")

        style.configure(
            "Message.TLabel",
            background="white",
            foreground="red",
            font=("TkDefaultFont", 12, "bold"),
        )

        info_box = ttk.Frame(category_frame, style="InfoBox.TFrame")
        info_box.pack(fill="both", padx=10, pady=10)

        exclamation_label = ttk.Label(
            info_box,
            text="?",
            font=("Arial", 60),
            foreground="#333333",
            style="QuestionMark.TLabel",
        )
        exclamation_label.grid(row=0, column=0, sticky="w", padx=(25, 50), pady=10)

        def open_github_link(event):
            webbrowser.open(
                "https://github.com/palicz/wlsboti"
            )

        text_widget = tk.Text(
            info_box, width=25, height=3, wrap="word", bd=0, highlightthickness=0
        )
        text_widget.tag_configure(
            "blue", foreground="blue", font=("TkDefaultFont", 12, "bold")
        )
        text_widget.tag_configure("gray", font=("TkDefaultFont", 12, "bold"))
        text_widget.insert(tk.END, "Bármi kérdésed van\njelezd ", "gray")
        text_widget.insert(tk.END, "githubon", "blue")
        text_widget.tag_bind("blue", "<Button-1>", open_github_link)
        text_widget.tag_bind(
            "blue", "<Enter>", lambda event: text_widget.configure(cursor="hand2")
        )
        text_widget.tag_bind(
            "blue", "<Leave>", lambda event: text_widget.configure(cursor="")
        )
        text_widget.configure(state="disabled")
        text_widget.grid(row=0, column=1, sticky="w")

        style.configure(
            "InfoBox.TFrame",
            background="white",
            borderwidth=2,
            relief="groove",
            padding=(20, 10, 10, 10),
        )

        style.configure(
            "InfoMessage.TLabel",
            background="white",
            foreground="#333333",
            font=("TkDefaultFont", 12, "bold"),
        )

        style.configure("QuestionMark.TLabel", background="white", foreground="red")


def on_mousewheel(event, canvas):
    try:
        canvas.yview_scroll(-int(event.delta / 120), "units")
    except tk.TclError:
        pass


def show_settings_window():
    global category_frame

    settings_window = tk.Toplevel()
    settings_window.title("Beállítások")
    settings_window.geometry("600x300")
    settings_window.resizable(False, False)

    categories_frame = tk.Frame(settings_window)
    categories_frame.grid(row=0, column=0, sticky="ns")

    categories = ["Használat", "Fejlesztés", "Info"]
    for idx, category in enumerate(categories):
        button = ttk.Button(
            categories_frame,
            text=category,
            style="Bold.TButton",
            width=20,
            command=lambda cat=category: show_category(settings_window, cat),
        )
        button.grid(row=idx, column=0, padx=10, pady=10)

    category_frame = tk.Frame(settings_window, width=200, height=200, bg="#f0f0f0")
    category_frame.grid(row=0, column=1, sticky="nsew")

    warning_box = ttk.Frame(category_frame, style="Warning.TFrame")
    warning_box.pack(fill="both", padx=10, pady=10)

    exclamation_label = ttk.Label(
        warning_box,
        text="!",
        font=("Arial", 60),
        foreground="red",
        style="Exclamation.TLabel",
    )
    exclamation_label.grid(row=0, column=0, sticky="w", padx=(25, 50), pady=10)

    text_label = ttk.Label(
        warning_box,
        text="Az esetleges szankciókért \naz alkalmazás készítője.\nNEM vállal felelősséget!",
        wraplength=300,
        justify="left",
        style="Message.TLabel",
    )
    text_label.grid(row=0, column=1, sticky="w")

    style.configure(
        "Warning.TFrame",
        background="white",
        borderwidth=2,
        relief="groove",
        padding=(20, 10, 10, 10),
    )

    style.configure("Exclamation.TLabel", background="white", foreground="red")

    style.configure(
        "Message.TLabel",
        background="white",
        foreground="red",
        font=("TkDefaultFont", 12, "bold"),
    )

    info_box = ttk.Frame(category_frame, style="InfoBox.TFrame")
    info_box.pack(fill="both", padx=10, pady=10)

    exclamation_label = ttk.Label(
        info_box,
        text="?",
        font=("Arial", 60),
        foreground="#333333",
        style="QuestionMark.TLabel",
    )
    exclamation_label.grid(row=0, column=0, sticky="w", padx=(25, 50), pady=10)

    def open_github_link(event):
        webbrowser.open("https://github.com/palicz/wlsboti")

    text_widget = tk.Text(
        info_box, width=25, height=3, wrap="word", bd=0, highlightthickness=0
    )
    text_widget.tag_configure(
        "blue", foreground="blue", font=("TkDefaultFont", 12, "bold")
    )
    text_widget.tag_configure("gray", font=("TkDefaultFont", 12, "bold"))
    text_widget.insert(tk.END, "Bármi kérdésed van\njelezd ", "gray")
    text_widget.insert(tk.END, "githubon", "blue")
    text_widget.tag_bind("blue", "<Button-1>", open_github_link)
    text_widget.tag_bind(
        "blue", "<Enter>", lambda event: text_widget.configure(cursor="hand2")
    )
    text_widget.tag_bind(
        "blue", "<Leave>", lambda event: text_widget.configure(cursor="")
    )
    text_widget.configure(state="disabled")
    text_widget.grid(row=0, column=1, sticky="w")

    style.configure(
        "InfoBox.TFrame",
        background="white",
        borderwidth=2,
        relief="groove",
        padding=(20, 10, 10, 10),
    )

    style.configure(
        "InfoMessage.TLabel",
        background="white",
        foreground="#333333",
        font=("TkDefaultFont", 12, "bold"),
    )

    style.configure("QuestionMark.TLabel", background="white", foreground="red")

    settings_window.grid_rowconfigure(0, weight=1)
    settings_window.grid_columnconfigure(1, weight=1)

    settings_window.mainloop()


footer_frame = ttk.Frame(root)
footer_frame.pack(side="bottom", fill="x")

settings_label = ttk.Label(
    footer_frame, text="Beállítások", foreground="blue", cursor="hand2"
)
settings_label.pack(side="right", padx=10)
settings_label.bind(
    "<Button-1>", lambda e: show_settings_window()
)

console_output = tk.Text(root, height=10)
console_output.pack(pady=10)

sys.stdout = ConsoleRedirector(console_output)

root.mainloop()
