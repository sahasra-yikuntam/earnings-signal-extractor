import React from 'react'
import { Link, useLocation } from 'react-router-dom'
const links = [{to:'/',label:'Extractor'},{to:'/signals',label:'Signals'},{to:'/backtest',label:'Backtest'},{to:'/about',label:'About'}]
export default function Nav() {
  const loc = useLocation()
  return (
    <nav style={{ background:'#060f06', borderBottom:'1px solid #1a2e1a', padding:'0 24px', display:'flex', alignItems:'center', gap:8, height:56, position:'sticky', top:0, zIndex:100 }}>
      <Link to="/" style={{ textDecoration:'none', marginRight:24, fontFamily:'Space Mono,monospace', fontSize:14, color:'#4ade80', fontWeight:700 }}>EARNINGS SIGNAL</Link>
      {links.map(({to,label}) => (
        <Link key={to} to={to} style={{ textDecoration:'none', padding:'6px 12px', borderRadius:6, color:loc.pathname===to?'#e2e8f0':'#64748b', background:loc.pathname===to?'#0f1a0f':'transparent', fontSize:13 }}>{label}</Link>
      ))}
    </nav>
  )
}
