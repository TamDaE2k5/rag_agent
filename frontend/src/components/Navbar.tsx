import React, { useState } from 'react';
import { Zap, Globe, BookOpen, Clock, Camera, RefreshCw, Wifi, WifiOff, Database } from 'lucide-react';
import { ConnectionStatus } from '../services/api';

interface NavbarProps {
  currentTab: 'solver' | 'chat' | 'history';
  setCurrentTab: (tab: 'solver' | 'chat' | 'history') => void;
  language: 'vi' | 'zh-CN';
  setLanguage: (lang: 'vi' | 'zh-CN') => void;
  labels: Record<string, string>;
  connectionStatus: ConnectionStatus | null;
  onRefreshConnection: () => Promise<void>;
  isTestingConnection: boolean;
}

export const Navbar: React.FC<NavbarProps> = ({
  currentTab,
  setCurrentTab,
  language,
  setLanguage,
  labels,
  connectionStatus,
  onRefreshConnection,
  isTestingConnection,
}) => {
  const isOnline = connectionStatus?.online;

  return (
    <header className="sticky top-0 z-50 glass-panel border-b border-slate-700/60 bg-slate-900/80">
      <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between gap-4">
        {/* Logo and Brand */}
        <div className="flex items-center gap-3 min-w-0">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center shadow-lg shadow-blue-500/20 flex-shrink-0">
            <Zap className="w-6 h-6 text-white" />
          </div>
          <div className="min-w-0">
            <h1 className="text-base font-bold text-white flex items-center gap-2 truncate">
              <span className="truncate">{labels.app_title || "AI Trợ lý Tự động hóa Lưới điện Phân phối"}</span>
              <span className="text-xs px-2 py-0.5 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20 flex-shrink-0">
                v1.3.0
              </span>
            </h1>
            <p className="text-xs text-slate-400 truncate">
              {language === 'vi' ? 'Đọc đề tiếng Trung • Giải thích tiếng Việt • PDF duy nhất' : '中文题目识别 • 分步推导 • 单一教材'}
            </p>
          </div>
        </div>

        {/* Tab Navigation */}
        <nav className="hidden md:flex items-center gap-1 bg-slate-800/80 p-1 rounded-xl border border-slate-700">
          <button
            onClick={() => setCurrentTab('solver')}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-sm font-medium transition-all ${
              currentTab === 'solver'
                ? 'bg-blue-600 text-white shadow-md'
                : 'text-slate-400 hover:text-white hover:bg-slate-700/50'
            }`}
          >
            <Camera className="w-4 h-4" />
            <span>{labels.tab_solver || 'Giải ảnh'}</span>
          </button>

          <button
            onClick={() => setCurrentTab('chat')}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-sm font-medium transition-all ${
              currentTab === 'chat'
                ? 'bg-blue-600 text-white shadow-md'
                : 'text-slate-400 hover:text-white hover:bg-slate-700/50'
            }`}
          >
            <BookOpen className="w-4 h-4" />
            <span>{labels.tab_chat || 'Hỏi đáp'}</span>
          </button>

          <button
            onClick={() => setCurrentTab('history')}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-sm font-medium transition-all ${
              currentTab === 'history'
                ? 'bg-blue-600 text-white shadow-md'
                : 'text-slate-400 hover:text-white hover:bg-slate-700/50'
            }`}
          >
            <Clock className="w-4 h-4" />
            <span>{labels.tab_history || 'Lịch sử'}</span>
          </button>
        </nav>

        {/* Right side controls: Connection Status badge & Language */}
        <div className="flex items-center gap-2.5 flex-shrink-0">
          {/* API Status Indicator Badge */}
          <div
            className={`flex items-center gap-2 px-2.5 py-1 rounded-xl border text-xs transition-all ${
              isOnline
                ? 'bg-emerald-950/40 border-emerald-500/30 text-emerald-300'
                : 'bg-blue-950/40 border-blue-500/30 text-blue-300'
            }`}
            title={connectionStatus?.message || (isOnline ? 'Cloud Gemini API' : 'Local RAG Mode')}
          >
            <div className="flex items-center gap-1.5">
              <span className="relative flex h-2 w-2">
                <span
                  className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${
                    isOnline ? 'bg-emerald-400' : 'bg-blue-400'
                  }`}
                />
                <span
                  className={`relative inline-flex rounded-full h-2 w-2 ${
                    isOnline ? 'bg-emerald-500' : 'bg-blue-500'
                  }`}
                />
              </span>
              <span className="font-medium text-[11px] hidden sm:inline">
                {isOnline ? labels.status_online || 'Gemini Online' : labels.status_local_rag || 'Local RAG Mode'}
              </span>
            </div>

            {/* Quick Test / Refresh Button */}
            <button
              onClick={onRefreshConnection}
              disabled={isTestingConnection}
              title={labels.test_connection || 'Kiểm tra kết nối backend / API'}
              className="p-1 text-slate-400 hover:text-white hover:bg-slate-800 rounded-lg transition disabled:opacity-50"
            >
              <RefreshCw className={`w-3 h-3 ${isTestingConnection ? 'animate-spin text-blue-400' : ''}`} />
            </button>
          </div>

          {/* Language Switcher */}
          <button
            onClick={() => setLanguage(language === 'vi' ? 'zh-CN' : 'vi')}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition"
          >
            <Globe className="w-3.5 h-3.5 text-blue-400" />
            <span>{language === 'vi' ? 'VI' : '中文'}</span>
          </button>
        </div>
      </div>

      {/* Mobile nav tabs */}
      <div className="md:hidden flex items-center justify-around border-t border-slate-800 bg-slate-900/90 py-1.5 px-2">
        <button
          onClick={() => setCurrentTab('solver')}
          className={`flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-medium ${
            currentTab === 'solver' ? 'bg-blue-600 text-white' : 'text-slate-400'
          }`}
        >
          <Camera className="w-3.5 h-3.5" />
          <span>{labels.tab_solver || 'Giải ảnh'}</span>
        </button>
        <button
          onClick={() => setCurrentTab('chat')}
          className={`flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-medium ${
            currentTab === 'chat' ? 'bg-blue-600 text-white' : 'text-slate-400'
          }`}
        >
          <BookOpen className="w-3.5 h-3.5" />
          <span>{labels.tab_chat || 'Hỏi đáp'}</span>
        </button>
        <button
          onClick={() => setCurrentTab('history')}
          className={`flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-medium ${
            currentTab === 'history' ? 'bg-blue-600 text-white' : 'text-slate-400'
          }`}
        >
          <Clock className="w-3.5 h-3.5" />
          <span>{labels.tab_history || 'Lịch sử'}</span>
        </button>
      </div>
    </header>
  );
};
