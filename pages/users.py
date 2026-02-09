import cv2
import os
import time
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QHeaderView, QFormLayout, QGroupBox, QGridLayout,
    QMessageBox, QComboBox, QTabWidget, QFileDialog, QDialog
)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QPixmap, QImage, QIcon
import api_client

class CameraDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Prendre une photo")
        self.setFixedSize(640, 520)
        
        self.layout = QVBoxLayout(self)
        
        self.image_label = QLabel()
        self.image_label.setFixedSize(640, 480)
        self.layout.addWidget(self.image_label)
        
        btn_layout = QHBoxLayout()
        self.capture_btn = QPushButton("Capturer")
        self.capture_btn.clicked.connect(self.capture_image)
        self.capture_btn.setStyleSheet("background-color: #2e7d32; color: white; padding: 10px;")
        btn_layout.addWidget(self.capture_btn)
        
        self.cancel_btn = QPushButton("Annuler")
        self.cancel_btn.clicked.connect(self.reject)
        self.cancel_btn.setStyleSheet("background-color: #c62828; color: white; padding: 10px;")
        btn_layout.addWidget(self.cancel_btn)
        
        self.layout.addLayout(btn_layout)
        
        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)
        self.captured_image_path = None

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Convert frame to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.image_label.setPixmap(QPixmap.fromImage(image))

    def capture_image(self):
        ret, frame = self.cap.read()
        if ret:
            # Save image
            if not os.path.exists("assets/doctors"):
                os.makedirs("assets/doctors", exist_ok=True)
            
            filename = f"assets/doctors/doc_{int(time.time())}.jpg"
            cv2.imwrite(filename, frame)
            self.captured_image_path = filename
            self.accept()

    def closeEvent(self, event):
        self.timer.stop()
        self.cap.release()
        super().closeEvent(event)


class UsersPage(QWidget):

    # Signal for navigation
    navigate_to_medications = pyqtSignal(str, str, str, str)
    navigate_to_chat = pyqtSignal(str, str, str, str)

    def __init__(self):
        super().__init__()
        self.current_patient_name = ""
        self.current_patient_phone = ""
        self.photo_path = None
        self.init_ui()
        self.load_doctors()

    def init_ui(self):
        self.setObjectName("UsersPage")
        self.setStyleSheet("""
            QWidget#UsersPage {
                background-color: #eef2f6;
            }
            QTabWidget::pane {
                border: 1px solid #cbd5e1;
                background-color: white;
                border-radius: 12px;
                margin-top: -1px; /* Fuse with tab */
            }
            QTabBar::tab {
                background: #f1f5f9;
                border: 1px solid #cbd5e1;
                padding: 20px 60px; /* Much wider and taller tabs */
                border-top-left-radius: 12px;
                border-top-right-radius: 12px;
                font-size: 24px;
                font-weight: bold;
                color: #64748b;
                min-height: 40px; /* Ensure a minimum height for the section */
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom-color: white;
                color: #0284c7;
            }
            QGroupBox {
                background-color: white;
                border: 1px solid #cbd5e1;
                border-radius: 15px;
                margin-top: 25px;
                padding: 20px; /* Interior space for the section */
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px;
                color: #0284c7;
                font-size: 20px;
                font-weight: bold;
            }
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 20, 40, 30) # More room around the main container

        title = QLabel("ENREGISTRER UN PATIENT")
        title.setFont(QFont("Times New Roman", 26, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        layout.addSpacing(10)

        # Tabs
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # Tab 1: Liste des Docteurs
        self.tab_list = QWidget()
        self.setup_list_tab()
        self.tabs.addTab(self.tab_list, "Liste des docteurs")

        # Tab 2: Ajouter un Docteur
        self.tab_add = QWidget()
        self.setup_add_tab()
        self.tabs.addTab(self.tab_add, "Ajouter un Docteur")

    def setup_add_tab(self):
        main_layout = QHBoxLayout(self.tab_add)
        main_layout.setSpacing(40)
        main_layout.setContentsMargins(35, 35, 35, 35) # Increased margins
        
        # --- Left Side: Photo Section (Narrower & Taller) ---
        left_layout = QVBoxLayout()
        photo_group = QGroupBox("PHOTO")
        photo_group.setFont(QFont("Times New Roman", 16, QFont.Bold))
        photo_layout = QVBoxLayout()
        
        self.photo_label = QLabel("Aucune photo")
        self.photo_label.setAlignment(Qt.AlignCenter)
        self.photo_label.setStyleSheet("border: 1px dashed gray; background: #f0f0f0;")
        self.photo_label.setScaledContents(True)
        # Narrower but taller aspect ratio
        self.photo_label.setMinimumSize(250, 350) 
        photo_layout.addWidget(self.photo_label, 1)
        
        photo_btns_layout = QHBoxLayout()
        select_photo_btn = QPushButton("📁 Choisir")
        select_photo_btn.clicked.connect(self.select_photo)
        photo_btns_layout.addWidget(select_photo_btn)
        
        take_photo_btn = QPushButton("📷 Prendre")
        take_photo_btn.clicked.connect(self.take_photo)
        photo_btns_layout.addWidget(take_photo_btn)
        
        photo_layout.addLayout(photo_btns_layout)
        photo_group.setLayout(photo_layout)
        left_layout.addWidget(photo_group)
        left_layout.addStretch()
        
        main_layout.addLayout(left_layout, 25) # Narrower: 25% width
        
        # --- Right Side: Form Section (Single Column) ---
        right_layout = QVBoxLayout()
        
        form_group = QGroupBox("INFORMATIONS GÉNÉRALES")
        form_group.setFont(QFont("Times New Roman", 15, QFont.Bold))
        form_layout = QFormLayout()
        form_layout.setSpacing(30) # Increased spacing to fill vertical space
        form_layout.setLabelAlignment(Qt.AlignRight)
        
        # Custom Font for inputs and labels
        input_font = QFont("Times New Roman", 22)
        label_font = QFont("Times New Roman", 20, QFont.Bold)
        
        # Input fields (Single column)
        self.nom_input = QLineEdit()
        self.nom_input.setPlaceholderText("NOM DU DOCTEUR")
        self.nom_input.setFont(input_font)
        self.nom_input.setFixedWidth(450)
        
        self.prenom_input = QLineEdit()
        self.prenom_input.setPlaceholderText("PRENOM DE L'UTILISATEUR")
        self.prenom_input.setFont(input_font)
        self.prenom_input.setFixedWidth(450)
        
        self.role_input = QComboBox()
        self.role_input.addItems(["Docteur", "Infirmier", "Pharmacist", "Administrateur", "Patient", "Autre"])
        self.role_input.setFont(input_font)
        self.role_input.setFixedWidth(450)
        
        self.specialite_input = QLineEdit()
        self.specialite_input.setPlaceholderText("Ex: CARDIOLOGUE, PEDIATRE, etc.")
        self.specialite_input.setFont(input_font)
        self.specialite_input.setFixedWidth(450)
        
        self.telephone_input = QLineEdit()
        self.telephone_input.setText("+224 ")
        self.telephone_input.setPlaceholderText("Ex: +224 623 45 67")
        self.telephone_input.setFont(input_font)
        self.telephone_input.setFixedWidth(450)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Ex: doc@example.com")
        self.email_input.setFont(input_font)
        self.email_input.setFixedWidth(450)

        # Add to form layout (Label : Input)
        for label_text, widget in [
            ("NOM:", self.nom_input),
            ("PRENOM:", self.prenom_input),
            ("SPECIALITE:", self.specialite_input),
            ("TELEPHONE:", self.telephone_input),
            ("EMAIL:", self.email_input),
            ("ROLE:", self.role_input)
        ]:
            label = QLabel(label_text)
            label.setFont(label_font)
            form_layout.addRow(label, widget)
        
        form_group.setLayout(form_layout)
        right_layout.addWidget(form_group)
        
        # Add button
        btn_container = QHBoxLayout()
        btn_container.addStretch()
        add_btn = QPushButton("AJOUTER L'UTILISATEUR")
        add_btn.clicked.connect(self.add_doctor)
        add_btn.setStyleSheet("background-color: #0284C7; color: white; padding: 18px 45px; font-size: 18px; border-radius: 12px; font-weight: bold;")
        btn_container.addWidget(add_btn)
        btn_container.addStretch()
        
        right_layout.addLayout(btn_container)
        right_layout.addStretch()
        
        main_layout.addLayout(right_layout, 75) # 75% width

    def setup_list_tab(self):
        layout = QVBoxLayout(self.tab_list)
        layout.setContentsMargins(30, 30, 30, 30) # Increased margins

        # Table to display doctors
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["PHOTO", "NOM", "PRENOMS", "ROLE", "SPECIALITE", "TELEPHONE", "EMAIL"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed) # Photo column fixed width
        self.table.setColumnWidth(0, 200)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.verticalHeader().setDefaultSectionSize(220) # Slightly larger for photos
        self.table.setFont(QFont("Segoe UI", 16)) 
        self.table.horizontalHeader().setFont(QFont("Segoe UI", 18, QFont.Bold))
        layout.addWidget(self.table)
        layout.addSpacing(15)

        # Buttons Layout (Horizontal)
        action_btn_layout = QHBoxLayout()
        action_btn_layout.addStretch()
        
        # Delete user button
        delete_btn = QPushButton("🗑️ Supprimer l'utilisateur sélectionné")
        delete_btn.clicked.connect(self.remove_doctor)
        delete_btn.setStyleSheet("background-color: #ef4444; color: white; padding: 16px 32px; font-size: 18px; border-radius: 10px; font-weight: bold;")
        action_btn_layout.addWidget(delete_btn)
        
        # Validate prescription button
        validate_btn = QPushButton("Valider une ordonnance")
        validate_btn.clicked.connect(self.validate_prescription)
        validate_btn.setStyleSheet("background-color: #22c55e; color: white; padding: 16px 32px; font-size: 18px; border-radius: 10px; font-weight: bold;")
        action_btn_layout.addWidget(validate_btn)
 
        # Book Appointment Button
        appointment_btn = QPushButton("PRENDRE RENDEZ-VOUS")
        appointment_btn.clicked.connect(self.handle_appointment_button)
        appointment_btn.setStyleSheet("background-color: #3b82f6; color: white; padding: 16px 32px; font-size: 18px; border-radius: 10px; font-weight: bold;")
        action_btn_layout.addWidget(appointment_btn)
        
        action_btn_layout.addStretch()
        layout.addLayout(action_btn_layout)

    def handle_appointment_button(self):
        """Handle appointment button click, passing selected doctor and current patient data"""
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            nom = self.table.item(selected_row, 1).text()
            prenom = self.table.item(selected_row, 2).text()
            telephone = self.table.item(selected_row, 5).text()
            fullname = f"Dr. {prenom} {nom}"
            
            self.navigate_to_chat.emit(
                fullname, 
                telephone, 
                self.current_patient_name if self.current_patient_name else "Inconnu", 
                self.current_patient_phone if self.current_patient_phone else "Inconnu"
            )
        else:
            QMessageBox.warning(
                self, "Sélection Requise",
                "Veuillez sélectionner un docteur pour prendre rendez-vous."
            )

    def set_patient_info(self, name, phone):
        """Store patient info passed from appointments page"""
        self.current_patient_name = name
        self.current_patient_phone = phone
        QMessageBox.information(self, "Patient Sélectionné", f"Patient actif: {name}")

    def validate_prescription(self):
        """Validate prescription for selected doctor"""
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            nom = self.table.item(selected_row, 1).text()
            prenom = self.table.item(selected_row, 2).text()
            telephone = self.table.item(selected_row, 5).text()
            
            fullname = f"Dr. {prenom} {nom}"
            
            # Emit with patient data (might be empty if came directly)
            self.navigate_to_medications.emit(
                fullname, 
                telephone, 
                self.current_patient_name, 
                self.current_patient_phone
            )
        else:
            QMessageBox.warning(
                self, "Sélection Requise",
                "Veuillez sélectionner un docteur pour valider son ordonnance."
            )

    def load_doctors(self):
        """Load doctors from the backend API"""
        doctors = api_client.get_doctors()
        self.table.setRowCount(0)
        for doctor in doctors:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            # Create items
            # Create items
            # Photo
            photo_widget = QLabel()
            photo_path = doctor.get("photo_path")
            if photo_path and os.path.exists(photo_path):
                pixmap = QPixmap(photo_path)
                photo_widget.setPixmap(pixmap)
                photo_widget.setScaledContents(True) # Zoom to fill content
            else:
                photo_widget.setText("No Img")
            photo_widget.setAlignment(Qt.AlignCenter)
            
            nom_item = QTableWidgetItem(doctor.get("nom", ""))
            prenom_item = QTableWidgetItem(doctor.get("prenom", ""))
            specialite_item = QTableWidgetItem(doctor.get("specialite", ""))
            telephone_item = QTableWidgetItem(doctor.get("telephone", ""))
            email_item = QTableWidgetItem(doctor.get("email", ""))
            role_item = QTableWidgetItem(doctor.get("role", "Non défini"))
            
            # Store ID in UserRole of the first item (Nom)
            nom_item.setData(Qt.UserRole, doctor.get("id"))
            
            self.table.setCellWidget(row, 0, photo_widget)
            self.table.setItem(row, 1, nom_item)
            self.table.setItem(row, 2, prenom_item)
            self.table.setItem(row, 3, role_item)
            self.table.setItem(row, 4, specialite_item)
            self.table.setItem(row, 5, telephone_item)
            self.table.setItem(row, 6, email_item)


    def remove_doctor(self):
        """Delete the selected doctor"""
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            # Get ID from UserRole (Column 1 is now Nom)
            doctor_id = self.table.item(selected_row, 1).data(Qt.UserRole)
            nom = self.table.item(selected_row, 1).text()
            prenom = self.table.item(selected_row, 2).text()
            
            reply = QMessageBox.question(
                self, 'Confirmer la Suppression',
                f"Voulez-vous vraiment supprimer l'utilisateur {prenom} {nom} ?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                if api_client.delete_doctor(doctor_id):
                    self.load_doctors()
                    QMessageBox.information(self, "Succès", "Docteur supprimé avec succès.")
                else:
                    QMessageBox.critical(self, "Erreur", "Impossible de supprimer le docteur.")
        else:
            QMessageBox.warning(
                self, "Sélection Requise",
                "Veuillez sélectionner un docteur dans le tableau avant de le supprimer."
            )

    def add_doctor(self):
        nom = self.nom_input.text().strip()
        prenom = self.prenom_input.text().strip()
        specialite = self.specialite_input.text().strip()
        telephone = self.telephone_input.text().strip()
        email = self.email_input.text().strip()
        role = self.role_input.currentText()

        if nom and prenom:
            doctor_data = {
                "nom": nom,
                "prenom": prenom,
                "specialite": specialite,
                "telephone": telephone,
                "email": email,
                "role": role,
                "photo_path": self.photo_path
            }
            
            result = api_client.create_doctor(doctor_data)
            if result:
                self.load_doctors()
                # Clear inputs
                self.nom_input.clear()
                self.prenom_input.clear()
                self.specialite_input.clear()
                self.telephone_input.clear()
                self.email_input.clear()
                self.photo_label.setText("Aucune photo")
                self.photo_label.setPixmap(QPixmap())
                self.photo_path = None
                QMessageBox.information(self, "Succès", f"Utilisateur {prenom} {nom} ajouté avec succès.")
            else:
                QMessageBox.critical(self, "Erreur", "Impossible d'ajouter le docteur. Vérifiez la connexion au serveur.")
        else:
            QMessageBox.warning(self, "Champs Manquants", "Le nom et le prénom sont obligatoires.")

    def select_photo(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Choisir une Photo", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.photo_path = file_path
            # Allow label to scale the image
            self.photo_label.setPixmap(QPixmap(file_path))

    def take_photo(self):
        dialog = CameraDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            if dialog.captured_image_path:
                self.photo_path = dialog.captured_image_path
                self.photo_label.setPixmap(QPixmap(self.photo_path))
