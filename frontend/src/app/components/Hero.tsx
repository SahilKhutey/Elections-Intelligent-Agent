"use client";

import React from 'react';
import { useLanguage } from '../context/LanguageContext';

export default function Hero() {
  const { lang } = useLanguage();

  return (
    <div className="mb-8 animate-fade-in">
      <h2 className="text-3xl font-bold tracking-tight mb-2">
        {lang === "hi"
          ? "मैं आपकी चुनाव प्रक्रिया समझने में मदद कर सकता हूँ"
          : "I can help you understand the election process"}
      </h2>

      <p className="text-[#9CA3AF] text-lg">
        {lang === "hi"
          ? "प्रश्न पूछें या नीचे से विकल्प चुनें"
          : "Ask a question or choose an option below"}
      </p>
    </div>
  );
}
