import React, { useEffect, useMemo, useRef, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { BookOpen, Filter, ChevronDown } from 'lucide-react'
import { useTopics, useTopicExplanation } from '../hooks/useApi'
import {
  Spinner,
  ErrorAlert,
  EmptyState,
  TopicCard,
  SectionHeader,
  MarkdownContent,
  TopicSkeletonGrid,
  SectionDivider,
} from '../components/UI'

const MODULES = [
  { value: '',         label: 'All Modules' },
  { value: 'Module 1', label: 'Module 1 — Quantum Mechanics' },
  { value: 'Module 2', label: 'Module 2 — Wave Optics' },
  { value: 'Module 3', label: 'Module 3 — Solid State Physics' },
  { value: 'Module 4', label: 'Module 4 — Lasers & Optical Fiber' },
  { value: 'Module 5', label: 'Module 5 — Electrostatics & Maxwell' },
]

export default function TopicsPage() {
  const [searchParams, setSearchParams] = useSearchParams()
  const initialModule = searchParams.get('module') || ''

  const [selectedModule, setSelectedModule] = useState(initialModule)
  const [topicFilter, setTopicFilter] = useState('')
  const [selectedTopic, setSelectedTopic] = useState(null)
  const [cooldownUntil, setCooldownUntil] = useState(0)
  const [cooldownTick, setCooldownTick] = useState(0)

  const explanationRef = useRef(null)

  const { data, loading, error } = useTopics(selectedModule || null)
  const {
    data: topicExplanation,
    loading: topicExplanationLoading,
    error: topicExplanationError,
    generate: generateTopicExplanation,
    reset: resetTopicExplanation,
  } = useTopicExplanation()

  const isCoolingDown = cooldownUntil && Date.now() < cooldownUntil
  const cooldownRemainingSec = useMemo(() => {
    if (!isCoolingDown) return 0
    return Math.max(0, Math.ceil((cooldownUntil - Date.now()) / 1000))
  }, [cooldownUntil, cooldownTick])

  const cardInteractionLocked = topicExplanationLoading || isCoolingDown

  useEffect(() => {
    if (!isCoolingDown) return
    const t = setInterval(() => setCooldownTick((x) => x + 1), 250)
    return () => clearInterval(t)
  }, [isCoolingDown])

  useEffect(() => {
    if (!selectedTopic) return
    const id = window.setTimeout(() => {
      explanationRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' })
      explanationRef.current?.focus?.({ preventScroll: true })
    }, 100)
    return () => window.clearTimeout(id)
  }, [selectedTopic, topicExplanationLoading])

  const handleModuleChange = (value) => {
    setSelectedModule(value)
    if (value) setSearchParams({ module: value })
    else setSearchParams({})
    setSelectedTopic(null)
    resetTopicExplanation()
    setCooldownUntil(0)
  }

  const handleTopicClick = (entry) => {
    if (topicExplanationLoading) return
    if (isCoolingDown) return
    setSelectedTopic(entry?.topic || null)
    generateTopicExplanation(entry?.topic || '', selectedModule || null)
  }

  useEffect(() => {
    if (!topicExplanationError) return
    const msg = String(topicExplanationError).toLowerCase()
    if (msg.includes('rate limit') || msg.includes('too many') || msg.includes('429')) {
      setCooldownUntil(Date.now() + 15000)
    }
  }, [topicExplanationError])

  const topics = data?.topics || []
  const filtered = topicFilter
    ? topics.filter((t) =>
        t.topic.toLowerCase().includes(topicFilter.toLowerCase()) ||
        t.question.toLowerCase().includes(topicFilter.toLowerCase())
      )
    : topics

  const grouped = filtered.reduce((acc, t) => {
    if (!acc[t.unit]) acc[t.unit] = []
    acc[t.unit].push(t)
    return acc
  }, {})

  const showExplanationPanel =
    !!(selectedTopic || topicExplanationLoading || topicExplanationError || topicExplanation)

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-14 pb-20">

      <SectionHeader
        title="Browse Topics"
        subtitle="Explore all exam-ready topics across the RGPV Engineering Physics syllabus. Select a card to generate an exam-format explanation."
        icon={BookOpen}
        count={data?.total}
      />

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-3 sm:gap-4 mb-8 sm:mb-10">
        <div className="relative sm:w-72 shrink-0">
          <select
            value={selectedModule}
            onChange={(e) => handleModuleChange(e.target.value)}
            className="input-field appearance-none pr-10 cursor-pointer"
            aria-label="Filter by module"
          >
            {MODULES.map(({ value, label }) => (
              <option key={value} value={value} className="bg-bg-secondary">
                {label}
              </option>
            ))}
          </select>
          <ChevronDown
            className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-muted pointer-events-none"
          />
        </div>

        <div className="relative flex-1 min-w-0">
          <Filter className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-text-muted pointer-events-none" />
          <input
            type="search"
            placeholder="Filter by topic or question…"
            value={topicFilter}
            onChange={(e) => setTopicFilter(e.target.value)}
            className="input-field pl-11"
            aria-label="Filter topics"
          />
        </div>
      </div>

      {loading && (
        <div className="animate-fade-in">
          <p className="text-text-muted text-sm mb-4">Loading syllabus topics…</p>
          <TopicSkeletonGrid count={6} />
        </div>
      )}

      {error && <ErrorAlert message={error} />}

      {!loading && !error && filtered.length === 0 && (
        <EmptyState
          title="No topics found"
          description="Try adjusting your module filter or search term."
          icon={BookOpen}
        />
      )}

      {!loading && !error && filtered.length > 0 && (
        <div className="space-y-12 sm:space-y-14 animate-fade-in">
          {Object.entries(grouped).map(([module, entries]) => (
            <section key={module} aria-labelledby={`module-${module.replace(/\s+/g, '-')}`}>
              <div className="flex items-center gap-3 mb-5 sm:mb-6">
                <h2
                  id={`module-${module.replace(/\s+/g, '-')}`}
                  className="font-serif text-sm sm:text-base font-semibold text-text-primary tracking-tight"
                >
                  {module}
                </h2>
                <div className="flex-1 h-px bg-gradient-to-r from-bg-border to-transparent min-w-[2rem]" />
                <span className="text-xs text-text-muted tabular-nums whitespace-nowrap">
                  {entries.length} topics
                </span>
              </div>

              <div className="grid sm:grid-cols-2 xl:grid-cols-3 gap-4 sm:gap-5">
                {entries.map((entry, idx) => (
                  <TopicCard
                    key={`${entry.unit}-${entry.topic}-${idx}`}
                    entry={entry}
                    onClick={handleTopicClick}
                    selected={selectedTopic === entry.topic}
                    disabled={cardInteractionLocked}
                    loading={topicExplanationLoading && selectedTopic === entry.topic}
                  />
                ))}
              </div>
            </section>
          ))}
        </div>
      )}

      {showExplanationPanel && !loading && (
        <>
          <SectionDivider />

          <section
            ref={explanationRef}
            id="topic-explanation"
            tabIndex={-1}
            className="scroll-mt-24 sm:scroll-mt-28 outline-none rounded-3xl
                       ring-offset-4 ring-offset-bg-primary
                       focus-visible:ring-2 focus-visible:ring-accent-blue/35"
            aria-label="Topic explanation"
          >
            <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4 mb-5 sm:mb-6">
              <div className="min-w-0">
                <p className="text-xs font-semibold uppercase tracking-wider text-accent-blue/80 mb-1">
                  Explanation
                </p>
                <h2 className="font-serif text-xl sm:text-2xl font-semibold text-text-primary tracking-tight">
                  {selectedTopic || 'Your selection'}
                </h2>
                {topicExplanation?.source_module && (
                  <p className="text-text-muted text-sm mt-1">
                    {topicExplanation.source_module}
                  </p>
                )}
              </div>
              {topicExplanation && !topicExplanationLoading && (
                <button
                  type="button"
                  className="btn-secondary shrink-0 self-start"
                  onClick={() => {
                    setSelectedTopic(null)
                    resetTopicExplanation()
                  }}
                >
                  Clear
                </button>
              )}
            </div>

            <div
              className={`rounded-2xl border border-bg-border bg-bg-card/90 backdrop-blur-sm p-5 sm:p-8
                shadow-card transition-all duration-500 ease-out
                ${topicExplanationLoading ? 'ring-2 ring-accent-blue/25 border-accent-blue/20' : ''}
                ${topicExplanation && !topicExplanationLoading ? 'animate-slide-up' : ''}`}
            >
              {topicExplanationLoading && (
                <Spinner inline size="sm" label="Generating explanation…" />
              )}

              {topicExplanationError && (
                <div className="space-y-3 animate-fade-in">
                  <ErrorAlert
                    message={topicExplanationError}
                    onRetry={
                      isCoolingDown
                        ? null
                        : () => generateTopicExplanation(selectedTopic || '', selectedModule || null)
                    }
                  />
                  {isCoolingDown && (
                    <p className="text-xs text-text-muted text-center sm:text-left">
                      Rate limited. Try again in{' '}
                      <span className="text-text-primary font-semibold tabular-nums">
                        {cooldownRemainingSec}s
                      </span>
                      .
                    </p>
                  )}
                </div>
              )}

              {!topicExplanationLoading && !topicExplanationError && topicExplanation?.explanation && (
                <MarkdownContent content={topicExplanation.explanation} />
              )}
            </div>
          </section>
        </>
      )}
    </div>
  )
}
