import os
import logging
from typing import Dict, Any, List, Optional
from openai import OpenAI

try:
    import google.generativeai as genai
except ImportError:
    genai = None

try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None

from ..config import settings
from .cache import cached

logger = logging.getLogger(__name__)

class AIService:
    """
    Service responsible for context-aware election guidance and AI orchestration.
    
    This service follows a hybrid architecture:
    1. Multi-provider AI (Primary: Gemini/OpenAI/Claude)
    2. Context-aware persona synthesis (Age/Location/Language)
    3. Rule-based fallback for reliability
    """

    def __init__(self) -> None:
        """Initializes AI clients using environment settings."""
        self.openai_key: Optional[str] = settings.OPENAI_API_KEY
        self.gemini_key: Optional[str] = settings.GEMINI_API_KEY
        self.claude_key: Optional[str] = settings.CLAUDE_API_KEY
        
        # Initialize OpenAI
        self.openai_client: Optional[OpenAI] = OpenAI(api_key=self.openai_key) if self.openai_key else None
        
        # Initialize Gemini
        if genai and self.gemini_key:
            genai.configure(api_key=self.gemini_key)
            self.gemini_model = genai.GenerativeModel('gemini-pro')
        else:
            self.gemini_model = None

        # Initialize Anthropic
        self.anthropic_client = Anthropic(api_key=self.claude_key) if Anthropic and self.claude_key else None

    @cached(ttl=600)
    def enhance_explanation(self, query: str, data: Dict[str, Any], context: Dict[str, Any]) -> str:
        """
        Public interface to synthesize structured data into natural language responses.
        
        Args:
            query (str): The user's original natural language question.
            data (Dict[str, Any]): Structured information from the knowledge base.
            context (Dict[str, Any]): Metadata (lang, location, age, provider).
            
        Returns:
            str: A human-friendly, context-aware explanation.
        """
        if not query or len(query.strip()) < 2:
            return self._handle_invalid_query(context.get('lang', 'en'))

        # Defense-in-Depth: Prompt Injection Guard
        if self._is_malicious(query):
            return self._handle_restricted_query(context.get('lang', 'en'))

        try:
            return self._generate_ai_response(query, data, context)
        except Exception as error:
            logger.warning(f"AI generation failed for provider {context.get('provider')}: {error}")
            return self._fallback_response(data, context)

    # ========================
    # INTERNAL METHODS
    # ========================

    def _generate_ai_response(self, query: str, data: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Internal logic for routing to specific AI providers."""
        provider: str = context.get('provider', 'openai').lower()
        lang: str = context.get('lang', 'en')
        age: Optional[int] = context.get('age')
        location: str = context.get('location', 'India')
        
        system_prompt, user_prompt = self._build_prompts(query, data, lang, age, location)

        if provider == "gemini" and self.gemini_model:
            return self._call_gemini(system_prompt, user_prompt)
        elif provider == "claude" and self.anthropic_client:
            return self._call_claude(system_prompt, user_prompt)
        elif self.openai_client:
            return self._call_openai(system_prompt, user_prompt)
        else:
            return self._fallback_response(data, context)

    def _build_prompts(self, query: str, data: Dict[str, Any], lang: str, age: Optional[int], location: str) -> tuple[str, str]:
        """Constructs system and user prompts based on context."""
        # Persona Logic
        if age and int(age) < 18:
            persona = (
                "The user is under 18. Provide an encouraging, educational response. Focus on 'How it works' for future voters."
                if lang == "en" else
                "उपयोगकर्ता 18 वर्ष से कम आयु का है। एक भविष्य के मतदाता के रूप में प्रक्रिया को समझाते हुए शैक्षिक प्रतिक्रिया दें।"
            )
        else:
            persona = (
                "The user is an eligible voter. Provide actionable, clear, and direct steps."
                if lang == "en" else
                "उपयोगकर्ता एक पात्र मतदाता है। कार्रवाई योग्य, स्पष्ट और सीधे कदम प्रदान करें।"
            )

        location_ctx = f"Currently in {location}." if lang == "en" else f"वर्तमान में {location} में हैं।"
        
        system = (
            f"आप एक विशेषज्ञ चुनाव सहायक हैं। {location_ctx} {persona} मित्रवत और मददगार रहें।"
            if lang == "hi" else 
            f"You are an expert election assistant. {location_ctx} {persona} Be friendly and helpful."
        )
        
        user = (
            f"प्रश्न: {query}\nडेटा: {data}\nदर्शक: {age if age else 'General'} वर्ष का नागरिक\nकृपया हिंदी में उत्तर दें।"
            if lang == "hi" else 
            f"Question: {query}\nData: {data}\nAudience: {age if age else 'General'} year old citizen\nPlease respond in English."
        )
        
        return system, user

    def _call_openai(self, system: str, user: str) -> str:
        """Internal helper for OpenAI GPT-3.5/4 completions."""
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            max_tokens=400
        )
        return response.choices[0].message.content.strip()

    def _call_gemini(self, system: str, user: str) -> str:
        """Internal helper for Google Gemini-Pro generations."""
        full_prompt = f"{system}\n\n{user}"
        response = self.gemini_model.generate_content(full_prompt)
        return response.text.strip()

    def _call_claude(self, system: str, user: str) -> str:
        """Internal helper for Anthropic Claude-3 generations."""
        response = self.anthropic_client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=400,
            system=system,
            messages=[{"role": "user", "content": user}]
        )
        return response.content[0].text.strip()

    def _is_malicious(self, query: str) -> bool:
        """Detects prompt injection attempts."""
        blocked = ["ignore previous", "system prompt", "bypass", "jailbreak", "developer mode"]
        return any(p in query.lower() for p in blocked)

    def _handle_invalid_query(self, lang: str) -> str:
        return "Please enter a valid question." if lang == "en" else "कृपया एक मान्य प्रश्न दर्ज करें।"

    def _handle_restricted_query(self, lang: str) -> str:
        return "I cannot process this request due to safety restrictions." if lang == "en" else "सुरक्षा प्रतिबंधों के कारण मैं इस अनुरोध को संसाधित नहीं कर सकता।"

    def _fallback_response(self, data: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Rule-based fallback if AI synthesis fails."""
        lang = context.get('lang', 'en')
        if lang == "hi":
            return "यहाँ आपके लिए कुछ जानकारी दी गई है।"
        return "Here is some information I found in our official database."

# Singleton instance for reuse
ai_service = AIService()
