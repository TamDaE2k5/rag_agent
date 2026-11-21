import React, { useState } from 'react';
import { Send, BookOpen, Bookmark, Bot, User, Trash2, ExternalLink } from 'lucide-react';
import { api } from '../services/api';
import { ChatResponse } from '../types';
import { SourceExcerptModal } from './SourceExcerptModal';

interface ChatGroundedProps {
  language: 'vi' | 'zh-CN';
  labels: Record<string, string>;
}

export const ChatGrounded: React.FC<ChatGroundedProps> = ({ language, labels }) => {
  const defaultInitialMessage = {
    role: 'assistant' as const,
    text:
      language === 'vi'
        ? 'Xin chào! Tôi là Trợ lý học tập môn Tự động hóa lưới điện phân phối. Mọi câu trả lời của tôi đều được trích xuất và đối chiếu trực tiếp từ PDF giáo trình tiếng Trung duy nhất 《配电网自动化技术》.'
        : '你好！我是配电网自动化技术助教。我的所有回答均直接基于单一指定的中文教材 PDF 《配电网自动化技术》，并标明页码出处。',
  };

  const [messages, setMessages] = useState<
    Array<{ role: 'user' | 'assistant'; data?: ChatResponse; text?: string }>
  >([defaultInitialMessage]);
  const [inputQuestion, setInputQuestion] = useState('');
  const [loading, setLoading] = useState(false);
  const [selectedRefForExcerpt, setSelectedRefForExcerpt] = useState<string | null>(null);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputQuestion.trim() || loading) return;

    const q = inputQuestion.trim();
    setInputQuestion('');
    setMessages((prev) => [...prev, { role: 'user', text: q }]);
    setLoading(true);

    try {
      const resp = await api.askChat(q, undefined, language);
      setMessages((prev) => [...prev, { role: 'assistant', data: resp }]);
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          text:
            language === 'vi'
              ? 'Lỗi: Không thể kết nối với dịch vụ AI hoặc không tìm thấy thông tin trong giáo trình.'
              : '错误：无法连接至 AI 服务或未在教材中检索到相关内容。',
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleClearChat = () => {
    setMessages([defaultInitialMessage]);
  };

  return (
    <div className="max-w-4xl mx-auto py-6 px-4 space-y-4">
      {/* Top note bar with clear button */}
      <div className="flex items-center justify-between gap-2 p-3.5 bg-blue-500/10 border border-blue-500/20 rounded-xl text-xs text-blue-300">
        <div className="flex items-center gap-2">
          <BookOpen className="w-4 h-4 flex-shrink-0 text-blue-400" />
          <span>
            {labels.chat_grounded_note ||
              'Hệ thống chỉ truy xuất trực tiếp từ một PDF giáo trình tiếng Trung duy nhất'}
          </span>
        </div>
        <button
          onClick={handleClearChat}
          title={labels.chat_clear || 'Xóa lịch sử chat'}
          className="flex items-center gap-1 px-2.5 py-1 text-[11px] bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg transition border border-slate-700/60"
        >
          <Trash2 className="w-3 h-3 text-slate-400" />
          <span>{labels.chat_clear || 'Xóa lịch sử'}</span>
        </button>
      </div>

      <div className="glass-panel rounded-2xl border border-slate-800 p-4 h-[560px] flex flex-col justify-between">
        <div className="overflow-y-auto space-y-4 pr-2">
          {messages.map((m, idx) => (
            <div key={idx} className={`flex gap-3 ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              {m.role === 'assistant' && (
                <div className="w-8 h-8 rounded-lg bg-blue-600/20 text-blue-400 flex items-center justify-center flex-shrink-0 border border-blue-500/20">
                  <Bot className="w-4 h-4" />
                </div>
              )}
              <div
                className={`max-w-[85%] rounded-2xl p-4 text-xs leading-relaxed ${
                  m.role === 'user'
                    ? 'bg-blue-600 text-white shadow-md'
                    : 'bg-slate-800/80 text-slate-200 border border-slate-700/60'
                }`}
              >
                {m.data ? (
                  <div className="space-y-3">
                    <div className="font-semibold text-sm text-white">{m.data.direct_answer}</div>
                    <div className="text-slate-300">{m.data.explanation}</div>
                    {m.data.course_relation && (
                      <div className="p-2.5 bg-slate-900/60 rounded-lg text-indigo-300 border border-slate-800">
                        <span className="font-semibold text-indigo-400">Liên hệ học phần: </span>
                        {m.data.course_relation}
                      </div>
                    )}
                    {/* Textbook reference badge - Clickable to open excerpt modal */}
                    <div className="pt-2 border-t border-slate-700/50 flex items-center justify-between text-[11px] text-blue-400">
                      <button
                        onClick={() => setSelectedRefForExcerpt(m.data!.textbook_reference)}
                        className="flex items-center gap-1.5 font-medium bg-blue-500/10 hover:bg-blue-500/25 px-2.5 py-1 rounded-full border border-blue-500/20 transition cursor-pointer text-blue-300"
                        title="Click để xem nguyên văn đoạn trích giáo trình tiếng Trung"
                      >
                        <Bookmark className="w-3 h-3 text-blue-400" />
                        <span className="underline decoration-dotted">{m.data.textbook_reference}</span>
                        <ExternalLink className="w-2.5 h-2.5 text-blue-400 opacity-70" />
                      </button>
                    </div>
                  </div>
                ) : (
                  <div>{m.text}</div>
                )}
              </div>
              {m.role === 'user' && (
                <div className="w-8 h-8 rounded-lg bg-slate-700 text-slate-300 flex items-center justify-center flex-shrink-0">
                  <User className="w-4 h-4" />
                </div>
              )}
            </div>
          ))}

          {/* Typing spinner indicator (T-FE-11) */}
          {loading && (
            <div className="flex gap-3 items-center text-xs text-slate-400 animate-fadeIn">
              <div className="w-8 h-8 rounded-lg bg-blue-600/20 text-blue-400 flex items-center justify-center flex-shrink-0 border border-blue-500/20">
                <Bot className="w-4 h-4 animate-bounce" />
              </div>
              <div className="bg-slate-800/80 border border-slate-700/60 rounded-2xl px-4 py-3 flex items-center gap-2">
                <div className="flex gap-1">
                  <span className="w-2 h-2 rounded-full bg-blue-400 animate-ping" />
                  <span className="w-2 h-2 rounded-full bg-blue-400 animate-pulse delay-75" />
                  <span className="w-2 h-2 rounded-full bg-blue-400 animate-pulse delay-150" />
                </div>
                <span className="text-[11px] text-slate-300">
                  Đang tra cứu trang sách giáo trình và đối chiếu ngữ nghĩa...
                </span>
              </div>
            </div>
          )}
        </div>

        {/* Form input */}
        <form onSubmit={handleSend} className="mt-4 pt-3 border-t border-slate-800 flex gap-2">
          <input
            type="text"
            value={inputQuestion}
            onChange={(e) => setInputQuestion(e.target.value)}
            placeholder={
              labels.chat_placeholder || 'Nhập câu hỏi kỹ thuật điện (tiếng Trung hoặc tiếng Việt)...'
            }
            className="flex-1 bg-slate-800 border border-slate-700 rounded-xl px-4 py-2.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-blue-500"
          />
          <button
            type="submit"
            disabled={!inputQuestion.trim() || loading}
            className="px-4 py-2.5 bg-blue-600 hover:bg-blue-500 disabled:bg-slate-800 disabled:text-slate-600 text-white rounded-xl text-xs font-semibold flex items-center gap-1.5 transition shadow-lg shadow-blue-500/20"
          >
            <Send className="w-3.5 h-3.5" />
            <span>{labels.chat_send || 'Gửi'}</span>
          </button>
        </form>
      </div>

      {/* Source excerpt modal for chat citations */}
      <SourceExcerptModal
        isOpen={Boolean(selectedRefForExcerpt)}
        onClose={() => setSelectedRefForExcerpt(null)}
        referenceText={selectedRefForExcerpt || ''}
        language={language}
      />
    </div>
  );
};
