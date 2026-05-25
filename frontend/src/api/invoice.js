import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

export const extractInvoice = (files) => {
  const formData = new FormData();
  files.forEach((file) => {
    formData.append("files", file);
  });
  return api.post("/extract", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
};

export const generateCsv = (invoices) =>
  api.post("/generate-csv", invoices, { responseType: "blob" });
