import os
import webbrowser
import urllib.parse

class MessagingService:
    @staticmethod
    def send_sms(to_number, message_body):
        """Opens the system's default SMS app with the pre-filled message"""
        try:
            # Clean number
            clean_to = to_number.replace(" ", "").replace("-", "").replace(".", "")
            # Encode the message for a URL
            encoded_msg = urllib.parse.quote(message_body)
            # Use sms: URI scheme
            sms_url = f"sms:{clean_to}?body={encoded_msg}"
            
            print(f"Opening SMS composer for: {clean_to}")
            webbrowser.open(sms_url)
            return True, "SMS Application Opened"
        except Exception as e:
            print(f"Error opening SMS browser: {e}")
            return False, str(e)

    @staticmethod
    def send_whatsapp(to_number, message_body):
        """Opens WhatsApp (Web or Desktop) with the pre-filled message"""
        try:
            # Clean number: Remove spaces and other common separators
            clean_to = to_number.replace(" ", "").replace("-", "").replace(".", "").replace("+", "")
            # Encode the message for a URL
            encoded_msg = urllib.parse.quote(message_body)
            # Use WhatsApp Public API link
            wa_url = f"https://wa.me/{clean_to}?text={encoded_msg}"
            
            print(f"Opening WhatsApp for: {clean_to}")
            webbrowser.open(wa_url)
            return True, "WhatsApp Window Opened"
        except Exception as e:
            print(f"Error opening WhatsApp browser: {e}")
            return False, str(e)
