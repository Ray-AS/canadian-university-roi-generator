import axios from "axios";
import type { Analysis, CompleteReport, FieldData, Methodology, PolicyRecommendations, Rankings, Summary, Table, VisualizationsDetails } from "./models";

const API_URL = "http://localhost:5177/api/report";

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export async function getCompleteReport(): Promise<CompleteReport> {
  const response = await api.get<CompleteReport>("/");
  return response.data;
}

export async function getSummary(): Promise<Summary> {
  const response = await api.get<Summary>("/summary");
  return response.data;
}

export async function getRankings(): Promise<Rankings> {
  const response = await api.get<Rankings>('/rankings');
  return response.data;
}

export async function getAnalysis(): Promise<Analysis> {
  const response = await api.get<Analysis>('/analysis');
  return response.data;
}

export async function getMethodology(): Promise<Methodology> {
  const response = await api.get<Methodology>('/methodology');
  return response.data;
}

export async function getPolicyRecommendations (): Promise<PolicyRecommendations> {
  const response = await api.get<PolicyRecommendations>('/recommendations');
  return response.data;
}

export async function getVisualizations(): Promise<VisualizationsDetails> {
  const response = await api.get<VisualizationsDetails>('/visualizations');
  return response.data;
}

export async function getTable(): Promise<Table> {
  const response = await api.get<Table>('/table');
  return response.data;
}

export async function getAllFields(): Promise<FieldData[]> {
  const response = await api.get<FieldData[]>('/fields');
  return response.data;
}

export async function getFieldByName(fieldName: string): Promise<FieldData> {
  const response = await api.get<FieldData>(`/fields/${fieldName}`);
  return response.data;
}
