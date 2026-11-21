import React, { useEffect, useState } from 'react';
import { Clock, ExternalLink, Calendar, FileText } from 'lucide-react';
import { api } from '../services/api';
import { SessionItem } from '../types';

export const HistoryList: React.FC = () => {
  const [sessions, setSessions] = useState<SessionItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getHistory()
      .then((data) => setSessions(data))
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="max-w-4xl mx-auto py-6 px-4 space-y-4">
      <div className="flex items-center justify-between pb-3 border-b border-slate-800">
        <h2 className="text-base font-bold text-white flex items-center gap-2">
          <Clock className="w-5 h-5 text-blue-400" />
          <span>Lịch sử các phiên giải bài & hỏi đáp</span>
        </h2>
        <span className="text-xs px-2.5 py-1 rounded-full bg-slate-800 text-slate-400 border border-slate-700">
          {sessions.length} phiên đã lưu
        </span>
      </div>

      {loading ? (
        <div className="text-center py-12 text-xs text-slate-500">Đang tải lịch sử...</div>
      ) : (
        <div className="space-y-3">
          {sessions.map((s) => (
            <div
              key={s.id}
              className="glass-panel p-4 rounded-xl border border-slate-800 hover:border-slate-700 transition flex items-start justify-between gap-4 cursor-pointer"
            >
              <div className="space-y-1.5">
                <div className="flex items-center gap-2">
                  <span className={`text-[10px] font-bold px-2 py-0.5 rounded ${
                    s.type === 'image_solver' ? 'bg-blue-500/10 text-blue-400 border border-blue-500/20' : 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                  }`}>
                    {s.type === 'image_solver' ? 'Giải ảnh' : 'Hỏi đáp'}
                  </span>
                  <h3 className="text-xs font-semibold text-white">{s.title}</h3>
                </div>
                <p className="text-xs text-slate-400 line-clamp-1">{s.preview}</p>
                <div className="flex items-center gap-1.5 text-[11px] text-slate-500">
                  <Calendar className="w-3 h-3" />
                  <span>{s.created_at}</span>
                </div>
              </div>

              <button className="text-slate-400 hover:text-white p-1.5 rounded-lg hover:bg-slate-800 transition">
                <ExternalLink className="w-4 h-4" />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
