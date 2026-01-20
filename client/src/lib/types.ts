// Authentication types
export interface AuthRequest {
  username: string;
  password: string;
}

export interface AuthResponse {
  success: boolean;
  message: string;
  token?: string;
  user?: {
    username: string;
  };
}

export interface AuthContextType {
  isAuthenticated: boolean;
  user: { username: string } | null;
  login: (username: string, password: string) => Promise<void>;
  register: (username: string, password: string) => Promise<void>;
  logout: () => void;
}

//Document types
export interface DocumentResponse{
  user_id:string
  document_id:string
  file_name:string
  file_path:string
  file_size:string
  uploaded_timestamp:Date
}

export interface SessionResponse{
  session_id:string
  user_id:string
  document_id:string
  provider:"gemini"|"grok"|"claude"
  model:"string"
}

export interface DocUploadResponse{
  doc_out:DocumentResponse
  session_out:SessionResponse
}