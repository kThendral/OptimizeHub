// src/api.js
const BASE_URL = 'http://localhost:5000';

export async function fetchAlgorithms() {
  const res = await fetch(`${BASE_URL}/algorithms`);
  return res.json();
}

export async function executeAlgorithm(payload) {
  const res = await fetch(`${BASE_URL}/execute`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  return res.json();
}
