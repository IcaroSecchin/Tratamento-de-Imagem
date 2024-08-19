import sys
import Janelas
from PyQt6.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Janelas.Janela_Principal()
    sys.exit(app.exec())