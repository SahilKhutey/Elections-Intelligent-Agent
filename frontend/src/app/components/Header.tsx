"use client";

import React from 'react';
import { MapPin, User, Brain, Shield } from 'lucide-react';
import LanguageToggle from './LanguageToggle';

interface HeaderProps {
  location: string;
  setLocation: (val: string) => void;
  age: number | "";
  setAge: (val: number | "") => void;
  provider: string;
  setProvider: (val: string) => void;
  setIsAdminOpen: (val: boolean) => void;
}

export default function Header({ 
  location, setLocation, age, setAge, provider, setProvider, setIsAdminOpen 
}: HeaderProps) {
  const isEligible = age !== "" && age >= 18;
  const persona = age === "" ? "User" : isEligible ? "Eligible Voter" : "Future Voter";

  return (
    <header className="flex justify-between items-center border-b border-[#E0E0E0] pb-4 mb-8 bg-white/50 backdrop-blur-sm sticky top-0 z-50 px-4 py-3 -mx-4 sm:mx-0 sm:px-0">
      <div className="flex items-center gap-4">
        <div className="w-10 h-10 bg-[#0B5FFF] rounded-lg flex items-center justify-center font-bold text-white shadow-md">
          E
        </div>
        <div>
          <h1 className="text-xl font-bold text-[#1A1A1A] leading-tight">
            Election Assistant
          </h1>
          <div className="flex items-center gap-2 mt-0.5">
            <span className="text-[10px] font-bold text-[#555555] tracking-wide uppercase">
              Govt Service
            </span>
            <span className="w-1 h-1 rounded-full bg-[#E0E0E0]"></span>
            <span className={`text-[10px] font-bold uppercase tracking-wide ${isEligible ? 'text-[#2E7D32]' : 'text-[#0B5FFF]'}`}>
              {persona}
            </span>
          </div>
        </div>
      </div>

      <div className="flex items-center gap-6">
        <div className="hidden lg:flex items-center gap-4 text-[11px] font-bold text-[#555555] uppercase tracking-tighter">
          <div className="flex items-center gap-1.5 bg-[#F4F7FE] px-3 py-1.5 rounded-full border border-[#E0E0E0]">
            <MapPin className="w-3 h-3 text-[#0B5FFF]" />
            <select 
              value={location} 
              onChange={(e) => setLocation(e.target.value)} 
              className="bg-transparent focus:outline-none cursor-pointer hover:text-[#0B5FFF] text-[10px]"
            >
              <option value="India">India</option>
              <option value="Bhopal">Bhopal</option>
              <option value="Delhi">Delhi</option>
              <option value="Mumbai">Mumbai</option>
            </select>
          </div>
          
          <div className="flex items-center gap-1.5 bg-[#F4F7FE] px-3 py-1.5 rounded-full border border-[#E0E0E0]">
            <Brain className="w-3 h-3 text-[#2E7D32]" />
            <select 
              value={provider} 
              onChange={(e) => setProvider(e.target.value)} 
              className="bg-transparent focus:outline-none cursor-pointer text-[10px]"
            >
              <option value="openai">OpenAI</option>
              <option value="gemini">Gemini</option>
              <option value="claude">Claude</option>
            </select>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button 
            onClick={() => setIsAdminOpen(true)} 
            className="p-2 hover:bg-gray-100 rounded-lg text-[#555555] hover:text-[#0B5FFF] transition-colors border border-[#E0E0E0]"
            title="Admin Portal"
          >
            <Shield className="w-4 h-4" />
          </button>
          <LanguageToggle />
        </div>
      </div>
    </header>
  );
}
