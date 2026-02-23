import axios from "axios";

// Use environment variable for API URL, fallback to localhost
const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

const axiosClient = axios.create({
  baseURL: API_URL,
  timeout: 30000, // 30 second timeout
});

axiosClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor for handling auth errors
axiosClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401 || error.response?.status === 403) {
      // Clear token and redirect to login
      localStorage.removeItem("token");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

export default axiosClient;