import os
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

class AIService:
    """
    Core AI Service responsible for generating context-aware election guidance.
    Supports OpenAI, Google Gemini, and Anthropic Claude providers.
    """
    def __init__(self):
        self.openai_key = settings.OPENAI_API_KEY
        self.gemini_key = settings.GEMINI_API_KEY
        self.claude_key = settings.CLAUDE_API_KEY
        
        # Initialize OpenAI
        self.openai_client = OpenAI(api_key=self.openai_key) if self.openai_key else None
        
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
        Enhances raw data explanations with audience-aware natural language synthesis.
        """
        provider = context.get('provider', 'openai').lower()
        lang = context.get('lang', 'en')
        age = context.get('age')
        location = context.get('location', 'India')
        
        # Determine persona based on age
        persona_guide = ""
        if age and int(age) < 18:
            persona_guide = (
                "The user is under 18. Provide an encouraging, educational response explaining the process as a future voter. Focus on 'How it works' rather than 'How to do it now'."
                if lang == "en" else
                "उपयोगकर्ता 18 वर्ष से कम आयु का है। एक भविष्य के मतदाता के रूप में प्रक्रिया को समझाते हुए एक उत्साहजनक, शैक्षिक प्रतिक्रिया प्रदान करें।"
            )
        else:
            persona_guide = (
                "The user is an eligible voter. Provide actionable, clear, and direct steps."
                if lang == "en" else
                "उपयोगकर्ता एक पात्र मतदाता है। कार्रवाई योग्य, स्पष्ट और सीधे कदम प्रदान करें।"
            )

        location_context = (
            f"You are currently in {location}."
            if lang == "en" else
            f"आप वर्तमान में {location} में हैं।"
        )

        system_prompt = (
            f"आप एक विशेषज्ञ चुनाव सहायक हैं। {location_context} {persona_guide} मित्रवत और मददगार रहें।"
            if lang == "hi" else 
            f"You are an expert election assistant. {location_context} {persona_guide} Be friendly and helpful."
        )
        
        user_prompt = (
            f"प्रश्न: {query}\nडेटा: {data}\nदर्शक: {age} वर्ष का नागरिक\nकृपया हिंदी में उत्तर दें।"
            if lang == "hi" else 
            f"Question: {query}\nData: {data}\nAudience: {age} year old citizen\nPlease respond in English."
        )

        try:
            if provider == "gemini" and self.gemini_model:
                return self._call_gemini(system_prompt, user_prompt)
            elif provider == "claude" and self.anthropic_client:
                return self._call_claude(system_prompt, user_prompt)
            elif self.openai_client:
                return self._call_openai(system_prompt, user_prompt)
            else:
                return self._format_fallback(data, context)
        except Exception as e:
            print(f"AI Provider Error ({provider}): {e}")
            return self._format_fallback(data, context)

    def _call_openai(self, system: str, user: str) -> str:
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user}
            ],
            max_tokens=400
        )
        return response.choices[0].message.content.strip()

    def _call_gemini(self, system: str, user: str) -> str:
        full_prompt = f"{system}\n\n{user}"
        response = self.gemini_model.generate_content(full_prompt)
        return response.text.strip()

    def _call_claude(self, system: str, user: str) -> str:
        response = self.anthropic_client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=400,
            system=system,
            messages=[
                {"role": "user", "content": user}
            ]
        )
        # Handle response content which is a list of content blocks
        return response.content[0].text.strip()

    def _format_fallback(self, data: Dict[str, Any], context: Dict[str, Any]) -> str:
        lang = context.get('lang', 'en')
        if lang == "hi":
            return "यहाँ आपके लिए कुछ जानकारी दी गई है।"
        return "Here is some information I found."

ai_service = AIService()

