"use client";

import React from 'react';
import { useLanguage } from '../context/LanguageContext';

const LanguageToggle: React.FC = () => {
  const { lang, setLang } = useLanguage();

  return (
    <div className="flex bg-white/5 border border-white/10 p-1 rounded-xl">
      <button
        onClick={() => setLang('en')}
        className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
          lang === 'en' ? 'bg-blue-600 text-white shadow-lg' : 'text-slate-400 hover:text-white'
        }`}
      >
        EN
      </button>
      <button
        onClick={() => setLang('hi')}
        className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
          lang === 'hi' ? 'bg-blue-600 text-white shadow-lg' : 'text-slate-400 hover:text-white'
        }`}
      >
        HI
      </button>
    </div>
  );
};

export default LanguageToggle;
