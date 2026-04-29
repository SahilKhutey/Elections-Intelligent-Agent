"use client";

import React from 'react';
import { useLanguage } from '../context/LanguageContext';

export default function Intro() {
  const { lang } = useLanguage();

  const content = {
    en: {
      title: "Understand the Election Process",
      description: "Get verified information on how to register, check your eligibility, and participate in the world's largest democratic process. Our AI assistant provides direct answers based on official guidelines."
    },
    hi: {
      title: "चुनाव प्रक्रिया को समझें",
      description: "दुनिया की सबसे बड़ी लोकतांत्रिक प्रक्रिया में पंजीकरण कैसे करें, अपनी पात्रता की जांच कैसे करें और भाग कैसे लें, इस पर सत्यापित जानकारी प्राप्त करें। हमारा एआई सहायक आधिकारिक दिशानिर्देशों के आधार पर सीधे उत्तर प्रदान करता है।"
    }
  };

  const t = content[lang] || content.en;

  return (
    <section className="mb-8 animate-fade-in" aria-labelledby="intro-title">
      <h2 id="intro-title" className="text-3xl font-bold text-[#1A1A1A] mb-3 tracking-tight">
        {t.title}
      </h2>
      <p className="text-[#555555] text-lg leading-relaxed max-w-3xl">
        {t.description}
      </p>
    </section>
  );
}
