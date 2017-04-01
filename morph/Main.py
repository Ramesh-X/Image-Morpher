from PyQt5.QtWidgets import QApplication
import morph.view.gui_window as ui
import sys

_excepthook = sys.excepthook


def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    _excepthook(exctype, value, traceback)
    sys.exit(1)

# Set the exception hook to our wrapping function
sys.excepthook = my_exception_hook

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ui.MainWindow()
    ex.show()
    sys.exit(app.exec_())
