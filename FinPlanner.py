import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import csv
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import traceback
import os

class Operation:
    def __init__(self, amount, category, date, comment, operation_type):
        self.amount = amount
        self.category = category
        self.date = date
        self.comment = comment
        self.operation_type = operation_type

    def to_dict(self):
        return {
            'amount': self.amount,
            'category': self.category,
            'date': self.date,
            'comment': self.comment,
            'operation_type': self.operation_type
        }

class Database:
    def __init__(self):
        self.operations = []
        self.next_id = 1

    def add_operation(self, operation):
        try:
            operation_dict = operation.to_dict()
            operation_dict['id'] = self.next_id
            self.next_id += 1
            self.operations.append(operation_dict)
            return True
        except Exception as e:
            print(f"Ошибка при добавлении операции: {str(e)}")
            return False
    
    def get_all_operations(self):  # Добавляем этот метод
        return self.operations

    def export_to_json(self, filename):
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(self.operations, file, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"Ошибка при экспорте в JSON: {str(e)}")
            return False   

class FinPlannerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Финансовый планировщик")
        self.db = Database()
        self.create_widgets()
        self.figure = plt.Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    def create_widgets(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(main_frame, columns=("ID", "Сумма", "Категория", "Дата", "Тип", "Комментарий"), show="headings")
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.tree.heading("ID", text="ID")
        self.tree.heading("Сумма", text="Сумма")
        self.tree.heading("Категория", text="Категория")
        self.tree.heading("Дата", text="Дата")
        self.tree.heading("Тип", text="Тип")
        self.tree.heading("Комментарий", text="Комментарий")

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        ttk.Button(button_frame, text="Добавить", command=self.add_operation_window).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Редактировать", command=self.edit_operation).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Удалить", command=self.delete_operation).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Экспорт CSV", command=self.export_to_csv).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Экспорт JSON", command=self.export_to_json).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Импорт CSV", command=self.import_from_csv).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Импорт JSON", command=self.import_from_json).pack(side=tk.LEFT, padx=5)

    def add_operation_window(self):
        try:
            add_window = tk.Toplevel(self.root)
            add_window.title("Добавить операцию")
            
            ttk.Label(add_window, text="Сумма:").grid(row=0, column=0, padx=5, pady=5)
            amount_entry = ttk.Entry(add_window)
            amount_entry.grid(row=0, column=1, padx=5, pady=5)
            
            ttk.Label(add_window, text="Категория:").grid(row=1, column=0, padx=5, pady=5)
            category_entry = ttk.Entry(add_window)
            category_entry.grid(row=1, column=1, padx=5, pady=5)
            
            ttk.Label(add_window, text="Дата (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5)
            date_entry = ttk.Entry(add_window)
            date_entry.grid(row=2, column=1, padx=5, pady=5)
            
            ttk.Label(add_window, text="Тип:").grid(row=3, column=0, padx=5, pady=5)
            operation_type = tk.StringVar(value="income")
            ttk.Radiobutton(add_window, text="Доход", variable=operation_type, value="income").grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
            ttk.Radiobutton(add_window, text="Расход", variable=operation_type, value="expense").grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
            
            ttk.Label(add_window, text="Комментарий:").grid(row=5, column=0, padx=5, pady=5)
            comment_entry = ttk.Entry(add_window)
            comment_entry.grid(row=5, column=1, padx=5, pady=5)

            def confirm_add():
                try:
                    amount = float(amount_entry.get())
                    category = category_entry.get().strip()
                    date = date_entry.get()
                    comment = comment_entry.get()
                    
                    if not self.validate_date(date):
                        raise ValueError("Неверный формат даты")
                    
                    if not category:
                        raise ValueError("Категория не может быть пустой")
                    
                    operation = Operation(
                        amount=amount,
                        category=category,
                        date=date,
                        comment=comment,
                        operation_type=operation_type.get()
                    )
                    
                    if self.db.add_operation(operation):
                        self.update_table()
                        self.update_balance()
                        self.plot_charts(self.db.get_all_operations())
                        add_window.destroy()
                except Exception as e:
                    messagebox.showerror("Ошибка", f"Не удалось добавить операцию: {str(e)}")

            ttk.Button(add_window, text="Добавить", command=confirm_add).grid(row=6, column=0, columnspan=2, pady=10)
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть окно добавления: {str(e)}")

    def validate_date(self, date_text):
        try:
            if date_text != datetime.datetime.strptime(date_text, "%Y-%m-%d").strftime('%Y-%m-%d'):
                raise ValueError
            return True
        except ValueError:
            return False

    def update_table(self, operations=None):
        try:
            for row in self.tree.get_children():
                self.tree.delete(row)
                
            if operations is None:
                operations = self.db.get_all_operations()
                
            for op in operations:
                                self.tree.insert("", "end", iid=str(op['id']), values=(
                    op['id'], 
                    op['amount'], 
                    op['category'], 
                    op['date'], 
                    op['operation_type'], 
                    op['comment']
                ))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось обновить таблицу: {str(e)}")

    def plot_charts(self, operations):
        try:
            self.figure.clf()
            ax = self.figure.add_subplot(111)
            
            categories = {}
            for op in operations:
                if op['operation_type'] == 'expense':
                    if op['category'] not in categories:
                        categories[op['category']] = 0
                    categories[op['category']] -= op['amount']
                else:
                    if op['category'] not in categories:
                        categories[op['category']] = 0
                    categories[op['category']] += op['amount']
            
            labels = list(categories.keys())
            values = list(categories.values())
            
            ax.bar(labels, values, color=['green' if v > 0 else 'red' for v in values])
            ax.set_title('Распределение финансов по категориям')
            ax.set_xlabel('Категории')
            ax.set_ylabel('Сумма')
            
            self.canvas.draw()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось построить график: {str(e)}")

    def update_balance(self):
        try:
            operations = self.db.get_all_operations()
            income = sum(op['amount'] for op in operations if op['operation_type'] == 'income')
            expense = sum(op['amount'] for op in operations if op['operation_type'] == 'expense')
            balance = income - expense
            
            self.balance_label = ttk.Label(self.root, text=f"Баланс: {balance}")
            self.balance_label.pack(pady=10)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось обновить баланс: {str(e)}")

    def run(self):
        try:
            self.root.mainloop()
        except Exception as e:
            messagebox.showerror("Критическая ошибка", f"Произошла ошибка: {str(e)}")

    def on_closing(self):
        try:
            if messagebox.askokcancel("Выход", "Хотите выйти из приложения?"):
                try:
                    if self.db.export_to_json("data.json"):
                        messagebox.showinfo("Сохранение", "Данные успешно сохранены")
                    else:
                        raise Exception("Ошибка при сохранении данных")
                except Exception as e:
                    messagebox.showwarning("Предупреждение", f"Не удалось сохранить данные: {str(e)}")
                self.root.destroy()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка при закрытии: {str(e)}")

    def export_to_csv(self):
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV файлы", "*.csv"), ("Все файлы", "*.*")]
            )
            if filename:
                with open(filename, 'w', encoding='utf-8', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=[
                        'id', 'amount', 'category', 'date', 'operation_type', 'comment'
                    ])
                    writer.writeheader()
                    writer.writerows(self.db.get_all_operations())
                messagebox.showinfo("Успех", "Данные успешно экспортированы в CSV")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось экспортировать в CSV: {str(e)}")

    def import_from_csv(self):
        try:
            filename = filedialog.askopenfilename(
                filetypes=[("CSV файлы", "*.csv"), ("Все файлы", "*.*")]
                            )
            if filename:
                with open(filename, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        operation = Operation(
                            amount=float(row['amount']),
                            category=row['category'],
                            date=row['date'],
                            comment=row['comment'],
                            operation_type=row['operation_type']
                        )
                        self.db.add_operation(operation)
                self.update_table()
                self.update_balance()
                self.plot_charts(self.db.get_all_operations())
                messagebox.showinfo("Успех", "Данные успешно импортированы из CSV")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось импортировать из CSV: {str(e)}")

    def export_to_json(self):
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON файлы", "*.json"), ("Все файлы", "*.*")]
            )
            if filename:
                with open(filename, 'w', encoding='utf-8') as file:
                    json.dump(self.db.operations, file, ensure_ascii=False, indent=4)
                messagebox.showinfo("Успех", "Данные успешно экспортированы в JSON")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось экспортировать в JSON: {str(e)}")

    def import_from_json(self):
        try:
            filename = filedialog.askopenfilename(
                filetypes=[("JSON файлы", "*.json"), ("Все файлы", "*.*")]
            )
            if filename:
                with open(filename, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    for op in data:
                        operation = Operation(
                            amount=op['amount'],
                            category=op['category'],
                            date=op['date'],
                            comment=op['comment'],
                            operation_type=op['operation_type']
                        )
                        self.db.add_operation(operation)
                self.update_table()
                self.update_balance()
                self.plot_charts(self.db.get_all_operations())
                messagebox.showinfo("Успех", "Данные успешно импортированы из JSON")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось импортировать из JSON: {str(e)}")

    def edit_operation(self):
        try:
            selected = self.tree.selection()
            if not selected:
                messagebox.showwarning("Предупреждение", "Выберите операцию для редактирования")
                return
            
            item = self.tree.item(selected[0])
            operation_id = item['values'][0]
            operation = next((op for op in self.db.operations if op['id'] == operation_id), None)
            
            if not operation:
                messagebox.showwarning("Предупреждение", "Операция не найдена")
                return
                
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Редактировать операцию")
            
            ttk.Label(edit_window, text="Сумма:").grid(row=0, column=0, padx=5, pady=5)
            amount_entry = ttk.Entry(edit_window)
            amount_entry.insert(0, operation['amount'])
            amount_entry.grid(row=0, column=1, padx=5, pady=5)
            
            ttk.Label(edit_window, text="Категория:").grid(row=1, column=0, padx=5, pady=5)
            category_entry = ttk.Entry(edit_window)
            category_entry.insert(0, operation['category'])
            category_entry.grid(row=1, column=1, padx=5, pady=5)
            
            ttk.Label(edit_window, text="Дата (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5)
            date_entry = ttk.Entry(edit_window)
            date_entry.insert(0, operation['date'])
            date_entry.grid(row=2, column=1, padx=5, pady=5)
            
            ttk.Label(edit_window, text="Тип:").grid(row=3, column=0, padx=5, pady=5)
            operation_type = tk.StringVar(value=operation['operation_type'])
            ttk.Radiobutton(edit_window, text="Доход", variable=operation_type, value="income").grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
            ttk.Radiobutton(edit_window, text="Расход", variable=operation_type, value="expense").grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
            
            ttk.Label(edit_window, text="Комментарий:").grid(row=5, column=0, padx=5, pady=5)
            comment_entry = ttk.Entry(edit_window)
            comment_entry.insert(0, operation['comment'])
            comment_entry.grid(row=5, column=1, padx=5, pady=5)

            def save_changes():
                try:
                    amount = float(amount_entry.get())
                    category = category_entry.get().strip()
                    date = date_entry.get()
                    comment = comment_entry.get()
                    
                    if not self.validate_date(date):
                        raise ValueError("Неверный формат даты")
                    
                    if not category:
                        raise ValueError("Категория не может быть пустой")
                    
                    # Обновляем операцию в базе данных
                    for op in self.db.operations:
                        if op['id'] == operation_id:
                            op['amount'] = amount
                            op['category'] = category
                            op['date'] = date
                            op['comment'] = comment
                            op['operation_type'] = operation_type.get()
                            break
                    
                    self.update_table()
                    self.update_balance()
                    self.plot_charts(self.db.get_all_operations())
                    edit_window.destroy()
                except Exception as e:
                    messagebox.showerror("Ошибка", f"Не удалось сохранить изменения: {str(e)}")

            ttk.Button(edit_window, text="Сохранить", command=save_changes).grid(row=6, column=0, columnspan=2, pady=10)
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть окно редактирования: {str(e)}")

    def delete_operation(self):
        try:
            selected = self.tree.selection()
            if not selected:
                messagebox.showwarning("Предупреждение", "Выберите операцию для удаления")
                return
            
            item = self.tree.item(selected[0])
            operation_id = item['values'][0]
            
            if messagebox.askyesno("Подтверждение", "Действительно удалить операцию?"):
                self.db.operations = [op for op in self.db.operations if op['id'] != operation_id]
                self.update_table()
                self.update_balance()
                self.plot_charts(self.db.get_all_operations())
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить операцию: {str(e)}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    try:
        app = FinPlannerApp()
        app.root.protocol("WM_DELETE_WINDOW", app.on_closing)
        app.run()
    except Exception as e:
        print(f"Критическая ошибка: {str(e)}")
        traceback.print_exc()
