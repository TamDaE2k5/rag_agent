export interface ParameterItem {
  name: string;
  symbol: string;
  value?: number;
  unit: string;
  is_confirmed: boolean;
  note?: string;
}

export interface UnknownItem {
  symbol: string;
  name: string;
  unit: string;
}

export interface ExtractedData {
  problem_type: string;
  raw_text_zh: string;
  interpreted_text_vi: string;
  parameters: ParameterItem[];
  unknowns: UnknownItem[];
  assumptions: string[];
  confidence_score: number;
  requires_user_confirmation: boolean;
}

export interface SolutionStep {
  step_number: number;
  title: string;
  explanation: string;
  formula_latex?: string;
  calculated_value?: string;
  verified_by_tool: boolean;
}

export interface SolutionResponse {
  session_id: string;
  status: string;
  problem_type: string;
  extracted_data: ExtractedData;
  steps: SolutionStep[];
  final_answer: string;
  unit: string;
  textbook_reference: string;
  warnings: string[];
  language: string;
}

export interface ChatResponse {
  session_id: string;
  direct_answer: string;
  explanation: string;
  course_relation: string;
  example?: string;
  textbook_reference: string;
  notes?: string;
  language: string;
}

export interface SessionItem {
  id: string;
  title: string;
  created_at: string;
  type: string;
  preview: string;
}
