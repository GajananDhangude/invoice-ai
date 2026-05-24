import axios from "axios";

const baseURL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

const api = axios.create({
  baseURL,
});

export const getStats = () => api.get("/stats");

export const getHistory = () => api.get("/history");

export const extractInvoice = (file) => {
  const formData = new FormData();
  formData.append("file", file);
  return api.post("/extract", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
};

export const generateCsv = (invoice) =>
  api.post("/generate-csv", invoice, { responseType: "blob" });
