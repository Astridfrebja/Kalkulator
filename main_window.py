from PySide6.QtWidgets import QMainWindow, QLabel, QPushButton
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Kalkulator")

        # Holder på det brukeren skriver
        self.expression = ""

        # Bakgrunnsbilde
        self.background = QLabel(self)

        pixmap = QPixmap("assets/bilder/kalkulator.png")

        if pixmap.isNull():
            print("Fant ikke bildet!")
            return

        pixmap = pixmap.scaled(
            800,
            1100,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        self.background.setPixmap(pixmap)
        self.background.setGeometry(0, 0, pixmap.width(), pixmap.height())

        self.resize(pixmap.width(), pixmap.height())

        # ------------------------
        # Knapper
        # ------------------------

        buttons = [
            # Øverste rad
            ("÷", 240, 410),
            ("×", 340, 410),
            ("⌫", 440, 410),

            # Rad 2
            ("7", 240, 470),
            ("8", 340, 470),
            ("9", 440, 470),

            # Rad 3
            ("4", 240, 520),
            ("5", 340, 520),
            ("6", 440, 520),

            # Rad 4
            ("1", 240, 580),
            ("2", 340, 580),
            ("3", 440, 580),

            # Rad 5
            ("0", 240, 640),
            ("-", 340, 640),
            ("+", 440, 640),

            # Nederste rad
            (".", 240, 700),
            ("=", 325, 700),
        ]

        for text, x, y in buttons:
            if text == "=":
                self.create_button(text, x, y, width=220)
            else:
                self.create_button(text, x, y)

    def create_button(self, text, x, y, width=90, height=70):
        """Oppretter en knapp."""

        button = QPushButton(text, self)
        button.setGeometry(x, y, width, height)

        button.setStyleSheet("""
        QPushButton {
            background: transparent;
            border: none;
            color: #d64b7f;
            font-size: 28px;
            font-weight: bold;
        }

        QPushButton:hover {
            color: #e85c92;
        }

        QPushButton:pressed {
            color: #b93f6c;
        }
    """)

        button.clicked.connect(lambda: self.press_button(text))

        def press_button(self, text):
            """Kalles når en knapp trykkes."""

            if text == "=":
                print("Regn ut:", self.expression)

                # Her skal vi senere koble til kalk.py
                self.expression = ""

            elif text == "⌫":
                self.expression = self.expression[:-1]
                print(self.expression)

            else:
                self.expression += text
                print(self.expression)