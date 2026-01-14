import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
});

// Request interceptor to add auth headers if needed
api.interceptors.request.use(
  (config) => {
    // Add any authorization headers here if needed
    // config.headers.Authorization = `Bearer ${localStorage.getItem('token')}`;
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors globally
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Handle global error responses here
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export const resumeApi = {
  uploadResume: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post('/upload-resume/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  },

  createJob: async (jobData: any) => {
    const response = await api.post('/jobs/', jobData);
    return response.data;
  },

  getJob: async (jobId: string) => {
    const response = await api.get(`/jobs/${jobId}`);
    return response.data;
  },

  runMatching: async (jobId: string) => {
    const response = await api.post(`/match/${jobId}`);
    return response.data;
  },

  getMatches: async (jobId: string) => {
    const response = await api.get(`/matches/${jobId}`);
    return response.data;
  },
};

export default api;
