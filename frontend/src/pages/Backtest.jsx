import React, { useState } from 'react'
import { runBacktest } from '../utils/api'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, PieChart, Pie, Legend } from 'recharts'
export default function Backtest() {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(false)
  const run = async () => { setLoading(true); try { const r = await runBacktest(); setStats(r.data) } finally { setLoading(false) } }
  const pie = stats ? [{ name:'Bullish', value:stats.bullish_count, fill:'#4ade80' },{ name:'Bearish', value:stats.bearish_count, fill:'#f87171' },{ name:'Neutral', value:stats.neutral_count, fill:'#facc15' }].filter(x=>x.value>0) : []
  const bars = stats ? [{ name:'Hit 1D', value:Math.round(stats.hit_rate_1d*100), color:'#4ade80' },{ name:'Hit 5D', value:Math.round(stats.hit_rate_5d*100), color:'#22d3ee' },{ name:'Sharpe', value:stats.sharpe_ratio, color:'#a78bfa' }] : []
  return (
    <div style={{ maxWidth:900, margin:'0 auto', padding:'32px 24px' }}>
      <h1 style={{ fontSize:24, marginBottom:8, color:'#4ade80' }}>Backtest Engine</h1>
      <p style={{ color:'#64748b', fontSize:14, marginBottom:24 }}>Test whether extracted signals predict post-earnings returns.</p>
      <button onClick={run} disabled={loading} style={{ background:loading?'#1a2e1a':'linear-gradient(135deg,#4ade80,#22d3ee)', border:'none', borderRadius:8, padding:'10px 24px', color:'#0a0f0a', fontWeight:700, fontSize:14, cursor:loading?'not-allowed':'pointer', fontFamily:'Space Mono,monospace', marginBottom:28 }}>{loading?'Running...':'RUN BACKTEST'}</button>
      {stats && <>
        <div style={{ display:'grid', gridTemplateColumns:'repeat(4,1fr)', gap:16, marginBottom:24 }}>
          {[['Signals',stats.total_signals,'#4ade80'],['Hit Rate 1D',Math.round(stats.hit_rate_1d*100)+'%','#22d3ee'],['Hit Rate 5D',Math.round(stats.hit_rate_5d*100)+'%','#a78bfa'],['Sharpe',stats.sharpe_ratio,'#facc15']].map(([l,v,c])=>(
            <div key={l} style={{ background:'#0f1a0f', border:'1px solid #1a2e1a', borderRadius:10, padding:20 }}>
              <div style={{ fontSize:28, fontFamily:'Space Mono,monospace', color:c }}>{v}</div>
              <div style={{ fontSize:11, color:'#64748b', marginTop:4 }}>{l}</div>
            </div>
          ))}
        </div>
        {pie.length > 0 && <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:16 }}>
          <div style={{ background:'#0f1a0f', border:'1px solid #1a2e1a', borderRadius:10, padding:20 }}>
            <h3 style={{ fontSize:13, marginBottom:16, color:'#94a3b8' }}>Signal Distribution</h3>
            <ResponsiveContainer width="100%" height={180}><PieChart><Pie data={pie} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={65}>{pie.map((e,i)=><Cell key={i} fill={e.fill}/>)}</Pie><Legend /></PieChart></ResponsiveContainer>
          </div>
          <div style={{ background:'#0f1a0f', border:'1px solid #1a2e1a', borderRadius:10, padding:20 }}>
            <h3 style={{ fontSize:13, marginBottom:16, color:'#94a3b8' }}>Performance</h3>
            <ResponsiveContainer width="100%" height={180}><BarChart data={bars}><XAxis dataKey="name" stroke="#64748b" fontSize={11}/><YAxis stroke="#64748b" fontSize={11}/><Tooltip contentStyle={{ background:'#0f1a0f', border:'1px solid #1a2e1a' }}/><Bar dataKey="value" radius={[4,4,0,0]}>{bars.map((e,i)=><Cell key={i} fill={e.color}/>)}</Bar></BarChart></ResponsiveContainer>
          </div>
        </div>}
      </>}
      {!stats && <div style={{ textAlign:'center', color:'#64748b', padding:60, background:'#0f1a0f', border:'1px solid #1a2e1a', borderRadius:12 }}>Extract signals first, then run the backtest to see performance metrics.</div>}
    </div>
  )
}
