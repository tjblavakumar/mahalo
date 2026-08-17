const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

async function request(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || `Request failed with ${response.status}`);
  }
  return response.json();
}

export function getPersonas() {
  return request('/api/chat/personas');
}

export function sendMessage(payload) {
  return request('/api/chat/message', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export function getSystemStatus() {
  return request('/api/admin/status');
}

export function resetDemoData() {
  return request('/api/admin/reset-data', { method: 'POST' });
}
