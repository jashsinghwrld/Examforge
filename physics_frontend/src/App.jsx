import React from 'react'
import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import HomePage from './pages/HomePage'
import TopicsPage from './pages/TopicsPage'

export default function App() {
  return (
    <div className="app-shell text-text-primary antialiased">
      <Navbar />
      <main className="relative">
        <Routes>
          <Route path="/"        element={<HomePage />}   />
          <Route path="/topics"  element={<TopicsPage />} />
          <Route path="*"        element={<NotFound />}   />
        </Routes>
      </main>
    </div>
  )
}

function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] gap-6 px-4 text-center animate-fade-in">
      <div className="text-7xl font-black text-bg-border/60 tracking-tighter">404</div>
      <p className="text-text-secondary max-w-sm">That page doesn’t exist. Head back to ExamForge home.</p>
      <a href="/" className="btn-primary px-8">Go home</a>
    </div>
  )
}
