#utils.py - вспомогательные функции

import datetime

def validate_date(date_text):
    try:
        if date_text != datetime.datetime.strptime(date_text, "%Y-%m-%d").strftime('%Y-%m-%d'):
            raise ValueError
        return True
    except ValueError:
        return False

def show_error(message):
    messagebox.showerror("Ошибка", message)

def show_warning(message):
    messagebox.showwarning("Предупреждение", message)

def show_info(message):
    messagebox.showinfo("Информация", message)
