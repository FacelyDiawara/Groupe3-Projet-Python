from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QHeaderView, QDateEdit, QTimeEdit, QLineEdit, QFormLayout,
    QComboBox, QGroupBox, QGridLayout, QMessageBox
)
from PyQt5.QtCore import Qt, QDate, QTime, pyqtSignal
from PyQt5.QtGui import QFont
import api_client

class AppointmentsPage(QWidget):
    # Signals for navigation
    navigate_to_medications = pyqtSignal()
    navigate_to_users = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_appointments()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 10, 30, 20)

        title = QLabel("Gestion des Rendez-vous")
        title.setFont(QFont("Times New Roman", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        layout.addSpacing(10)

        # Form Group for Patient Information
        form_group = QGroupBox("Renseignements du Patient")
        form_group.setFont(QFont("Times New Roman", 15, QFont.Bold))
        grid_layout = QGridLayout()
        grid_layout.setSpacing(15)

        # Input fields
        self.nom_input = QLineEdit()
        self.nom_input.setPlaceholderText("Nom de famille du patient")
        
        self.prenom_input = QLineEdit()
        self.prenom_input.setPlaceholderText("Prénom du patient")
        
        self.phone_input = QLineEdit()
        self.phone_input.setText("+224 ")
        self.phone_input.setPlaceholderText("Ex: +221 77 000 00 00")
        
        self.sexe_input = QComboBox()
        self.sexe_input.addItems(["Masculin", "Féminin"])

        self.date_input = QDateEdit(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        self.time_input = QTimeEdit(QTime.currentTime())
        
        # Add fields to grid (2 per row)
        # Row 1: Nom & Prénom
        grid_layout.addWidget(QLabel("NOM:"), 0, 0)
        grid_layout.addWidget(self.nom_input, 0, 1)
        grid_layout.addWidget(QLabel("PRENOMS:"), 0, 2)
        grid_layout.addWidget(self.prenom_input, 0, 3)

        # Row 2: Téléphone & Sexe
        grid_layout.addWidget(QLabel("TELEPHONE:"), 1, 0)
        grid_layout.addWidget(self.phone_input, 1, 1)
        grid_layout.addWidget(QLabel("SEXE:"), 1, 2)
        grid_layout.addWidget(self.sexe_input, 1, 3)

        # Row 3: Date & Heure
        grid_layout.addWidget(QLabel("DATE:"), 2, 0)
        grid_layout.addWidget(self.date_input, 2, 1)
        grid_layout.addWidget(QLabel("HEURE:"), 2, 2)
        grid_layout.addWidget(self.time_input, 2, 3)

        form_group.setLayout(grid_layout)
        layout.addWidget(form_group)
        layout.addSpacing(15)

        # Add button
        add_btn_layout = QHBoxLayout()
        add_btn_layout.addStretch()
        add_btn = QPushButton("AJOUTER RENDEZ-VOUS")
        add_btn.clicked.connect(self.add_appointment)
        add_btn.setStyleSheet("background-color: #0284C7; color: white; padding: 12px 24px; font-size: 15px; border-radius: 8px;")
        add_btn_layout.addWidget(add_btn)
        add_btn_layout.addStretch()
        layout.addLayout(add_btn_layout)
        layout.addSpacing(20)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["NOM", "PRENOMS", "TELEPHONE", "SEXE", "DOCTEUR", "DATE", "HEURE"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)
        
        # Navigation Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        contact_doctor_btn = QPushButton("👨‍⚕️ CONTACTER UN SPECIALISTE")
        contact_doctor_btn.clicked.connect(self.go_to_users)
        contact_doctor_btn.setStyleSheet("background-color: #2e7d32; color: white; padding: 12px 24px; font-size: 15px; border-radius: 8px;")

        btn_layout.addWidget(contact_doctor_btn)
        
        delete_btn = QPushButton("🗑️ SUPPRIMER RENDEZ-VOUS")
        delete_btn.clicked.connect(self.remove_appointment)
        delete_btn.setStyleSheet("background-color: #c62828; color: white; padding: 12px 24px; font-size: 15px; border-radius: 8px;")
        btn_layout.addWidget(delete_btn)
        
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

    def load_appointments(self):
        """Load appointments from the backend API"""
        appointments = api_client.get_appointments()
        self.table.setRowCount(0)
        for appt in appointments:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            nom_item = QTableWidgetItem(appt.get("nom_patient", ""))
            prenom_item = QTableWidgetItem(appt.get("prenom_patient", ""))
            phone_item = QTableWidgetItem(appt.get("telephone_patient", ""))
            sexe_item = QTableWidgetItem(appt.get("sexe_patient", ""))
            doctor_item = QTableWidgetItem(appt.get("docteur_name", ""))
            date_item = QTableWidgetItem(appt.get("date", ""))
            heure_item = QTableWidgetItem(appt.get("heure", ""))
            
            # Store ID in UserRole
            nom_item.setData(Qt.UserRole, appt.get("id"))
            
            self.table.setItem(row, 0, nom_item)
            self.table.setItem(row, 1, prenom_item)
            self.table.setItem(row, 2, phone_item)
            self.table.setItem(row, 3, sexe_item)
            self.table.setItem(row, 4, doctor_item)
            self.table.setItem(row, 5, date_item)
            self.table.setItem(row, 6, heure_item)

    def add_appointment(self):
        nom = self.nom_input.text().strip()
        prenom = self.prenom_input.text().strip()
        phone = self.phone_input.text().strip()
        sexe = self.sexe_input.currentText()
        doctor = "" # No doctor selected at this stage
            
        date = self.date_input.date().toString("dd/MM/yyyy")
        time = self.time_input.time().toString("HH:mm")

        if nom and prenom:
            appointment_data = {
                "nom_patient": nom,
                "prenom_patient": prenom,
                "telephone_patient": phone,
                "sexe_patient": sexe,
                "docteur_name": doctor,
                "date": date,
                "heure": time
            }
            
            result = api_client.create_appointment(appointment_data)
            if result:
                self.load_appointments()
                # Clear inputs
                self.nom_input.clear()
                self.prenom_input.clear()
                self.phone_input.clear()
                QMessageBox.information(self, "Succès", f"Rendez-vous pour {prenom} {nom} enregistré.")
            else:
                QMessageBox.critical(self, "Erreur", "Impossible d'enregistrer le rendez-vous.")
        else:
            QMessageBox.warning(self, "Champs Manquants", "Le nom et le prénom du patient sont obligatoires.")


    def go_to_users(self):
        """Navigate to users page to contact a doctor"""
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            nom = self.table.item(selected_row, 0).text()
            prenom = self.table.item(selected_row, 1).text()
            telephone = self.table.item(selected_row, 2).text()
            
            fullname = f"{prenom} {nom}"
            self.navigate_to_users.emit(fullname, telephone)
        else:
            QMessageBox.warning(
                self, "Sélection Requise",
                "Veuillez sélectionner un patient dans le tableau pour contacter un spécialiste."
            )

    def remove_appointment(self):
        """Delete the selected appointment"""
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            # Get ID from UserRole
            appt_id = self.table.item(selected_row, 0).data(Qt.UserRole)
            nom = self.table.item(selected_row, 0).text()
            prenom = self.table.item(selected_row, 1).text()
            
            reply = QMessageBox.question(
                self, 'Confirmer la Suppression',
                f"Voulez-vous vraiment supprimer le rendez-vous de {prenom} {nom} ?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                if api_client.delete_appointment(appt_id):
                    self.load_appointments()
                    QMessageBox.information(self, "Succès", "Rendez-vous supprimé avec succès.")
                else:
                    QMessageBox.critical(self, "Erreur", "Impossible de supprimer le rendez-vous.")
        else:
            QMessageBox.warning(
                self, "Sélection Requise",
                "Veuillez sélectionner un rendez-vous dans le tableau avant de le supprimer."
            )
