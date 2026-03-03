import React, { useState } from 'react'
import { analyzeTranscript, fetchTicker } from '../utils/api'
import SignalBadge from '../components/SignalBadge'
import ScoreBar from '../components/ScoreBar'
const TICKERS = ['AAPL','META','MSFT','GOOGL','NVDA']
const QUARTERS = ['Q1','Q2','Q3','Q4']
export default function Extractor() {
  const [mode, setMode] = useState('fetch')
  const [ticker, setTicker] = useState('NVDA')
  const [quarter, setQuarter] = useState('Q1')
  const [year, setYear] = useState(2024)
  const [content, setContent] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const run = async () => {
    setLoading(true); setError(null); setResult(null)
    try {
      const r = mode === 'fetch' ? await fetchTicker(ticker, quarter, year) : await analyzeTranscript({ ticker, quarter, year, content })
      setResult(r.data)
    } catch(e) { setError(e.response?.data?.detail || 'Failed') } finally { setLoading(false) }
  }
  const lc = result ? (result.signal_label === 'bullish' ? '#4ade80' : result.signal_label === 'bearish' ? '#f87171' : '#facc15') : '#4ade80'
  return (
    <div style={{ maxWidth:800, margin:'0 auto', padding:'32px 24px' }}>
      <h1 style={{ fontSize:28, marginBottom:8, color:'#4ade80' }}>Signal Extractor</h1>
      <p style={{ color:'#64748b', fontSize:14, marginBottom:28 }}>Extract LLM sentiment signals from earnings call transcripts.</p>
      <div style={{ background:'#0f1a0f', border:'1px solid #1a2e1a', borderRadius:12, padding:24, marginBottom:24 }}>
        <div style={{ display:'flex', gap:8, marginBottom:20 }}>
          {[['fetch','Fetch from SEC EDGAR'],['paste','Paste Transcript']].map(([m,l])=>(
            <button key={m} onClick={()=>setMode(m)} style={{ background:mode===m?'#1a2e1a':'transparent', border:'1px solid #1a2e1a', color:mode===m?'#4ade80':'#64748b', padding:'6px 16px', borderRadius:6, cursor:'pointer', fontSize:13 }}>{l}</button>
          ))}
        </div>
        <div style={{ display:'flex', gap:12, flexWrap:'wrap', marginBottom:16 }}>
          <div><label style={{ fontSize:11, color:'#64748b', display:'block', marginBottom:4 }}>TICKER</label>
            {mode==='fetch'
              ? <select value={ticker} onChange={e=>setTicker(e.target.value)} style={{ background:'#0a0f0a', border:'1px solid #1a2e1a', color:'#4ade80', padding:'8px 12px', borderRadius:8, fontSize:14, fontFamily:'Space Mono,monospace' }}>{TICKERS.map(t=><option key={t}>{t}</option>)}</select>
              : <input value={ticker} onChange={e=>setTicker(e.target.value.toUpperCase())} placeholder="AAPL" style={{ background:'#0a0f0a', border:'1px solid #1a2e1a', color:'#4ade80', padding:'8px 12px', borderRadius:8, fontSize:14, width:80, fontFamily:'Space Mono,monospace', outline:'none' }} />}
          </div>
          <div><label style={{ fontSize:11, color:'#64748b', display:'block', marginBottom:4 }}>QUARTER</label>
            <select value={quarter} onChange={e=>setQuarter(e.target.value)} style={{ background:'#0a0f0a', border:'1px solid #1a2e1a', color:'#e2e8f0', padding:'8px 12px', borderRadius:8, fontSize:14 }}>{QUARTERS.map(q=><option key={q}>{q}</option>)}</select>
          </div>
          <div><label style={{ fontSize:11, color:'#64748b', display:'block', marginBottom:4 }}>YEAR</label>
            <select value={year} onChange={e=>setYear(Number(e.target.value))} style={{ background:'#0a0f0a', border:'1px solid #1a2e1a', color:'#e2e8f0', padding:'8px 12px', borderRadius:8, fontSize:14 }}>{[2022,2023,2024].map(y=><option key={y}>{y}</option>)}</select>
          </div>
        </div>
        {mode==='paste' && <textarea value={content} onChange={e=>setContent(e.target.value)} placeholder="Paste earnings call transcript here..." rows={6} style={{ width:'100%', background:'#0a0f0a', border:'1px solid #1a2e1a', borderRadius:8, color:'#e2e8f0', padding:'10px 12px', fontSize:13, resize:'vertical', outline:'none', fontFamily:'Inter,sans-serif', marginBottom:16 }} />}
        <button onClick={run} disabled={loading||(mode==='paste'&&!content.trim())} style={{ background:loading?'#1a2e1a':'linear-gradient(135deg,#4ade80,#22d3ee)', border:'none', borderRadius:8, padding:'10px 24px', color:'#0a0f0a', fontWeight:700, fontSize:14, cursor:loading?'not-allowed':'pointer', fontFamily:'Space Mono,monospace' }}>{loading?'Extracting...':'EXTRACT SIGNAL'}</button>
        {error && <p style={{ color:'#f87171', fontSize:13, marginTop:12 }}>Error: {error}</p>}
      </div>
      {result && (
        <div style={{ background:'#0f1a0f', border:'1px solid '+lc+'44', borderRadius:12, padding:24 }}>
          <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom:20 }}>
            <div><div style={{ fontSize:20, fontFamily:'Space Mono,monospace', marginBottom:6 }}>{result.ticker} / {result.quarter} {result.year}</div><SignalBadge label={result.signal_label} /></div>
            <div style={{ textAlign:'right' }}><div style={{ fontSize:11, color:'#64748b' }}>COMPOSITE SCORE</div><div style={{ fontSize:40, fontFamily:'Space Mono,monospace', color:lc }}>{Math.round((result.composite_score||0)*100)}</div></div>
          </div>
          <ScoreBar label="Confidence" value={result.confidence_score} />
          <ScoreBar label="Hedging (lower = better)" value={result.hedging_score} invert />
          <ScoreBar label="Forward Guidance" value={result.guidance_score} />
          <ScoreBar label="Risk Acknowledgment (lower = better)" value={result.risk_score} invert />
        </div>
      )}
    </div>
  )
}
