import { useState } from 'react';

const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <nav className="bg-black text-white border-b border-gray-800 animate-slide-down">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-20">
          {/* Logo */}
          <div className="flex-shrink-0">
            <a href="/" className="text-2xl font-bold tracking-tight text-[#76B900] hover:text-[#5d9100] transition-colors">
              NVIDIA Track
            </a>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex space-x-10">
            <a href="#home" className="text-sm font-medium hover:text-[#76B900] transition-colors uppercase tracking-wide">
              Home
            </a>
            <a href="#features" className="text-sm font-medium hover:text-[#76B900] transition-colors uppercase tracking-wide">
              Features
            </a>
            <a href="#about" className="text-sm font-medium hover:text-[#76B900] transition-colors uppercase tracking-wide">
              About
            </a>
            <a href="#contact" className="text-sm font-medium hover:text-[#76B900] transition-colors uppercase tracking-wide">
              Contact
            </a>
          </div>

          {/* CTA Button */}
          <div className="hidden md:block">
            <button className="bg-white text-black px-8 py-2.5 rounded-lg font-semibold hover:bg-[#76B900] hover:text-black transition-all transform hover:scale-105 border-2 border-white hover:border-[#76B900]">
              Get Started
            </button>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="text-white hover:text-gray-300 focus:outline-none"
            >
              <svg
                className="h-7 w-7"
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

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="md:hidden pb-6 pt-2 border-t border-gray-800">
            <div className="flex flex-col space-y-4">
              <a href="#home" className="text-sm font-medium hover:text-[#76B900] transition-colors uppercase tracking-wide">
                Home
              </a>
              <a href="#features" className="text-sm font-medium hover:text-[#76B900] transition-colors uppercase tracking-wide">
                Features
              </a>
              <a href="#about" className="text-sm font-medium hover:text-[#76B900] transition-colors uppercase tracking-wide">
                About
              </a>
              <a href="#contact" className="text-sm font-medium hover:text-[#76B900] transition-colors uppercase tracking-wide">
                Contact
              </a>
              <button className="bg-white text-black px-6 py-2.5 rounded-lg font-semibold hover:bg-[#76B900] hover:text-black transition-all w-full mt-2 border-2 border-white hover:border-[#76B900]">
                Get Started
              </button>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
