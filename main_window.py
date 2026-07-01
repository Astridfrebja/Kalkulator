from PySide6.QtWidgets import QMainWindow, QLabel, QPushButton
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

import kalk


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Kalkulator")

        # Holder styr på regnestykket
        self.first_number = ""
        self.second_number = ""
        self.operator = ""

        # Det brukeren ser på skjermen
        self.display_text = ""

        # ------------------------
        # Bakgrunnsbilde
        # ------------------------

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
        # Display
        # ------------------------

        self.display = QLabel("", self)
        self.display.setGeometry(125, 190, 390, 160)
        self.display.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.display.setStyleSheet("""
            QLabel {
                background: transparent;
                color: #3a3a3a;
                font-size: 40px;
                font-weight: bold;
                padding-right: 10px;
            }
        """)

        # ------------------------
        # Knapper
        # ------------------------

        buttons = [
            ("÷", 240, 410),
            ("×", 340, 410),
            ("⌫", 440, 410),

            ("7", 235, 470),
            ("8", 340, 470),
            ("9", 440, 470),

            ("4", 235, 525),
            ("5", 340, 525),
            ("6", 440, 525),

            ("1", 235, 585),
            ("2", 340, 585),
            ("3", 440, 585),

            ("0", 235, 645),
            ("-", 340, 645),
            ("+", 445, 640),

            (".", 240, 700),
            ("=", 325, 700),
        ]

        for text, x, y in buttons:
            if text == "=":
                self.create_button(text, x, y, width=220)
            else:
                self.create_button(text, x, y)

    # --------------------------------------------------

    def create_button(self, text, x, y, width=90, height=70):

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

    # --------------------------------------------------

    def press_button(self, text):

        # ------------------------
        # Regn ut
        # ------------------------

        if text == "=":

            if self.first_number == "" or self.second_number == "":
                return

            a = float(self.first_number)
            b = float(self.second_number)

            try:
                if self.operator == "+":
                    result = kalk.add(a, b)

                elif self.operator == "-":
                    result = kalk.subtract(a, b)

                elif self.operator == "×":
                    result = kalk.multiply(a, b)

                elif self.operator == "÷":
                    result = kalk.divide(a, b)

                else:
                    return

                # Fjern .0 dersom resultatet er heltall
                if result == int(result):
                    result = int(result)

                self.display.setText(str(result))

                # Gjør resultatet klart til neste regnestykke
                self.first_number = str(result)
                self.second_number = ""
                self.operator = ""
                self.display_text = str(result)

            except Exception:
                self.display.setText("Feil")

            return

        # ------------------------
        # Backspace
        # ------------------------

        if text == "⌫":

            if self.operator == "":
                self.first_number = self.first_number[:-1]

            elif self.second_number == "":
                self.operator = ""

            else:
                self.second_number = self.second_number[:-1]

            self.display_text = (
                self.first_number +
                self.operator +
                self.second_number
            )

            self.display.setText(self.display_text)

            return

        # ------------------------
        # Operator
        # ------------------------

        if text in ["+", "-", "×", "÷"]:

            if self.first_number != "":
                self.operator = text

        # ------------------------
        # Tall
        # ------------------------

        else:

            if self.operator == "":
                self.first_number += text
            else:
                self.second_number += text

        self.display_text = (
            self.first_number +
            self.operator +
            self.second_number
        )

        self.display.setText(self.display_text)