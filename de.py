import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard – Hôpital Central")
        self.resize(1200, 700)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        header = QLabel("📊 Tableau de bord médical")
        header.setFont(QFont("Times New Roman", 22, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)

        cards_layout = QHBoxLayout()

        cards = [
            ("👨‍⚕️ Médecins", "24"),
            ("🧑‍🤝‍🧑 Patients", "180"),
            ("📅 Rendez-vous", "32"),
            ("🚑 Urgences", "5")
        ]

        for title, value in cards:
            card = QFrame()
            card.setFixedHeight(130)
            card_layout = QVBoxLayout(card)

            lbl_title = QLabel(title)
            lbl_title.setFont(QFont("Times New Roman", 15))
            lbl_title.setAlignment(Qt.AlignCenter)

            lbl_value = QLabel(value)
            lbl_value.setFont(QFont("Times New Roman", 28, QFont.Bold))
            lbl_value.setAlignment(Qt.AlignCenter)

            card_layout.addWidget(lbl_title)
            card_layout.addWidget(lbl_value)

            card.setStyleSheet("""
                background-color: white;
                border-radius: 12px;
            """)

            cards_layout.addWidget(card)

        main_layout.addWidget(header)
        main_layout.addSpacing(30)
        main_layout.addLayout(cards_layout)
        main_layout.addStretch()

        self.setStyleSheet("""
            QMainWindow {
                background-color: #f2f7fb;
            }
            QLabel {
                color: #0a2a43;
            }
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Dashboard()
    window.show()
    sys.exit(app.exec_())
