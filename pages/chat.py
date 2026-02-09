from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
    QHBoxLayout, QScrollArea, QRadioButton, QButtonGroup, QFrame,
    QTextEdit, QListWidget, QGroupBox, QGridLayout, QTimeEdit
)
from PyQt5.QtCore import Qt, QTime, QDateTime
from PyQt5.QtGui import QFont
from datetime import datetime
from messaging_service import MessagingService

class MessageBubble(QFrame):
    """Custom widget for displaying a message bubble"""
    def __init__(self, sender, message, timestamp, is_doctor=False):
        super().__init__()
        self.is_doctor = is_doctor
        self.init_ui(sender, message, timestamp)
    
    def init_ui(self, sender, message, timestamp):
        # Prevent layout re-creation warning
        if self.layout() is None:
            layout = QVBoxLayout(self)
        else:
            layout = self.layout()
            # Clear existing items if any
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
                    
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(4)
        
        # Sender name
        sender_label = QLabel(sender)
        sender_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        
        # Message content
        message_label = QLabel(message)
        message_label.setFont(QFont("Segoe UI", 13))
        message_label.setWordWrap(True)
        message_label.setMaximumWidth(320)
        
        # Timestamp
        time_label = QLabel(timestamp)
        time_label.setFont(QFont("Segoe UI", 10))
        time_label.setStyleSheet("color: rgba(255, 255, 255, 0.7);" if self.is_doctor else "color: #64748B;")
        
        layout.addWidget(sender_label)
        layout.addWidget(message_label)
        layout.addWidget(time_label, 0, Qt.AlignRight)
        
        # Styling based on platform and sender
        is_wa = getattr(self, "is_whatsapp", False)
        
        if self.is_doctor:
            bg_color = "#0ea5e9" if not is_wa else "#22c55e" # Blue-500 or Green-500
            self.setStyleSheet(f"""
                QFrame {{
                    background-color: {bg_color};
                    border-radius: 12px;
                    border-top-right-radius: 2px;
                }}
                QLabel {{
                    color: #FFFFFF;
                    background-color: transparent;
                }}
            """)
        else:
            bg_color = "#ffffff" # White for contrast on grey background
            text_color = "#334155"
            self.setStyleSheet(f"""
                QFrame {{
                    background-color: {bg_color};
                    border: 1px solid #e2e8f0;
                    border-radius: 12px;
                    border-top-left-radius: 2px;
                }}
                QLabel {{
                    color: {text_color};
                    background-color: transparent;
                }}
            """)

class ChatPage(QWidget):
    def __init__(self):
        super().__init__()
        self.patient_name = "Patient Inconnu"
        self.patient_phone = "Inconnu"
        self.doctor_name = "Docteur Inconnu"
        self.doctor_phone = "Inconnu"
        self.init_ui()

    def set_chat_data(self, p_name, p_phone, d_name, d_phone):
        """Set patient and doctor data and update headers"""
        self.patient_name = p_name
        self.patient_phone = p_phone
        self.doctor_name = d_name
        self.doctor_phone = d_phone
        
        # Update labels
        self.sms_p_label.setText(f"👤 {p_name}\n📞 {p_phone}")
        self.sms_d_label.setText(f"👨‍⚕️ {d_name}\n📞 {d_phone}")
        self.wa_p_label.setText(f"👤 {p_name}\n📞 {p_phone}")
        self.wa_d_label.setText(f"👨‍⚕️ {d_name}\n📞 {d_phone}")

    def init_ui(self):
        self.setObjectName("ChatPage")
        self.setStyleSheet("""
            QWidget#ChatPage {
                background-color: #eef2f6;
            }
            QLineEdit {
                background-color: white;
                border: 1px solid #cbd5e1;
                border-radius: 8px;
                padding: 8px;
            }
            QPushButton#sendButton {
                color: white;
                font-weight: bold;
                border-radius: 8px;
                padding: 5px 10px;
                font-size: 11px;
            }
            QLabel#HeaderInfo {
                background-color: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 5px;
                font-size: 11px;
                color: #475569;
            }
        """)
        # Main layout is Horizontal to hold two columns
        self.main_h_layout = QHBoxLayout(self)
        self.main_h_layout.setContentsMargins(15, 5, 15, 15)
        self.main_h_layout.setSpacing(15)

        # ================= LEFT COLUMN: SMS / CHAT =================
        self.left_widget = QWidget()
        self.left_layout = QVBoxLayout(self.left_widget)
        
        # SMS Header Row
        sms_header_layout = QHBoxLayout()
        self.sms_p_label = QLabel(f"👤 {self.patient_name}\n📞 {self.patient_phone}")
        self.sms_p_label.setObjectName("HeaderInfo")
        self.sms_d_label = QLabel(f"👨‍⚕️ {self.doctor_name}\n📞 {self.doctor_phone}")
        self.sms_d_label.setObjectName("HeaderInfo")
        self.sms_d_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        sms_header_layout.addWidget(self.sms_p_label, 1)
        sms_header_layout.addSpacing(10)
        sms_header_layout.addWidget(self.sms_d_label, 1)
        self.left_layout.addLayout(sms_header_layout)

        chat_title = QLabel("💬 SMS & DISCUSSION")
        chat_title.setFont(QFont("Times New Roman", 16, QFont.Bold))
        chat_title.setStyleSheet("color: #0288d1; margin-top: 5px;")
        chat_title.setAlignment(Qt.AlignCenter)
        self.left_layout.addWidget(chat_title)

        # Scroll Area for Messages
        self.sms_scroll = QScrollArea()
        self.sms_scroll.setWidgetResizable(True)
        self.sms_scroll.setStyleSheet("""
            QScrollArea {
                border: 1px solid #cbd5e1;
                border-radius: 12px;
                background-color: #f8fafc;
            }
        """)
        self.sms_container = QWidget()
        self.sms_container.setStyleSheet("background-color: transparent;")
        self.sms_layout = QVBoxLayout(self.sms_container)
        self.sms_layout.addStretch()
        self.sms_scroll.setWidget(self.sms_container)
        self.left_layout.addWidget(self.sms_scroll)

        # Dual Input Area (Bottom)
        sms_inputs_layout = QHBoxLayout()
        
        # Patient Side
        sms_p_side = QVBoxLayout()
        self.sms_p_input = QLineEdit()
        self.sms_p_input.setPlaceholderText("SMS Patient...")
        self.sms_p_input.returnPressed.connect(lambda: self.send_message("sms", "patient"))
        sms_p_send = QPushButton("Patient Envoyer")
        sms_p_send.setObjectName("sendButton")
        sms_p_send.setStyleSheet("background-color: #64748b;")
        sms_p_send.clicked.connect(lambda: self.send_message("sms", "patient"))
        sms_p_side.addWidget(self.sms_p_input)
        sms_p_side.addWidget(sms_p_send)

        # Doctor Side
        sms_d_side = QVBoxLayout()
        self.sms_d_input = QLineEdit()
        self.sms_d_input.setPlaceholderText("SMS Docteur...")
        self.sms_d_input.returnPressed.connect(lambda: self.send_message("sms", "doctor"))
        sms_d_send = QPushButton("Docteur Envoyer")
        sms_d_send.setObjectName("sendButton")
        sms_d_send.setStyleSheet("background-color: #0284c7;")
        sms_d_send.clicked.connect(lambda: self.send_message("sms", "doctor"))
        sms_d_side.addWidget(self.sms_d_input)
        sms_d_side.addWidget(sms_d_send)

        sms_inputs_layout.addLayout(sms_p_side)
        sms_inputs_layout.addLayout(sms_d_side)
        self.left_layout.addLayout(sms_inputs_layout)

        # --- Separator ---
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("color: #cfd8dc;")

        # ================= RIGHT COLUMN: WHATSAPP =================
        self.right_widget = QWidget()
        self.right_layout = QVBoxLayout(self.right_widget)
        
        # WhatsApp Header Row
        wa_header_layout = QHBoxLayout()
        self.wa_p_label = QLabel(f"👤 {self.patient_name}\n📞 {self.patient_phone}")
        self.wa_p_label.setObjectName("HeaderInfo")
        self.wa_d_label = QLabel(f"👨‍⚕️ {self.doctor_name}\n📞 {self.doctor_phone}")
        self.wa_d_label.setObjectName("HeaderInfo")
        self.wa_d_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        wa_header_layout.addWidget(self.wa_p_label, 1)
        wa_header_layout.addSpacing(10)
        wa_header_layout.addWidget(self.wa_d_label, 1)
        self.right_layout.addLayout(wa_header_layout)

        wa_title = QLabel("📱 WHATSAPP")
        wa_title.setFont(QFont("Times New Roman", 16, QFont.Bold))
        wa_title.setStyleSheet("color: #25D366; margin-top: 5px;")
        wa_title.setAlignment(Qt.AlignCenter)
        self.right_layout.addWidget(wa_title)
        
        # WhatsApp Scroll Area
        self.wa_scroll = QScrollArea()
        self.wa_scroll.setWidgetResizable(True)
        self.wa_scroll.setStyleSheet("""
            QScrollArea {
                border: 1px solid #cbd5e1;
                border-radius: 12px;
                background-color: #f8fafc;
            }
        """)
        self.wa_container = QWidget()
        self.wa_container.setStyleSheet("background-color: transparent;")
        self.wa_layout = QVBoxLayout(self.wa_container)
        self.wa_layout.addStretch()
        self.wa_scroll.setWidget(self.wa_container)
        self.right_layout.addWidget(self.wa_scroll)

        # Dual Input Area (Bottom)
        wa_inputs_layout = QHBoxLayout()
        
        # Patient Side
        wa_p_side = QVBoxLayout()
        self.wa_p_input = QLineEdit()
        self.wa_p_input.setPlaceholderText("WA Patient...")
        self.wa_p_input.returnPressed.connect(lambda: self.send_message("wa", "patient"))
        wa_p_send = QPushButton("Patient Envoyer")
        wa_p_send.setObjectName("sendButton")
        wa_p_send.setStyleSheet("background-color: #64748b;")
        wa_p_send.clicked.connect(lambda: self.send_message("wa", "patient"))
        wa_p_side.addWidget(self.wa_p_input)
        wa_p_side.addWidget(wa_p_send)

        # Doctor Side
        wa_d_side = QVBoxLayout()
        self.wa_d_input = QLineEdit()
        self.wa_d_input.setPlaceholderText("WA Docteur...")
        self.wa_d_input.returnPressed.connect(lambda: self.send_message("wa", "doctor"))
        wa_d_send = QPushButton("Docteur Envoyer")
        wa_d_send.setObjectName("sendButton")
        wa_d_send.setStyleSheet("background-color: #22c55e;")
        wa_d_send.clicked.connect(lambda: self.send_message("wa", "doctor"))
        wa_d_side.addWidget(self.wa_d_input)
        wa_d_side.addWidget(wa_d_send)

        wa_inputs_layout.addLayout(wa_p_side)
        wa_inputs_layout.addLayout(wa_d_side)
        self.right_layout.addLayout(wa_inputs_layout)

        # Add to main
        self.main_h_layout.addWidget(self.left_widget, 1)
        self.main_h_layout.addWidget(line)
        self.main_h_layout.addWidget(self.right_widget, 1)

        self.add_welcome_messages()

    def send_message(self, platform, role):
        if platform == "sms":
            if role == "patient":
                text = self.sms_p_input.text().strip()
                input_field = self.sms_p_input
                dest_phone = self.doctor_phone
            else:
                text = self.sms_d_input.text().strip()
                input_field = self.sms_d_input
                dest_phone = self.patient_phone
                
            if text:
                timestamp = datetime.now().strftime('%H:%M')
                is_doctor = (role == "doctor")
                sender = f"👨‍⚕️ {self.doctor_name}" if is_doctor else f"👤 {self.patient_name}"
                self.add_bubble(self.sms_layout, self.sms_scroll, sender, text, timestamp, is_doctor, False)
                
                # Real SMS sending (if number is available)
                if dest_phone and dest_phone not in ["Inconnu", ""]:
                    MessagingService.send_sms(dest_phone, text)
                
                input_field.clear()
        else:
            if role == "patient":
                text = self.wa_p_input.text().strip()
                input_field = self.wa_p_input
                dest_phone = self.doctor_phone
            else:
                text = self.wa_d_input.text().strip()
                input_field = self.wa_d_input
                dest_phone = self.patient_phone
                
            if text:
                timestamp = datetime.now().strftime('%H:%M')
                is_doctor = (role == "doctor")
                sender = f"👨‍⚕️ {self.doctor_name}" if is_doctor else f"👤 {self.patient_name}"
                self.add_bubble(self.wa_layout, self.wa_scroll, sender, text, timestamp, is_doctor, True)
                
                # Real WhatsApp sending
                if dest_phone and dest_phone not in ["Inconnu", ""]:
                    MessagingService.send_whatsapp(dest_phone, text)
                
                input_field.clear()

    def add_bubble(self, layout, scroll_area, sender, message, timestamp, is_doctor, is_wa):
        # Remove stretch
        if layout.count() > 0:
            layout.takeAt(layout.count() - 1)
            
        container = QHBoxLayout()
        bubble = MessageBubble(sender, message, timestamp, is_doctor)
        bubble.is_whatsapp = is_wa # Custom attribute for dynamic styling
        bubble.init_ui(sender, message, timestamp) # Re-init UI to apply styles
        bubble.setMaximumWidth(320)
        
        if is_doctor:
            container.addStretch()
            container.addWidget(bubble)
        else:
            container.addWidget(bubble)
            container.addStretch()
            
        layout.addLayout(container)
        layout.addStretch()
        
        # Auto-scroll
        from PyQt5.QtWidgets import QApplication
        QApplication.processEvents()
        scroll_area.verticalScrollBar().setValue(scroll_area.verticalScrollBar().maximum())

    def add_welcome_messages(self):
        self.add_bubble(self.sms_layout, self.sms_scroll, f"👤 {self.patient_name}", "Bonjour, j'ai une question sur mon RDV.", "09:30", False, False)
        self.add_bubble(self.wa_layout, self.wa_scroll, f"👨‍⚕️ {self.doctor_name}", "Veuillez envoyer vos résultats ici.", "10:15", True, True)
