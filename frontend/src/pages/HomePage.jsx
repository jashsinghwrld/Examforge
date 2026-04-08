import React from 'react'
import { Link } from 'react-router-dom'
import { BookOpen, Atom, ChevronRight } from 'lucide-react'

const MODULE_INFO = [
  { name: 'Module 1', title: 'Quantum Mechanics',           topics: 10, color: 'text-accent-blue',   bg: 'bg-accent-blue/[0.08]',   border: 'border-accent-blue/20'   },
  { name: 'Module 2', title: 'Wave Optics',                 topics: 10, color: 'text-accent-purple', bg: 'bg-accent-purple/[0.08]', border: 'border-accent-purple/20' },
  { name: 'Module 3', title: 'Solid State Physics',         topics: 9,  color: 'text-accent-cyan',   bg: 'bg-accent-cyan/[0.08]',   border: 'border-accent-cyan/20'   },
  { name: 'Module 4', title: 'Lasers & Optical Fiber',      topics: 10, color: 'text-accent-green',  bg: 'bg-accent-green/[0.08]',  border: 'border-accent-green/20'  },
  { name: 'Module 5', title: 'Electrostatics & Maxwell',    topics: 8,  color: 'text-accent-yellow', bg: 'bg-accent-yellow/[0.08]', border: 'border-accent-yellow/20' },
]

export default function HomePage() {
  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-20">

      <div className="max-w-3xl mx-auto text-center mb-16 sm:mb-24 animate-fade-in">
        <p className="text-[11px] sm:text-xs font-semibold uppercase tracking-[0.2em] text-text-muted mb-6">
          RGPV B.Tech · Semester 1
        </p>

        <h1 className="font-serif text-display sm:text-5xl md:text-[3.25rem] text-text-primary mb-6">
          Exam-ready
          <span className="block mt-1 text-accent-blue">Engineering Physics</span>
        </h1>

        <p className="text-text-secondary text-base sm:text-lg leading-[1.65] mb-10 max-w-xl mx-auto">
          Forty-seven syllabus topics, structured explanations, and a calm workspace built for focused study.
        </p>

        <Link
          to="/topics"
          className="btn-primary inline-flex px-8 py-3.5 text-[15px] min-h-[48px]"
        >
          <BookOpen className="w-5 h-5 opacity-90" strokeWidth={1.75} />
          Browse topics
          <ChevronRight className="w-4 h-4 opacity-70" strokeWidth={2} />
        </Link>
      </div>

      <div className="grid grid-cols-3 gap-3 sm:gap-6 mb-20 sm:mb-28 max-w-2xl mx-auto">
        {[
          { value: '5',  label: 'Modules' },
          { value: '47', label: 'Topics' },
          { value: '7',  label: 'Marks' },
        ].map(({ value, label }) => (
          <div
            key={label}
            className="text-center py-5 sm:py-6 px-2 rounded-2xl bg-bg-card border border-bg-border
                       shadow-card transition-shadow duration-300 hover:shadow-card-hover"
          >
            <div className="font-serif text-2xl sm:text-3xl text-text-primary tabular-nums mb-1">
              {value}
            </div>
            <div className="text-text-muted text-[11px] sm:text-xs font-medium uppercase tracking-wider">
              {label}
            </div>
          </div>
        ))}
      </div>

      <div className="max-w-xl mx-auto mb-20 sm:mb-28">
        <Link
          to="/topics"
          className="group block rounded-2xl border border-bg-border bg-bg-card p-8 sm:p-10
                     shadow-card hover:shadow-card-hover transition-all duration-300
                     hover:border-accent-blue/25"
        >
          <div className="flex items-start gap-4">
            <div
              className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl
                         border border-bg-border bg-bg-secondary text-accent-blue"
            >
              <BookOpen className="w-6 h-6" strokeWidth={1.5} />
            </div>
            <div className="min-w-0 text-left">
              <h2 className="font-serif text-xl sm:text-2xl text-text-primary mb-2 tracking-tight">
                Topic library
              </h2>
              <p className="text-text-secondary text-sm leading-relaxed mb-4">
                Open the full list, filter by module, and generate RGPV-style explanations on demand.
              </p>
              <span className="inline-flex items-center gap-1 text-sm font-semibold text-accent-blue">
                Continue
                <ChevronRight className="w-4 h-4 transition-transform group-hover:translate-x-0.5" />
              </span>
            </div>
          </div>
        </Link>
      </div>

      <div>
        <h2 className="font-serif text-xl sm:text-2xl text-text-primary mb-8 flex items-center gap-3">
          <Atom className="w-5 h-5 text-accent-blue shrink-0" strokeWidth={1.5} />
          Syllabus
        </h2>
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {MODULE_INFO.map(({ name, title, topics, color, bg, border }) => (
            <Link
              key={name}
              to={`/topics?module=${encodeURIComponent(name)}`}
              className={`group block p-5 rounded-2xl border ${border} ${bg}
                          bg-bg-card/80 backdrop-blur-sm
                          shadow-card hover:shadow-card-hover transition-all duration-300
                          hover:-translate-y-0.5`}
            >
              <div className="flex items-start justify-between gap-2 mb-3">
                <span className={`text-[11px] font-semibold uppercase tracking-wider ${color}`}>
                  {name}
                </span>
                <span className="text-[11px] text-text-muted tabular-nums bg-bg-secondary px-2 py-1 rounded-lg border border-bg-border">
                  {topics} topics
                </span>
              </div>
              <h3 className="font-medium text-[15px] text-text-primary leading-snug group-hover:text-accent-blue transition-colors">
                {title}
              </h3>
              <div className={`flex items-center gap-1 mt-4 text-xs font-medium ${color} opacity-90`}>
                Open
                <ChevronRight className="w-3 h-3" />
              </div>
            </Link>
          ))}
        </div>
      </div>

    </div>
  )
}
