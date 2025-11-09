import { useState } from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <nav className="bg-black/95 backdrop-blur-sm text-white border-b border-gray-800/50 sticky top-0 z-50 animate-slide-down">
      <div className="max-w-[97rem] mx-auto lg:px-8">
        <div className="flex justify-between items-center h-20">
          {/* Logo - Simplified */}
          <Link to="/" className="text-2xl font-bold text-[#76B900] hover:text-[#5d9100] transition-colors">
            AutoDoc
          </Link>

          {/* Desktop CTA Button - Single Focus */}
          <div className="hidden md:block">
            <Link 
              to="/login" 
              className="bg-[#76B900] text-white px-8 py-3 rounded-lg font-semibold hover:bg-[#5d9100] transition-all transform hover:scale-105 shadow-lg"
            >
              Get Started
            </Link>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="text-white hover:text-[#76B900] focus:outline-none transition-colors"
              aria-label="Toggle menu"
            >
              <svg
                className="h-6 w-6"
                fill="none"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                {isMenuOpen ? (
                  <path d="M6 18L18 6M6 6l12 12" />
                ) : (
                  <path d="M4 6h16M4 12h16M4 18h16" />
                )}
              </svg>
            </button>
          </div>
        </div>

        {/* Mobile Menu - Minimal */}
        {isMenuOpen && (
          <div className="md:hidden pb-6 pt-2 animate-fade-in">
            <Link 
              to="/login" 
              className="block bg-[#76B900] text-white px-6 py-3 rounded-lg font-semibold hover:bg-[#5d9100] transition-all text-center"
              onClick={() => setIsMenuOpen(false)}
            >
              Get Started
            </Link>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
