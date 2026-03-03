import React from 'react'
import { Routes, Route } from 'react-router-dom'
import Nav from './components/Nav'
import Extractor from './pages/Extractor'
import Signals from './pages/Signals'
import Backtest from './pages/Backtest'
import About from './pages/About'
export default function App() {
  return (<><Nav /><Routes><Route path="/" element={<Extractor />} /><Route path="/signals" element={<Signals />} /><Route path="/backtest" element={<Backtest />} /><Route path="/about" element={<About />} /></Routes></>)
}
