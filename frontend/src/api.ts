const API_BASE = process.env.REACT_APP_API_BASE_URL || "http://localhost:8000";

export async function fetchSampleQuery() {
  const res = await fetch(`${API_BASE}/sample-query`);
  return res.json();
}

export {};
