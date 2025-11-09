const Footer = () => {
  return (
    <footer className="bg-black text-gray-400 border-t border-gray-800/50 animate-fade-in">
      <div className="max-w-7xl mx-auto px-6 py-12">
        {/* Minimal Footer Layout */}
        <div className="flex flex-col md:flex-row justify-between items-center space-y-6 md:space-y-0">
          
          {/* Logo */}
          <div className="text-center md:text-left">
            <h3 className="text-2xl font-bold text-[#76B900]">AutoDoc</h3>
            <p className="text-gray-500 text-sm mt-2">GPU Monitoring Made Simple</p>
          </div>

          {/* Legal Links */}
          <div className="flex space-x-6 text-sm">
            <a href="#" className="text-gray-500 hover:text-[#76B900] transition-colors">
              Privacy
            </a>
            <a href="#" className="text-gray-500 hover:text-[#76B900] transition-colors">
              Terms
            </a>
          </div>
        </div>

        {/* Copyright */}
        <div className="mt-8 pt-8 border-t border-gray-800/50 text-center">
          <p className="text-gray-500 text-sm">
            © {new Date().getFullYear()} AutoDoc. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
