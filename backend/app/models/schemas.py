from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class ParameterItem(BaseModel):
    name: str = Field(..., description="Tên đại lượng")
    symbol: str = Field(..., description="Ký hiệu (P, Q, U, I, cos phi...)")
    value: Optional[float] = Field(None, description="Giá trị số")
    unit: str = Field("", description="Đơn vị đo (kW, kvar, kV, A, km...)")
    is_confirmed: bool = Field(True, description="Đã được xác nhận hay nghi vấn")
    note: Optional[str] = Field(None, description="Ghi chú nếu số mờ/không chắc chắn")

class UnknownItem(BaseModel):
    symbol: str = Field(..., description="Ký hiệu đại lượng cần tìm")
    name: str = Field(..., description="Tên đại lượng cần tìm")
    unit: str = Field("", description="Đơn vị mong đợi")

class ExtractedData(BaseModel):
    problem_type: str = Field("calculation", description="Dạng bài: calculation, diagram, error_check, theory, logic_control")
    raw_text_zh: str = Field("", description="Nội dung chữ tiếng Trung trích xuất từ đề")
    interpreted_text_vi: str = Field("", description="Diễn giải đề bài sang tiếng Việt")
    parameters: List[ParameterItem] = Field(default_factory=list, description="Danh sách thông số đã bóc tách")
    unknowns: List[UnknownItem] = Field(default_factory=list, description="Các đại lượng cần tìm")
    assumptions: List[str] = Field(default_factory=list, description="Các giả thiết kỹ thuật bổ sung")
    confidence_score: float = Field(1.0, description="Độ tin cậy của việc nhận diện (0-1)")
    requires_user_confirmation: bool = Field(False, description="Cần người dùng xác nhận thông số mờ không")

class SolutionStep(BaseModel):
    step_number: int = Field(..., description="Thứ tự bước")
    title: str = Field(..., description="Tên bước thực hiện")
    explanation: str = Field(..., description="Giải thích phương pháp")
    formula_latex: Optional[str] = Field(None, description="Công thức toán dạng LaTeX")
    substituted_values: Optional[str] = Field(None, description="Biểu thức sau khi thay số")
    calculated_value: Optional[str] = Field(None, description="Kết quả trung gian")
    verified_by_tool: bool = Field(False, description="Được kiểm tra bởi Python Calculator")

class SolutionResponse(BaseModel):
    model_config = {"extra": "allow"}

    session_id: str
    status: str = "success"
    problem_type: str
    extracted_data: ExtractedData
    parameters: Optional[List[ParameterItem]] = None
    steps: List[SolutionStep] = Field(default_factory=list)
    final_answer: str = Field(..., description="Đáp số cuối cùng")
    unit: str = Field("", description="Đơn vị kết quả")
    textbook_reference: str = Field("PDF giáo trình, trang --", description="Trích dẫn số trang giáo trình tiếng Trung")
    warnings: List[str] = Field(default_factory=list)
    language: str = "vi"

class ConfirmParametersRequest(BaseModel):
    session_id: str
    parameters: List[ParameterItem]
    language: str = "vi"

class ChatMessageRequest(BaseModel):
    session_id: Optional[str] = None
    question: str = Field(..., description="Câu hỏi tiếng Trung hoặc tiếng Việt")
    language: str = Field("vi", description="Ngôn ngữ câu trả lời mong muốn: vi hoặc zh-CN")

class ChatResponse(BaseModel):
    model_config = {"extra": "allow"}

    session_id: str
    direct_answer: str = Field(..., description="Trả lời trực tiếp kết luận")
    explanation: str = Field(..., description="Giải thích nguyên lý/cơ chế")
    course_relation: str = Field(..., description="Liên hệ tới tự động hóa lưới điện phân phối")
    example: Optional[str] = Field(None, description="Ví dụ minh họa")
    textbook_reference: str = Field(..., description="Căn cứ: PDF giáo trình, trang N")
    notes: Optional[str] = Field(None, description="Lưu ý hoặc giới hạn")
    language: str = "vi"

class SessionItem(BaseModel):
    id: str
    title: str
    created_at: str
    type: str # 'image_solver' | 'chat'
    preview: str
