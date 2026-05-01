from typing import Dict, Any, List, Optional
try:
    from google.cloud import translate_v2 as translate
except ImportError:
    translate = None

class TranslationService:
    """
    Multilingual Orchestration Service.
    Supports local dictionary-based mapping and Google Cloud Translation API.
    """
    def __init__(self):
        self.translate_client = None
        try:
            if translate:
                self.translate_client = translate.Client()
        except Exception:
            self.translate_client = None

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
        """
        Translates a single string into the target language.
        Prioritizes Google Cloud Translate, falls back to local dictionary.
        """
        if lang == "en":
            return text

        # 1. Try Google Cloud Translate
        if self.translate_client:
            try:
                result = self.translate_client.translate(text, target_language=lang)
                return result["translatedText"]
            except Exception:
                pass

        # 2. Fallback to Local Dictionary
        lookup_key = text.lower().replace(" ", "_")
        return self.translations.get(lang, {}).get(lookup_key, text)

    def translate_response(self, data: Any, lang: str = "en") -> Any:
        """
        Recursively translates complex data structures (dicts, lists).
        """
        if lang == "en":
            return data
        
        if isinstance(data, dict):
            return {k: self.translate_response(v, lang) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.translate_response(item, lang) for item in data]
        elif isinstance(data, str):
            return self.translate_text(data, lang)
        return data

translation_service = TranslationService()
