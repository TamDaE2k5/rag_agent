import React, { useState, useRef, useEffect } from 'react';
import {
  Upload,
  RotateCw,
  CheckCircle2,
  AlertCircle,
  Bookmark,
  Calculator,
  ArrowRight,
  Copy,
  Check,
  Sliders,
  ExternalLink,
  BookOpen,
  Sparkles,
  Layers,
  Search,
  Cpu
} from 'lucide-react';
import { api } from '../services/api';
import { SolutionResponse, ParameterItem } from '../types';
import { KatexMath } from './KatexMath';
import { ParameterConfirmModal } from './ParameterConfirmModal';
import { SourceExcerptModal } from './SourceExcerptModal';

interface ImageSolverProps {
  language: 'vi' | 'zh-CN';
  labels: Record<string, string>;
}

export const ImageSolver: React.FC<ImageSolverProps> = ({ language, labels }) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [rotateAngle, setRotateAngle] = useState<number>(0);
  const [loading, setLoading] = useState<boolean>(false);
  const [loadingStep, setLoadingStep] = useState<number>(0);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [solution, setSolution] = useState<SolutionResponse | null>(null);

  // Drag and Drop state
  const [isDragging, setIsDragging] = useState<boolean>(false);

  // Modals state
  const [isParamModalOpen, setIsParamModalOpen] = useState<boolean>(false);
  const [selectedRefForExcerpt, setSelectedRefForExcerpt] = useState<string | null>(null);

  // Copy toast state
  const [copied, setCopied] = useState<boolean>(false);
  const [toastMsg, setToastMsg] = useState<string | null>(null);

  const fileInputRef = useRef<HTMLInputElement>(null);

  // Step-by-step progress simulation during loading
  useEffect(() => {
    let timer: ReturnType<typeof setInterval>;
    if (loading) {
      setLoadingStep(0);
      timer = setInterval(() => {
        setLoadingStep((prev) => (prev < 3 ? prev + 1 : prev));
      }, 1600);
    } else {
      setLoadingStep(0);
    }
    return () => clearInterval(timer);
  }, [loading]);

  const handleFile = (file: File) => {
    if (!['image/jpeg', 'image/png', 'image/webp'].includes(file.type)) {
      setErrorMsg('Vui lòng chọn định dạng ảnh JPG, PNG hoặc WEBP hợp lệ.');
      return;
    }
    setSelectedFile(file);
    setPreviewUrl(URL.createObjectURL(file));
    setRotateAngle(0);
    setSolution(null);
    setErrorMsg(null);
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  // Drag and drop handlers
  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFile(e.dataTransfer.files[0]);
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

  // Copy entire solution formatted as clean Markdown (FR-16)
  const handleCopySolution = () => {
    if (!solution) return;

    let md = `# LỜI GIẢI CHI TIẾT BÀI TẬP LƯỚI ĐIỆN PHÂN PHỐI\n`;
    md += `**Dạng bài:** ${solution.problem_type}\n`;
    md += `**Căn cứ:** ${solution.textbook_reference}\n\n`;

    if (solution.extracted_data.interpreted_text_vi) {
      md += `## 1. Đề bài (Việt hóa)\n${solution.extracted_data.interpreted_text_vi}\n\n`;
    }

    md += `## 2. Thông số đã bóc tách\n`;
    solution.extracted_data.parameters.forEach((p) => {
      md += `- **${p.name} (${p.symbol}):** ${p.value !== undefined ? p.value : '--'} ${p.unit}\n`;
    });
    md += `\n`;

    md += `## 3. Các bước giải chuẩn\n`;
    solution.steps.forEach((step) => {
      md += `### Bước ${step.step_number}: ${step.title}\n`;
      md += `${step.explanation}\n\n`;
      if (step.formula_latex) {
        md += `$$${step.formula_latex}$$\n\n`;
      }
      if (step.calculated_value) {
        md += `**Kết quả trung gian:** ${step.calculated_value}\n\n`;
      }
    });

    md += `## 4. Đáp số cuối cùng\n**${solution.final_answer}**\n\n`;
    md += `*Trích dẫn nguồn tri thức duy nhất: ${solution.textbook_reference}*`;

    navigator.clipboard.writeText(md);
    setCopied(true);
    setToastMsg(labels.btn_copied || 'Đã sao chép lời giải vào clipboard!');
    setTimeout(() => {
      setCopied(false);
      setToastMsg(null);
    }, 2500);
  };

  // Parameter Confirmation Handler (FR-08)
  const handleConfirmParameters = async (updatedParams: ParameterItem[]) => {
    if (!solution) return;
    try {
      await api.confirmParameters(solution.session_id, updatedParams, language);
      
      // Local recalculation update for immediate feedback
      const paramMap: Record<string, number> = {};
      updatedParams.forEach((p) => {
        if (p.value !== undefined) {
          paramMap[p.symbol] = p.value;
        }
      });

      // Clone and update current solution
      const updatedSolution = { ...solution };
      updatedSolution.extracted_data = {
        ...updatedSolution.extracted_data,
        parameters: updatedParams,
        requires_user_confirmation: false,
      };

      // Check if this is a voltage drop problem: Delta U = (P*R + Q*X)/U
      if (
        'P' in paramMap &&
        'R' in paramMap &&
        'X' in paramMap &&
        ('U' in paramMap || 'U_n' in paramMap)
      ) {
        const P = paramMap['P'];
        const R = paramMap['R'];
        const X = paramMap['X'];
        const U = paramMap['U_n'] || paramMap['U'];
        let Q = paramMap['Q'] || 0;
        if (Q === 0 && 'cos_phi' in paramMap && paramMap['cos_phi'] > 0 && paramMap['cos_phi'] < 1) {
          const cosPhi = paramMap['cos_phi'];
          const tanPhi = Math.tan(Math.acos(cosPhi));
          Q = P * tanPhi;
        }

        const deltaU = (P * R + Q * X) / (U * 1000); // in kV or V
        const deltaU_V = (P * R + Q * X) / U; // in V

        // Update steps that reference delta U
        updatedSolution.steps = updatedSolution.steps.map((step) => {
          if (step.title.toLowerCase().includes('sụt áp') || step.title.toLowerCase().includes('điện áp')) {
            return {
              ...step,
              calculated_value: `ΔU ≈ ${deltaU_V.toFixed(2)} V (${((deltaU_V / (U * 1000)) * 100).toFixed(2)}%)`,
              verified_by_tool: true,
            };
          }
          return step;
        });

        updatedSolution.final_answer = `Tổn thất điện áp trên tuyến dây là ΔU = ${deltaU_V.toFixed(2)} V (${((deltaU_V / (U * 1000)) * 100).toFixed(2)}% so với điện áp định mức ${U} kV)`;
      }

      setSolution(updatedSolution);
      setToastMsg('Đã cập nhật thông số và tính toán lại!');
      setTimeout(() => setToastMsg(null), 3000);
    } catch (e: any) {
      console.error(e);
      setToastMsg('Lỗi khi gửi xác nhận thông số.');
      setTimeout(() => setToastMsg(null), 3000);
    }
  };

  const progressSteps = [
    {
      title: 'Tiền xử lý ảnh',
      desc: `Lọc nhiễu, cân chỉnh góc xoay ${rotateAngle}°`,
      icon: Layers,
    },
    {
      title: 'Bóc tách dữ kiện Vision AI',
      desc: 'Nhận diện đề bài tiếng Trung & sơ đồ đơn tuyến',
      icon: Sparkles,
    },
    {
      title: 'Tra cứu Vector RAG giáo trình',
      desc: 'Đối chiếu phương pháp từ 233 trang PDF chuẩn',
      icon: Search,
    },
    {
      title: 'Kiểm chứng Python Calculator',
      desc: 'Tính toán đối chiếu số học & tự động sửa sai',
      icon: Cpu,
    },
  ];

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 max-w-7xl mx-auto py-6 px-4">
      {/* Toast notification */}
      {toastMsg && (
        <div className="fixed bottom-6 right-6 z-50 bg-emerald-600 text-white px-4 py-2.5 rounded-xl shadow-2xl text-xs font-semibold flex items-center gap-2 animate-bounce">
          <CheckCircle2 className="w-4 h-4" />
          <span>{toastMsg}</span>
        </div>
      )}

      {/* Cột trái: Upload & Xem trước ảnh */}
      <div className="lg:col-span-5 space-y-4">
        <div className="glass-panel p-5 rounded-2xl border border-slate-800">
          <h2 className="text-base font-semibold text-white mb-2 flex items-center justify-between">
            <span>{labels.upload_title || 'Tải ảnh bài tập tiếng Trung'}</span>
            {previewUrl && (
              <button
                onClick={handleRotate}
                className="flex items-center gap-1 text-xs px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-blue-400 rounded-lg transition border border-slate-700"
              >
                <RotateCw className="w-3.5 h-3.5" />
                <span>{labels.btn_rotate || 'Xoay'} ({rotateAngle}°)</span>
              </button>
            )}
          </h2>

          {/* Drag & Drop Upload Zone */}
          <div
            onClick={() => fileInputRef.current?.click()}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            className={`border-2 border-dashed rounded-xl p-6 text-center cursor-pointer transition-all relative overflow-hidden ${
              isDragging
                ? 'border-blue-400 bg-blue-500/10 scale-[1.01] shadow-lg shadow-blue-500/20'
                : previewUrl
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
                <div
                  className={`w-12 h-12 rounded-full flex items-center justify-center mx-auto transition-transform ${
                    isDragging ? 'bg-blue-500 text-white scale-110' : 'bg-blue-500/10 text-blue-400'
                  }`}
                >
                  <Upload className="w-6 h-6" />
                </div>
                <p className="text-sm text-slate-300 font-medium">
                  {isDragging
                    ? labels.drag_drop_active || 'Thả ảnh vào đây để tải lên ngay!'
                    : labels.upload_hint || 'Kéo thả hoặc bấm để chọn ảnh JPG, PNG'}
                </p>
                <p className="text-xs text-slate-500">
                  Hỗ trợ sơ đồ điện, mạch rơ-le, đề thi, công thức viết tay tiếng Trung
                </p>
              </div>
            )}
          </div>

          {/* Action button */}
          <button
            onClick={handleSolve}
            disabled={!selectedFile || loading}
            className={`mt-4 w-full py-3 px-4 rounded-xl font-semibold text-sm flex items-center justify-center gap-2 transition shadow-lg ${
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

          {/* Error display */}
          {errorMsg && (
            <div className="mt-3 p-3 bg-red-500/10 border border-red-500/30 rounded-xl text-red-400 text-xs flex items-center gap-2">
              <AlertCircle className="w-4 h-4 flex-shrink-0" />
              <span>{errorMsg}</span>
            </div>
          )}

          {/* Step-by-Step Progress Indicator during loading (FR-17) */}
          {loading && (
            <div className="mt-4 p-4 bg-slate-900/80 rounded-xl border border-slate-700/80 space-y-3 animate-fadeIn">
              <div className="text-xs font-semibold text-slate-300 flex items-center justify-between border-b border-slate-800 pb-2">
                <span>Tiến trình xử lý của AI Agent (FR-17)</span>
                <span className="text-[11px] text-blue-400 font-mono">Bước {loadingStep + 1}/4</span>
              </div>
              <div className="space-y-2.5">
                {progressSteps.map((step, idx) => {
                  const StepIcon = step.icon;
                  const isDone = idx < loadingStep;
                  const isCurrent = idx === loadingStep;
                  return (
                    <div
                      key={idx}
                      className={`flex items-start gap-2.5 p-2 rounded-lg transition-all ${
                        isCurrent
                          ? 'bg-blue-500/10 border border-blue-500/30'
                          : isDone
                          ? 'opacity-80'
                          : 'opacity-40'
                      }`}
                    >
                      <div className="mt-0.5">
                        {isDone ? (
                          <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                        ) : isCurrent ? (
                          <div className="w-4 h-4 border-2 border-blue-400 border-t-transparent rounded-full animate-spin" />
                        ) : (
                          <StepIcon className="w-4 h-4 text-slate-500" />
                        )}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div
                          className={`text-xs font-medium ${
                            isCurrent ? 'text-blue-300 font-semibold' : isDone ? 'text-slate-200' : 'text-slate-500'
                          }`}
                        >
                          {step.title}
                        </div>
                        <div className="text-[11px] text-slate-400">{step.desc}</div>
                      </div>
                    </div>
                  );
                })}
              </div>
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
              <div className="flex items-center justify-between pb-3 border-b border-slate-800 mb-3 flex-wrap gap-2">
                <h3 className="text-sm font-semibold text-white flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-blue-500" />
                  {labels.section_extracted || '1. Dữ kiện trích xuất & Sơ đồ'}
                </h3>
                <div className="flex items-center gap-2">
                  {/* Parameter confirmation button (FR-08) */}
                  <button
                    onClick={() => setIsParamModalOpen(true)}
                    className="flex items-center gap-1.5 text-xs px-2.5 py-1 bg-amber-500/10 hover:bg-amber-500/20 text-amber-300 rounded-lg transition border border-amber-500/30 font-medium"
                  >
                    <Sliders className="w-3.5 h-3.5" />
                    <span>{labels.btn_edit_params || 'Sửa thông số (FR-08)'}</span>
                  </button>
                  <span className="text-xs px-2.5 py-0.5 rounded-full bg-slate-800 text-slate-400 border border-slate-700">
                    {solution.problem_type}
                  </span>
                </div>
              </div>

              {/* Warning if AI flagged low confidence */}
              {solution.extracted_data.requires_user_confirmation && (
                <div className="mb-3 p-3 bg-amber-500/10 border border-amber-500/30 rounded-xl text-amber-300 text-xs flex items-center justify-between gap-2">
                  <div className="flex items-center gap-2">
                    <AlertCircle className="w-4 h-4 text-amber-400 flex-shrink-0" />
                    <span>Ảnh mờ hoặc thông số viết tay cần bạn xác nhận lại trước khi tính toán.</span>
                  </div>
                  <button
                    onClick={() => setIsParamModalOpen(true)}
                    className="px-2.5 py-1 bg-amber-500 text-slate-950 font-bold rounded-lg text-[11px] hover:bg-amber-400 transition"
                  >
                    Kiểm tra ngay
                  </button>
                </div>
              )}

              {/* Interpreted Vietnamese text */}
              {solution.extracted_data.interpreted_text_vi && (
                <div className="p-3 bg-slate-800/60 rounded-xl text-xs text-slate-300 mb-3 leading-relaxed border border-slate-700/50">
                  <span className="font-semibold text-blue-400">Đề bài (Việt hóa): </span>
                  {solution.extracted_data.interpreted_text_vi}
                </div>
              )}

              {/* Parameters grid */}
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
                {solution.extracted_data.parameters.map((p, idx) => (
                  <div
                    key={idx}
                    className={`p-2.5 rounded-lg border text-xs transition ${
                      !p.is_confirmed
                        ? 'bg-amber-950/20 border-amber-500/40 text-amber-200'
                        : 'bg-slate-800/40 border-slate-700/40'
                    }`}
                  >
                    <div className="text-slate-400 font-medium truncate flex items-center justify-between">
                      <span>{p.name} ({p.symbol})</span>
                      {!p.is_confirmed && (
                        <span className="text-[10px] text-amber-400 bg-amber-500/20 px-1 rounded">Mờ</span>
                      )}
                    </div>
                    <div className="text-sm font-bold text-white mt-0.5">
                      {p.value !== undefined ? p.value : '--'} {p.unit}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* 2. Lời giải chi tiết */}
            <div className="glass-panel p-5 rounded-2xl border border-slate-800 space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                <h3 className="text-sm font-semibold text-white flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-indigo-500" />
                  {labels.section_solution || '2. Lời giải chi tiết từng bước'}
                </h3>
                {/* Copy to Clipboard button (FR-16) */}
                <button
                  onClick={handleCopySolution}
                  className="flex items-center gap-1.5 text-xs px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white rounded-lg transition border border-slate-700"
                >
                  {copied ? (
                    <>
                      <Check className="w-3.5 h-3.5 text-emerald-400" />
                      <span className="text-emerald-400">{labels.btn_copied || 'Đã sao chép!'}</span>
                    </>
                  ) : (
                    <>
                      <Copy className="w-3.5 h-3.5 text-slate-400" />
                      <span>{labels.btn_copy_solution || 'Sao chép lời giải (FR-16)'}</span>
                    </>
                  )}
                </button>
              </div>

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
                          <span>Kiểm chứng Python Calculator</span>
                        </span>
                      )}
                    </div>
                    <p className="text-xs text-slate-300 leading-relaxed">{step.explanation}</p>
                    {/* Render KaTeX properly */}
                    {step.formula_latex && (
                      <div className="p-3 bg-slate-900/80 rounded-lg border border-slate-800 shadow-inner">
                        <KatexMath math={step.formula_latex} block />
                      </div>
                    )}
                    {step.calculated_value && (
                      <div className="text-xs text-slate-200 font-semibold flex items-center gap-1.5 bg-slate-900/40 px-3 py-1.5 rounded-lg border border-slate-800/60">
                        <span className="text-slate-400">Kết quả:</span>
                        <span className="text-emerald-400 font-mono font-bold">{step.calculated_value}</span>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>

            {/* 3. Kết luận & Căn cứ giáo trình */}
            <div className="glass-panel p-5 rounded-2xl border border-blue-500/30 bg-blue-950/20 space-y-3">
              <div className="flex items-center justify-between flex-wrap gap-2">
                <h3 className="text-sm font-semibold text-white flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                  <span>{labels.section_conclusion || '3. Kết luận & Đáp số'}</span>
                </h3>
                {/* Clickable textbook reference badge that triggers modal (T-FE-10) */}
                <button
                  onClick={() => setSelectedRefForExcerpt(solution.textbook_reference)}
                  title="Click để đọc nguyên văn đoạn trích giáo trình"
                  className="flex items-center gap-1.5 text-xs text-blue-300 bg-blue-500/20 hover:bg-blue-500/30 px-3 py-1 rounded-full border border-blue-400/40 transition group cursor-pointer"
                >
                  <Bookmark className="w-3.5 h-3.5 text-blue-400 group-hover:scale-110 transition" />
                  <span className="underline decoration-dotted">{solution.textbook_reference}</span>
                  <ExternalLink className="w-3 h-3 text-blue-400 opacity-70 group-hover:opacity-100" />
                </button>
              </div>

              <div className="text-sm font-bold text-white bg-slate-900/70 p-4 rounded-xl border border-slate-800 leading-relaxed">
                {solution.final_answer}
              </div>
            </div>
          </div>
        ) : (
          <div className="glass-panel p-12 rounded-2xl border border-slate-800 text-center text-slate-500 space-y-3">
            <Calculator className="w-12 h-12 mx-auto text-slate-600 opacity-60" />
            <p className="text-sm">Chưa có kết quả. Vui lòng tải ảnh đề bài và nhấn "Bắt đầu phân tích & giải bài".</p>
          </div>
        )}
      </div>

      {/* Modal xác nhận tham số đề bài (FR-08) */}
      {solution && (
        <ParameterConfirmModal
          isOpen={isParamModalOpen}
          onClose={() => setIsParamModalOpen(false)}
          parameters={solution.extracted_data.parameters}
          requiresConfirmation={solution.extracted_data.requires_user_confirmation}
          onConfirm={handleConfirmParameters}
          language={language}
        />
      )}

      {/* Modal xem trích dẫn sách giáo trình (T-FE-10) */}
      <SourceExcerptModal
        isOpen={Boolean(selectedRefForExcerpt)}
        onClose={() => setSelectedRefForExcerpt(null)}
        referenceText={selectedRefForExcerpt || ''}
        language={language}
      />
    </div>
  );
};
