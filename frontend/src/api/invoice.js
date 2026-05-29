import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "/api",
});

export const extractInvoice = (files) => {
  const formData = new FormData();
  files.forEach((file) => {
    formData.append("files", file);
  });
  return api.post("/extract", formData);
};

export const exportExcel = (invoiceList) => {
  return api.post("/export-excel", invoiceList, {
    responseType: "blob",
  });
};
