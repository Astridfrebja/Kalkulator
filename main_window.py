from PySide6.QtWidgets import QMainWindow, QLabel, QPushButton
from PySide6.QtGui import QPixmap, QFont, QFontMetrics
from PySide6.QtCore import Qt

import kalk
import os
import sys


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

        # --------------------------------------------------
        # Bakgrunnsbilde
        # --------------------------------------------------

        self.background = QLabel(self)

        if getattr(sys, "frozen", False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))

        image_path = os.path.join(
            base_path,
            "assets",
            "bilder",
            "kalkulator.png"
        )

        pixmap = QPixmap(image_path)

        if pixmap.isNull():
            print("Fant ikke bildet!")
            return

        # Størrelsen på hele kalkulatoren
        pixmap = pixmap.scaled(
            500,
            700,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        self.background.setPixmap(pixmap)

        self.background.setGeometry(
            0,
            0,
            pixmap.width(),
            pixmap.height()
        )

        self.resize(
            pixmap.width(),
            pixmap.height()
        )

        # --------------------------------------------------
        # Display
        # --------------------------------------------------

        self.display = QLabel("", self)

        # Passer til det grå displayet i bildet
        self.display.setGeometry(
            135,
            70,
            245,
            160
        )

        self.display.setAlignment(
            Qt.AlignRight | Qt.AlignVCenter
        )

        self.display.setContentsMargins(
            0,
            0,
            10,
            0
        )

        self.display.setStyleSheet("""
            QLabel {
                background: transparent;
                color: #3a3a3a;
                font-weight: bold;
            }
        """)

        # --------------------------------------------------
        # Knapper
        # --------------------------------------------------

        buttons = [

            # Første rad
            ("÷", 101, 257),
            ("×", 206, 257),
            ("⌫", 314, 257),

            # Andre rad
            ("7", 101, 312),
            ("8", 206, 312),
            ("9", 314, 312),

            # Tredje rad
            ("4", 101, 368),
            ("5", 206, 368),
            ("6", 314, 368),

            # Fjerde rad
            ("1", 101, 423),
            ("2", 206, 423),
            ("3", 314, 423),

            # Femte rad
            ("0", 101, 479),
            ("-", 206, 479),
            ("+", 314, 479),

            # Nederste rad
            (".", 101, 532),
            ("=", 210, 539),
        ]

        for text, x, y in buttons:

            if text == "=":

                self.create_button(
                    text,
                    x,
                    y,
                    width=190,
                    height=50
                )

            else:

                self.create_button(
                    text,
                    x,
                    y,
                    width=80,
                    height=50
                )

    # --------------------------------------------------
    # Oppdater display og tilpass skriftstørrelse
    # --------------------------------------------------

    def update_display(self, text):

        max_width = self.display.width() - 20

        # Starter ganske stor
        font_size = 40

        while font_size > 10:

            font = QFont("Arial")
            font.setPixelSize(font_size)
            font.setBold(True)

            metrics = QFontMetrics(font)

            if metrics.horizontalAdvance(text) <= max_width:
                break

            font_size -= 1

        self.display.setFont(font)
        self.display.setText(text)

    # --------------------------------------------------
    # Lag knapp
    # --------------------------------------------------

    def create_button(
        self,
        text,
        x,
        y,
        width=80,
        height=50
    ):

        button = QPushButton(text, self)

        button.setGeometry(
            x,
            y,
            width,
            height
        )

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

        button.clicked.connect(
            lambda: self.press_button(text)
        )

    # --------------------------------------------------
    # Når en knapp trykkes
    # --------------------------------------------------

    def press_button(self, text):

        # --------------------------------------------------
        # Regn ut
        # --------------------------------------------------

        if text == "=":

            if (
                self.first_number == ""
                or self.second_number == ""
            ):
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
                else:
                    result = round(result, 2)

                self.update_display(str(result))

                # Gjør resultatet klart til neste regnestykke
                self.first_number = str(result)
                self.second_number = ""
                self.operator = ""
                self.display_text = str(result)

            except Exception:

                self.update_display("Feil")

            return

        # --------------------------------------------------
        # Backspace
        # --------------------------------------------------

        if text == "⌫":

            if self.operator == "":
                self.first_number = self.first_number[:-1]

            elif self.second_number == "":
                self.operator = ""

            else:
                self.second_number = self.second_number[:-1]

            self.display_text = (
                self.first_number
                + self.operator
                + self.second_number
            )

            self.update_display(self.display_text)

            return

        # --------------------------------------------------
        # Operator
        # --------------------------------------------------

        if text in ["+", "-", "×", "÷"]:

            if self.first_number != "":
                self.operator = text

        # --------------------------------------------------
        # Tall
        # --------------------------------------------------

        else:

            if self.operator == "":
                self.first_number += text

            else:
                self.second_number += text

            self.display_text = (
                self.first_number
                + self.operator
                + self.second_number
            )

            self.update_display(self.display_text)