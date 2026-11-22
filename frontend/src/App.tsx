import React, { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { ImageSolver } from './components/ImageSolver';
import { ChatGrounded } from './components/ChatGrounded';
import { HistoryList } from './components/HistoryList';
import { api, ConnectionStatus } from './services/api';
import viLocale from './locales/vi.json';
import zhLocale from './locales/zh-CN.json';

export const App: React.FC = () => {
  const [currentTab, setCurrentTab] = useState<'solver' | 'chat' | 'history'>('solver');
  const [language, setLanguage] = useState<'vi' | 'zh-CN'>('vi');
  const [connectionStatus, setConnectionStatus] = useState<ConnectionStatus | null>(null);
  const [isTestingConnection, setIsTestingConnection] = useState<boolean>(false);

  const labels = language === 'vi' ? viLocale : zhLocale;

  const checkConnection = async () => {
    setIsTestingConnection(true);
    try {
      const status = await api.testConnection();
      setConnectionStatus(status);
    } catch {
      setConnectionStatus({
        online: false,
        mode: 'local_rag',
        message: 'Local RAG Mode',
      });
    } finally {
      setIsTestingConnection(false);
    }
  };

  useEffect(() => {
    checkConnection();
  }, []);

  const isLocalRag = !connectionStatus?.online || connectionStatus?.mode === 'local_rag';

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col justify-between selection:bg-blue-600 selection:text-white">
      <div>
        <Navbar
          currentTab={currentTab}
          setCurrentTab={setCurrentTab}
          language={language}
          setLanguage={setLanguage}
          labels={labels}
          connectionStatus={connectionStatus}
          onRefreshConnection={checkConnection}
          isTestingConnection={isTestingConnection}
        />

        <main className="py-2">
          {currentTab === 'solver' && (
            <ImageSolver
              language={language}
              labels={labels}
              isLocalRag={isLocalRag}
            />
          )}
          {currentTab === 'chat' && (
            <ChatGrounded
              language={language}
              labels={labels}
              isLocalRag={isLocalRag}
            />
          )}
          {currentTab === 'history' && <HistoryList />}
        </main>
      </div>

      <footer className="py-4 border-t border-slate-900 text-center text-xs text-slate-500 flex flex-col sm:flex-row items-center justify-center gap-2">
        <span>Đồ án AI Agent Tự động hóa Lưới điện Phân phối v1.3.0</span>
        <span className="hidden sm:inline">•</span>
        <span>Nguồn tri thức duy nhất: PDF Giáo trình tiếng Trung 233 trang</span>
        <span className="hidden sm:inline">•</span>
        <span className={isLocalRag ? 'text-blue-400 font-medium' : 'text-emerald-400 font-medium'}>
          {isLocalRag ? 'Chế độ Local RAG Tự hành' : 'Gemini Cloud API'}
        </span>
      </footer>
    </div>
  );
};

export default App;
