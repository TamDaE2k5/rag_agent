import axios from 'axios';
import { SolutionResponse, ChatResponse, SessionItem } from '../types';

const API_BASE = '/api/v1';

export const api = {
  async solveImage(file: File, rotateAngle: number = 0, language: string = 'vi'): Promise<SolutionResponse> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('rotate_angle', rotateAngle.toString());
    formData.append('language', language);

    const res = await axios.post<SolutionResponse>(`${API_BASE}/solver/solve-image`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return res.data;
  },

  async askChat(question: string, sessionId?: string, language: string = 'vi'): Promise<ChatResponse> {
    const res = await axios.post<ChatResponse>(`${API_BASE}/chat`, {
      question,
      session_id: sessionId,
      language,
    });
    return res.data;
  },

  async getHistory(): Promise<SessionItem[]> {
    const res = await axios.get<SessionItem[]>(`${API_BASE}/history`);
    return res.data;
  },

  async getSettings(): Promise<any> {
    const res = await axios.get(`${API_BASE}/settings`);
    return res.data;
  }
};
