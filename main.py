  #main.py - точка входа в приложение

from gui import FinPlannerApp

if __name__ == "__main__":
    try:
        app = FinPlannerApp()
        app.root.protocol("WM_DELETE_WINDOW", app.on_closing)
        app.run()
    except Exception as e:
        print(f"Критическая ошибка: {str(e)}")
        traceback.print_exc()
