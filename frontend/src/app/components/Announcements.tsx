"use client";

import React, { useEffect, useState } from "react";
import { useUser } from "../context/UserContext";
import { useLanguage } from "../context/LanguageContext";
import { Bell, Info, AlertTriangle, MapPin, ChevronRight } from "lucide-react";

interface Announcement {
  title: string;
  message: string;
  type: "info" | "urgent" | "important" | "alert";
}

export default function Announcements() {
  const { user } = useUser();
  const { lang } = useLanguage();
  const [items, setItems] = useState<Announcement[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user.location) return;

    setLoading(true);
    fetch(`http://localhost:8000/api/announcements?location=${encodeURIComponent(user.location)}`)
      .then((res) => res.json())
      .then((data) => {
        setItems(data.announcements || []);
      })
      .catch((err) => {
        console.error("Failed to fetch announcements:", err);
        setItems([]);
      })
      .finally(() => setLoading(false));
  }, [user.location]);

  if (!user.onboarded || items.length === 0) return null;

  const getBadgeColor = (type: string) => {
    switch (type) {
      case "urgent":
      case "alert":
        return "bg-red-50 text-red-700 border-red-100";
      case "important":
        return "bg-amber-50 text-amber-700 border-amber-100";
      default:
        return "bg-blue-50 text-blue-700 border-blue-100";
    }
  };

  return (
    <div className="bg-white border border-[#E0E0E0] rounded-2xl shadow-sm overflow-hidden animate-fade-in mt-8">
      <div className="bg-[#F4F7FE] border-b border-[#E0E0E0] px-6 py-4 flex items-center justify-between">
        <h3 className="text-sm font-bold text-[#1A1A1A] flex items-center gap-2">
          <Bell className="w-4 h-4 text-[#0B5FFF]" />
          {lang === "hi" ? "सार्वजनिक घोषणाएं" : "Public Announcements"}
        </h3>
        <span className="text-[10px] font-bold text-[#555555] uppercase tracking-wider flex items-center gap-1">
          <MapPin className="w-3 h-3" /> {user.location}
        </span>
      </div>
      
      <div className="divide-y divide-[#E0E0E0]">
        {items.map((item, i) => (
          <div 
            key={i} 
            className="p-5 hover:bg-gray-50 transition-colors group cursor-pointer"
          >
            <div className="flex items-start justify-between gap-4">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-2">
                  <span className={`text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded border ${getBadgeColor(item.type)}`}>
                    {item.type}
                  </span>
                </div>
                <p className="font-bold text-[#1A1A1A] mb-1 group-hover:text-[#0B5FFF] transition-colors">
                  {item.title}
                </p>
                <p className="text-sm text-[#555555] leading-relaxed">
                  {item.message}
                </p>
              </div>
              <ChevronRight className="w-5 h-5 text-[#E0E0E0] group-hover:text-[#0B5FFF] transition-all mt-1" />
            </div>
          </div>
        ))}
      </div>
      
      <div className="bg-gray-50 px-6 py-3 border-t border-[#E0E0E0]">
        <button className="text-xs font-bold text-[#0B5FFF] hover:underline uppercase tracking-wider">
          {lang === "hi" ? "सभी सूचनाएं देखें" : "View All Notices"}
        </button>
      </div>
    </div>
  );
}
