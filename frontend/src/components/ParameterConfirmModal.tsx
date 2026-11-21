import React, { useState } from 'react';
import { X, Check, Plus, Trash2, AlertTriangle, Sliders, RefreshCw } from 'lucide-react';
import { ParameterItem } from '../types';

interface ParameterConfirmModalProps {
  isOpen: boolean;
  onClose: () => void;
  parameters: ParameterItem[];
  requiresConfirmation?: boolean;
  onConfirm: (updatedParams: ParameterItem[]) => Promise<void> | void;
  language: 'vi' | 'zh-CN';
}

export const ParameterConfirmModal: React.FC<ParameterConfirmModalProps> = ({
  isOpen,
  onClose,
  parameters,
  requiresConfirmation = false,
  onConfirm,
  language,
}) => {
  const [params, setParams] = useState<ParameterItem[]>(() =>
    parameters.map((p) => ({ ...p }))
  );
  const [isSubmitting, setIsSubmitting] = useState(false);

  if (!isOpen) return null;

  const handleChange = (index: number, field: keyof ParameterItem, value: any) => {
    setParams((prev) => {
      const next = [...prev];
      next[index] = { ...next[index], [field]: value };
      return next;
    });
  };

  const handleAddParam = () => {
    setParams((prev) => [
      ...prev,
      {
        name: 'Đại lượng mới',
        symbol: 'X',
        value: 0,
        unit: '',
        is_confirmed: true,
        note: 'Người dùng bổ sung',
      },
    ]);
  };

  const handleRemoveParam = (index: number) => {
    setParams((prev) => prev.filter((_, i) => i !== index));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    try {
      await onConfirm(params);
      onClose();
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm animate-fadeIn">
      <div className="relative w-full max-w-2xl bg-slate-900 border border-slate-700 rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[85vh]">
        {/* Header */}
        <div className="flex items-center justify-between p-4 px-6 border-b border-slate-800 bg-slate-950/70">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-amber-500/10 text-amber-400 flex items-center justify-center border border-amber-500/20">
              <Sliders className="w-4 h-4" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-white flex items-center gap-2">
                <span>{language === 'vi' ? 'Xác nhận & Điều chỉnh Thông số Đề bài (FR-08)' : '确认并修改题目参数 (FR-08)'}</span>
              </h3>
              <p className="text-[11px] text-slate-400">
                {language === 'vi'
                  ? 'Kiểm tra và sửa lại các số liệu bị mờ hoặc nhận diện sai trước khi tính toán lại'
                  : '核对并在重算前更正模糊或识别有误的数据'}
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Warning notification if AI confidence is uncertain */}
        {requiresConfirmation && (
          <div className="mx-6 mt-4 p-3 bg-amber-500/10 border border-amber-500/30 rounded-xl text-amber-300 text-xs flex items-center gap-2.5">
            <AlertTriangle className="w-4 h-4 flex-shrink-0 text-amber-400" />
            <span>
              {language === 'vi'
                ? 'Hệ thống phát hiện ảnh có độ nét thấp hoặc ký hiệu viết tay không rõ. Vui lòng xác minh kỹ các giá trị được đánh dấu cảnh báo.'
                : '检测到图片清晰度较低或存在手写歧义，请仔细核对标黄的数值。'}
            </span>
          </div>
        )}

        {/* Form table */}
        <form onSubmit={handleSubmit} className="p-6 overflow-y-auto space-y-3 flex-1">
          <div className="space-y-2.5">
            {params.map((p, idx) => (
              <div
                key={idx}
                className={`p-3 rounded-xl border transition-all flex flex-wrap sm:flex-nowrap items-center gap-3 ${
                  !p.is_confirmed
                    ? 'bg-amber-950/20 border-amber-500/40'
                    : 'bg-slate-800/40 border-slate-700/60 hover:border-slate-600'
                }`}
              >
                {/* Ký hiệu */}
                <div className="w-20">
                  <label className="text-[10px] text-slate-400 block mb-0.5">Ký hiệu</label>
                  <input
                    type="text"
                    value={p.symbol}
                    onChange={(e) => handleChange(idx, 'symbol', e.target.value)}
                    className="w-full bg-slate-900 border border-slate-700 rounded-lg px-2 py-1 text-xs text-white font-mono font-semibold focus:outline-none focus:border-blue-500"
                    placeholder="P, Q, U..."
                  />
                </div>

                {/* Tên đại lượng */}
                <div className="flex-1 min-w-[130px]">
                  <label className="text-[10px] text-slate-400 block mb-0.5">Tên đại lượng</label>
                  <input
                    type="text"
                    value={p.name}
                    onChange={(e) => handleChange(idx, 'name', e.target.value)}
                    className="w-full bg-slate-900 border border-slate-700 rounded-lg px-2.5 py-1 text-xs text-slate-200 focus:outline-none focus:border-blue-500"
                    placeholder="Công suất tác dụng..."
                  />
                </div>

                {/* Giá trị số */}
                <div className="w-28">
                  <label className="text-[10px] text-slate-400 block mb-0.5">Giá trị</label>
                  <input
                    type="number"
                    step="any"
                    value={p.value !== undefined ? p.value : ''}
                    onChange={(e) => handleChange(idx, 'value', e.target.value === '' ? undefined : parseFloat(e.target.value))}
                    className="w-full bg-slate-900 border border-slate-700 rounded-lg px-2.5 py-1 text-xs text-emerald-400 font-bold focus:outline-none focus:border-blue-500"
                    placeholder="0.0"
                  />
                </div>

                {/* Đơn vị */}
                <div className="w-20">
                  <label className="text-[10px] text-slate-400 block mb-0.5">Đơn vị</label>
                  <input
                    type="text"
                    value={p.unit}
                    onChange={(e) => handleChange(idx, 'unit', e.target.value)}
                    className="w-full bg-slate-900 border border-slate-700 rounded-lg px-2 py-1 text-xs text-indigo-300 focus:outline-none focus:border-blue-500"
                    placeholder="kW, kvar..."
                  />
                </div>

                {/* Checkbox Đã xác nhận */}
                <div className="flex items-center gap-1.5 pt-3">
                  <button
                    type="button"
                    onClick={() => handleChange(idx, 'is_confirmed', !p.is_confirmed)}
                    title={p.is_confirmed ? 'Đã xác nhận' : 'Cần kiểm tra'}
                    className={`p-1.5 rounded-lg border text-xs transition ${
                      p.is_confirmed
                        ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400'
                        : 'bg-amber-500/10 border-amber-500/30 text-amber-400'
                    }`}
                  >
                    <Check className="w-3.5 h-3.5" />
                  </button>

                  {/* Nút xóa */}
                  <button
                    type="button"
                    onClick={() => handleRemoveParam(idx)}
                    title="Xóa tham số"
                    className="p-1.5 rounded-lg text-slate-500 hover:text-red-400 hover:bg-slate-800 transition"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            ))}
          </div>

          {/* Add parameter button */}
          <button
            type="button"
            onClick={handleAddParam}
            className="w-full py-2 border-2 border-dashed border-slate-800 hover:border-slate-700 rounded-xl text-xs text-slate-400 hover:text-white flex items-center justify-center gap-1.5 transition"
          >
            <Plus className="w-3.5 h-3.5" />
            <span>Thêm thông số khác</span>
          </button>
        </form>

        {/* Footer */}
        <div className="p-4 px-6 border-t border-slate-800 bg-slate-950/80 flex items-center justify-between">
          <button
            type="button"
            onClick={onClose}
            className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-medium rounded-xl transition"
          >
            Hủy
          </button>
          <button
            type="button"
            onClick={handleSubmit}
            disabled={isSubmitting}
            className="px-5 py-2 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white text-xs font-semibold rounded-xl transition flex items-center gap-2 shadow-lg shadow-blue-500/20"
          >
            {isSubmitting ? (
              <>
                <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                <span>Đang tính toán lại...</span>
              </>
            ) : (
              <>
                <Check className="w-3.5 h-3.5" />
                <span>Xác nhận & Tính toán lại</span>
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};
