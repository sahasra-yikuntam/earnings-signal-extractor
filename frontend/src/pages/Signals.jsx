import React, { useState, useEffect } from 'react'
import { listSignals, deleteSignal } from '../utils/api'
import SignalBadge from '../components/SignalBadge'
export default function Signals() {
  const [signals, setSignals] = useState([])
  useEffect(() => { listSignals().then(r=>setSignals(r.data)).catch(()=>{}) }, [])
  const del = async (id) => { await deleteSignal(id); setSignals(s=>s.filter(x=>x.id!==id)) }
  return (
    <div style={{ maxWidth:900, margin:'0 auto', padding:'32px 24px' }}>
      <h1 style={{ fontSize:24, marginBottom:24, color:'#4ade80' }}>Signal History</h1>
      {signals.map(s=>(
        <div key={s.id} style={{ background:'#0f1a0f', border:'1px solid #1a2e1a', borderRadius:10, padding:'16px 20px', marginBottom:10, display:'flex', justifyContent:'space-between', alignItems:'center' }}>
          <div style={{ display:'flex', gap:16, alignItems:'center' }}>
            <span style={{ fontFamily:'Space Mono,monospace', fontSize:16, color:'#4ade80', minWidth:60 }}>{s.ticker}</span>
            <span style={{ fontSize:13, color:'#64748b' }}>{s.quarter} {s.year}</span>
            <SignalBadge label={s.signal_label} />
            <span style={{ fontSize:13, color:'#94a3b8' }}>Score: <b style={{ fontFamily:'Space Mono,monospace', color:'#e2e8f0' }}>{Math.round((s.composite_score||0)*100)}</b></span>
          </div>
          <button onClick={()=>del(s.id)} style={{ background:'transparent', border:'1px solid #1a2e1a', color:'#f87171', padding:'4px 10px', borderRadius:6, cursor:'pointer', fontSize:12 }}>Delete</button>
        </div>
      ))}
      {signals.length===0 && <div style={{ textAlign:'center', color:'#64748b', padding:60 }}>No signals yet. Extract one from the Extractor tab.</div>}
    </div>
  )
}
