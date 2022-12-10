import sys
from application import Application

if __name__ == '__main__':
    def hook(type_, value, traceback):
        print(type_)
        print(traceback)
    sys.__excepthook__ = hook

    app = Application(sys.argv)
    app.start()

    sys.exit(app.exec())