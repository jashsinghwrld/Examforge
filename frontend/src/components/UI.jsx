import React from 'react'
import { AlertCircle, Loader2, SearchX } from 'lucide-react'

export function Spinner({ size = 'md', label = 'Loading...', inline = false }) {
  const sizes = { sm: 'w-4 h-4', md: 'w-6 h-6', lg: 'w-8 h-8' }
  const inner = (
    <>
      <Loader2 className={`${sizes[size]} text-accent-blue animate-spin`} />
      {label && <p className="text-text-muted text-sm">{label}</p>}
    </>
  )
  if (inline) {
    return (
      <div className="flex items-center gap-3 py-4">
        {inner}
      </div>
    )
  }
  return (
    <div className="flex flex-col items-center justify-center gap-3 py-10">
      {inner}
    </div>
  )
}

export function TopicSkeleton() {
  return (
    <div className="rounded-2xl border border-bg-border bg-bg-card/80 p-5 shadow-card animate-pulse">
      <div className="flex justify-between gap-3 mb-4">
        <div className="h-5 w-24 skeleton" />
        <div className="h-5 w-14 skeleton" />
      </div>
      <div className="h-4 w-[85%] max-w-md skeleton mb-3" />
      <div className="h-3 w-full skeleton mb-2" />
      <div className="h-3 w-5/6 skeleton" />
    </div>
  )
}

export function TopicSkeletonGrid({ count = 6 }) {
  return (
    <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
      {Array.from({ length: count }).map((_, i) => (
        <TopicSkeleton key={i} />
      ))}
    </div>
  )
}

export function ErrorAlert({ message, onRetry }) {
  return (
    <div
      className="flex items-start gap-3 p-4 sm:p-5 bg-accent-red/10 border border-accent-red/25
                 rounded-2xl text-sm animate-fade-in"
    >
      <AlertCircle className="w-5 h-5 text-accent-red flex-shrink-0 mt-0.5" />
      <div className="flex-1 min-w-0">
        <p className="text-accent-red font-medium mb-1">Something went wrong</p>
        <p className="text-text-secondary break-words">{message}</p>
        {onRetry && (
          <button
            type="button"
            onClick={onRetry}
            className="mt-3 btn-primary !py-2 !px-4 !text-xs w-full sm:w-auto"
          >
            Try again
          </button>
        )}
      </div>
    </div>
  )
}

export function EmptyState({ title, description, icon: Icon = SearchX }) {
  return (
    <div className="flex flex-col items-center justify-center py-20 gap-4 text-center animate-fade-in">
      <div
        className="w-20 h-20 rounded-2xl bg-bg-card border border-bg-border shadow-card
                   flex items-center justify-center"
      >
        <Icon className="w-9 h-9 text-text-muted" />
      </div>
      <div>
        <p className="text-text-primary font-semibold text-lg mb-1">{title}</p>
        {description && (
          <p className="text-text-muted text-sm max-w-sm mx-auto leading-relaxed">{description}</p>
        )}
      </div>
    </div>
  )
}

const MODULE_COLORS = {
  'Module 1': { bg: 'bg-accent-blue/15',   text: 'text-accent-blue',   border: 'border-accent-blue/30'   },
  'Module 2': { bg: 'bg-accent-purple/15', text: 'text-accent-purple', border: 'border-accent-purple/30' },
  'Module 3': { bg: 'bg-accent-cyan/15',   text: 'text-accent-cyan',   border: 'border-accent-cyan/30'   },
  'Module 4': { bg: 'bg-accent-green/15',  text: 'text-accent-green',  border: 'border-accent-green/30'  },
  'Module 5': { bg: 'bg-accent-yellow/15', text: 'text-accent-yellow', border: 'border-accent-yellow/30' },
}

export function ModuleBadge({ module }) {
  const colors = MODULE_COLORS[module] || MODULE_COLORS['Module 1']
  return (
    <span
      className={`inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium
                  border ${colors.bg} ${colors.text} ${colors.border}`}
    >
      {module}
    </span>
  )
}

export function TopicCard({ entry, onClick, selected = false, disabled = false, loading = false }) {
  return (
    <button
      type="button"
      disabled={disabled}
      onClick={() => onClick?.(entry)}
      className={`
        w-full text-left rounded-2xl border p-5 sm:p-5
        transition-all duration-300 ease-out
        shadow-card
        ${selected
          ? 'ring-2 ring-accent-blue/55 border-accent-blue/40 bg-accent-blue/[0.08] shadow-card-hover scale-[1.01]'
          : 'border-bg-border bg-bg-card hover:border-accent-blue/35 hover:bg-bg-hover hover:shadow-card-hover hover:-translate-y-0.5'
        }
        ${disabled ? 'opacity-55 cursor-not-allowed pointer-events-none hover:translate-y-0' : 'cursor-pointer'}
        ${loading && selected ? 'animate-pulse' : ''}
        active:scale-[0.99]
      `}
    >
      <div className="flex items-start justify-between gap-3 mb-3">
        <ModuleBadge module={entry.unit} />
        <span
          className="text-xs text-text-muted bg-bg-secondary px-2 py-0.5 rounded-lg border border-bg-border
                     whitespace-nowrap"
        >
          {entry.marks} marks
        </span>
      </div>
      <h3
        className={`text-text-primary font-semibold text-sm sm:text-base mb-2 leading-snug tracking-tight
                    transition-colors ${selected ? 'text-accent-blue' : 'group-hover:text-accent-blue'}`}
      >
        {entry.topic}
      </h3>
      <p className="text-text-muted text-xs sm:text-sm leading-relaxed line-clamp-2">
        {entry.question}
      </p>
      {selected && loading && (
        <div className="mt-4 flex items-center gap-2 text-xs text-accent-blue">
          <Loader2 className="w-3.5 h-3.5 animate-spin flex-shrink-0" />
          <span>Generating explanation…</span>
        </div>
      )}
    </button>
  )
}

export function SectionHeader({ title, subtitle, icon: Icon, count }) {
  return (
    <header className="mb-8 sm:mb-10 animate-fade-in">
      <div className="flex flex-wrap items-center gap-3 sm:gap-4 mb-2">
        {Icon && (
          <div
            className="w-10 h-10 rounded-xl bg-accent-blue/12 border border-accent-blue/25
                       flex items-center justify-center shadow-sm"
          >
            <Icon className="w-5 h-5 text-accent-blue" />
          </div>
        )}
        <div className="flex flex-wrap items-baseline gap-2 sm:gap-3 min-w-0">
          <h1 className="font-serif text-2xl sm:text-3xl font-semibold text-text-primary tracking-tight">
            {title}
          </h1>
          {count !== undefined && (
            <span className="badge-blue tabular-nums">{count}</span>
          )}
        </div>
      </div>
      {subtitle && (
        <p className="text-text-muted text-sm sm:text-base max-w-2xl leading-relaxed pl-0 sm:pl-[3.25rem]">
          {subtitle}
        </p>
      )}
    </header>
  )
}

export function MarkdownContent({ content }) {
  if (!content) return null

  const lines = content.split('\n')
  const rendered = []
  let key = 0

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i]

    if (line.startsWith('## ')) {
      rendered.push(
        <h2 key={key++} className="text-lg font-semibold text-text-primary mt-5 mb-2 first:mt-0 tracking-tight">
          {line.slice(3)}
        </h2>
      )
    } else if (line.startsWith('### ')) {
      rendered.push(
        <h3 key={key++} className="text-sm font-semibold text-accent-blue mt-4 mb-1.5">
          {line.slice(4)}
        </h3>
      )
    } else if (line.startsWith('**') && line.endsWith('**')) {
      rendered.push(
        <p key={key++} className="text-text-primary font-semibold text-sm my-1">{line.slice(2, -2)}</p>
      )
    } else if (line.startsWith('- ') || line.startsWith('* ')) {
      rendered.push(
        <li key={key++} className="text-text-secondary text-sm ml-4 list-disc leading-relaxed">
          {line.slice(2)}
        </li>
      )
    } else if (line.match(/^\d+\. /)) {
      rendered.push(
        <li key={key++} className="text-text-secondary text-sm ml-4 list-decimal leading-relaxed">
          {line.replace(/^\d+\. /, '')}
        </li>
      )
    } else if (line.startsWith('---')) {
      rendered.push(<hr key={key++} className="border-bg-border my-4" />)
    } else if (line.startsWith('> ')) {
      rendered.push(
        <blockquote
          key={key++}
          className="border-l-4 border-accent-blue/40 pl-4 my-2 text-text-muted text-sm italic"
        >
          {line.slice(2)}
        </blockquote>
      )
    } else if (line.trim() === '') {
      rendered.push(<div key={key++} className="h-2" />)
    } else {
      const parts = line.split(/(\*\*[^*]+\*\*|`[^`]+`)/)
      const inline = parts.map((part, idx) => {
        if (part.startsWith('**') && part.endsWith('**'))
          return <strong key={idx} className="text-text-primary font-semibold">{part.slice(2, -2)}</strong>
        if (part.startsWith('`') && part.endsWith('`'))
          return (
            <code
              key={idx}
              className="bg-bg-secondary text-accent-cyan font-mono text-xs px-1.5 py-0.5 rounded-md"
            >
              {part.slice(1, -1)}
            </code>
          )
        return part
      })
      rendered.push(
        <p key={key++} className="text-text-secondary text-sm leading-relaxed">{inline}</p>
      )
    }
  }

  return (
    <div className="markdown-body space-y-0.5 animate-slide-up">
      {rendered}
    </div>
  )
}

export function SectionDivider() {
  return (
    <div className="relative my-14 sm:my-16 flex items-center gap-5" aria-hidden>
      <div className="flex-1 h-px bg-bg-border" />
      <div className="h-1 w-1 rounded-full bg-text-muted/40 shrink-0" />
      <div className="flex-1 h-px bg-bg-border" />
    </div>
  )
}
