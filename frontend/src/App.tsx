import React, { useState } from 'react';
import { Navbar } from './components/Navbar';
import { ImageSolver } from './components/ImageSolver';
import { ChatGrounded } from './components/ChatGrounded';
import { HistoryList } from './components/HistoryList';
import viLocale from './locales/vi.json';
import zhLocale from './locales/zh-CN.json';

export const App: React.FC = () => {
  const [currentTab, setCurrentTab] = useState<'solver' | 'chat' | 'history'>('solver');
  const [language, setLanguage] = useState<'vi' | 'zh-CN'>('vi');

  const labels = language === 'vi' ? viLocale : zhLocale;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col justify-between selection:bg-blue-600 selection:text-white">
      <div>
        <Navbar
          currentTab={currentTab}
          setCurrentTab={setCurrentTab}
          language={language}
          setLanguage={setLanguage}
          labels={labels}
        />

        <main className="py-2">
          {currentTab === 'solver' && <ImageSolver language={language} labels={labels} />}
          {currentTab === 'chat' && <ChatGrounded language={language} labels={labels} />}
          {currentTab === 'history' && <HistoryList />}
        </main>
      </div>

      <footer className="py-4 border-t border-slate-900 text-center text-xs text-slate-600">
        Đồ án AI Agent Tự động hóa Lưới điện Phân phối • Nguồn tri thức duy nhất: PDF Giáo trình tiếng Trung
      </footer>
    </div>
  );
};

export default App;
