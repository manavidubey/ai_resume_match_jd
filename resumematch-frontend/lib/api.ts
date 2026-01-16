import axios from "axios";

const api = axios.create({
  baseURL: "",
  timeout: 30000,
});

export const resumeApi = {
  uploadResume: async (file: File) => {
    const formData = new FormData();
    formData.append("file", file);

    const response = await api.post("/api/upload-resume", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    return response.data;
  },

  createJob: async (jobData: any) => {
    const response = await api.post("/api/jobs", jobData);
    return response.data;
  },

  getJob: async (jobId: string) => {
    const response = await api.get(`/api/jobs/${jobId}`);
    return response.data;
  },

  runMatching: async (jobId: string) => {
    const response = await api.post(`/api/match/${jobId}`);
    return response.data;
  },

  getMatches: async (jobId: string) => {
    const response = await api.get(`/api/matches/${jobId}`);
    return response.data;
  },
};

export default api;
