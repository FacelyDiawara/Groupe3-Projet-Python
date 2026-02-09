from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import os

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Background Image via Stylesheet
        image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../assets/fac.jpg"))
        self.setObjectName("HomePage")
        if os.path.exists(image_path):
            css_path = image_path.replace("\\", "/")
            self.setStyleSheet(f"""
                QWidget#HomePage {{
                    border-image: url({css_path}) 0 0 0 0 stretch stretch;
                }}
            """)

        # Overlay content
        overlay_widget = QWidget()
        overlay_widget.setStyleSheet("background-color: transparent;")
        overlay_layout = QVBoxLayout(overlay_widget)
        
        desc = QLabel(
            "L'Hôpital Central est un établissement de référence offrant des soins de qualité "
            "dans un cadre moderne et accueillant. Nos équipes dévouées sont à votre service "
            "24h/24 pour assurer votre bien-être et votre santé."
        )
        desc.setFont(QFont("Times New Roman", 20, QFont.Bold)) # Correction: QFont.Bold is correct, QFont.Center does not exist
        desc.setAlignment(Qt.AlignCenter)
        desc.setStyleSheet("color: #0a2a43; background: transparent; padding: 20px;")
        desc.setWordWrap(True)
        
        overlay_layout.addWidget(desc)
        overlay_layout.setContentsMargins(50, 50, 50, 50)
        
        # Layout alignment: Center Verticaly
        layout.addStretch()
        layout.addWidget(overlay_widget, 0, Qt.AlignCenter)
        layout.addStretch()
