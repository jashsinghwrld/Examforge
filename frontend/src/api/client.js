/**
 * API Client
 * Handles all communication with the FastAPI backend.
 * Base URL proxied through Vite to http://localhost:8000
 */

const BASE_URL = '/api'

async function request(method, path, body = null) {
  const options = {
    method,
    headers: { 'Content-Type': 'application/json' },
  }
  if (body) options.body = JSON.stringify(body)

  const res = await fetch(`${BASE_URL}${path}`, options)

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Unknown error' }))
    throw new Error(err.detail || `HTTP ${res.status}`)
  }
  return res.json()
}

// ── Topics ────────────────────────────────────────────────────────────────
export const topicsApi = {
  /** GET /topics — list all topics (optionally filtered by module) */
  getAll: (module = null) => {
    const params = module ? `?module=${encodeURIComponent(module)}` : ''
    return request('GET', `/topics${params}`)
  },
}

// ── Topic Explanation (Exam Format) ─────────────────────────────────────────
export const topicExplanationApi = {
  /** POST /topic-explanation — exam-format topic explanation */
  generate: (topic, module = null) =>
    request('POST', '/topic-explanation', {
      topic,
      module: module || undefined,
    }),
}
