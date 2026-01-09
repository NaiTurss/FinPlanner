#storage.py - работа с данными

import json
import csv
import os

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

    def get_all_operations(self):
        return self.operations

    def export_to_json(self, filename):
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(self.operations, file, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"Ошибка при экспорте в JSON: {str(e)}")
            return False

    def export_to_csv(self, filename):
        try:
            with open(filename, 'w', encoding='utf-8', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=[
                    'id', 'amount', 'category', 'date', 'operation_type', 'comment'
                ])
                writer.writeheader()
                writer.writerows(self.operations)
            return True
        except Exception as e:
            print(f"Ошибка при экспорте в CSV: {str(e)}")
            return False

    def import_from_csv(self, filename):
        try:
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
                    self.add_operation(operation)
            return True
        except Exception as e:
            print(f"Ошибка при импорте из CSV: {str(e)}")
            return False

    def import_from_json(self, filename):
        try:
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
                    self.add_operation(operation)
            return True
        except Exception as e:
            print(f"Ошибка при импорте из JSON: {str(e)}")
            return False
