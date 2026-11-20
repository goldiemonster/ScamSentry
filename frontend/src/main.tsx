import React, { useState } from 'react'
import { createRoot } from 'react-dom/client'
import './style.css'

type Finding = { reason: string; points: number }
type Result = { risk_score: number; risk_level: string; findings: Finding[]; recommendation: string; disclaimer: string }
function App() {
  const [message, setMessage] = useState('URGENT! Your account suspended. Click this link and pay with a gift card: https://example.invalid')
  const [result, setResult] = useState<Result | null>(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  async function check() {
    setLoading(true); setError(''); setResult(null)
    try {
      const response = await fetch('/api/analyze', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ text: message }) })
      if (!response.ok) throw new Error('Could not analyze message. Is the backend running?')
      setResult(await response.json())
    } catch (e) { setError(e instanceof Error ? e.message : 'Unknown error') }
    finally { setLoading(false) }
  }
  return <main><h1>ScamSentry</h1><p>Check a synthetic message for common scam warning signs.</p>
    <section><label htmlFor="message">Message</label><textarea id="message" rows={7} maxLength={10000} value={message} onChange={e => setMessage(e.target.value)} />
    <button disabled={!message.trim() || loading} onClick={check}>{loading ? 'Checking…' : 'Check message'}</button>
    <p className="note">Prototype only. Do not enter real private communications.</p></section>
    {error && <p role="alert">{error}</p>}
    {result && <section aria-live="polite"><h2>Risk: {result.risk_level.toUpperCase()} ({result.risk_score}/100)</h2><p>{result.recommendation}</p>
    <h3>Warning signs</h3>{result.findings.length ? <ul>{result.findings.map(f => <li key={f.reason}>{f.reason}</li>)}</ul> : <p>No rule matches.</p>}
    <p className="note">{result.disclaimer}</p></section>}</main>
}
createRoot(document.getElementById('root')!).render(<React.StrictMode><App /></React.StrictMode>)
