from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QMessageBox, QListWidget,
    QGridLayout, QGroupBox, QTimeEdit, QHBoxLayout, QSpinBox, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtCore import Qt, QTime, pyqtSignal, QDate
from PyQt5.QtGui import QFont
from datetime import datetime
from messaging_service import MessagingService

class SMSPage(QWidget):
    request_validation = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        self.patient_nom = ""
        self.patient_prenom = ""
        self.init_ui()
        self.load_active_reminders()

    def init_ui(self):
        self.setObjectName("SMSPage")
        self.setStyleSheet("""
            QWidget#SMSPage {
                background-color: #eef2f6;
            }
            QGroupBox {
                background-color: white;
                border: 1px solid #d1d9e0;
                border-radius: 12px;
                margin-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: #0284c7;
            }
            QLineEdit, QTextEdit, QTimeEdit, QSpinBox {
                background-color: #ffffff;
                border: 1px solid #cbd5e1;
                border-radius: 8px;
            }
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 10, 30, 20)

        title = QLabel("Génération de SMS")
        title.setFont(QFont("Times New Roman", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        layout.addSpacing(10)

        # Input Group
        form_group = QGroupBox("Nouveau SMS")
        form_group.setFont(QFont("Times New Roman", 15, QFont.Bold))
        grid_layout = QGridLayout()
        grid_layout.setSpacing(15)

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Numéro de téléphone (ex: +224...)")
        self.phone_input.setReadOnly(False) # Permission d'éditer le numéro
        self.phone_input.setStyleSheet("background-color: white; border: 2px solid #0284c7;")
        
        # Time inputs for reminders
        self.morning_time = QTimeEdit()
        self.morning_time.setDisplayFormat("HH:mm")
        self.morning_time.setTime(QTime(8, 0)) # Default 8:00 AM
        
        self.evening_time = QTimeEdit()
        self.evening_time.setDisplayFormat("HH:mm")
        self.evening_time.setTime(QTime(20, 0)) # Default 8:00 PM
        
        self.message_input = QTextEdit()
        self.message_input.setPlaceholderText("Votre message ici...")
        
        send_btn = QPushButton("✅ VALIDER L'ORDONNANCE & ENVOYER")
        send_btn.clicked.connect(self.send_sms)
        send_btn.setStyleSheet("background-color: #2e7d32; color: white; padding: 12px; font-weight: bold; border-radius: 8px;")

        # Add to grid
        # Row 0: Phone, Validity & Validate/Send Button
        top_row_layout = QHBoxLayout()
        top_row_layout.setSpacing(15)
        
        top_row_layout.addWidget(QLabel("Téléphone:"))
        top_row_layout.addWidget(self.phone_input)
        
        top_row_layout.addSpacing(10)
        top_row_layout.addWidget(QLabel("Validité (jours):"))
        self.validity_input = QSpinBox()
        self.validity_input.setRange(1, 365)
        self.validity_input.setValue(7)
        self.validity_input.setStyleSheet("min-width: 80px;")
        top_row_layout.addWidget(self.validity_input)
        
        top_row_layout.addSpacing(10)
        top_row_layout.addWidget(send_btn)
        
        grid_layout.addLayout(top_row_layout, 0, 0, 1, 3)
        
        # Row 1: Reminder Times (Horizontal Layout)
        time_layout = QHBoxLayout()
        time_layout.addWidget(QLabel("Heure de rappel (Matin):"))
        time_layout.addWidget(self.morning_time)
        time_layout.addSpacing(20)
        time_layout.addWidget(QLabel("Heure de rappel (Soir):"))
        time_layout.addWidget(self.evening_time)
        
        grid_layout.addLayout(time_layout, 1, 0, 1, 3)

        # Row 2: Message
        grid_layout.addWidget(QLabel("Message:"), 2, 0)
        grid_layout.addWidget(self.message_input, 2, 1, 1, 2)

        form_group.setLayout(grid_layout)
        layout.addWidget(form_group)
        layout.addSpacing(10)

        # Active Reminders Section
        layout.addWidget(QLabel("🔔 RAPPELS EN COURS (Actifs)"))
        self.reminders_table = QTableWidget()
        self.reminders_table.setColumnCount(4)
        self.reminders_table.setHorizontalHeaderLabels(["Patient", "Téléphone", "Date de Fin", "Statut"])
        self.reminders_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.reminders_table)

    def populate(self, phone, nom, prenom, message, doc_name):
        self.phone_input.setText(phone)
        self.patient_nom = nom
        self.patient_prenom = prenom
        
        # Personalized message construction
        current_time = datetime.now().strftime('%H:%M')
        custom_msg = (
            f"Bonjour {prenom} {nom}, c'est {doc_name}.\n\n"
            "Votre traitement est important pour votre santé.\n"
            "Merci de penser à prendre vos médicaments aujourd’hui aux heures prévues "
            f"(il est {current_time}).\n"
            "Nous restons à votre disposition si besoin.\n\n"
            "Détails de l'ordonnance:\n"
            f"{message}"
        )
        self.message_input.setText(custom_msg)

    def load_active_reminders(self):
        """Fetch reminders and filter out those that are expired"""
        import api_client
        reminders = api_client.get_reminders()
        self.reminders_table.setRowCount(0)
        
        current_date = QDate.currentDate()
        
        for rem in reminders:
            if rem.get("type_canal") != "SMS":
                continue
                
            # Parse start date and check expiry
            start_date_str = rem.get("date_debut")
            try:
                day, month, year = map(int, start_date_str.split("/"))
                start_date = QDate(year, month, day)
                end_date = start_date.addDays(rem.get("duree", 0))
                
                if current_date > end_date:
                    # Automatically delete expired reminders if needed, 
                    # or just don't show them
                    api_client.delete_reminder(rem.get("id"))
                    continue
                
                row = self.reminders_table.rowCount()
                self.reminders_table.insertRow(row)
                
                patient_name = f"{rem.get('nom_patient', '')} {rem.get('prenom_patient', '')}"
                self.reminders_table.setItem(row, 0, QTableWidgetItem(patient_name))
                self.reminders_table.setItem(row, 1, QTableWidgetItem(rem.get("telephone_patient", "")))
                self.reminders_table.setItem(row, 2, QTableWidgetItem(end_date.toString("dd/MM/yyyy")))
                
                status_item = QTableWidgetItem("EN COURS")
                status_item.setForeground(Qt.darkGreen)
                self.reminders_table.setItem(row, 3, status_item)
                
            except Exception as e:
                print(f"Error parsing date for reminder {rem.get('id')}: {e}")

    def send_sms(self):
        import api_client
        number = self.phone_input.text()
        msg = self.message_input.toPlainText()
        matin = self.morning_time.time().toString("HH:mm")
        soir = self.evening_time.time().toString("HH:mm")
        validity = self.validity_input.value()

        if number and msg:
            # 1. Emit validation signal (PDF + Cleanup) with validity
            self.request_validation.emit(validity)
            
            # 2. Save Active Reminder to Backend
            reminder_data = {
                "nom_patient": self.patient_nom,
                "prenom_patient": self.patient_prenom,
                "telephone_patient": number,
                "medicaments": msg, # The message contains the drug list
                "date_debut": datetime.now().strftime('%d/%m/%Y'),
                "duree": validity,
                "matin": matin,
                "soir": soir,
                "type_canal": "SMS"
            }
            api_client.create_reminder(reminder_data)
            
            # 3. Real Messaging (SMS)
            success, sid_or_error = MessagingService.send_sms(number, msg)
            
            if success:
                print(f"Rappels SMS programmés pour {self.patient_nom} pendant {validity} jours. SID: {sid_or_error}")
                QMessageBox.information(
                    self, "Succès", 
                    f"Ordonnance validée.\n\nLe SMS a été envoyé à {number} et les rappels ont été programmés."
                )
            else:
                QMessageBox.warning(
                    self, "Erreur Envoi", 
                    f"Ordonnance validée mais le SMS n'a pas pu être envoyé.\nErreur: {sid_or_error}\n\nAssurez-vous d'avoir configuré des identifiants Twilio valides dans config.py."
                )
            
            self.load_active_reminders()
            self.message_input.clear()
        else:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs")
