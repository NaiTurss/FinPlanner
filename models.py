#models.py - описание структуры данных

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
