"use client";

import React from 'react';
import { Calendar } from 'lucide-react';

/**
 * TimelineView component displays a step-by-step chronological guide
 * for the election process tailored to the user's location.
 */
interface TimelineViewProps {
  timeline: any[];
  title: string;
}

export default function TimelineView({ timeline, title }: TimelineViewProps) {
  return (
    <div className="bg-white border border-[#E0E0E0] rounded-2xl p-8 shadow-sm animate-fade-in">
      <h2 className="text-2xl font-bold mb-8 flex items-center gap-2 text-[#1A1A1A]">
        <Calendar className="text-[#0B5FFF] w-6 h-6" /> {title}
      </h2>
      <div className="grid gap-6">
        {timeline.length === 0 ? (
          <p className="text-[#555555] italic">No timeline data available for your location.</p>
        ) : (
          timeline.map((step, i) => (
            <div key={i} className="flex items-start gap-5 p-5 rounded-xl bg-white border border-[#E0E0E0] hover:bg-[#F4F7FE] transition-all group">
              <div className="w-11 h-11 rounded-lg bg-[#F4F7FE] flex items-center justify-center text-[#0B5FFF] font-bold group-hover:bg-[#0B5FFF] group-hover:text-white transition-all shadow-sm border border-[#0B5FFF]/10">
                {i + 1}
              </div>
              <div>
                <h4 className="font-bold text-[#1A1A1A] text-lg">{step.stage}</h4>
                <p className="text-sm text-[#555555] leading-relaxed mt-1 font-medium">{step.status}</p>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
