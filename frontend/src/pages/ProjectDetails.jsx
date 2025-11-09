import * as React from "react"
import { useParams, Link, useNavigate } from "react-router-dom"
import axios from "axios"

const ProjectDetails = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const [data, setData] = React.useState(null)
  const [loading, setLoading] = React.useState(true)
  const [error, setError] = React.useState(null)

  // Derive API slug: remove hyphens and lowercase (mirrors ProjectCard logic)
  const apiSlug = React.useMemo(() => (id || "").toLowerCase().replace(/-/g, ""), [id])

  React.useEffect(() => {
    let cancelled = false
    const controller = new AbortController()
    const fetchRepo = async () => {
      if (!apiSlug) return
      try {
        setLoading(true)
        setError(null)
        const resp = await axios.get("https://apihackutd.siru.dev/repo", {
          params: { name: apiSlug },
          signal: controller.signal,
        })
        if (!cancelled) setData(resp.data)
      } catch (e) {
        if (!cancelled) setError(e?.message || "Failed to load repository data")
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    fetchRepo()
    return () => {
      cancelled = true
      try { controller.abort() } catch {}
    }
  }, [apiSlug])

  const retry = () => {
    setData(null)
    setError(null)
    setLoading(true)
    // trigger effect by updating dependency through temporary state change
    // we can simply re-run logic inline instead of duplicating
    const controller = new AbortController()
    axios.get("https://apihackutd.siru.dev/repo", { params: { name: apiSlug }, signal: controller.signal })
      .then(r => setData(r.data))
      .catch(e => setError(e?.message || "Failed to load repository data"))
      .finally(() => setLoading(false))
  }

  const siteUrl = data?.doc_generation?.response?.url
  const pagesObj = data?.pages || {}
  const installation = data?.installation || []
  const dependencies = data?.dependencies || []
  const goal = data?.goal || data?.description || "No description available"
  const displayName = data?.name || (id || '').replace(/-/g, ' ')

  return (
    <div className="min-h-screen bg-black">
      <div className="border-b border-gray-800">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center gap-2 text-sm text-gray-400 mb-4">
            <button onClick={() => navigate("/dashboard")} className="hover:text-white transition-colors">Projects</button>
            <span>/</span>
            <span className="text-white capitalize">{displayName}</span>
          </div>
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-semibold text-white capitalize mb-2">{displayName}</h1>
              <div className="flex items-center gap-4 text-sm">
                {siteUrl && (
                  <a href={siteUrl} target="_blank" rel="noopener noreferrer" className="text-gray-400 hover:text-white transition-colors">
                    {siteUrl}
                  </a>
                )}
                <span className="text-gray-600">•</span>
                <span className="text-gray-400">Nemotron</span>
              </div>
            </div>
            <div className="flex items-center gap-3">
              {siteUrl && (
                <a href={siteUrl} target="_blank" rel="noreferrer" className="px-4 py-2 text-sm font-medium text-gray-300 hover:text-white bg-gray-900 hover:bg-gray-800 border border-gray-800 rounded-md transition-colors">Visit Docs</a>
              )}
              <button className="px-4 py-2 text-sm font-medium text-black bg-white hover:bg-gray-200 rounded-md transition-colors">Re-Ingest</button>
            </div>
          </div>
        </div>
      </div>
      <div className="max-w-7xl mx-auto px-6 py-8">
        {loading ? (
          <div className="space-y-8 animate-fade-in">
            <div className="h-6 bg-gray-800 rounded w-48 mb-4 animate-pulse"></div>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              {[1,2,3,4].map(i => (
                <div key={i} className="bg-[#0a0a0a] border border-gray-800 rounded-lg p-6 animate-pulse">
                  <div className="h-4 bg-gray-800 rounded w-20 mb-2"></div>
                  <div className="h-8 bg-gray-800 rounded w-16"></div>
                </div>
              ))}
            </div>
          </div>
        ) : error ? (
          <div className="flex flex-col items-start gap-4 bg-[#0a0a0a] border border-red-800/40 rounded-lg p-6">
            <div className="text-red-400 text-sm">{error}</div>
            <button onClick={retry} className="px-3 py-1.5 text-sm bg-red-600 hover:bg-red-500 text-white rounded-md">Retry</button>
          </div>
        ) : (
          <div className="space-y-8 animate-fade-in">
            <h2 className="text-lg font-semibold text-white">Nemotron Pipeline</h2>
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Left column: pipeline steps & project stats */}
              <div className="space-y-4">
                <div className="flex flex-col gap-3">
                  {["Ingest","Plan","Write","Publish"].map((step, idx) => (
                    <div key={step} className="bg-[#0a0a0a] border border-gray-800 rounded-lg p-4">
                      <div className="flex items-start justify-between">
                        <div>
                          <div className="text-sm text-gray-400">{step}</div>
                          <div className="text-white font-medium mt-1 text-sm">
                            {step === 'Ingest' ? 'Analyze repository code, comments and architecture to build context.' : step === 'Plan' ? 'Produce a documentation outline, sections and flowcharts.' : step === 'Write' ? 'Generate docs pages and examples from plans.' : 'Build and deploy generated docs.'}
                          </div>
                        </div>
                        <div className="text-right">
                          <div className={`text-xs px-2 py-1 rounded ${idx===0 ? 'bg-[#07200a] text-[#76B900]' : 'bg-gray-900 text-gray-400'}`}>{idx===0 ? 'Ready' : 'Idle'}</div>
                        </div>
                      </div>
                      <div className="mt-4 flex items-center gap-2">
                        <button className="px-3 py-1.5 text-sm bg-[#76B900] text-black rounded-md">{step === 'Ingest' ? 'Run Ingest' : step === 'Plan' ? 'Generate Plan' : step === 'Write' ? 'Start Writing' : 'Publish Docs'}</button>
                        <button className="px-3 py-1.5 text-sm bg-transparent border border-gray-800 text-gray-300 rounded-md">Logs</button>
                      </div>
                    </div>
                  ))}
                </div>
                <div className="bg-[#0a0a0a] border border-gray-800 rounded-lg p-4">
                  <div className="text-sm text-gray-400">Project</div>
                  <div className="text-white font-semibold text-lg">{displayName}</div>
                  <div className="mt-3 grid grid-cols-2 gap-2 text-sm text-gray-400">
                    <div>Dependencies</div>
                    <div className="text-right">{dependencies.length ? dependencies.slice(0,3).join(', ') : '—'}</div>
                    <div>Status</div>
                    <div className="text-right text-[#76B900]">{data?.doc_generation?.status || 'Unknown'}</div>
                    <div>Docs</div>
                    <div className="text-right">{siteUrl ? <a href={siteUrl} target="_blank" rel="noreferrer" className="text-[#76B900] underline">Open</a> : '—'}</div>
                  </div>
                </div>
              </div>
              {/* Middle: goal & installation */}
              <div className="bg-[#0a0a0a] border border-gray-800 rounded-lg p-4 flex flex-col">
                <div className="mb-4">
                  <div className="text-sm text-gray-400 mb-1">Project Goal</div>
                  <div className="text-sm text-gray-300 whitespace-pre-line">{goal}</div>
                </div>
                <div>
                  <div className="text-sm text-gray-400 mb-2">Installation Steps</div>
                  <ol className="list-decimal list-inside space-y-1 text-sm text-gray-300">
                    {installation.length ? installation.map((step,i)=>(<li key={i}>{step}</li>)) : <li>No steps provided.</li>}
                  </ol>
                </div>
              </div>
              {/* Right: pages list */}
              <div className="space-y-4">
                <div className="bg-[#0a0a0a] border border-gray-800 rounded-lg p-4">
                  <div className="flex items-center justify-between">
                    <div className="text-sm text-gray-400">Generated Pages</div>
                    {siteUrl && <a href={siteUrl} target="_blank" rel="noreferrer" className="text-sm text-[#76B900] hover:underline">Open Site</a>}
                  </div>
                  <div className="mt-3 text-sm text-gray-300">Pages inferred from last run:</div>
                  <ul className="mt-3 space-y-2 text-sm">
                    {Object.keys(pagesObj).length ? (
                      Object.entries(pagesObj).slice(0,8).map(([title, desc]) => (
                        <li key={title} className="flex flex-col">
                          <span className="text-white font-medium">{title}</span>
                          <span className="text-xs text-gray-400 line-clamp-2">{desc}</span>
                        </li>
                      ))
                    ) : (
                      <li className="text-xs text-gray-500">No pages generated yet.</li>
                    )}
                  </ul>
                </div>
                <div className="bg-[#0a0a0a] border border-gray-800 rounded-lg p-4">
                  <div className="text-sm text-gray-400 mb-2">Recent Activity</div>
                  <div className="text-sm text-gray-300">No recent Nemotron runs. Use pipeline buttons to start ingestion.</div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default ProjectDetails
