import { useState, useRef } from 'react'
import Markdown from 'react-markdown'

const NODE_LABELS = {
  grounding: 'Initializing...',
  company_analyzer: 'Researching company...',
  industry_analyzer: 'Analyzing industry...',
  financial_analyst: 'Pulling financials...',
  news_scanner: 'Scanning news...',
  competitor_scanner: 'Mapping competitors...',
  collector: 'Collecting results...',
  curator: 'Curating data...',
  briefing: 'Writing section briefs...',
  editor: 'Compiling final report...',
  validator: 'Validating report...',
  done: 'Done',
}

export default function App() {
  const [company, setCompany] = useState('')
  const [website, setWebsite] = useState('')
  const [status, setStatus] = useState(null)   // null | 'running' | 'completed' | 'failed'
  const [node, setNode] = useState('')
  const [report, setReport] = useState('')
  const [validationNotes, setValidationNotes] = useState(null)
  const esRef = useRef(null)

  async function handleSubmit(e) {
    e.preventDefault()
    if (!company.trim()) return

    setStatus('running')
    setNode('grounding')
    setReport('')
    setValidationNotes(null)

    const res = await fetch('/research', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ company: company.trim(), website: website.trim() }),
    })
    const { job_id } = await res.json()

    // Stream progress via SSE
    if (esRef.current) esRef.current.close()
    const es = new EventSource(`/research/${job_id}/stream`)
    esRef.current = es

    es.onmessage = async (e) => {
      const data = JSON.parse(e.data)
      setNode(data.node)
      if (data.status === 'completed') {
        es.close()
        const r = await fetch(`/research/${job_id}/report`)
        const body = await r.json()
        setReport(body.report)
        setStatus('completed')
      } else if (data.status === 'failed') {
        es.close()
        setStatus('failed')
      }
    }

    es.onerror = () => {
      es.close()
      setStatus('failed')
    }
  }

  function handleExport() {
    const blob = new Blob([report], { type: 'text/markdown' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${company.trim().replace(/\s+/g, '-')}-report.md`
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <>
      <h1>Company Researcher</h1>

      <form className="search-form" onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Company name (e.g. Stripe)"
          value={company}
          onChange={e => setCompany(e.target.value)}
          disabled={status === 'running'}
        />
        <input
          type="text"
          placeholder="Website (optional)"
          value={website}
          onChange={e => setWebsite(e.target.value)}
          disabled={status === 'running'}
          style={{ maxWidth: 220 }}
        />
        <button type="submit" disabled={status === 'running' || !company.trim()}>
          {status === 'running' ? 'Researching...' : 'Research'}
        </button>
      </form>

      {status === 'running' && (
        <div className="status-bar">
          {NODE_LABELS[node] || node}
        </div>
      )}
      {status === 'failed' && (
        <div className="status-bar error">Research failed. Check backend logs.</div>
      )}
      {status === 'completed' && (
        <div className="status-bar done">Report ready</div>
      )}

      {report && (
        <div className="report-box">
          <Markdown>{report}</Markdown>
          {validationNotes && (
            <div className="validation-notes">
              <strong>Validator notes:</strong>
              <pre style={{ whiteSpace: 'pre-wrap', marginTop: 4 }}>{validationNotes}</pre>
            </div>
          )}
          <button className="export-btn" onClick={handleExport}>Export as Markdown</button>
        </div>
      )}
    </>
  )
}
