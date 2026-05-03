"use client";

import React from 'react';
import { Shield, X, AlertTriangle } from 'lucide-react';

/**
 * AdminPortal component provides a secure interface for election officials
 * to publish urgent notices and updates to the platform.
 * 
 * Includes password protection and notice type selection.
 */
interface AdminPortalProps {
  isOpen: boolean;
  setIsOpen: (open: boolean) => void;
  adminPassword: string;
  setAdminPassword: (pw: string) => void;
  newNotice: { title: string; content: string; type: string };
  setNewNotice: (notice: any) => void;
  adminError: string;
  publishNotice: () => void;
  t: any;
}

export default function AdminPortal({
  isOpen, setIsOpen, adminPassword, setAdminPassword, 
  newNotice, setNewNotice, adminError, publishNotice, t
}: AdminPortalProps) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-[#1A1A1A]/40 backdrop-blur-sm animate-fade-in">
      <div className="bg-white border border-[#E0E0E0] rounded-2xl p-8 max-w-md w-full shadow-2xl relative">
        <button onClick={() => setIsOpen(false)} className="absolute top-4 right-4 p-2 hover:bg-gray-100 rounded-full transition-colors">
          <X className="w-5 h-5 text-[#555555]" />
        </button>
        <h2 className="text-2xl font-bold mb-6 flex items-center gap-2 text-[#1A1A1A]">
          <Shield className="text-[#0B5FFF]" /> {t.adminTitle}
        </h2>
        <div className="space-y-4">
          <div>
            <label className="block text-xs font-bold text-[#555555] uppercase mb-1.5 ml-1">Access Key</label>
            <input 
              type="password" 
              placeholder="••••••••" 
              value={adminPassword} 
              onChange={(e) => setAdminPassword(e.target.value)} 
              className="w-full bg-white border border-[#E0E0E0] rounded-xl py-3 px-5 focus:outline-none focus:border-[#0B5FFF] focus:ring-4 focus:ring-[#0B5FFF]/5 text-[#1A1A1A]" 
            />
          </div>
          <div className="h-px bg-[#E0E0E0] my-2"></div>
          <div>
            <label className="block text-xs font-bold text-[#555555] uppercase mb-1.5 ml-1">Notice Details</label>
            <input 
              type="text" 
              placeholder="Title" 
              value={newNotice.title} 
              onChange={(e) => setNewNotice({...newNotice, title: e.target.value})} 
              className="w-full bg-white border border-[#E0E0E0] rounded-xl py-3 px-5 focus:outline-none focus:border-[#0B5FFF] mb-3 text-[#1A1A1A]" 
            />
            <textarea 
              placeholder="Message content..." 
              value={newNotice.content} 
              onChange={(e) => setNewNotice({...newNotice, content: e.target.value})} 
              className="w-full bg-white border border-[#E0E0E0] rounded-xl py-3 px-5 focus:outline-none focus:border-[#0B5FFF] min-h-[100px] text-[#1A1A1A]" 
            />
          </div>
          <select 
            value={newNotice.type} 
            onChange={(e) => setNewNotice({...newNotice, type: e.target.value})} 
            className="w-full bg-white border border-[#E0E0E0] rounded-xl py-3 px-5 focus:outline-none focus:border-[#0B5FFF] text-[#1A1A1A]"
          >
            <option value="info">General Information</option>
            <option value="urgent">Urgent Alert</option>
            <option value="success">Status Update</option>
          </select>
          {adminError && (
            <p className="text-[#D32F2F] text-xs px-2 flex items-center gap-1 font-medium">
              <AlertTriangle className="w-3.5 h-3.5" /> {adminError}
            </p>
          )}
          <button 
            onClick={publishNotice} 
            className="w-full bg-[#0B5FFF] hover:bg-[#084ACC] text-white py-4 rounded-xl font-bold transition-all shadow-lg shadow-[#0B5FFF]/10 active:scale-95"
          >
            Publish Notice
          </button>
        </div>
      </div>
    </div>
  );
}
