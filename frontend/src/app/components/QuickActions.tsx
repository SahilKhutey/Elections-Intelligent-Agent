"use client";

import React from 'react';
import { useLanguage } from '../context/LanguageContext';
import { HelpCircle, CheckCircle, Calendar, BookOpen } from 'lucide-react';

interface QuickActionsProps {
  onSelect: (id: string, intent: string) => void;
  actions: string[];
  intents: string[];
}

export default function QuickActions({ onSelect, actions, intents }: QuickActionsProps) {
  const { lang } = useLanguage();

  const getIcon = (index: number) => {
    switch (index) {
      case 0: return <BookOpen className="w-5 h-5 text-[#0B5FFF]" />;
      case 1: return <Calendar className="w-5 h-5 text-[#0B5FFF]" />;
      case 2: return <CheckCircle className="w-5 h-5 text-[#0B5FFF]" />;
      case 3: return <HelpCircle className="w-5 h-5 text-[#0B5FFF]" />;
      default: return <HelpCircle className="w-5 h-5 text-[#0B5FFF]" />;
    }
  };

  const descriptions = {
    en: [
      "Step-by-step process for new voters",
      "Key dates and registration deadlines",
      "Know if you are eligible to vote",
      "Answers to common election queries"
    ],
    hi: [
      "नए मतदाताओं के लिए चरण-दर-चरण प्रक्रिया",
      "महत्वपूर्ण तिथियां और पंजीकरण की समय सीमा",
      "जानें कि क्या आप वोट देने के पात्र हैं",
      "सामान्य चुनावी प्रश्नों के उत्तर"
    ]
  };

  const d = descriptions[lang] || descriptions.en;

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-8">
      {actions.map((action, i) => (
        <button
          key={i}
          onClick={() => onSelect(i === 1 ? 'timeline' : i === 0 ? 'guide' : 'chat', intents[i])}
          className="flex items-start gap-4 p-5 text-left bg-white border border-[#E0E0E0] rounded-xl hover:bg-[#F4F7FE] hover:border-[#0B5FFF]/30 transition-all group focus:ring-2 focus:ring-[#0B5FFF]/20 focus:outline-none"
        >
          <div className="mt-0.5 p-2 rounded-lg bg-[#F4F7FE] group-hover:bg-white transition-colors">
            {getIcon(i)}
          </div>
          <div>
            <p className="font-bold text-[#1A1A1A] group-hover:text-[#0B5FFF] transition-colors">
              {action}
            </p>
            <p className="text-sm text-[#555555] mt-1">
              {d[i]}
            </p>
          </div>
        </button>
      ))}
    </div>
  );
}
