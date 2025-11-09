import { useState, useEffect } from "react";
import { Link } from "react-router-dom";

const DashboardNavbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [showSearch, setShowSearch] = useState(false);

  // Handle keyboard shortcut
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'f' || e.key === 'F') {
        e.preventDefault();
        setShowSearch(true);
      }
      if (e.key === 'Escape') {
        setShowSearch(false);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

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
                NVIDIA Track
              </span>
            </Link>

            {/* Divider */}
            <div className="hidden md:block w-px h-6 bg-gray-800"></div>

            {/* Main Navigation */}
            <div className="hidden md:flex items-center gap-1">
              <Link 
                to="/projects" 
                className="px-3 py-1.5 text-sm text-white font-medium rounded-md hover:bg-gray-900 transition-colors duration-150"
              >
                Overview
              </Link>
              <Link 
                to="/projects/integrations" 
                className="px-3 py-1.5 text-sm text-gray-400 hover:text-white font-medium rounded-md hover:bg-gray-900 transition-colors duration-150"
              >
                Integrations
              </Link>
              <Link 
                to="/projects/activity" 
                className="px-3 py-1.5 text-sm text-gray-400 hover:text-white font-medium rounded-md hover:bg-gray-900 transition-colors duration-150"
              >
                Activity
              </Link>
              <Link 
                to="/projects/domains" 
                className="px-3 py-1.5 text-sm text-gray-400 hover:text-white font-medium rounded-md hover:bg-gray-900 transition-colors duration-150"
              >
                Domains
              </Link>
              <Link 
                to="/projects/settings" 
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

            {/* Deploy Button */}
            <Link 
              to="/projects/deploy"
              className="hidden md:flex items-center gap-2 px-3 py-1.5 text-sm font-medium text-black bg-white hover:bg-gray-200 rounded-md transition-colors duration-150"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
              </svg>
              Deploy
            </Link>

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
              <Link 
                to="/projects/deploy"
                className="mt-2 flex items-center justify-center gap-2 px-3 py-2 text-sm font-medium text-black bg-white hover:bg-gray-200 rounded-md"
                onClick={() => setIsMenuOpen(false)}
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
                Deploy
              </Link>
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
                <button className="w-full flex items-center gap-3 px-3 py-2 text-sm text-gray-300 hover:bg-gray-900 rounded transition-colors duration-150">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                  </svg>
                  New Project
                </button>
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
    </nav>
  );
};

export default DashboardNavbar;
