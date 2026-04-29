"use client";

import React, { useState } from 'react';
import { useLanguage } from '../context/LanguageContext';
import { ArrowLeft, ArrowRight, CheckCircle2, Circle } from 'lucide-react';

const GUIDE_DATA = {
  en: [
    { title: "Check Registration", desc: "Verify if your name is on the electoral roll. Use the official ECI portal or helpline.", icon: "🔍" },
    { title: "Identify Your Booth", desc: "Locate your assigned polling station near your residence.", icon: "📍" },
    { title: "Verify with ID", desc: "Bring your Voter ID (EPIC) or any other approved government photo identity.", icon: "🆔" },
    { title: "Mark & Vote", desc: "Get your finger marked and cast your vote securely on the EVM.", icon: "🗳️" }
  ],
  hi: [
    { title: "पंजीकरण जांचें", desc: "जांचें कि क्या आपका नाम मतदाता सूची में है। आधिकारिक चुनाव आयोग पोर्टल का उपयोग करें।", icon: "🔍" },
    { title: "अपने बूथ की पहचान करें", desc: "अपने निवास के पास अपने निर्दिष्ट मतदान केंद्र का पता लगाएं।", icon: "📍" },
    { title: "आईडी से सत्यापित करें", desc: "अपना वोटर आईडी (EPIC) या कोई अन्य स्वीकृत सरकारी फोटो पहचान पत्र लाएं।", icon: "🆔" },
    { title: "निशान और वोट", desc: "अपनी उंगली पर निशान लगवाएं और EVM पर सुरक्षित रूप से अपना वोट डालें।", icon: "🗳️" }
  ]
};

const StepByStepGuide: React.FC = () => {
  const { lang } = useLanguage();
  const [step, setStep] = useState(0);
  const steps = GUIDE_DATA[lang];

  return (
    <div className="bg-white rounded-2xl animate-fade-in relative overflow-hidden">
      <div className="absolute top-0 right-0 p-8 opacity-5 pointer-events-none">
        <div className="text-9xl">{steps[step].icon}</div>
      </div>
      
      <div className="relative z-10">
        <div className="flex gap-2 mb-8">
          {steps.map((_, i) => (
            <div key={i} className={`h-1.5 flex-1 rounded-full transition-all duration-500 ${i <= step ? 'bg-[#0B5FFF]' : 'bg-[#E0E0E0]'}`} />
          ))}
        </div>

        <div className="min-h-[180px]">
          <span className="text-[#0B5FFF] font-bold text-xs tracking-widest uppercase mb-2 block">Step {step + 1} of {steps.length}</span>
          <h2 className="text-3xl font-bold mb-4 text-[#1A1A1A]">{steps[step].title}</h2>
          <p className="text-[#555555] text-lg leading-relaxed max-w-xl">{steps[step].desc}</p>
        </div>

        <div className="flex justify-between items-center mt-12 pt-8 border-t border-[#E0E0E0]">
          <button
            onClick={() => setStep(s => Math.max(0, s - 1))}
            disabled={step === 0}
            className="flex items-center gap-2 px-6 py-3 rounded-xl hover:bg-gray-100 disabled:opacity-20 transition-all text-[#555555] font-bold text-sm uppercase tracking-wider"
          >
            <ArrowLeft className="w-4 h-4" /> {lang === 'en' ? 'Back' : 'पीछे'}
          </button>

          <div className="flex gap-3">
            {steps.map((_, i) => (
              <div key={i} onClick={() => setStep(i)} className="cursor-pointer group">
                {i <= step ? <CheckCircle2 className="w-5 h-5 text-[#0B5FFF]" /> : <Circle className="w-5 h-5 text-[#E0E0E0] group-hover:text-[#555555] transition-colors" />}
              </div>
            ))}
          </div>

          <button
            onClick={() => setStep(s => Math.min(steps.length - 1, s + 1))}
            disabled={step === steps.length - 1}
            className="flex items-center gap-2 px-8 py-3 rounded-xl bg-[#0B5FFF] hover:bg-[#084ACC] disabled:opacity-20 transition-all text-white font-bold shadow-lg shadow-[#0B5FFF]/10 text-sm uppercase tracking-wider"
          >
            {lang === 'en' ? 'Next' : 'आगे'} <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default StepByStepGuide;
