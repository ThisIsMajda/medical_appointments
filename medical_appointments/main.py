from app.database.db import init_db
from app.gui.app_tk import TkApp

def main():
    init_db()
    app = TkApp()
    app.mainloop()

if __name__ == "__main__":
    main()