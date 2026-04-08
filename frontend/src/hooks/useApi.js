/**
 * Custom React Hooks
 * Wraps API calls with loading, error, and data state management.
 */

import { useState, useEffect, useCallback } from 'react'
import { topicsApi, topicExplanationApi } from '../api/client'

// ── Topics hooks ──────────────────────────────────────────────────────────
export function useTopics(module = null) {
  const [data, setData]       = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError]     = useState(null)

  useEffect(() => {
    setLoading(true)
    setError(null)
    topicsApi.getAll(module)
      .then(setData)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false))
  }, [module])

  return { data, loading, error }
}

// ── Topic Explanation (Exam Format) hook ───────────────────────────────────
export function useTopicExplanation() {
  const [data, setData]       = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError]     = useState(null)

  const generate = useCallback(async (topic, module = null) => {
    if (!topic?.trim()) return
    setLoading(true)
    setError(null)
    setData(null)
    try {
      const res = await topicExplanationApi.generate(topic.trim(), module)
      setData(res)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }, [])

  const reset = () => { setData(null); setError(null) }

  return { data, loading, error, generate, reset }
}
