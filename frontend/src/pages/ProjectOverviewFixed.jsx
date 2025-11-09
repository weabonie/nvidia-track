import { useParams, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";

const ProjectOverviewFixed = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState("overview");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => setIsLoading(false), 600);
    return () => clearTimeout(timer);
  }, [id]);

  const project = {
    id,
    name: id?.replace(/-/g, " ") || "Project",
    status: "Ready",
    url: `https://${id || "project"}.example.com`,
    framework: "Nemotron",
    lastDeployed: "3 minutes ago",
  };

  return (
    <div className="min-h-screen bg-black">
      <div className="border-b border-gray-800">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center gap-2 text-sm text-gray-400 mb-4">
            <button onClick={() => navigate("/projects")} className="hover:text-white transition-colors">
              Projects
            </button>
            <span>/</span>
            <span className="text-white capitalize">{project.name}</span>
          </div>

          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-semibold text-white capitalize mb-2">{project.name}</h1>
              <div className="flex items-center gap-4 text-sm">
                <a href={project.url} target="_blank" rel="noopener noreferrer" className="text-gray-400 hover:text-white transition-colors">
                  {project.url}
                </a>
                <span className="text-gray-600">•</span>
                <span className="text-gray-400">{project.framework}</span>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <button className="px-4 py-2 text-sm font-medium text-gray-300 hover:text-white bg-gray-900 hover:bg-gray-800 border border-gray-800 rounded-md transition-colors">
                Visit
              </button>
              <button className="px-4 py-2 text-sm font-medium text-black bg-white hover:bg-gray-200 rounded-md transition-colors">
                Run Pipeline
              </button>
            </div>
          </div>

          <div className="flex items-center gap-6 mt-6 border-b border-gray-800 -mb-px">
            <button
              onClick={() => setActiveTab("overview")}
              className={`pb-3 text-sm font-medium transition-colors border-b-2 ${
                activeTab === "overview" ? "text-white border-white" : "text-gray-400 border-transparent hover:text-white"
              }`}
            >
              Overview
            </button>
            <button
              onClick={() => setActiveTab("deployments")}
              className={`pb-3 text-sm font-medium transition-colors border-b-2 ${
                activeTab === "deployments" ? "text-white border-white" : "text-gray-400 border-transparent hover:text-white"
              }`}
            >
              Deployments
            </button>
            <button
              onClick={() => setActiveTab("analytics")}
              className={`pb-3 text-sm font-medium transition-colors border-b-2 ${
                activeTab === "analytics" ? "text-white border-white" : "text-gray-400 border-transparent hover:text-white"
              }`}
            >
              Analytics
            </button>
            <button
              onClick={() => setActiveTab("settings")}
              className={`pb-3 text-sm font-medium transition-colors border-b-2 ${
                activeTab === "settings" ? "text-white border-white" : "text-gray-400 border-transparent hover:text-white"
              }`}
            >
              Settings
            </button>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-8">
        {isLoading ? (
          <div className="space-y-8 animate-fade-in">
            <div className="h-6 bg-gray-800 rounded w-48 mb-4 animate-pulse"></div>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              {[1, 2, 3, 4].map((i) => (
                <div key={i} className="bg-[#0a0a0a] border border-gray-800 rounded-lg p-6 animate-pulse">
                  <div className="h-4 bg-gray-800 rounded w-20 mb-2"></div>
                  <div className="h-8 bg-gray-800 rounded w-16"></div>
                </div>
              ))}
            </div>
          </div>
        ) : (
          <>
            {activeTab === "overview" && (
              <div className="space-y-8 animate-fade-in">
                <h2 className="text-lg font-semibold text-white">Nemotron Pipeline</h2>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                  {/* Left: Pipeline cards and quick stats */}
                  <div className="space-y-4">
                    <div className="flex flex-col gap-3">
                      {[
                        {
                          key: "ingest",
                          title: "Ingest",
                          desc: "Analyze repository code, comments and architecture to build context.",
                          status: "Ready",
                          action: "Run Ingest",
                        },
                        {
                          key: "plan",
                          title: "Plan",
                          desc: "Produce a documentation outline, sections and flowcharts.",
                          status: "Queued",
                          action: "Generate Plan",
                        },
                        {
                          key: "write",
                          title: "Write",
                          desc: "Generate Docusaurus pages and code examples from plans.",
                          status: "Idle",
                          action: "Start Writing",
                        },
                        {
                          key: "publish",
                          title: "Publish",
                          desc: "Build and deploy generated docs to the configured host.",
                          status: "Idle",
                          action: "Publish Docs",
                        },
                      ].map((step) => (
                        <div key={step.key} className="bg-[#0a0a0a] border border-gray-800 rounded-lg p-4">
                          <div className="flex items-start justify-between">
                            <div>
                              <div className="text-sm text-gray-400">{step.title}</div>
                              <div className="text-white font-medium mt-1 text-sm">{step.desc}</div>
                            </div>
                            <div className="text-right">
                              <div className={`text-xs px-2 py-1 rounded ${step.status === 'Ready' ? 'bg-[#07200a] text-[#76B900]' : 'bg-gray-900 text-gray-400'}`}>{step.status}</div>
                            </div>
                          </div>
                          <div className="mt-4 flex items-center gap-2">
                            <button className="px-3 py-1.5 text-sm bg-[#76B900] text-black rounded-md">{step.action}</button>
                            <button className="px-3 py-1.5 text-sm bg-transparent border border-gray-800 text-gray-300 rounded-md">Logs</button>
                          </div>
                        </div>
                      ))}
                    </div>

                    <div className="bg-[#0a0a0a] border border-gray-800 rounded-lg p-4">
                      <div className="text-sm text-gray-400">Project</div>
                      <div className="text-white font-semibold text-lg">{project.name}</div>
                      <div className="mt-3 grid grid-cols-2 gap-2 text-sm text-gray-400">
                        <div>Agents</div>
                        <div className="text-right">Nemotron Suite</div>
                        <div>Last Run</div>
                        <div className="text-right">{project.lastDeployed}</div>
                        <div>Status</div>
                        <div className="text-right text-[#76B900]">{project.status}</div>
                      </div>
                    </div>
                  </div>

                  {/* Middle: Flowchart preview */}
                  <div className="bg-[#0a0a0a] border border-gray-800 rounded-lg p-4 flex flex-col">
                    <div className="flex items-center justify-between mb-3">
                      <div className="text-sm text-gray-400">Generated Flowchart</div>
                      <div className="text-xs text-gray-400">Auto-updated</div>
                    </div>
                    <div className="flex-1 bg-black/20 rounded-md p-4 flex items-center justify-center">
                      <svg width="100%" height="220" viewBox="0 0 600 220" className="max-h-[220px]">
                        <rect x="20" y="30" width="140" height="60" rx="8" fill="#07180a" stroke="#2b6a19" />
                        <text x="90" y="65" textAnchor="middle" fill="#76B900" fontSize="12">Ingest</text>
                        <rect x="230" y="30" width="140" height="60" rx="8" fill="#07180a" stroke="#2b6a19" />
                        <text x="300" y="65" textAnchor="middle" fill="#76B900" fontSize="12">Plan</text>
                        <rect x="440" y="30" width="140" height="60" rx="8" fill="#07180a" stroke="#2b6a19" />
                        <text x="510" y="65" textAnchor="middle" fill="#76B900" fontSize="12">Write</text>
                        <path d="M160 60 L230 60" stroke="#3b7a2e" strokeWidth="2" markerEnd="url(#arrow)" />
                        <path d="M370 60 L440 60" stroke="#3b7a2e" strokeWidth="2" markerEnd="url(#arrow)" />
                        <defs>
                          <marker id="arrow" markerWidth="10" markerHeight="10" refX="6" refY="3" orient="auto">
                            <path d="M0,0 L0,6 L6,3 z" fill="#3b7a2e" />
                          </marker>
                        </defs>
                      </svg>
                    </div>
                    <div className="mt-3 flex gap-2">
                      <button className="px-3 py-1.5 bg-transparent border border-gray-800 text-gray-300 rounded-md">Open in Diagram Editor</button>
                      <button className="px-3 py-1.5 bg-[#76B900] text-black rounded-md">Export SVG</button>
                    </div>
                  </div>

                  {/* Right: Docs preview & pages */}
                  <div className="space-y-4">
                    <div className="bg-[#0a0a0a] border border-gray-800 rounded-lg p-4">
                      <div className="flex items-center justify-between">
                        <div className="text-sm text-gray-400">Generated Docs</div>
                        <a href={project.url} target="_blank" rel="noreferrer" className="text-sm text-[#76B900] hover:underline">Open Site</a>
                      </div>
                      <div className="mt-3 text-sm text-gray-300">Pages generated from the last ingest.</div>
                      <ul className="mt-3 space-y-2 text-sm">
                        <li className="flex items-center justify-between"><span>Introduction</span><span className="text-xs text-gray-400">docs/introduction.md</span></li>
                        <li className="flex items-center justify-between"><span>Installation</span><span className="text-xs text-gray-400">docs/installation.md</span></li>
                        <li className="flex items-center justify-between"><span>Usage Guide</span><span className="text-xs text-gray-400">docs/usage.md</span></li>
                      </ul>
                    </div>

                    <div className="bg-[#0a0a0a] border border-gray-800 rounded-lg p-4">
                      <div className="text-sm text-gray-400">Recent Activity</div>
                      <div className="mt-3 text-sm text-gray-300">No recent Nemotron runs. Use the pipeline buttons to start ingestion and generation.</div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {activeTab === "deployments" && (
              <div className="animate-fade-in">
                <div className="text-center py-12">
                  <div className="text-gray-400 mb-4">
                    <svg className="w-12 h-12 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                    </svg>
                  </div>
                  <h3 className="text-lg font-medium text-white mb-2">All Deployments</h3>
                  <p className="text-gray-400">View all deployment history here</p>
                </div>
              </div>
            )}

            {activeTab === "analytics" && (
              <div className="animate-fade-in">
                <div className="text-center py-12">
                  <div className="text-gray-400 mb-4">
                    <svg className="w-12 h-12 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                    </svg>
                  </div>
                  <h3 className="text-lg font-medium text-white mb-2">Analytics Dashboard</h3>
                  <p className="text-gray-400">Track your project's performance metrics</p>
                </div>
              </div>
            )}

            {activeTab === "settings" && (
              <div className="animate-fade-in">
                <div className="text-center py-12">
                  <div className="text-gray-400 mb-4">
                    <svg className="w-12 h-12 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                  </div>
                  <h3 className="text-lg font-medium text-white mb-2">Project Settings</h3>
                  <p className="text-gray-400">Configure your project settings</p>
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default ProjectOverviewFixed;
