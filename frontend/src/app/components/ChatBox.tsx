"use client";

import React, { useRef, useEffect } from 'react';
import { Send, Loader2, Bot, User, Shield } from 'lucide-react';
import VoiceInput from './VoiceInput';

interface ChatBoxProps {
  chat: { role: 'user' | 'ai', content: string }[];
  loading: boolean;
  query: string;
  setQuery: (val: string) => void;
  handleSend: (custom?: string) => void;
  placeholder: string;
  aiThinking: string;
  location: string;
  lang: 'en' | 'hi';
}

export default function ChatBox({ 
  chat, loading, query, setQuery, handleSend, placeholder, aiThinking, location, lang 
}: ChatBoxProps) {
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [chat, loading]);

  return (
    <div className="bg-white border border-[#E0E0E0] rounded-2xl flex flex-col h-[600px] shadow-sm overflow-hidden animate-fade-in">
      {/* Header Area */}
      <div className="bg-[#F4F7FE] border-b border-[#E0E0E0] px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
          <span className="text-xs font-bold text-[#555555] uppercase tracking-wider">AI Assistant Active</span>
        </div>
        <span className="text-xs font-medium text-[#555555]">{location} Service Node</span>
      </div>

      {/* Messages */}
      <div 
        ref={scrollRef}
        className="flex-1 overflow-y-auto p-6 space-y-6 scroll-smooth"
      >
        {chat.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-center p-10">
            <div className="w-16 h-16 bg-[#F4F7FE] rounded-2xl flex items-center justify-center mb-4">
              <Bot className="w-8 h-8 text-[#0B5FFF]" />
            </div>
            <h3 className="text-xl font-bold text-[#1A1A1A] mb-2">How can I help you today?</h3>
            <p className="text-[#555555] text-sm max-w-xs">Ask about voter registration, polling booths, eligibility, or the election schedule.</p>
          </div>
        ) : (
          chat.map((msg, i) => (
            <div 
              key={i} 
              className={`flex items-start gap-4 ${msg.role === 'user' ? 'flex-row-reverse' : ''} animate-fade-in`}
            >
              <div className={`w-9 h-9 rounded-lg flex items-center justify-center flex-shrink-0 ${msg.role === 'user' ? 'bg-[#0B5FFF] text-white' : 'bg-[#F4F7FE] text-[#0B5FFF]'}`}>
                {msg.role === 'user' ? <User className="w-5 h-5" /> : <Bot className="w-5 h-5" />}
              </div>
              <div className={`max-w-[85%] p-4 rounded-2xl text-[15px] leading-relaxed ${msg.role === 'user' ? 'bg-[#0B5FFF] text-white rounded-tr-none' : 'bg-[#F4F7FE] text-[#1A1A1A] rounded-tl-none border border-[#E0E0E0]'}`}>
                {msg.content}
              </div>
            </div>
          ))
        )}
        {loading && (
          <div className="flex items-start gap-4 animate-fade-in">
            <div className="w-9 h-9 rounded-lg bg-[#F4F7FE] text-[#0B5FFF] flex items-center justify-center">
              <Loader2 className="w-5 h-5 animate-spin" />
            </div>
            <div className="bg-[#F4F7FE] text-[#555555] p-4 rounded-2xl rounded-tl-none border border-[#E0E0E0] text-[15px] italic">
              {aiThinking}
            </div>
          </div>
        )}
      </div>

      {/* Input Form */}
      <div className="p-6 border-t border-[#E0E0E0] bg-white">
        <form 
          onSubmit={(e) => { e.preventDefault(); handleSend(); }}
          className="relative flex flex-col gap-2"
        >
          <label htmlFor="ask-question" className="text-xs font-bold text-[#555555] uppercase tracking-wider mb-1">
            Ask your question
          </label>
          <div className="flex gap-2">
            <input
              id="ask-question"
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder={placeholder}
              className="flex-1 bg-white border border-[#E0E0E0] rounded-xl px-5 py-3.5 focus:outline-none focus:border-[#0B5FFF] focus:ring-4 focus:ring-[#0B5FFF]/5 transition-all text-[#1A1A1A]"
            />
            <VoiceInput 
              lang={lang} 
              onResult={(text) => {
                setQuery(text);
                setTimeout(() => handleSend(text), 100);
              }} 
            />
            <button 
              type="submit"
              disabled={loading || !query.trim()}
              className="bg-[#0B5FFF] hover:bg-[#084ACC] text-white p-3.5 rounded-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-[#0B5FFF]/10 active:scale-95 flex items-center justify-center min-w-[56px]"
            >
              {loading ? <Loader2 className="w-6 h-6 animate-spin" /> : <Send className="w-6 h-6" />}
            </button>
          </div>
          <p className="text-[10px] text-[#9CA3AF] mt-2 flex items-center gap-1 px-1">
            <Shield className="w-3 h-3" /> Powered by Official Election Data & Secure AI
          </p>
        </form>
      </div>
    </div>
  );
}
