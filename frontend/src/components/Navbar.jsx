import React from 'react'
import { NavLink } from 'react-router-dom'
import { BookOpen, Moon, Sun, Zap } from 'lucide-react'
import { useTheme } from '../context/ThemeContext'

const navItems = [
  { to: '/',        label: 'Home',          icon: Zap },
  { to: '/topics',  label: 'Topics',        icon: BookOpen },
]

export default function Navbar() {
  const { toggleTheme, theme } = useTheme()
  const isDark = theme === 'dark'

  return (
    <header
      className="sticky top-0 z-50 border-b border-bg-border bg-bg-secondary/85 backdrop-blur-xl
                 supports-[backdrop-filter]:bg-bg-secondary/70"
    >
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-14 sm:h-16">

          <NavLink
            to="/"
            className="flex items-center gap-3 min-w-0 group rounded-xl py-1 -ml-1 pr-2
                       focus:outline-none focus-visible:ring-2 focus-visible:ring-accent-blue/30"
          >
            <span
              className="flex h-9 w-9 sm:h-10 sm:w-10 items-center justify-center rounded-xl
                         border border-bg-border bg-bg-elevated text-sm font-semibold tracking-tight text-text-primary
                         group-hover:border-accent-blue/35 transition-colors duration-200"
              aria-hidden
            >
              E
            </span>
            <div className="hidden sm:block min-w-0 text-left">
              <div className="text-[15px] font-semibold text-text-primary tracking-tight truncate font-serif">
                ExamForge
              </div>
              <div className="text-[11px] text-text-muted tracking-wide truncate uppercase">
                Engineering Physics · RGPV
              </div>
            </div>
          </NavLink>

          <div className="flex items-center gap-1 sm:gap-2">
            <nav className="flex items-center gap-0.5 sm:gap-1" aria-label="Main">
              {navItems.map(({ to, label, icon: Icon }) => (
                <NavLink
                  key={to}
                  to={to}
                  className={({ isActive }) =>
                    `flex items-center gap-2 px-3 sm:px-4 py-2 rounded-xl text-sm font-medium
                     transition-all duration-200 active:scale-[0.98] ${
                       isActive
                         ? 'bg-bg-elevated text-text-primary border border-bg-border shadow-sm'
                         : 'text-text-secondary hover:text-text-primary hover:bg-bg-hover border border-transparent'
                     }`
                  }
                >
                  <Icon className="w-4 h-4 opacity-80" strokeWidth={1.75} />
                  <span className="hidden sm:inline">{label}</span>
                </NavLink>
              ))}
            </nav>

            <button
              type="button"
              onClick={toggleTheme}
              className="btn-icon ml-1"
              aria-label={isDark ? 'Switch to light mode' : 'Switch to dark mode'}
            >
              {isDark ? (
                <Sun className="w-[18px] h-[18px]" strokeWidth={1.75} />
              ) : (
                <Moon className="w-[18px] h-[18px]" strokeWidth={1.75} />
              )}
            </button>
          </div>

        </div>
      </div>
    </header>
  )
}
