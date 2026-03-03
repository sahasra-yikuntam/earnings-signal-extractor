import React from 'react'
const C = { bullish:{color:'#4ade80',bg:'#4ade8022',emoji:'🟢'}, bearish:{color:'#f87171',bg:'#f8717122',emoji:'🔴'}, neutral:{color:'#facc15',bg:'#facc1522',emoji:'🟡'} }
export default function SignalBadge({ label }) {
  const c = C[label] || C.neutral
  return <span style={{ background:c.bg, color:c.color, padding:'3px 10px', borderRadius:20, fontSize:12, fontFamily:'Space Mono,monospace', fontWeight:700 }}>{c.emoji} {(label||'neutral').toUpperCase()}</span>
}
