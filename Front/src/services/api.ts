// services/api.ts
import axios from "axios";

export const api = axios.create({
  baseURL: "http://localhost:8000", // ou o IP da sua máquina com FastAPI
});
