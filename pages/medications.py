from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QHeaderView, QLineEdit, QSpinBox, QFormLayout, QGroupBox, QGridLayout,
    QMessageBox, QComboBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from datetime import datetime
import os
import api_client

# ReportLab imports for professional PDF
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

class MedicationsPage(QWidget):
    # Signals to navigate to SMS and WhatsApp pages: (phone, patient_name, patient_prenom, message)
    request_sms = pyqtSignal(str, str, str, str, str)
    request_whatsapp = pyqtSignal(str, str, str, str, str)
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_medications()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 5, 30, 10)

        # Title & Date Row
        header_layout = QHBoxLayout()
        
        title = QLabel("📋 Ordonnance Médicale")
        title.setFont(QFont("Times New Roman", 22, QFont.Bold))
        title.setAlignment(Qt.AlignLeft)
        
        date_label = QLabel(f"Date: {datetime.now().strftime('%d/%m/%Y')}")
        date_label.setFont(QFont("Times New Roman", 15))
        date_label.setAlignment(Qt.AlignRight)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(date_label)
        
        layout.addLayout(header_layout)
        layout.addSpacing(5)

        # Form Group for Medication
        form_group = QGroupBox("Ajouter un Médicament")
        form_group.setFont(QFont("Times New Roman", 15, QFont.Bold))
        grid_layout = QGridLayout()
        grid_layout.setSpacing(15)
        
        # Input fields
        # Input fields
        # Doctor Info (Read-Only)
        self.doc_name = QLineEdit()
        self.doc_name.setPlaceholderText("Nom du Docteur (Non modifiable)")
        self.doc_name.setReadOnly(True)
        self.doc_name.setStyleSheet("background-color: #f0f0f0; color: #555;")
        
        self.doc_phone = QLineEdit()
        self.doc_phone.setPlaceholderText("Téléphone (Non modifiable)")
        self.doc_phone.setReadOnly(True)
        self.doc_phone.setStyleSheet("background-color: #f0f0f0; color: #555;")
        
        # Patient Info (Read-Only)
        self.pat_name = QLineEdit()
        self.pat_name.setPlaceholderText("Nom du Patient (Non modifiable)")
        self.pat_name.setReadOnly(True)
        self.pat_name.setStyleSheet("background-color: #f0f0f0; color: #555;")
        
        self.pat_phone = QLineEdit()
        self.pat_phone.setPlaceholderText("Téléphone (Non modifiable)")
        self.pat_phone.setReadOnly(True)
        self.pat_phone.setStyleSheet("background-color: #f0f0f0; color: #555;")

        self.nom_produit = QLineEdit()
        self.nom_produit.setPlaceholderText("Ex: Paracétamol, Amoxicilline, etc.")
        
        self.dose_input = QLineEdit()
        self.dose_input.setPlaceholderText("Ex: 500mg, 2 comprimés, 5ml, etc.")
        
        self.quantite_input = QSpinBox()
        self.quantite_input.setMinimum(1)
        self.quantite_input.setMaximum(999)
        self.quantite_input.setValue(1)
        self.quantite_input.setSuffix(" unité(s)")
        
        # Add fields to grid (2 per row)
        # Row 0: Doctor Info
        grid_layout.addWidget(QLabel("DOCTEUR PRESENT:"), 0, 0)
        grid_layout.addWidget(self.doc_name, 0, 1)
        grid_layout.addWidget(QLabel("CONTACT DOCTEUR:"), 0, 2)
        grid_layout.addWidget(self.doc_phone, 0, 3)

        # Row 1: Patient Info
        grid_layout.addWidget(QLabel("PATIENT:"), 1, 0)
        grid_layout.addWidget(self.pat_name, 1, 1)
        grid_layout.addWidget(QLabel("CONTACT PATIENT:"), 1, 2)
        grid_layout.addWidget(self.pat_phone, 1, 3)
        
        # Row 2: Nom du Produit & Dose / Posologie
        grid_layout.addWidget(QLabel("NOM DU PRODUIT :"), 2, 0)
        grid_layout.addWidget(self.nom_produit, 2, 1)
        grid_layout.addWidget(QLabel("DOSE / POSOLOGIE :"), 2, 2)
        grid_layout.addWidget(self.dose_input, 2, 3)

        grid_layout.addWidget(QLabel("QUANTITE :"), 3, 0)
        grid_layout.addWidget(self.quantite_input, 3, 1)
        
        form_group.setLayout(grid_layout)
        layout.addWidget(form_group)
        layout.addSpacing(5)
        
        # Action buttons
        btn_layout = QHBoxLayout()
        # Use addStretch to center/group buttons without full expansion
        btn_layout.addStretch()
        
        add_btn = QPushButton("➕ AJOUTER LE PRODUIT")
        add_btn.clicked.connect(self.add_medication)
        add_btn.setObjectName("primaryButton")
        
        add_btn = QPushButton("➕ AJOUTER LE PRODUIT")
        add_btn.clicked.connect(self.add_medication)
        add_btn.setObjectName("primaryButton")
        
        remove_btn = QPushButton("🗑️ RETIRER LE PRODUIT")
        remove_btn.clicked.connect(self.remove_medication)
        remove_btn.setObjectName("secondaryButton")
        
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(remove_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        layout.addSpacing(10)

        # Table to display medications (ordonnance)
        ordonnance_label = QLabel("📄 LISTE DES PRODUITS PRESCRITS")
        ordonnance_label.setFont(QFont("Times New Roman", 16, QFont.Bold))
        layout.addWidget(ordonnance_label)
        layout.addSpacing(8)
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["N°", "NOM PRODUITS", "DOSE / POSOLOGIE", "QUANTITE"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setColumnWidth(0, 50)  # N° column narrower
        layout.addWidget(self.table)
        layout.addSpacing(10)
        
        # SMS and WhatsApp reminder buttons
        reminder_layout = QHBoxLayout()
        reminder_layout.addStretch()
        
        self.sms_btn = QPushButton("📱 ENVOYER UN RAPPEL PAR SMS")
        self.sms_btn.clicked.connect(self.send_sms_reminder)
        self.sms_btn.setObjectName("primaryButton")
        
        self.whatsapp_btn = QPushButton("💬 ENVOYER UN RAPPEL PAR WHATSAPP")
        self.whatsapp_btn.clicked.connect(self.send_whatsapp_reminder)
        self.whatsapp_btn.setObjectName("primaryButton")
        
        reminder_layout.addWidget(self.sms_btn)
        reminder_layout.addWidget(self.whatsapp_btn)
        reminder_layout.addStretch()
        layout.addLayout(reminder_layout)

    def load_medications(self):
        """Load medications from the backend API"""
        meds = api_client.get_medications()
        self.table.setRowCount(0)
        for i, med in enumerate(meds):
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            # Store ID in UserRole
            num_item = QTableWidgetItem(str(i + 1))
            num_item.setTextAlignment(Qt.AlignCenter)
            num_item.setData(Qt.UserRole, med.get("id"))
            
            self.table.setItem(row, 0, num_item)
            
            self.table.setItem(row, 1, QTableWidgetItem(med.get("nom_produit", "")))
            self.table.setItem(row, 2, QTableWidgetItem(med.get("dose", "")))
            
            quantite_item = QTableWidgetItem(str(med.get("quantite", "")))
            quantite_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 3, quantite_item)

    def add_medication(self):
        nom = self.nom_produit.text().strip()
        dose = self.dose_input.text().strip()
        quantite = self.quantite_input.value()
        if nom and dose:
            medication_data = {
                "nom_produit": nom,
                "dose": dose,
                "quantite": quantite,
                "date_prescription": datetime.now().strftime('%d/%m/%Y')
            }
            
            result = api_client.create_medication(medication_data)
            if result:
                self.load_medications()
                # Clear inputs
                self.nom_produit.clear()
                self.dose_input.clear()
                self.quantite_input.setValue(1)
                QMessageBox.information(self, "Succès", f"Médicament {nom} ajouté à l'ordonnance.")
            else:
                QMessageBox.critical(self, "Erreur", "Impossible d'ajouter le médicament.")
        else:
            QMessageBox.warning(self, "Champs Manquants", "Le nom du produit et la dose sont obligatoires.")
    
    def remove_medication(self):
        """Remove selected medication from the prescription"""
        current_row = self.table.currentRow()
        
        if current_row >= 0:
            # Confirmation dialog
            reply = QMessageBox.question(
                self, 'Confirmer la Suppression',
                f"Voulez-vous vraiment retirer ce médicament de l'ordonnance ?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                # Get ID from UserRole
                med_id = self.table.item(current_row, 0).data(Qt.UserRole)
                
                if med_id:
                    if api_client.delete_medication(med_id):
                        self.load_medications()
                        QMessageBox.information(self, "Succès", "Médicament supprimé de la base de données.")
                    else:
                        QMessageBox.critical(self, "Erreur", "Impossible de supprimer le médicament de la base de données.")
                else:
                    # If no ID, just remove from table (shouldn't happen with reloads)
                    self.table.removeRow(current_row)
                    self.renumber_rows()
        else:
            QMessageBox.warning(
                self, 'Aucune Sélection',
                "Veuillez sélectionner un médicament dans le tableau avant de le retirer."
            )
    
    def renumber_rows(self):
        """Renumber all rows in the table after deletion"""
        for row in range(self.table.rowCount()):
            num_item = QTableWidgetItem(str(row + 1))
            num_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 0, num_item)
    
    def send_sms_reminder(self):
        """Send SMS reminder for medication"""
        # Get all medications from table
        medications_list = []
        for row in range(self.table.rowCount()):
            nom = self.table.item(row, 1).text()
            dose = self.table.item(row, 2).text()
            medications_list.append(f"- {nom}: {dose}")
        
        if medications_list:
            message = "Rappel de prise de médicaments:\n" + "\n".join(medications_list)
            phone = self.pat_phone.text().strip()
            # Split patient name if possible, or just send full name
            full_name = self.pat_name.text().strip()
            parts = full_name.split(" ", 1)
            nom = parts[0]
            prenom = parts[1] if len(parts) > 1 else ""
            
            doc_name = self.doc_name.text().strip()
            self.request_sms.emit(phone, nom, prenom, message, doc_name)
        else:
            QMessageBox.warning(
                self, 'Aucun Médicament',
                "Veuillez ajouter au moins un médicament avant d'envoyer un rappel."
            )

    def set_prescription_data(self, doc_name, doc_phone, pat_name, pat_phone):
        """Update doctor and patient information fields"""
        self.doc_name.setText(doc_name)
        self.doc_phone.setText(doc_phone)
        self.pat_name.setText(pat_name)
        self.pat_phone.setText(pat_phone)
    
    def send_whatsapp_reminder(self):
        """Send WhatsApp reminder for medication"""
        # Get all medications from table
        medications_list = []
        for row in range(self.table.rowCount()):
            nom = self.table.item(row, 1).text()
            dose = self.table.item(row, 2).text()
            medications_list.append(f"- {nom}: {dose}")
        
        if medications_list:
            message = "Rappel de prise de médicaments:\n" + "\n".join(medications_list)
            phone = self.pat_phone.text().strip()
            full_name = self.pat_name.text().strip()
            parts = full_name.split(" ", 1)
            nom = parts[0]
            prenom = parts[1] if len(parts) > 1 else ""

            doc_name = self.doc_name.text().strip()
            self.request_whatsapp.emit(phone, nom, prenom, message, doc_name)
        else:
            QMessageBox.warning(
                self, 'Aucun Médicament',
                "Veuillez ajouter au moins un médicament avant d'envoyer un rappel."
            )

    def generate_pdf(self, validity):
        """Generates the professional PDF for the current prescription"""
        if self.table.rowCount() == 0:
            return False, "Ordonnance Vide: Veuillez ajouter au moins un produit."
            
        if validity == 0:
            return False, "Validité Requise: Veuillez définir une validité supérieure à 0."

        # Prepare Data for PDF
        patient_name = self.pat_name.text()
        doctor_name = self.doc_name.text()
        doctor_phone = self.doc_phone.text()
        current_date = datetime.now().strftime('%d/%m/%Y')
        
        # PDF filename
        pdf_dir = "prescriptions"
        if not os.path.exists(pdf_dir):
            os.makedirs(pdf_dir)
        filename = f"{pdf_dir}/ordonnance_{patient_name.replace(' ', '_')}_{int(datetime.now().timestamp())}.pdf"

        try:
            # Generate PDF
            doc = SimpleDocTemplate(filename, pagesize=A4)
            styles = getSampleStyleSheet()
            elements = []

            # Custom Styles
            title_style = ParagraphStyle('Title', parent=styles['Heading1'], alignment=1, fontSize=24, spaceAfter=20, textColor=colors.navy)
            header_style = ParagraphStyle('Header', parent=styles['Normal'], fontSize=12, leading=14)
            
            # Header: Hospital Info
            elements.append(Paragraph("🏥 HÔPITAL CENTRAL - DAKAR", title_style))
            elements.append(Spacer(1, 12))
            
            # Doctor & Patient Info
            info_data = [
                [Paragraph(f"<b>DOCTEUR:</b> {doctor_name}", header_style), Paragraph(f"<b>DATE:</b> {current_date}", header_style)],
                [Paragraph(f"<b>CONTACT:</b> {doctor_phone}", header_style), Paragraph(f"<b>PATIENT:</b> {patient_name}", header_style)]
            ]
            info_table = Table(info_data, colWidths=[250, 250])
            info_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
            elements.append(info_table)
            elements.append(Spacer(1, 30))
            
            elements.append(Paragraph("<u>PRESCRIPTION MÉDICALE</u>", styles['Heading2']))
            elements.append(Spacer(1, 15))
            
            # Medications Table
            table_data = [["N°", "MÉDICAMENT", "POSOLOGIE", "QUANTITÉ"]]
            for row in range(self.table.rowCount()):
                num = self.table.item(row, 0).text()
                nom = self.table.item(row, 1).text()
                poso = self.table.item(row, 2).text()
                qty = self.table.item(row, 3).text()
                table_data.append([num, nom, poso, qty])
            
            med_table = Table(table_data, colWidths=[40, 200, 180, 80])
            med_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.navy),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.white])
            ]))
            elements.append(med_table)
            elements.append(Spacer(1, 40))
            
            # Validity & Signature
            elements.append(Paragraph(f"<b>Validité de cette ordonnance :</b> {validity} jours", header_style))
            elements.append(Spacer(1, 60))
            
            sig_data = [["", "Cachet et Signature du Docteur"]]
            sig_table = Table(sig_data, colWidths=[300, 200])
            sig_table.setStyle(TableStyle([
                ('ALIGN', (1,0), (1,0), 'CENTER'),
                ('LINEABOVE', (1,0), (1,0), 1, colors.black)
            ]))
            elements.append(sig_table)
            
            # Build PDF
            doc.build(elements)

            # Open PDF
            os.startfile(os.path.abspath(filename))
            return True, filename

        except Exception as e:
            return False, str(e)

    def clear_data(self):
        """Clears the prescription data from backend and UI"""
        if api_client.clear_medications():
            self.load_medications()
            self.nom_produit.clear()
            self.dose_input.clear()
            return True
        return False
