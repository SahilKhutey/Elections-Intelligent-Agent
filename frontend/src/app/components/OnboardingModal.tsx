"use client";

import React, { useState } from 'react';
import { User, MapPin, ArrowRight } from 'lucide-react';
import { useUser } from '../context/UserContext';
import { useLanguage } from '../context/LanguageContext';

export default function OnboardingModal() {
  const { updateUser, initSession } = useUser();
  const { lang } = useLanguage();
  const [age, setAge] = useState("");
  const [location, setLocation] = useState("India");
  const [isCitizen, setIsCitizen] = useState(true);
  const [isResident, setIsResident] = useState(true);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!age) return;
    updateUser({ 
      age: parseInt(age), 
      location, 
      is_citizen: isCitizen, 
      is_resident: isResident,
      onboarded: true 
    });
    
    // Create secure session
    setTimeout(() => {
       initSession();
    }, 100);
  };

  return (
    <div className="fixed inset-0 z-[200] flex items-center justify-center p-4 bg-[#1A1A1A]/40 backdrop-blur-sm animate-fade-in">
      <div className="bg-white border border-[#E0E0E0] rounded-3xl p-10 max-w-md w-full shadow-2xl relative overflow-hidden">
        {/* Subtle Decoration */}
        <div className="absolute -top-24 -right-24 w-48 h-48 bg-[#0B5FFF]/5 rounded-full blur-3xl"></div>
        <div className="absolute -bottom-24 -left-24 w-48 h-48 bg-[#2E7D32]/5 rounded-full blur-3xl"></div>

        <div className="relative z-10">
          <div className="w-14 h-14 bg-[#0B5FFF] rounded-2xl flex items-center justify-center mb-8 shadow-lg shadow-[#0B5FFF]/10">
            <User className="w-7 h-7 text-white" />
          </div>

          <h2 className="text-3xl font-bold mb-3 tracking-tight text-[#1A1A1A]">
            {lang === "hi" ? "आपका स्वागत है!" : "Welcome!"}
          </h2>
          <p className="text-[#555555] mb-8 leading-relaxed font-medium">
            {lang === "hi" 
              ? "बेहतर चुनावी मार्गदर्शन और पात्रता जाँच के लिए कृपया अपनी जानकारी साझा करें।" 
              : "Please share a few details to personalize your election guidance and check your eligibility."}
          </p>

          <form onSubmit={handleSubmit} className="space-y-5">
            <div className="space-y-2">
              <label className="text-xs font-bold text-[#555555] uppercase tracking-wider px-1 flex items-center gap-2">
                <User className="w-3.5 h-3.5" /> {lang === "hi" ? "आपकी उम्र" : "Your Age"}
              </label>
              <input
                required
                type="number"
                placeholder="e.g. 24"
                value={age}
                onChange={(e) => setAge(e.target.value)}
                className="w-full bg-white border border-[#E0E0E0] rounded-xl py-4 px-6 focus:outline-none focus:border-[#0B5FFF] focus:ring-4 focus:ring-[#0B5FFF]/5 transition-all text-[#1A1A1A] text-lg font-medium"
              />
            </div>

            <div className="space-y-2">
              <label className="text-xs font-bold text-[#555555] uppercase tracking-wider px-1 flex items-center gap-2">
                <MapPin className="w-3.5 h-3.5" /> {lang === "hi" ? "आपका स्थान" : "Your Location"}
              </label>
              <select
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                className="w-full bg-white border border-[#E0E0E0] rounded-xl py-4 px-6 focus:outline-none focus:border-[#0B5FFF] focus:ring-4 focus:ring-[#0B5FFF]/5 transition-all text-[#1A1A1A] cursor-pointer text-lg font-medium"
              >
                <option value="India">India</option>
                <option value="Bhopal">Bhopal</option>
                <option value="Delhi">Delhi</option>
                <option value="Mumbai">Mumbai</option>
              </select>
            </div>

            <div className="space-y-4 pt-2">
              <label className="flex items-center gap-3 cursor-pointer group">
                <input
                  type="checkbox"
                  checked={isCitizen}
                  onChange={(e) => setIsCitizen(e.target.checked)}
                  className="w-5 h-5 rounded border-[#E0E0E0] text-[#0B5FFF] focus:ring-[#0B5FFF]/20"
                />
                <span className="text-[#555555] font-medium text-sm group-hover:text-[#1A1A1A] transition-colors">
                  {lang === "hi" ? "मैं भारत का नागरिक हूँ" : "I am a Citizen of India"}
                </span>
              </label>

              <label className="flex items-center gap-3 cursor-pointer group">
                <input
                  type="checkbox"
                  checked={isResident}
                  onChange={(e) => setIsResident(e.target.checked)}
                  className="w-5 h-5 rounded border-[#E0E0E0] text-[#0B5FFF] focus:ring-[#0B5FFF]/20"
                />
                <span className="text-[#555555] font-medium text-sm group-hover:text-[#1A1A1A] transition-colors">
                  {lang === "hi" ? "मैं वर्तमान स्थान का निवासी हूँ" : "I am a resident of my current location"}
                </span>
              </label>
            </div>

            <button
              type="submit"
              className="w-full bg-[#0B5FFF] hover:bg-[#084ACC] py-4 rounded-xl font-bold transition-all shadow-lg shadow-[#0B5FFF]/10 active:scale-95 flex items-center justify-center gap-2 mt-4 text-white uppercase tracking-widest text-sm"
            >
              {lang === "hi" ? "शुरू करें" : "Start Assistant"}
              <ArrowRight className="w-5 h-5" />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
