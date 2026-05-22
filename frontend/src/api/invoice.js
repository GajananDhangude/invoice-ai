import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

export const extractInvoice = (file) => {
  const formData = new FormData();
  formData.append("file", file);
  return api.post("/extract", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
};

export const generateCsv = (invoice) =>
  api.post("/generate-csv", invoice, { responseType: "blob" });
