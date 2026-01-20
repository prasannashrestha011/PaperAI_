import axios from "axios";
import { DocumentResponse, DocUploadResponse } from "@/lib/types";

const API_URL = `http://localhost:8000/pdf`;

export const docService = {
  async getDocBlob(user_id: string, doc_id: string): Promise<Blob> {
    const response = await axios.get(`${API_URL}/view/${user_id}/${doc_id}`, {
      responseType: "blob", 
    });
    return response.data; 
  },
  async getDocInfo(doc_id:string):Promise<DocumentResponse>{
    const response= await axios.get(`${API_URL}/info/${doc_id}`)
    return response.data
  }
  ,

  async uploadDoc(user_id: string, doc: File): Promise<DocUploadResponse> {
    const formData = new FormData();
    formData.append("file", doc);
    formData.append("user_id", user_id);

    const response = await axios.post(`${API_URL}/upload`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data;
  },
};
