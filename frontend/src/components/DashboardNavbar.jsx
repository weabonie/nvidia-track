import { useState, useEffect } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

const DashboardNavbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [showSearch, setShowSearch] = useState(false);
  const [showDeployModal, setShowDeployModal] = useState(false);
  const [githubUrl, setGithubUrl] = useState("");

  // Handle keyboard shortcut
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'f' || e.key === 'F') {
        e.preventDefault();
        setShowSearch(true);
      }
      if (e.key === 'Escape') {
        setShowSearch(false);
        setShowDeployModal(false);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const handleDeploy = (e) => {
    e.preventDefault();
    if (githubUrl.trim()) {
      // Call backend ingest endpoint to retrieve project metadata
      const controller = new AbortController();
      setIngestAbortController(controller);
      setDeployStartTime(Date.now());
      setIngestCompleted(false);
      (async () => {
        try {
          setIngestLoading(true);
          setIngestError(null);
          const resp = await axios.get("https://apihackutd.siru.dev/ingest", {
            params: { repo_url: githubUrl.trim() },
            signal: controller.signal,
          });
          console.log("Ingest response:", resp.data);
          setIngestData(resp.data);
          setIngestCompleted(true);
          // clear the input so user can add another later
          setGithubUrl("");
        } catch (err) {
          console.error("Ingest failed", err);
          const message = err?.name === 'CanceledError' || err?.code === 'ERR_CANCELED' ? 'Deploy cancelled' : (err?.message || "Failed to ingest repository");
          setIngestError(message);
        } finally {
          setIngestLoading(false);
          setIngestAbortController(null);
        }
      })();
    }
  };


  // Ingest state
  const [ingestLoading, setIngestLoading] = useState(false);
  const [ingestData, setIngestData] = useState(null);
  const [ingestError, setIngestError] = useState(null);
  const [ingestAbortController, setIngestAbortController] = useState(null);
  const [ingestCompleted, setIngestCompleted] = useState(false);
  const [deployStartTime, setDeployStartTime] = useState(null);
  const [elapsedMs, setElapsedMs] = useState(0);

  const cancelDeploy = () => {
    if (ingestAbortController) {
      try {
        ingestAbortController.abort();
      } catch (e) {
        // ignore
      }
    }
    setIngestLoading(false);
    setIngestAbortController(null);
    setIngestError('Deploy cancelled');
    setIngestCompleted(false);
  }

  // update elapsed time while loading
  useEffect(() => {
    if (!ingestLoading) {
      setElapsedMs(0);
      return;
    }
    const id = setInterval(() => {
      setElapsedMs(Date.now() - (deployStartTime || Date.now()));
    }, 1000);
    return () => clearInterval(id);
  }, [ingestLoading, deployStartTime]);

  return (
    <nav className="sticky top-0 z-50 bg-black border-b border-gray-800/50">
      <div className="mx-auto px-6">
        <div className="flex items-center justify-between h-16">
          {/* Left Section - Logo & Navigation */}
          <div className="flex items-center gap-8">
            {/* Logo */}
            <Link to="/" className="flex items-center gap-2 group">
              <div className="w-6 h-6 bg-gradient-to-br from-[#76B900] to-[#5d9100] rounded-md flex items-center justify-center transform group-hover:scale-105 transition-transform duration-200">
                <span className="text-black font-bold text-sm">N</span>
              </div>
              <span className="text-sm font-medium text-white hidden sm:block">
                AutoDoc
              </span>
            </Link>

            {/* Divider */}
            <div className="hidden md:block w-px h-6 bg-gray-800"></div>

            {/* Main Navigation */}
            <div className="hidden md:flex items-center gap-1">
              <Link 
                to="/dashboard" 
                className="px-3 py-1.5 text-sm text-white font-medium rounded-md hover:bg-gray-900 transition-colors duration-150"
              >
                Projects
              </Link>
              <Link 
                to="/dashboard/integrations" 
                className="px-3 py-1.5 text-sm text-gray-400 hover:text-white font-medium rounded-md hover:bg-gray-900 transition-colors duration-150"
              >
                Integrations
              </Link>
              <Link 
                to="/dashboard/activity" 
                className="px-3 py-1.5 text-sm text-gray-400 hover:text-white font-medium rounded-md hover:bg-gray-900 transition-colors duration-150"
              >
                Activity
              </Link>
              <Link 
                to="/dashboard/domains" 
                className="px-3 py-1.5 text-sm text-gray-400 hover:text-white font-medium rounded-md hover:bg-gray-900 transition-colors duration-150"
              >
                Domains
              </Link>
              <Link 
                to="/dashboard/settings" 
                className="px-3 py-1.5 text-sm text-gray-400 hover:text-white font-medium rounded-md hover:bg-gray-900 transition-colors duration-150"
              >
                Settings
              </Link>
            </div>
          </div>

          {/* Right Section - Actions & User */}
          <div className="flex items-center gap-3">
            {/* Search Button */}
            <button 
              onClick={() => setShowSearch(true)}
              className="hidden md:flex items-center gap-2 px-3 py-1.5 text-sm text-gray-400 bg-gray-900/50 hover:bg-gray-900 border border-gray-800 rounded-md transition-colors duration-150"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <span className="hidden lg:inline">Search...</span>
              <span className="hidden lg:inline text-xs text-gray-600">F</span>
            </button>

            {/* Feedback Button */}
            <button className="hidden md:flex items-center gap-2 px-3 py-1.5 text-sm text-gray-400 hover:text-white bg-gray-900/50 hover:bg-gray-900 border border-gray-800 rounded-md transition-colors duration-150">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
              Feedback
            </button>

            {/* User Menu */}
            <div className="relative">
              <button 
                onClick={() => setShowUserMenu(!showUserMenu)}
                className="flex items-center gap-2 hover:opacity-80 transition-opacity duration-150"
              >
                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-[#76B900] to-[#5d9100] flex items-center justify-center">
                  <span className="text-white font-semibold text-xs">JD</span>
                </div>
                <svg className="hidden md:block w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>

              {/* Dropdown Menu */}
              {showUserMenu && (
                <div className="absolute right-0 mt-2 w-64 bg-black border border-gray-800 rounded-lg shadow-2xl overflow-hidden animate-scale-in">
                  {/* User Info */}
                  <div className="px-4 py-3 border-b border-gray-800">
                    <div className="text-sm font-medium text-white">John Doe</div>
                    <div className="text-xs text-gray-400">john.doe@nvidia.com</div>
                  </div>

                  {/* Menu Items */}
                  <div className="py-2">
                    <Link 
                      to="/projects/settings/profile"
                      className="flex items-center gap-3 px-4 py-2 text-sm text-gray-300 hover:bg-gray-900 hover:text-white transition-colors duration-150"
                      onClick={() => setShowUserMenu(false)}
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                      </svg>
                      Your Profile
                    </Link>
                    <Link 
                      to="/projects/settings/account"
                      className="flex items-center gap-3 px-4 py-2 text-sm text-gray-300 hover:bg-gray-900 hover:text-white transition-colors duration-150"
                      onClick={() => setShowUserMenu(false)}
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      </svg>
                      Settings
                    </Link>
                    <Link 
                      to="/projects/billing"
                      className="flex items-center gap-3 px-4 py-2 text-sm text-gray-300 hover:bg-gray-900 hover:text-white transition-colors duration-150"
                      onClick={() => setShowUserMenu(false)}
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
                      </svg>
                      Billing
                    </Link>
                  </div>

                  {/* Team Section */}
                  <div className="border-t border-gray-800 py-2">
                    <div className="px-4 py-2">
                      <div className="text-xs font-medium text-gray-500 uppercase tracking-wider mb-2">Team</div>
                      <button className="flex items-center gap-2 w-full px-2 py-1.5 text-sm text-gray-300 hover:bg-gray-900 hover:text-white rounded transition-colors duration-150">
                        <div className="w-5 h-5 rounded bg-[#76B900] flex items-center justify-center">
                          <span className="text-black font-bold text-[10px]">N</span>
                        </div>
                        <span>NVIDIA Team</span>
                      </button>
                    </div>
                  </div>

                  {/* Bottom Actions */}
                  <div className="border-t border-gray-800 py-2">
                    <Link 
                      to="/login"
                      className="flex items-center gap-3 px-4 py-2 text-sm text-gray-300 hover:bg-gray-900 hover:text-white transition-colors duration-150"
                      onClick={() => setShowUserMenu(false)}
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                      </svg>
                      Logout
                    </Link>
                  </div>
                </div>
              )}
            </div>

            {/* Mobile Menu Button */}
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="md:hidden p-2 text-gray-400 hover:text-white transition-colors duration-150"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                {isMenuOpen ? (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                ) : (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                )}
              </svg>
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="md:hidden border-t border-gray-800 py-4 animate-slide-down">
            <div className="flex flex-col gap-1">
              <Link 
                to="/projects" 
                className="px-3 py-2 text-sm text-white font-medium rounded-md hover:bg-gray-900"
                onClick={() => setIsMenuOpen(false)}
              >
                Overview
              </Link>
              <Link 
                to="/projects/integrations" 
                className="px-3 py-2 text-sm text-gray-400 hover:text-white rounded-md hover:bg-gray-900"
                onClick={() => setIsMenuOpen(false)}
              >
                Integrations
              </Link>
              <Link 
                to="/projects/activity" 
                className="px-3 py-2 text-sm text-gray-400 hover:text-white rounded-md hover:bg-gray-900"
                onClick={() => setIsMenuOpen(false)}
              >
                Activity
              </Link>
              <Link 
                to="/projects/domains" 
                className="px-3 py-2 text-sm text-gray-400 hover:text-white rounded-md hover:bg-gray-900"
                onClick={() => setIsMenuOpen(false)}
              >
                Domains
              </Link>
              <Link 
                to="/projects/settings" 
                className="px-3 py-2 text-sm text-gray-400 hover:text-white rounded-md hover:bg-gray-900"
                onClick={() => setIsMenuOpen(false)}
              >
                Settings
              </Link>
              <button 
                onClick={() => {
                  setIsMenuOpen(false);
                  setShowDeployModal(true);
                }}
                className="mt-2 flex items-center justify-center gap-2 px-3 py-2 text-sm font-medium text-black bg-white hover:bg-gray-200 rounded-md"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
                Deploy
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Search Modal */}
      {showSearch && (
        <div className="fixed inset-0 z-50 flex items-start justify-center pt-20 px-4 bg-black/80 backdrop-blur-sm animate-fade-in">
          <div className="w-full max-w-2xl bg-black border border-gray-800 rounded-lg shadow-2xl animate-scale-in">
            {/* Search Input */}
            <div className="flex items-center gap-3 px-4 py-3 border-b border-gray-800">
              <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <input
                type="text"
                placeholder="Search projects, deployments, and more..."
                className="flex-1 bg-transparent text-white placeholder-gray-500 outline-none text-sm"
                autoFocus
              />
              <button
                onClick={() => setShowSearch(false)}
                className="text-xs text-gray-500 hover:text-gray-300 px-2 py-1 border border-gray-800 rounded"
              >
                ESC
              </button>
            </div>

            {/* Search Results/Suggestions */}
            <div className="p-3 max-h-96 overflow-y-auto">
              <div className="text-xs text-gray-500 uppercase tracking-wider mb-2">Recent</div>
              <div className="space-y-1">
                <button className="w-full flex items-center gap-3 px-3 py-2 text-sm text-gray-300 hover:bg-gray-900 rounded transition-colors duration-150">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
                  </svg>
                  nvidia-track-frontend
                </button>
                <button className="w-full flex items-center gap-3 px-3 py-2 text-sm text-gray-300 hover:bg-gray-900 rounded transition-colors duration-150">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
                  </svg>
                  model-eval
                </button>
              </div>

              <div className="text-xs text-gray-500 uppercase tracking-wider mb-2 mt-4">Quick Actions</div>
              <div className="space-y-1">
                {/* Deploy Button */}
                <button className="w-full flex items-center gap-3 px-3 py-2 text-sm text-gray-300 hover:bg-gray-900 rounded transition-colors duration-150">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                  Go to Settings
                </button>
              </div>
            </div>

            {/* Footer */}
            <div className="px-4 py-2 border-t border-gray-800 flex items-center justify-between text-xs text-gray-500">
              <span>Press <kbd className="px-1.5 py-0.5 bg-gray-900 border border-gray-800 rounded">F</kbd> to search</span>
              <span>Press <kbd className="px-1.5 py-0.5 bg-gray-900 border border-gray-800 rounded">ESC</kbd> to close</span>
            </div>
          </div>
        </div>
      )}

      {/* Deploy Modal */}
      {showDeployModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center px-4 bg-black/80 backdrop-blur-sm animate-fade-in" onClick={() => { if (!ingestLoading) setShowDeployModal(false); else { cancelDeploy(); setShowDeployModal(false); } }}>
          <div className="w-full max-w-lg bg-[#0a0a0a] border border-gray-800 rounded-md shadow-2xl animate-scale-in" onClick={(e) => e.stopPropagation()}>
            {/* Header */}
            <div className="px-6 py-4 border-b border-gray-800">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-semibold text-white">Deploy New Project</h2>
                <button 
                  onClick={() => { if (!ingestLoading) { setShowDeployModal(false); } else { cancelDeploy(); setShowDeployModal(false); } }}
                  className="text-gray-400 hover:text-white transition-colors"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>

            {/* Content */}
            {!(ingestLoading || ingestCompleted || ingestError) ? (
              <form onSubmit={handleDeploy} className="p-6">
              <div className="mb-6">
                <label htmlFor="github-url" className="block text-sm font-medium text-gray-300 mb-2">
                  GitHub Repository URL
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <svg className="w-5 h-5 text-gray-500" fill="currentColor" viewBox="0 0 24 24">
                      <path fillRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <input
                    type="text"
                    id="github-url"
                    value={githubUrl}
                    onChange={(e) => setGithubUrl(e.target.value)}
                    placeholder="https://github.com/username/repository"
                    className="w-full pl-10 pr-4 py-2.5 bg-black border border-gray-800 rounded-md text-white placeholder-gray-600 focus:outline-none focus:border-[#76B900] transition-colors"
                    required
                  />
                </div>
                <p className="mt-2 text-xs text-gray-500">
                  Enter the full URL of your GitHub repository to deploy
                </p>
              </div>

              {/* Framework Detection */}
              <div className="mb-6 p-4 bg-gray-900/50 border border-gray-800 rounded-md">
                <div className="flex items-start gap-3">
                  <svg className="w-5 h-5 text-[#76B900] mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <div>
                    <p className="text-sm text-white font-medium mb-1">Auto-detect Framework</p>
                    <p className="text-xs text-gray-400">
                      AutoDoc will automatically detect your framework and configure build settings
                    </p>
                  </div>
                </div>
              </div>

              {/* Actions */}
              <div className="flex items-center gap-3">
                <button
                  type="button"
                  onClick={() => setShowDeployModal(false)}
                  className="flex-1 px-4 py-2.5 text-sm font-medium text-gray-300 bg-gray-900 hover:bg-gray-800 border border-gray-800 rounded-md transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex-1 px-4 py-2.5 text-sm font-medium text-black bg-white hover:bg-gray-200 rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  disabled={!githubUrl.trim() || ingestLoading}
                >
                  {ingestLoading ? "Deploying..." : "Deploy"}
                </button>
              </div>
              </form>
            ) : (
              <div className="p-6">
                {ingestLoading && (
                  <div className="flex flex-col gap-4">
                    <div className="flex items-center gap-4">
                      <svg className="w-6 h-6 animate-spin text-white" viewBox="0 0 24 24" fill="none">
                        <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" className="opacity-20" />
                        <path d="M22 12a10 10 0 00-10-10" stroke="currentColor" strokeWidth="4" strokeLinecap="round" className="opacity-100" />
                      </svg>
                      <div>
                        <div className="text-white font-medium">Deploying project…</div>
                        <div className="text-xs text-gray-400">Elapsed: {Math.floor(elapsedMs/1000)}s</div>
                      </div>
                    </div>
                    <div className="flex gap-2">
                      <button onClick={() => { cancelDeploy(); setShowDeployModal(false); }} className="px-4 py-2 text-sm bg-gray-900 text-gray-300 rounded-md">Cancel</button>
                      <button onClick={() => { /* keep modal open */ }} className="px-4 py-2 text-sm bg-transparent border border-gray-800 text-gray-300 rounded-md">Keep Open</button>
                    </div>
                  </div>
                )}

                {ingestCompleted && ingestData && (
                  <div className="flex flex-col gap-4">
                    <div className="text-white font-medium">Deploy completed successfully</div>
                    <div className="text-sm text-gray-300">Project: <strong>{ingestData.name || ingestData['repo-name']}</strong></div>
                    {ingestData.doc_generation?.response?.url && (
                      <a href={ingestData.doc_generation.response.url} target="_blank" rel="noreferrer" className="text-sm text-[#76B900] underline">Open generated site</a>
                    )}
                    <div className="flex gap-2">
                      <button onClick={() => setShowDeployModal(false)} className="px-4 py-2 text-sm bg-[#76B900] text-black rounded-md">Close</button>
                      <button onClick={() => { /* TODO: navigate to project details or add to list */ setShowDeployModal(false); }} className="px-4 py-2 text-sm bg-transparent border border-gray-800 text-gray-300 rounded-md">View Project</button>
                    </div>
                  </div>
                )}

                {ingestError && (
                  <div className="flex flex-col gap-4">
                    <div className="text-white font-medium">Deploy failed</div>
                    <div className="text-sm text-red-400">{ingestError}</div>
                    <div className="flex gap-2">
                      <button onClick={() => { setIngestError(null); setIngestData(null); setIngestCompleted(false); }} className="px-4 py-2 text-sm bg-gray-900 text-gray-300 rounded-md">Retry</button>
                      <button onClick={() => setShowDeployModal(false)} className="px-4 py-2 text-sm bg-transparent border border-gray-800 text-gray-300 rounded-md">Close</button>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      )}
    </nav>
  );
};

export default DashboardNavbar;
