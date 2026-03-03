import React from 'react'
export default function ScoreBar({ label, value, invert=false }) {
  if (value == null) return null
  const d = invert ? 1 - value : value
  const color = d >= 0.65 ? '#4ade80' : d >= 0.4 ? '#facc15' : '#f87171'
  return (
    <div style={{ marginBottom:10 }}>
      <div style={{ display:'flex', justifyContent:'space-between', fontSize:12, color:'#94a3b8', marginBottom:4 }}>
        <span>{label}</span><span style={{ color, fontFamily:'Space Mono,monospace', fontWeight:700 }}>{Math.round(d*100)}</span>
      </div>
      <div style={{ height:6, background:'#1a2e1a', borderRadius:3, overflow:'hidden' }}>
        <div style={{ height:'100%', width:(d*100)+'%', background:color, borderRadius:3 }} />
      </div>
    </div>
  )
}
