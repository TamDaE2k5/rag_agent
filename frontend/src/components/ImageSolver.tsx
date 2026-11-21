import React, { useState, useRef } from 'react';
import { Upload, RotateCw, CheckCircle2, AlertCircle, Bookmark, Calculator, ArrowRight } from 'lucide-react';
import { api } from '../services/api';
import { SolutionResponse } from '../types';

interface ImageSolverProps {
  language: 'vi' | 'zh-CN';
  labels: Record<string, string>;
}

export const ImageSolver: React.FC<ImageSolverProps> = ({ language, labels }) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [rotateAngle, setRotateAngle] = useState<number>(0);
  const [loading, setLoading] = useState<boolean>(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [solution, setSolution] = useState<SolutionResponse | null>(null);
  
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      setRotateAngle(0);
      setSolution(null);
      setErrorMsg(null);
    }
  };

  const handleRotate = () => {
    setRotateAngle((prev) => (prev + 90) % 360);
  };

  const handleSolve = async () => {
    if (!selectedFile) return;
    setLoading(true);
    setErrorMsg(null);
    try {
      const data = await api.solveImage(selectedFile, rotateAngle, language);
      setSolution(data);
    } catch (err: any) {
      setErrorMsg(err.response?.data?.detail || 'Không thể kết nối API hoặc xử lý ảnh.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 max-w-7xl mx-auto py-6 px-4">
      {/* Cột trái: Upload & Xem trước ảnh */}
      <div className="lg:col-span-5 space-y-4">
        <div className="glass-panel p-5 rounded-2xl border border-slate-800">
          <h2 className="text-base font-semibold text-white mb-2 flex items-center justify-between">
            <span>{labels.upload_title || 'Tải ảnh bài tập tiếng Trung'}</span>
            {previewUrl && (
              <button
                onClick={handleRotate}
                className="flex items-center gap-1 text-xs px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-blue-400 rounded-lg transition"
              >
                <RotateCw className="w-3.5 h-3.5" />
                <span>{labels.btn_rotate || 'Xoay'}</span>
              </button>
            )}
          </h2>

          <div
            onClick={() => fileInputRef.current?.click()}
            className={`border-2 border-dashed rounded-xl p-6 text-center cursor-pointer transition-all ${
              previewUrl
                ? 'border-blue-500/40 bg-slate-900/40'
                : 'border-slate-700 hover:border-blue-500/60 bg-slate-800/40'
            }`}
          >
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileChange}
              accept="image/jpeg,image/png,image/webp"
              className="hidden"
            />
            {previewUrl ? (
              <div className="flex justify-center items-center overflow-hidden max-h-[380px] rounded-lg bg-black/40">
                <img
                  src={previewUrl}
                  alt="Đề bài"
                  style={{ transform: `rotate(${rotateAngle}deg)` }}
                  className="max-h-[380px] object-contain transition-transform duration-200"
                />
              </div>
            ) : (
              <div className="py-10 space-y-3">
                <div className="w-12 h-12 rounded-full bg-blue-500/10 text-blue-400 flex items-center justify-center mx-auto">
                  <Upload className="w-6 h-6" />
                </div>
                <p className="text-sm text-slate-300 font-medium">
                  {labels.upload_hint || 'Kéo thả hoặc bấm để chọn ảnh JPG, PNG'}
                </p>
                <p className="text-xs text-slate-500">
                  Hỗ trợ sơ đồ điện, mạch rơ-le, công thức viết tay tiếng Trung
                </p>
              </div>
            )}
          </div>

          <button
            onClick={handleSolve}
            disabled={!selectedFile || loading}
            className={`mt-4 w-full py-3 px-4 rounded-xl font-medium text-sm flex items-center justify-center gap-2 transition shadow-lg ${
              !selectedFile || loading
                ? 'bg-slate-800 text-slate-500 cursor-not-allowed'
                : 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white hover:from-blue-500 hover:to-indigo-500 shadow-blue-500/25'
            }`}
          >
            {loading ? (
              <>
                <div className="w-4 h-4 border-2 border-white/20 border-t-white rounded-full animate-spin" />
                <span>{labels.btn_solving || 'Đang nhận diện & tính toán...'}</span>
              </>
            ) : (
              <>
                <span>{labels.btn_solve || 'Bắt đầu phân tích & giải bài'}</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>

          {errorMsg && (
            <div className="mt-3 p-3 bg-red-500/10 border border-red-500/30 rounded-xl text-red-400 text-xs flex items-center gap-2">
              <AlertCircle className="w-4 h-4 flex-shrink-0" />
              <span>{errorMsg}</span>
            </div>
          )}
        </div>
      </div>

      {/* Cột phải: Kết quả bài giải */}
      <div className="lg:col-span-7 space-y-4">
        {solution ? (
          <div className="space-y-4">
            {/* 1. Dữ kiện trích xuất & Sơ đồ */}
            <div className="glass-panel p-5 rounded-2xl border border-slate-800">
              <div className="flex items-center justify-between pb-3 border-b border-slate-800 mb-3">
                <h3 className="text-sm font-semibold text-white flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-blue-500" />
                  {labels.section_extracted || '1. Dữ kiện trích xuất & Sơ đồ'}
                </h3>
                <span className="text-xs px-2.5 py-0.5 rounded-full bg-slate-800 text-slate-400 border border-slate-700">
                  {solution.problem_type}
                </span>
              </div>

              {solution.extracted_data.interpreted_text_vi && (
                <div className="p-3 bg-slate-800/60 rounded-xl text-xs text-slate-300 mb-3 leading-relaxed border border-slate-700/50">
                  <span className="font-semibold text-blue-400">Đề bài (Việt hóa): </span>
                  {solution.extracted_data.interpreted_text_vi}
                </div>
              )}

              <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
                {solution.extracted_data.parameters.map((p, idx) => (
                  <div key={idx} className="p-2.5 bg-slate-800/40 rounded-lg border border-slate-700/40 text-xs">
                    <div className="text-slate-400 font-medium truncate">{p.name} ({p.symbol})</div>
                    <div className="text-sm font-bold text-white mt-0.5">
                      {p.value !== undefined ? p.value : '--'} {p.unit}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* 2. Lời giải chi tiết */}
            <div className="glass-panel p-5 rounded-2xl border border-slate-800 space-y-4">
              <h3 className="text-sm font-semibold text-white flex items-center gap-2 pb-3 border-b border-slate-800">
                <span className="w-2 h-2 rounded-full bg-indigo-500" />
                {labels.section_solution || '2. Lời giải chi tiết từng bước'}
              </h3>

              <div className="space-y-3">
                {solution.steps.map((step) => (
                  <div key={step.step_number} className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/40 space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-bold text-blue-400 uppercase tracking-wider">
                        Bước {step.step_number}: {step.title}
                      </span>
                      {step.verified_by_tool && (
                        <span className="flex items-center gap-1 text-[11px] text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/20">
                          <CheckCircle2 className="w-3 h-3" />
                          <span>Kiểm chứng Python</span>
                        </span>
                      )}
                    </div>
                    <p className="text-xs text-slate-300 leading-relaxed">{step.explanation}</p>
                    {step.formula_latex && (
                      <div className="p-2.5 bg-slate-900/60 rounded-lg font-mono text-xs text-indigo-300 overflow-x-auto border border-slate-800">
                        {step.formula_latex}
                      </div>
                    )}
                    {step.calculated_value && (
                      <div className="text-xs text-slate-200 font-semibold flex items-center gap-1">
                        <span className="text-slate-400">Kết quả:</span>
                        <span className="text-emerald-400">{step.calculated_value}</span>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>

            {/* 3. Kết luận & Căn cứ giáo trình */}
            <div className="glass-panel p-5 rounded-2xl border border-blue-500/30 bg-blue-950/20 space-y-3">
              <div className="flex items-center justify-between">
                <h3 className="text-sm font-semibold text-white flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                  <span>{labels.section_conclusion || '3. Kết luận & Đáp số'}</span>
                </h3>
                <div className="flex items-center gap-1 text-xs text-blue-300 bg-blue-500/20 px-3 py-1 rounded-full border border-blue-400/30">
                  <Bookmark className="w-3.5 h-3.5" />
                  <span>{solution.textbook_reference}</span>
                </div>
              </div>

              <div className="text-sm font-bold text-white bg-slate-900/60 p-4 rounded-xl border border-slate-800">
                {solution.final_answer}
              </div>
            </div>
          </div>
        ) : (
          <div className="glass-panel p-12 rounded-2xl border border-slate-800 text-center text-slate-500 space-y-3">
            <Calculator className="w-12 h-12 mx-auto text-slate-600 opacity-60" />
            <p className="text-sm">Chưa có kết quả. Vui lòng tải ảnh đề bài và nhấn "Bắt đầu giải".</p>
          </div>
        )}
      </div>
    </div>
  );
};
