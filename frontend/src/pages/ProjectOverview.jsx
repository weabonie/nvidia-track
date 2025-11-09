import { useParams, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";

const ProjectOverview = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState("overview");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Simulate loading delay
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 800); // 0.8 seconds loading

    return () => clearTimeout(timer);
  }, [id]);

  // Mock project data - in real app, fetch based on id
  const project = {
    id: id,
    name: id?.replace(/-/g, " "),
    status: "Ready",
    url: `https://${id}.vercel.app`,
    framework: "React",
    lastDeployed: "2 minutes ago",
  };

  const deployments = [
    {
      id: 1,
      commit: "Update navbar design",
      branch: "main",
      status: "Ready",
      time: "2 minutes ago",
      url: `https://${id}-git-main.vercel.app`,
    },
    {
      id: 2,
      commit: "Fix login animation",
      branch: "main",
      status: "Ready",
      time: "1 hour ago",
      url: `https://${id}-abc123.vercel.app`,
    },
    {
      id: 3,
      commit: "Add dashboard skeleton",
      branch: "main",
      status: "Ready",
      time: "3 hours ago",
      url: `https://${id}-def456.vercel.app`,
    },
  ];

  const stats = [
    { label: "Visitors", value: "1.2K", change: "+12%" },
    { label: "Requests", value: "8.4K", change: "+8%" },
    { label: "Bandwidth", value: "124 MB", change: "+5%" },
    { label: "Errors", value: "0", change: "0%" },
  ];

  return (
    <div className="min-h-screen bg-black">
      {/* Header */}
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
                <a href={project.url} target="_blank" rel="noopener noreferrer" className="text-gray-400 hover:text-white transition-colors flex items-center gap-1">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                  </svg>
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
                Deploy
              </button>
            </div>
          </div>

          {/* Tabs */}
          <div className="flex items-center gap-6 mt-6 border-b border-gray-800 -mb-px">
            <button
              onClick={() => setActiveTab("overview")}
              className={`pb-3 text-sm font-medium transition-colors border-b-2 ${
                activeTab === "overview"
                  ? "text-white border-white"
                  : "text-gray-400 border-transparent hover:text-white"
              }`}
            >
              Overview
            </button>
            <button
              onClick={() => setActiveTab("deployments")}
              className={`pb-3 text-sm font-medium transition-colors border-b-2 ${
                activeTab === "deployments"
                  ? "text-white border-white"
                  : "text-gray-400 border-transparent hover:text-white"
              }`}
            >
              Deployments
            </button>
            <button
              onClick={() => setActiveTab("analytics")}
              className={`pb-3 text-sm font-medium transition-colors border-b-2 ${
                activeTab === "analytics"
                  ? "text-white border-white"
                  : "text-gray-400 border-transparent hover:text-white"
              }`}
            >
              Analytics
            </button>
            <button
              onClick={() => setActiveTab("settings")}
              className={`pb-3 text-sm font-medium transition-colors border-b-2 ${
                activeTab === "settings"
                  ? "text-white border-white"
                  : "text-gray-400 border-transparent hover:text-white"
              }`}
            >
              Settings
            </button>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        {isLoading ? (
          // Skeleton Loading State
          <div className="space-y-8 animate-fade-in">
            {/* Production Deployment Skeleton */}
            <div>
              <div className="h-6 bg-gray-800 rounded w-48 mb-4 animate-pulse"></div>
              <div className="bg-[#0a0a0a] border border-gray-800 rounded-lg p-6 animate-pulse">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div className="w-2 h-2 bg-gray-800 rounded-full"></div>
                    <div className="h-5 bg-gray-800 rounded w-24"></div>
                    <div className="h-5 bg-gray-800 rounded w-32"></div>
                  </div>
                  <div className="h-9 bg-gray-800 rounded w-24"></div>
                </div>
                <div className="h-4 bg-gray-800 rounded w-64"></div>
              </div>
            </div>

            {/* Stats Grid Skeleton */}
            <div>
              <div className="h-6 bg-gray-800 rounded w-32 mb-4 animate-pulse"></div>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                {[1, 2, 3, 4].map((i) => (
                  <div key={i} className="bg-[#0a0a0a] border border-gray-800 rounded-lg p-6 animate-pulse">
                    <div className="h-4 bg-gray-800 rounded w-20 mb-2"></div>
                    <div className="h-8 bg-gray-800 rounded w-16"></div>
                  </div>
                ))}
              </div>
            </div>

            {/* Recent Deployments Skeleton */}
            <div>
              <div className="h-6 bg-gray-800 rounded w-40 mb-4 animate-pulse"></div>
              <div className="bg-[#0a0a0a] border border-gray-800 rounded-lg divide-y divide-gray-800">
                {[1, 2, 3].map((i) => (
                  <div key={i} className="p-6 animate-pulse">
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          <div className="w-2 h-2 bg-gray-800 rounded-full"></div>
                          <div className="h-5 bg-gray-800 rounded w-48"></div>
                          <div className="h-5 bg-gray-800 rounded w-16"></div>
                        </div>
                        <div className="flex items-center gap-3">
                          <div className="h-4 bg-gray-800 rounded w-24"></div>
                          <div className="h-4 bg-gray-800 rounded w-32"></div>
                        </div>
                      </div>
                      <div className="h-9 bg-gray-800 rounded w-16"></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ) : (
          // Actual Content
          <>
            {activeTab === "overview" && (
          <div className="space-y-8 animate-fade-in">
            {/* Production Deployment */}
            <div>
              <h2 className="text-lg font-semibold text-white mb-4">Production Deployment</h2>
              <div className="bg-[#0a0a0a] border border-gray-800 rounded-lg p-6">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div className="w-2 h-2 bg-[#76B900] rounded-full"></div>
                    <span className="text-white font-medium">{project.status}</span>
                    <span className="text-gray-400 text-sm">•</span>
                    <span className="text-gray-400 text-sm">{project.lastDeployed}</span>
                  </div>
                  <button className="px-3 py-1.5 text-sm text-gray-300 hover:text-white bg-gray-900 hover:bg-gray-800 border border-gray-800 rounded-md transition-colors">
                    Redeploy
                  </button>
                </div>
                
                <a href={project.url} target="_blank" rel="noopener noreferrer" className="text-[#76B900] hover:underline text-sm">
                  {project.url}
                </a>
              </div>
            </div>

            {/* Stats Grid */}
            <div>
              <h2 className="text-lg font-semibold text-white mb-4">Project Stats</h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                {stats.map((stat) => (
                  <div key={stat.label} className="bg-[#0a0a0a] border border-gray-800 rounded-lg p-6">
                    <div className="text-sm text-gray-400 mb-2">{stat.label}</div>
                    <div className="flex items-baseline gap-2">
                      <div className="text-2xl font-semibold text-white">{stat.value}</div>
                      <div className={`text-xs ${stat.change.startsWith('+') ? 'text-[#76B900]' : 'text-gray-400'}`}>
                        {stat.change}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Recent Deployments */}
            <div>
              <h2 className="text-lg font-semibold text-white mb-4">Recent Deployments</h2>
              <div className="bg-[#0a0a0a] border border-gray-800 rounded-lg divide-y divide-gray-800">
                {deployments.map((deployment) => (
                  <div key={deployment.id} className="p-6 hover:bg-gray-900/50 transition-colors">
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          <div className="w-2 h-2 bg-[#76B900] rounded-full"></div>
                          <span className="text-white font-medium">{deployment.commit}</span>
                          <span className="px-2 py-0.5 text-xs text-gray-400 bg-gray-800 rounded">
                            {deployment.branch}
                          </span>
                        </div>
                        <div className="flex items-center gap-3 text-sm text-gray-400">
                          <span>{deployment.status}</span>
                          <span>•</span>
                          <span>{deployment.time}</span>
                        </div>
                      </div>
                      <a
                        href={deployment.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="px-3 py-1.5 text-sm text-gray-300 hover:text-white border border-gray-800 hover:border-gray-700 rounded-md transition-colors"
                      >
                        Visit
                      </a>
                    </div>
                  </div>
                ))}
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

export default ProjectOverview;
