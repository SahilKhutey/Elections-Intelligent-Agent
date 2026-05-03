"use client";

import React, { useState, useEffect } from 'react';
import { Shield, Bell, X, AlertTriangle, MessageSquare, ListChecks, Calendar, HelpCircle, MapPin } from 'lucide-react';
import { useLanguage } from './context/LanguageContext';
import { useUser } from './context/UserContext';
import Header from './components/Header';
import Intro from './components/Intro';
import ChatBox from './components/ChatBox';
import QuickActions from './components/QuickActions';
import StepByStepGuide from './components/StepByStepGuide';
import OnboardingModal from './components/OnboardingModal';
import Announcements from './components/Announcements';
import BoothMap from './components/BoothMap';
import AdminPortal from './components/AdminPortal';
import TimelineView from './components/TimelineView';
import { loadOfflineDB, findOfflineAnswer } from './utils/offlineEngine';
import { saveToCache, getFromCache } from './utils/cache';
import { speak } from './utils/speech';

const API_BASE = "http://localhost:8000/api";

const UI_STRINGS = {
  en: {
    placeholder: "Ask something about elections...",
    timelineTitle: "Election Timeline",
    footer: "© 2026 Election Commission Information Service • Powered by Secure AI",
    aiThinking: "Generating response based on official guidelines...",
    actions: ["Voter Guide", "Key Dates", "Eligibility", "Common Questions"],
    intents: ["How do I vote?", "Show election timeline", "Am I eligible to vote?", "Show FAQs"],
    nav: ["Assistant", "Guide", "Timeline", "Booths"],
    adminTitle: "Admin Portal",
    noticeTitle: "Publish Official Notice"
  },
  hi: {
    placeholder: "चुनावों के बारे में कुछ पूछें...",
    timelineTitle: "चुनाव समयरेखा",
    footer: "© 2026 चुनाव आयोग सूचना सेवा • सुरक्षित एआई द्वारा संचालित",
    aiThinking: "आधिकारिक दिशानिर्देशों के आधार पर प्रतिक्रिया उत्पन्न की जा रही है...",
    actions: ["मतदाता गाइड", "महत्वपूर्ण तिथियां", "पात्रता", "सामान्य प्रश्न"],
    intents: ["मैं वोट कैसे डालूं?", "चुनाव की समयरेखा दिखाएं", "क्या मैं वोट देने के लिए पात्र हूं?", "सामान्य प्रश्न दिखाएं"],
    nav: ["सहायक", "गाइड", "समयरेखा", "केंद्र"],
    adminTitle: "एडमिन पोर्टल",
    noticeTitle: "आधिकारिक सूचना प्रकाशित करें"
  }
};

export default function ElectionAssistant() {
  const { lang } = useLanguage();
  const { user, updateUser } = useUser();
  const [activeView, setActiveView] = useState<'chat' | 'guide' | 'timeline' | 'booths'>('chat');
  const [query, setQuery] = useState("");
  const [chat, setChat] = useState<{ role: 'user' | 'ai', content: string }[]>([]);
  const [timeline, setTimeline] = useState<any[]>([]);
  const [notices, setNotices] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [provider, setProvider] = useState("openai");
  
  // Admin State
  const [isAdminOpen, setIsAdminOpen] = useState(false);
  const [adminPassword, setAdminPassword] = useState("");
  const [newNotice, setNewNotice] = useState({ title: "", content: "", type: "info" });
  const [adminError, setAdminError] = useState("");
  const [isOnline, setIsOnline] = useState(true);

  const t = UI_STRINGS[lang];

  useEffect(() => {
    loadOfflineDB();
    
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  useEffect(() => {
    if (user.onboarded) {
      fetchTimeline();
      fetchNotices();
    }
  }, [lang, user.location, user.onboarded]);

  const fetchTimeline = async () => {
    try {
      const headers: any = {};
      if (user.token) headers['Authorization'] = `Bearer ${user.token}`;
      
      const res = await fetch(`${API_BASE}/timeline?lang=${lang}&location=${user.location}`, {
        headers: headers
      });
      const data = await res.json();
      setTimeline(data.timeline || []);
    } catch (err) {
      console.error("Failed to fetch timeline", err);
    }
  };

  const fetchNotices = async () => {
    try {
      const headers: any = {};
      if (user.token) headers['Authorization'] = `Bearer ${user.token}`;

      const res = await fetch(`${API_BASE}/notices`, {
        headers: headers
      });
      const data = await res.json();
      setNotices(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error("Failed to fetch notices", err);
      setNotices([]);
    }
  };

  const handleSend = async (customQuery?: string) => {
    const activeQuery = customQuery || query;
    if (!activeQuery) return;

    setActiveView('chat');
    setLoading(true);
    setChat(prev => [...prev, { role: 'user', content: activeQuery }]);
    if (!customQuery) setQuery("");

    // 1. Check local cache first
    const cachedResponse = getFromCache(activeQuery);
    if (cachedResponse) {
      setChat(prev => [...prev, { role: 'ai', content: cachedResponse }]);
      speak(cachedResponse, lang);
      setLoading(false);
      return;
    }

    // 2. Check offline DB
    const offlineResponse = findOfflineAnswer(activeQuery, lang);
    if (offlineResponse) {
      setChat(prev => [...prev, { role: 'ai', content: offlineResponse }]);
      speak(offlineResponse, lang);
      setLoading(false);
      return;
    }

    // 3. Call Streaming API if online
    if (!isOnline) {
      setChat(prev => [...prev, { role: 'ai', content: lang === 'en' ? "You are offline and no saved data was found for this query." : "आप ऑफलाइन हैं और इस प्रश्न के लिए कोई सहेजा गया डेटा नहीं मिला।" }]);
      setLoading(false);
      return;
    }

    try {
      // Add a placeholder for the AI response
      setChat(prev => [...prev, { role: 'ai', content: "" }]);
      
      const headers: any = { 'Content-Type': 'application/json' };
      if (user.token) headers['Authorization'] = `Bearer ${user.token}`;

      const response = await fetch(`${API_BASE}/stream`, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify({ 
          query: activeQuery, 
          lang: lang,
          location: user.location,
          age: user.age || undefined,
          provider: provider
        })
      });

      if (!response.body) throw new Error("No response body");
      
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let accumulatedResponse = "";

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split("\n");

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            const data = line.slice(6).trim();
            
            if (data === "[DONE]") {
              // Finalize and cache
              saveToCache(activeQuery, accumulatedResponse);
              speak(accumulatedResponse, lang);
              setLoading(false);
              return;
            }

            accumulatedResponse += data;
            
            // Update the last message in chat
            setChat(prev => {
              const updated = [...prev];
              updated[updated.length - 1].content = accumulatedResponse;
              return updated;
            });
          }
        }
      }
    } catch (err) {
      console.error("Streaming error:", err);
      setChat(prev => {
        const updated = [...prev];
        const errorMsg = lang === 'en' ? "Service temporarily unavailable. Please try again later." : "सेवा अस्थायी रूप से अनुपलब्ध है। कृपया बाद में पुनः प्रयास करें।";
        if (updated[updated.length - 1].role === 'ai' && !updated[updated.length - 1].content) {
           updated[updated.length - 1].content = errorMsg;
        } else {
           updated.push({ role: 'ai', content: errorMsg });
        }
        return updated;
      });
    } finally {
      setLoading(false);
    }
  };

  const publishNotice = async () => {
    try {
      const res = await fetch(`${API_BASE}/notices`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...newNotice, password: adminPassword })
      });
      if (!res.ok) throw new Error("Unauthorized");
      const data = await res.json();
      setNotices(prev => [data, ...prev]);
      setIsAdminOpen(false);
      setAdminPassword("");
      setNewNotice({ title: "", content: "", type: "info" });
      setAdminError("");
    } catch (err) {
      setAdminError("Authentication failed.");
    }
  };

  const handleCheckEligibility = async () => {
    setLoading(true);
    setActiveView('chat');
    const userMsg = lang === 'hi' ? "क्या मैं वोट देने के लिए पात्र हूं?" : "Am I eligible to vote?";
    setChat(prev => [...prev, { role: 'user', content: userMsg }]);

    try {
      const headers: any = { 'Content-Type': 'application/json' };
      if (user.token) headers['Authorization'] = `Bearer ${user.token}`;

      const response = await fetch(`${API_BASE}/eligibility`, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify({ 
          age: user.age || 0,
          is_citizen: user.is_citizen,
          is_resident: user.is_resident,
          lang: lang
        })
      });
      const data = await response.json();
      setChat(prev => [...prev, { role: 'ai', content: data.message }]);
    } catch (err) {
      setChat(prev => [...prev, { role: 'ai', content: lang === 'en' ? "Failed to check eligibility. Please try again." : "पात्रता जाँच विफल रही। कृपया पुनः प्रयास करें।" }]);
    } finally {
      setLoading(false);
    }
  };

  const handleActionClick = (id: string, intent: string) => {
    if (id === 'guide') setActiveView('guide');
    else if (id === 'timeline') setActiveView('timeline');
    else if (intent.includes("eligible")) handleCheckEligibility();
    else handleSend(intent);
  };

  return (
    <div className="min-h-screen bg-[#F4F7FE] text-[#1A1A1A] font-sans">
      {!user.onboarded && <OnboardingModal />}

      {/* Urgent Notice Bar (UX4G Style) */}
      {Array.isArray(notices) && notices.filter(n => n.type === 'urgent').length > 0 && (
        <div className="bg-[#D32F2F] text-white py-2.5 px-6 flex items-center justify-center gap-3 sticky top-0 z-[60] shadow-md border-b border-red-700/20">
          <AlertTriangle className="w-4 h-4 fill-white text-[#D32F2F]" />
          <p className="text-sm font-bold tracking-wide">
            {lang === 'hi' ? 'महत्वपूर्ण:' : 'URGENT:'} {(notices || []).find(n => n.type === 'urgent')?.title}
          </p>
          <span className="hidden sm:inline opacity-90 text-sm font-medium">| {(notices || []).find(n => n.type === 'urgent')?.content}</span>
        </div>
      )}

      <AdminPortal 
        isOpen={isAdminOpen} 
        setIsOpen={setIsAdminOpen} 
        adminPassword={adminPassword} 
        setAdminPassword={setAdminPassword} 
        newNotice={newNotice} 
        setNewNotice={setNewNotice} 
        adminError={adminError} 
        publishNotice={publishNotice} 
        t={t} 
      />

      <main className="max-w-6xl mx-auto px-4 sm:px-6 py-6 pb-32">
        {!isOnline && (
          <div className="mb-6 bg-yellow-50 border border-yellow-200 text-yellow-800 px-4 py-3 rounded-xl flex items-center gap-3 animate-pulse">
            <AlertTriangle className="w-5 h-5" />
            <p className="text-sm font-bold">
              {lang === 'hi' ? 'आप ऑफलाइन हैं। सहेजे गए मार्गदर्शन का उपयोग किया जा रहा है।' : 'You are offline. Using saved guidance for instant responses.'}
            </p>
          </div>
        )}
        <Header 
          location={user.location} setLocation={(loc) => updateUser({ location: loc })} 
          age={user.age || ""} setAge={(age) => updateUser({ age: age || null })} 
          provider={provider} setProvider={setProvider}
          setIsAdminOpen={setIsAdminOpen}
        />

        <Intro />

        {/* Dynamic Views */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
          <div className="lg:col-span-2 space-y-8">
            {activeView === 'chat' && (
              <div className="animate-fade-in space-y-8">
                <ChatBox 
                  chat={chat} loading={loading} 
                  query={query} setQuery={setQuery} 
                  handleSend={handleSend} 
                  placeholder={t.placeholder}
                  aiThinking={t.aiThinking}
                  location={user.location}
                  lang={lang}
                />
                <QuickActions 
                  onSelect={handleActionClick} 
                  actions={t.actions} 
                  intents={t.intents} 
                />
              </div>
            )}

            {activeView === 'guide' && (
              <div className="animate-fade-in bg-white border border-[#E0E0E0] rounded-2xl p-8 shadow-sm">
                <StepByStepGuide />
              </div>
            )}

            {activeView === 'timeline' && (
              <TimelineView timeline={timeline} title={t.timelineTitle} />
            )}

            {activeView === 'booths' && (
              <div className="animate-fade-in bg-white border border-[#E0E0E0] rounded-2xl p-8 shadow-sm">
                <BoothMap />
              </div>
            )}
          </div>

          <aside className="space-y-8">
            <Announcements />
            
            {/* Gov Help Desk Info */}
            <div className="bg-[#0B5FFF] text-white p-6 rounded-2xl shadow-lg shadow-[#0B5FFF]/10">
              <h4 className="font-bold mb-2 flex items-center gap-2">
                <HelpCircle className="w-4 h-4" /> Need Immediate Help?
              </h4>
              <p className="text-xs text-blue-50 leading-relaxed mb-4">
                Contact the Voter Helpline for urgent queries regarding your registration or polling location.
              </p>
              <div className="bg-white/10 p-3 rounded-lg flex items-center justify-between">
                <span className="text-sm font-bold tracking-wider">HELPLINE</span>
                <span className="text-xl font-black">1950</span>
              </div>
            </div>
          </aside>
        </div>

        {/* Bottom Navigation (UX4G Style) */}
        <div className="fixed bottom-10 left-1/2 -translate-x-1/2 bg-white/90 backdrop-blur-xl border border-[#E0E0E0] rounded-2xl p-1.5 shadow-2xl flex gap-1 z-50">
          {[
            { id: 'chat', label: t.nav[0], icon: <MessageSquare className="w-4 h-4" /> },
            { id: 'guide', label: t.nav[1], icon: <ListChecks className="w-4 h-4" /> },
            { id: 'timeline', label: t.nav[2], icon: <Calendar className="w-4 h-4" /> },
            { id: 'booths', label: t.nav[3], icon: <MapPin className="w-4 h-4" /> }
          ].map((nav) => (
            <button 
              key={nav.id} 
              onClick={() => setActiveView(nav.id as any)} 
              className={`flex items-center gap-2 px-6 py-3 rounded-xl text-xs font-bold uppercase tracking-wider transition-all ${activeView === nav.id ? 'bg-[#0B5FFF] text-white shadow-lg shadow-[#0B5FFF]/20' : 'text-[#555555] hover:text-[#0B5FFF] hover:bg-[#F4F7FE]'}`}
            >
              {nav.icon}
              <span className="hidden sm:inline">{nav.label}</span>
            </button>
          ))}
        </div>

        <p className="text-center mt-16 text-[#9CA3AF] text-[10px] font-bold tracking-[0.2em] uppercase max-w-lg mx-auto leading-relaxed">
          {t.footer}
        </p>
      </main>
    </div>
  );
}

