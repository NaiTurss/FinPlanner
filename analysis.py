#analysis.py - анализ данных и графики

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Analysis:
    def plot_charts(self, operations, figure):
        figure.clf()
        ax = figure.add_subplot(111)
        
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
        
        return figure
