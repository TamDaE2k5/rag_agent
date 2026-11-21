import React from 'react';
import { Zap, Globe, BookOpen, Clock, Camera } from 'lucide-react';

interface NavbarProps {
  currentTab: 'solver' | 'chat' | 'history';
  setCurrentTab: (tab: 'solver' | 'chat' | 'history') => void;
  language: 'vi' | 'zh-CN';
  setLanguage: (lang: 'vi' | 'zh-CN') => void;
  labels: Record<string, string>;
}

export const Navbar: React.FC<NavbarProps> = ({
  currentTab,
  setCurrentTab,
  language,
  setLanguage,
  labels,
}) => {
  return (
    <header className="sticky top-0 z-50 glass-panel border-b border-slate-700/60 bg-slate-900/80">
      <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
        {/* Logo and Brand */}
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center shadow-lg shadow-blue-500/20">
            <Zap className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-base font-bold text-white flex items-center gap-2">
              {labels.app_title || "AI Trợ lý Tự động hóa Lưới điện Phân phối"}
              <span className="text-xs px-2 py-0.5 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20">
                v1.2
              </span>
            </h1>
            <p className="text-xs text-slate-400">
              {language === 'vi' ? 'Đọc đề tiếng Trung • Giải thích tiếng Việt • PDF duy nhất' : '中文题目识别 • 分步推导 • 单一教材'}
            </p>
          </div>
        </div>

        {/* Tab Navigation */}
        <nav className="flex items-center gap-1 bg-slate-800/80 p-1 rounded-xl border border-slate-700">
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

        {/* Language Switcher */}
        <div className="flex items-center gap-2">
          <button
            onClick={() => setLanguage(language === 'vi' ? 'zh-CN' : 'vi')}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition"
          >
            <Globe className="w-3.5 h-3.5 text-blue-400" />
            <span>{language === 'vi' ? 'VI' : '中文'}</span>
          </button>
        </div>
      </div>
    </header>
  );
};
