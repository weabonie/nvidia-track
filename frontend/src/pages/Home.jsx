import { Link } from "react-router-dom";

const Home = () => {
  return (
    <div className="w-full h-full flex items-center">
      {/* Hero Banner Section with NVIDIA Theme */}
      <div className="relative bg-black border-b border-gray-800 py-32 md:py-40 w-full h-full flex items-center justify-center overflow-hidden">
        {/* NVIDIA-style geometric background */}
        <div className="absolute inset-0">
          {/* Dark gradient base */}
          <div className="absolute inset-0 bg-gradient-to-br from-gray-900 via-black to-gray-900"></div>

          {/* Animated green glow effects */}
          <div className="absolute top-1/4 right-1/4 w-96 h-96 bg-[#76B900] rounded-full blur-[120px] opacity-10 animate-pulse"></div>
          <div className="absolute bottom-1/4 left-1/4 w-96 h-96 bg-[#76B900] rounded-full blur-[120px] opacity-10 animate-pulse" style={{ animationDelay: "1s" }}></div>
        </div>
        
        <div className="relative max-w-4xl mx-auto text-center px-4 z-10">
          <h1
            className="text-6xl md:text-7xl font-bold text-[#76B900] mb-6 tracking-tight animate-fade-in-up opacity-0"
            style={{ animationDelay: "0.1s" }}
          >
            Welcome to NVIDIA Track
          </h1>
          <p
            className="text-xl md:text-2xl text-white mb-12 leading-relaxed animate-fade-in-up opacity-0"
            style={{ animationDelay: "0.3s" }}
          >
            Modern GPU monitoring and tracking solutions for developers
          </p>
          <div
            className="flex justify-center animate-fade-in-up opacity-0"
            style={{ animationDelay: "0.5s" }}
          >
            <Link to={"/login"} className="bg-[#76B900] text-white px-10 py-4 rounded-lg font-semibold hover:bg-[#5d9100] hover:text-white transition-all transform hover:scale-105 text-lg shadow-lg border-2 border-[#76B900] hover:border-[#5d9100]">
              Get Started
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
