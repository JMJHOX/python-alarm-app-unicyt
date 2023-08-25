import tkinter as tk
from datetime import datetime
import winsound
import threading
from tkinter import messagebox
from tkinter import ttk
import utils


class AlarmThread(threading.Thread):
    def __init__(self, set_alarm_timer, stop_callback):
        super().__init__()
        self.set_alarm_timer = set_alarm_timer
        self.stop_callback = stop_callback
        self.stopped = threading.Event()

    def run(self):
        while not self.stopped.is_set():
            current_time = datetime.now()
            now = current_time.strftime("%H:%M:%S")
            if now == self.set_alarm_timer:
                winsound.PlaySound("sound.wav", winsound.SND_ASYNC)
                self.stop_callback()
                break

    def stop(self):
        self.stopped.set()


class AlarmApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PyAlarms")
        self.root.geometry("400x300")
        self.display_time = tk.StringVar(value="")
        self.hour = tk.StringVar()
        self.minute = tk.StringVar()
        self.second = tk.StringVar()
        self.use_am_pm = tk.BooleanVar()
        self.setup_ui()

        self.update_interval = 1  # Intervalo de actualización en segundos
        self.update_countdown()

        self.alarm_thread = None

    def setup_ui(self):
        ttk.Label(self.root, text="Colocar Hora:",
                  font=("Arial", 10)).place(x=50, y=30)
        self.hour = ttk.Combobox(
            self.root, values=utils.format_time(24), width=5)
        self.minute = ttk.Combobox(
            self.root, values=utils.format_time(60), width=5)
        self.second = ttk.Combobox(
            self.root, values=utils.format_time(60), width=5)
        self.hour.place(x=150, y=30)
        self.minute.place(x=200, y=30)
        self.second.place(x=250, y=30)

        tk.Button(self.root, text="Poner Alarma", fg="red", width=10,
                  command=self.button_put_alarm).place(x=110, y=70)
        tk.Label(self.root, text="Hora Formato",
                 font=("Arial", 10)).place(x=50, y=150)
        tk.Label(self.root, textvariable=self.display_time,
                 font=("Arial", 10)).place(x=180, y=150)

        self.stop_button = tk.Button(self.root, text="Detener Alarma", fg="blue", width=15,
                                     command=self.stop_alarm, state=tk.DISABLED)
        self.stop_button.place(x=150, y=220)

        self.check_button = ttk.Checkbutton(self.root, text="FORMATO 12 HORAS", variable=self.use_am_pm,
                                            command=self.update_display_time, state=tk.DISABLED)
        self.check_button.place(x=150, y=120)

        self.countdown_label = tk.Label(self.root, text="", font=("Arial", 9))
        self.countdown_label.place(x=50, y=260, width=300)

        self.reset_button = tk.Button(self.root, text="Reiniciar Alarma", fg="green", width=15,
                                      command=self.reset_alarm, state=tk.DISABLED)
        self.reset_button.place(x=280, y=220)

    def get_alarm_time(self):
        return f"{self.hour.get()}:{self.minute.get()}:{self.second.get()}"

    def start_countdown(self):
        set_alarm_timer = self.get_alarm_time()
        alarm_time = datetime.strptime(
            set_alarm_timer, "%H:%M:%S").strftime("%I:%M %p")

        self.countdown_label.config(
            text=f"Alarma a las {alarm_time}, faltan ...")

    def reset_alarm(self):
        self.countdown_label.config(text="")
        # self.stop_alarm()
        self.stop_button.config(state=tk.DISABLED)
        self.check_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.DISABLED)
        self.hour.set("")
        self.minute.set("")
        self.second.set("")

    def update_countdown(self):
        set_alarm_timer = self.get_alarm_time()

        try:
            alarm_time = datetime.strptime(
                set_alarm_timer, "%H:%M:%S").strftime("%I:%M %p")

            current_time = datetime.now()
            now = current_time.strftime("%H:%M:%S")

            if now == set_alarm_timer:
                remaining_time = "¡Es hora de la alarma!"
                messagebox.showinfo("Alarma en curso",
                                    "HORA DE DESPERTAR")
            else:
                remaining_time = utils.get_time_difference(
                    set_alarm_timer, now)

            countdown_text = f"Alarma: {alarm_time} - Tiempo restante: {remaining_time}"
        except ValueError:
            countdown_text = "No hay alarma"

        self.countdown_label.config(text=countdown_text)

        self.root.after(int(self.update_interval * 1000),
                        self.update_countdown)

    def update_display_time(self):
        hour = self.hour.get()
        minute = self.minute.get()
        second = self.second.get()
        use_am_pm = self.use_am_pm.get()
        formatted_time = utils.format_time_with_am_pm(
            hour, minute, second, use_am_pm)

        self.display_time.set(formatted_time)

    def stop_alarm(self):
        if self.alarm_thread and self.alarm_thread.is_alive():
            self.alarm_thread.stop()
            winsound.PlaySound(None, winsound.SND_PURGE)
            messagebox.showinfo("Alarma detenida",
                                "La alarma ha sido detenida")

            self.reset_alarm()

    def replace_alarm(self):
        self.alarm_thread.stop()
        self.alarm_thread.join()
        winsound.PlaySound(None, winsound.SND_PURGE)
        messagebox.showinfo("Alarma Reemplazada",
                            "La alarma ha sido reemplazada")

    def button_put_alarm(self):
        set_alarm_timer = self.get_alarm_time()
        hour = self.hour.get()
        minute = self.minute.get()
        second = self.second.get()
        check_alarm_is_updated = False

        if hour and minute and second:
            self.check_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.NORMAL)
            self.reset_button.config(state=tk.NORMAL)

            if self.alarm_thread and self.alarm_thread.is_alive():
                self.replace_alarm()
                check_alarm_is_updated = True

            self.alarm_thread = AlarmThread(set_alarm_timer, self.stop_alarm)
            self.alarm_thread.daemon = True
            self.alarm_thread.start()

            if not check_alarm_is_updated:
                messagebox.showinfo("Alarma en curso",
                                    "La alarma ha sido activada")


if __name__ == '__main__':
    root = tk.Tk()
    app = AlarmApp(root)
    root.mainloop()
