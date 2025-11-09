import { Link } from "react-router-dom";

const Home = () => {
  return (
    <div className="w-full">
      {/* Hero Banner Section with NVIDIA Theme */}
      <div className="relative bg-black border-b border-gray-800 py-32 md:py-40 w-full min-h-[calc(100vh-5rem)] flex items-center justify-center overflow-hidden">
        {/* NVIDIA-style geometric background */}
        <div className="absolute inset-0">
          {/* NVIDIA Background Image */}
          <div 
            className="absolute inset-0 opacity-25"
            style={{
              backgroundImage: "url('https://images.unsplash.com/photo-1591488320449-011701bb6704?q=80&w=2070&auto=format&fit=crop')",
              backgroundSize: "cover",
              backgroundPosition: "center",
              backgroundRepeat: "no-repeat",
            }}
          ></div>
          
          {/* Dark gradient overlay to blend with image */}
          <div className="absolute inset-0 bg-gradient-to-br from-[#76B900]/20 via-black/70 to-[#5d9100]/20"></div>
          
          {/* Additional green gradient overlay */}
          <div className="absolute inset-0 bg-gradient-to-tr from-transparent via-[#76B900]/5 to-transparent"></div>
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
