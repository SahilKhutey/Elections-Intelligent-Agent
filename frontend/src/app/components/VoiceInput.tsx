"use client";

import React, { useState, useEffect } from 'react';
import { Mic, MicOff, Loader2 } from 'lucide-react';

interface VoiceInputProps {
  onResult: (text: string) => void;
  lang: 'en' | 'hi';
}

export default function VoiceInput({ onResult, lang }: VoiceInputProps) {
  const [isListening, setIsListening] = useState(false);
  const [isSupported, setIsSupported] = useState(true);

  useEffect(() => {
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRecognition) {
      setIsSupported(false);
    }
  }, []);

  const startListening = () => {
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRecognition) return;

    const recognition = new SpeechRecognition();
    recognition.lang = lang === 'hi' ? 'hi-IN' : 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onstart = () => {
      setIsListening(true);
    };

    recognition.onresult = (event: any) => {
      const transcript = event.results[0][0].transcript;
      onResult(transcript);
      setIsListening(false);
    };

    recognition.onerror = (event: any) => {
      console.error('Speech recognition error:', event.error);
      setIsListening(false);
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    recognition.start();
  };

  if (!isSupported) return null;

  return (
    <button
      onClick={startListening}
      disabled={isListening}
      className={`relative flex items-center justify-center w-11 h-11 rounded-xl transition-all duration-300 ${
        isListening 
          ? 'bg-[#D32F2F] text-white shadow-lg shadow-red-200 animate-pulse' 
          : 'bg-[#F4F7FE] text-[#0B5FFF] hover:bg-[#0B5FFF] hover:text-white border border-[#0B5FFF]/10'
      }`}
      title={lang === 'hi' ? 'बोलें' : 'Speak'}
    >
      {isListening ? (
        <div className="relative">
          <Loader2 className="w-5 h-5 animate-spin opacity-20 absolute inset-0" />
          <Mic className="w-5 h-5 relative z-10" />
        </div>
      ) : (
        <Mic className="w-5 h-5" />
      )}
      
      {isListening && (
        <span className="absolute -top-1 -right-1 flex h-3 w-3">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
          <span className="relative inline-flex rounded-full h-3 w-3 bg-red-500"></span>
        </span>
      )}
    </button>
  );
}
