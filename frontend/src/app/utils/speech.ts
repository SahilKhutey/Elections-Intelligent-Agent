/**
 * Utility for text-to-speech synthesis in the Election Intelligence Assistant.
 */

export function speak(text: string, lang: 'en' | 'hi' = 'en') {
  if (typeof window === 'undefined') return;

  // Cancel any ongoing speech
  window.speechSynthesis.cancel();

  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = lang === 'hi' ? 'hi-IN' : 'en-US';
  
  // Professional voice settings
  utterance.rate = 1.0;
  utterance.pitch = 1.0;
  utterance.volume = 1.0;

  window.speechSynthesis.speak(utterance);
}
