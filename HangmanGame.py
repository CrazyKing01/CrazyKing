import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QInputDialog
from PyQt5.QtCore import Qt
from PyQt5 import QtGui

class HangmanGame(QWidget):
    def __init__(self):
        super().__init__()

        self.words = {
            "Города": ["москва", "париж", "нью-йорк", "токио"],
            "Страны": ["россия", "франция", "сша", "япония"],
            "Фрукты": ["яблоко", "банан", "груша", "апельсин"],
            "Разное": ["слон", "дом", "книга", "автомобиль"]
        }

        self.current_word = ""
        self.remaining_attempts = 6
        self.guesses = []
        self.current_theme = None

        self.hangman_images = [
            "  +---+\n"
            "  |   |\n"
            "      |\n"
            "      |\n"
            "      |\n"
            "      |\n"
            "=========",
            "  +---+\n"
            "  |   |\n"
            "  O   |\n"
            "      |\n"
            "      |\n"
            "      |\n"
            "=========",
            "  +---+\n"
            "  |   |\n"
            "  O   |\n"
            "  |   |\n"
            "      |\n"
            "      |\n"
            "=========",
            "  +---+\n"
            "  |   |\n"
            "  O   |\n"
            " /|   |\n"
            "      |\n"
            "      |\n"
            "=========",
            "  +---+\n"
            "  |   |\n"
            "  O   |\n"
            " /|\\  |\n"
            "      |\n"
            "      |\n"
            "=========",
            "  +---+\n"
            "  |   |\n"
            "  O   |\n"
            " /|\\  |\n"
            " / \\  |\n"
            "      |\n"
            "========="
        ]

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Игра Виселица")
        self.setGeometry(100, 100, 400, 400)

        self.theme_buttons = {}
        for theme in self.words.keys():
            button = QPushButton(theme, self)
            button.clicked.connect(lambda checked, theme=theme: self.chooseTheme(theme))
            self.theme_buttons[theme] = button

        self.word_label = QLabel(self)
        self.word_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.word_label.setFont(QtGui.QFont("Arial", 24))
        self.updateWordLabel()

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setFont(QtGui.QFont("Monospace", 16))
        self.updateHangmanImage()

        self.input_field = QLineEdit(self)
        self.input_field.returnPressed.connect(self.checkGuess)

        layout = QVBoxLayout()
        for button in self.theme_buttons.values():
            layout.addWidget(button)
        layout.addWidget(self.image_label)
        layout.addWidget(self.word_label)
        layout.addWidget(self.input_field)

        self.setLayout(layout)

    def chooseTheme(self, theme):
        self.current_theme = theme
        self.newGame()

    def newGame(self):
        if self.current_theme is None:
            self.word_label.setText("Сначала нужно выбрать тему.")
            return

        self.current_word = random.choice(self.words[self.current_theme]).lower()
        self.remaining_attempts = 6
        self.guesses = []
        self.updateWordLabel()
        self.updateHangmanImage()

    def updateWordLabel(self):
        displayed_word = ""
        for letter in self.current_word:
            if letter in self.guesses:
                displayed_word += letter
            else:
                displayed_word += "_"
        self.word_label.setText(displayed_word)

    def checkGuess(self):
        if self.current_theme is None:
            self.word_label.setText("Сначала нужно выбрать тему.")
            return

        guess = self.input_field.text().lower()
        if guess.isalpha() and len(guess) == 1:
            if guess not in self.guesses:
                self.guesses.append(guess)
                if guess not in self.current_word:
                    self.remaining_attempts -= 1
                    self.updateHangmanImage()

                self.updateWordLabel()
                self.input_field.clear()

                if self.remaining_attempts == 0:
                    self.word_label.setText(f"Вы проиграли! Слово было '{self.current_word}'.")
                elif "_" not in self.word_label.text():
                    self.word_label.setText("Вы выиграли! Вы угадали слово.")
            else:
                self.word_label.setText("Вы уже угадывали эту букву.")
        else:
            self.word_label.setText("Пожалуйста, введите одну букву.")

    def updateHangmanImage(self):
        image_number = 6 - self.remaining_attempts
        if image_number >= 0 and image_number < len(self.hangman_images):
            self.image_label.setText(self.hangman_images[image_number])
        else:
            self.image_label.setText("")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = HangmanGame()
    game.show()
    sys.exit(app.exec_())