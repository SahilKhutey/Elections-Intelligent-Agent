from typing import Dict, Any, List

class TranslationService:
    def __init__(self):
        self.translations = {
            "en": {
                "welcome": "Hi! I'm your Election Assistant. Ask me anything about voting!",
                "register_to_vote": "Register to vote",
                "verify_identity": "Verify your identity",
                "find_polling_booth": "Find your polling booth",
                "cast_vote": "Cast your vote",
                "voter_id": "Voter ID card",
                "photo_id": "Government photo ID",
                "address_proof": "Proof of address",
                "voting_day": "Voting Day",
                "results_day": "Results Declaration"
            },
            "hi": {
                "welcome": "नमस्ते! मैं आपका चुनाव सहायक हूँ। मतदान के बारे में कुछ भी पूछें!",
                "register_to_vote": "मतदाता के रूप में पंजीकरण करें",
                "verify_identity": "अपनी पहचान सत्यापित करें",
                "find_polling_booth": "अपना मतदान केंद्र ढूंढें",
                "cast_vote": "अपना वोट डालें",
                "voter_id": "मतदाता पहचान पत्र",
                "photo_id": "सरकारी फोटो आईडी",
                "address_proof": "पता प्रमाण",
                "voting_day": "मतदान दिवस",
                "results_day": "परिणाम घोषणा"
            }
        }
    
    def translate_text(self, text: str, lang: str = "en") -> str:
        if lang == "en" or lang not in self.translations:
            return text
        return self.translations[lang].get(text.lower().replace(" ", "_"), text)

    def translate_response(self, data: Any, lang: str = "en") -> Any:
        """Recursive dictionary translation engine"""
        if lang == "en":
            return data
        
        if isinstance(data, dict):
            return {k: self.translate_response(v, lang) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.translate_response(item, lang) for item in data]
        elif isinstance(data, str):
            # Attempt to translate known terms
            lookup_key = data.lower().replace(" ", "_")
            return self.translations[lang].get(lookup_key, data)
        return data

translation_service = TranslationService()
