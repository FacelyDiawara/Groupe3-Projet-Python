import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QStackedWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# Import pages
from pages.home import HomePage
from pages.appointments import AppointmentsPage
from pages.medications import MedicationsPage
from pages.sms import SMSPage
from pages.whatsapp import WhatsAppPage
from pages.users import UsersPage
from pages.chat import ChatPage



class HospitalUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("")
        self.resize(1250, 720)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # ================= SIDEBAR =================
        sidebar = QWidget()
        sidebar.setFixedHeight(120) # Hauteur fixe pour la barre du haut
        sidebar_layout = QHBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(10, 10, 10, 10)

        logo = QLabel("🏥  HÔPITAL CENTRAL")
        logo.setFont(QFont("Times New Roman", 16, QFont.Bold))
        logo.setAlignment(Qt.AlignCenter)

        self.buttons = []

        btns_text = [
            "ACCUEIL",
            "ENREGISTREZ UN PATIENT",
            "LES DOCTEURS DISPONIBLE",
            "PRISE DE MÉDICAMENT",
            "GÉNÉRER SMS",
            "GÉNÉRER WHATSAPP",
            "DISCUSSION"
        ]

        for index, text in enumerate(btns_text):
            btn = QPushButton(text)
            btn.setMinimumHeight(48)
            btn.setMaximumWidth(220) # Constrain width for professionalism
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda _, i=index: self.change_page(i))
            sidebar_layout.addWidget(btn)
            self.buttons.append(btn)

        sidebar_layout.addStretch()

        # ================= CONTENU =================
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0) # Removed margins for full-screen home page

        self.pages = QStackedWidget()

        # Add Pages from modules
        # Store pages as attributes to access them later
        self.home_page = self.create_home_page()
        self.appointments_page = AppointmentsPage()
        self.medications_page = MedicationsPage()
        self.sms_page = SMSPage()
        self.whatsapp_page = WhatsAppPage()
        self.chat_page = ChatPage()
        self.users_page = UsersPage()
        
        # Connect signals for navigation
        self.appointments_page.navigate_to_medications.connect(lambda: self.change_page(3))
        self.appointments_page.navigate_to_users.connect(self.go_to_users_with_patient)
        self.users_page.navigate_to_medications.connect(self.go_to_medications_with_doctor)
        self.users_page.navigate_to_chat.connect(self.go_to_chat_with_data)

        
        # Connect signals from medications page to SMS and WhatsApp pages
        self.medications_page.request_sms.connect(self.go_to_sms_reminder)
        self.medications_page.request_whatsapp.connect(self.go_to_whatsapp_reminder)
        
        # Connect validation requests from messaging pages
        self.sms_page.request_validation.connect(self.handle_prescription_validation)
        self.whatsapp_page.request_validation.connect(self.handle_prescription_validation)

        self.pages.addWidget(self.home_page)
        self.pages.addWidget(self.appointments_page)
        self.pages.addWidget(self.users_page)
        self.pages.addWidget(self.medications_page)
        self.pages.addWidget(self.sms_page)
        self.pages.addWidget(self.whatsapp_page)
        self.pages.addWidget(self.chat_page)

        # ===== Footer =====
        footer = QLabel(
            "© 2026 Hôpital Central | Urgences : 15 | contact@hopitalcentral.sn"
        )
        footer.setObjectName("FooterLabel")
        footer.setAlignment(Qt.AlignCenter)
        footer.setFixedHeight(50)

        content_layout.addWidget(self.pages)
        content_layout.addWidget(footer)

        # ================= MAIN =================
        main_layout.addWidget(sidebar)
        main_layout.addWidget(content)

        self.apply_style()
        self.change_page(0)  # onglet par défaut

    # ================= PAGE TEMPLATE =================
    def create_page(self, title_text, desc_text):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 10, 30, 20)

        title = QLabel(title_text)
        title.setFont(QFont("Times New Roman", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        desc = QLabel(desc_text)
        desc.setFont(QFont("Times New Roman", 15))
        desc.setAlignment(Qt.AlignCenter)
        desc.setWordWrap(True)

        layout.addStretch()
        layout.addWidget(title)
        layout.addSpacing(10)
        layout.addWidget(desc)
        layout.addStretch()

        return page

    def create_home_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # Background Image
        import os
        image_path = os.path.join(os.path.dirname(__file__), "assets/fac.jpg")
        
        # Using Stylesheet for background image (more consistent scaling)
        page.setObjectName("HomePage")
        if os.path.exists(image_path):
            # Normalize path for CSS
            css_path = image_path.replace("\\", "/")
            page.setStyleSheet(f"""
                QWidget#HomePage {{
                    border-image: url({css_path}) 0 0 0 0 stretch stretch;
                }}
            """)

        # Overlay content
        overlay_widget = QWidget()
        # Removed background color, kept transparent
        overlay_widget.setStyleSheet("background-color: transparent;")
        overlay_layout = QVBoxLayout(overlay_widget)
        
        # New text content - Description only, no "Bienvenue" title
        desc = QLabel(
            "NOTRE SERVICE EST DE METTRE EN PLACE UN SYSTEME DE RAPPELLE AUTOMATIQUE DE NOS PATIENTS"
            " DANS UN CADRE MODERNE ET ACCUEILLANT.NOS EQUIPES DEVOUEES SONT VOTRE SERVICE "
            "24h/24 POUR ASSURER VOTRE BIEN ETRE."
        )
        desc.setFont(QFont("Times New Roman", 26, QFont.Bold))
        desc.setAlignment(Qt.AlignCenter)
        # Added text shadow and color for readability on image
        desc.setStyleSheet("color: #0a2a43; background-color: rgba(255, 255, 255, 0.7); border-radius: 15px; padding: 30px; font-size: 26px;")
        desc.setWordWrap(True)
        
        overlay_layout.addWidget(desc)
        overlay_layout.setContentsMargins(50, 40, 50, 40)
        overlay_widget.setFixedWidth(1100)
        overlay_widget.setMinimumHeight(350) # Assurer assez de hauteur pour le texte
        
        
        # Layout alignment: Center
        layout.addStretch()
        layout.addWidget(overlay_widget, 0, Qt.AlignCenter)
        layout.addStretch()
        
        return page

    # ================= NAVIGATION & SLOTS =================
    def go_to_sms_reminder(self, phone, nom, prenom, message, doc_name):
        # Index of SMS Page is 4
        self.change_page(4) 
        self.sms_page.populate(phone, nom, prenom, message, doc_name)

    def go_to_whatsapp_reminder(self, phone, nom, prenom, message, doc_name):
        # Index of WhatsApp Page is 5
        self.change_page(5)
        self.whatsapp_page.populate(phone, nom, prenom, message, doc_name)

    def go_to_medications_with_doctor(self, doc_name, doc_phone, pat_name, pat_phone):
        # Index of Medications Page is 3
        self.change_page(3)
        self.medications_page.set_prescription_data(doc_name, doc_phone, pat_name, pat_phone)

    def go_to_users_with_patient(self, pat_name, pat_phone):
        # Index of Users Page is 2
        self.change_page(2)
        self.users_page.set_patient_info(pat_name, pat_phone)

    def go_to_chat_with_data(self, doc_name, doc_phone, pat_name, pat_phone):
        # Index of Chat Page is 6
        self.change_page(6)
        self.chat_page.set_chat_data(pat_name, pat_phone, doc_name, doc_phone)

    def handle_prescription_validation(self, validity):
        """Orchestrates PDF generation and data cleanup when triggered from messaging pages"""
        success, info = self.medications_page.generate_pdf(validity)
        if not success:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Erreur de Validation", info)
            return
            
        # Clear medications from backend and UI
        if self.medications_page.clear_data():
            print("Prescription validated: PDF generated and system cleared.")
        else:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Erreur Nettoyage", "Le PDF a été généré mais la base de données n'a pas pu être vidée.")

    def change_page(self, index):
        self.pages.setCurrentIndex(index)
        for i, btn in enumerate(self.buttons):
            btn.setProperty("active", i == index)
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    # ================= STYLE =================
    def apply_style(self):
        self.setStyleSheet("""
            /* --- Premium Enterprise Palette --- */
            QMainWindow {
                background-color: #F1F5F9;
            }

            QWidget {
                font-family: 'Segoe UI', 'SF Pro Display', 'Inter', sans-serif;
                color: #0F172A;
            }

            /* --- Elegant Navigation Bar --- */
            QWidget#HospitalUI > QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #F8FAFC);
                border-bottom: 1px solid #CBD5E1;
            }

            QPushButton {
                background-color: transparent;
                color: #475569;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 13px;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }

            QPushButton:hover {
                background-color: #E2E8F0;
                color: #0284C7;
            }

            QPushButton[active="true"] {
                background-color: #0EA5E9;
                color: white;
                border-bottom: 3px solid #0369A1;
            }

            /* --- Refined Action Buttons --- */
            QPushButton#primaryButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #0EA5E9, stop:1 #0284C7);
                color: #FFFFFF;
                border: 1px solid #0369A1;
                border-radius: 10px;
                padding: 12px 24px;
                font-size: 14px;
            }
            
            QPushButton#primaryButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #0284C7, stop:1 #0369A1);
            }
            
            QPushButton#secondaryButton {
                background-color: #FFFFFF;
                color: #334155;
                border: 1px solid #E2E8F0;
                border-radius: 10px;
                padding: 12px 24px;
            }

            /* --- Sophisticated Input Fields --- */
            QLineEdit, QTextEdit, QComboBox, QDateEdit, QTimeEdit, QSpinBox {
                background-color: #FFFFFF;
                border: 1px solid #CBD5E1;
                border-radius: 10px;
                padding: 12px;
                font-size: 14px;
                color: #1E293B;
            }

            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
                border: 2px solid #38BDF8;
                background-color: #F0F9FF;
            }

            /* --- Enterprise Grade Tables --- */
            QTableWidget {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
                gridline-color: #F1F5F9;
                selection-background-color: #F0F9FF;
                selection-color: #0369A1;
            }

            QHeaderView::section {
                background-color: #F8FAFC;
                color: #64748B;
                padding: 14px;
                font-weight: 700;
                text-transform: uppercase;
                font-size: 11px;
                border: none;
                border-bottom: 2px solid #E2E8F0;
            }

            /* --- Professional Content Containers --- */
            QGroupBox {
                font-weight: 700;
                font-size: 16px;
                color: #334155;
                border: 1px solid #E2E8F0;
                border-radius: 16px;
                margin-top: 20px;
                background-color: #FFFFFF;
                padding-top: 20px;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px;
                background-color: #FFFFFF;
                color: #0284C7;
            }

            /* --- Clean Scrollbars --- */
            QScrollBar:vertical {
                border: none;
                background: #F8FAFC;
                width: 8px;
                border-radius: 4px;
            }

            QScrollBar::handle:vertical {
                background: #E2E8F0;
                min-height: 40px;
                border-radius: 4px;
            }

            QScrollBar::handle:vertical:hover {
                background: #94A3B8;
            }

            /* --- Polished Footer --- */
            QLabel#FooterLabel {
                background-color: #0F172A;
                color: #94A3B8;
                padding: 15px;
                font-size: 12px;
                font-weight: 500;
                letter-spacing: 0.5px;
            }
        """)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HospitalUI()
    window.show()
    sys.exit(app.exec_())
