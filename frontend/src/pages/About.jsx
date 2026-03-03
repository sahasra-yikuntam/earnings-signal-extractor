import React from 'react'
export default function About() {
  return (
    <div style={{ maxWidth:750, margin:'0 auto', padding:'32px 24px' }}>
      <h1 style={{ fontSize:24, marginBottom:24, color:'#4ade80' }}>About This Project</h1>
      <div style={{ background:'#0f1a0f', border:'1px solid #1a2e1a', borderRadius:12, padding:28, marginBottom:16 }}>
        <h2 style={{ fontSize:15, marginBottom:12 }}>What It Does</h2>
        <p style={{ color:'#94a3b8', fontSize:14, lineHeight:1.8 }}>Extracts quantitative sentiment signals from SEC earnings call transcripts using LLMs, then backtests whether those signals predict short-term post-earnings stock returns — mimicking alternative data pipelines used at quantitative hedge funds.</p>
      </div>
      <div style={{ background:'#0f1a0f', border:'1px solid #1a2e1a', borderRadius:12, padding:28, marginBottom:16 }}>
        <h2 style={{ fontSize:15, marginBottom:12 }}>Signal Axes</h2>
        {[['Confidence Score','How assertively management speaks. High = confident.','#4ade80'],['Hedging Score','Frequency of hedging language. Lower = more bullish.','#f87171'],['Forward Guidance','How positive is guidance? Raised = high score.','#22d3ee'],['Risk Acknowledgment','How many risks flagged. Lower = more bullish.','#facc15']].map(([t,d,c])=>(
          <div key={t} style={{ marginBottom:14 }}><div style={{ fontSize:13, color:c, fontFamily:'Space Mono,monospace', marginBottom:3 }}>{t}</div><div style={{ fontSize:13, color:'#64748b' }}>{d}</div></div>
        ))}
      </div>
      <div style={{ background:'#0f1a0f', border:'1px solid #1a2e1a', borderRadius:12, padding:28 }}>
        <h2 style={{ fontSize:15, marginBottom:8 }}>Built By</h2>
        <p style={{ color:'#94a3b8', fontSize:14 }}>Sahasra Yikuntam</p>
        <p style={{ color:'#64748b', fontSize:13, marginTop:8 }}>Stack: FastAPI · React · SQLite · Anthropic/OpenAI · SEC EDGAR · Docker · GitHub Actions</p>
      </div>
    </div>
  )
}
