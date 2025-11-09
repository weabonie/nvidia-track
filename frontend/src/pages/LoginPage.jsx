import LoginForm from "../components/LoginForm";
import { useState } from "react";

const LoginPage = () => {
  const [imageLoaded, setImageLoaded] = useState(false);

  return (
    <div className="w-full min-h-screen flex animate-fade-in">
      {/* Left Side - Login Form */}
      <div className="bg-gradient-to-b from-lime-900 to-zinc-900 to-lime-800 w-1/2 min-h-screen bg-black flex flex-col justify-center items-center">
        <div className="animate-scale-in opacity-0" style={{ animationDelay: "0.3s" }}>
          <LoginForm/>
        </div>
      </div>

      {/* Right Side - Interactive Image */}
      <div className="w-1/2 min-h-screen bg-black relative overflow-hidden group">
        {/* Background overlay with gradient */}
        <div className="absolute inset-0 bg-gradient-to-br from-black/80 via-[#76B900]/10 to-black/80 z-10 pointer-events-none"></div>
        
        {/* Main GPU Image */}
        <img
          src="https://images.unsplash.com/photo-1591488320449-011701bb6704?w=1920&q=80&fit=crop"
          alt="NVIDIA GPU Technology"
          className={`w-full h-full object-cover transition-all duration-700 ${
            imageLoaded ? 'scale-100 opacity-100' : 'scale-110 opacity-0'
          } group-hover:scale-105`}
          onLoad={() => setImageLoaded(true)}
        />

        {/* Interactive overlay content */}
        <div className="absolute inset-0 z-20 flex flex-col justify-center items-center text-center px-12 opacity-0 group-hover:opacity-100 transition-opacity duration-500">
          <div className="bg-black/60 backdrop-blur-md p-8 rounded-2xl border border-[#76B900]/30 transform group-hover:scale-105 transition-transform duration-500">
            <h2 className="text-4xl font-bold text-white mb-4 animate-fade-in">
              Welcome to <span className="text-[#76B900]">NVIDIA Track</span>
            </h2>
            <p className="text-gray-300 text-lg mb-6">
              Monitor your GPUs in real-time with cutting-edge AI technology
            </p>
            <div className="flex gap-4 justify-center">
              <div className="bg-[#76B900]/20 backdrop-blur-sm px-6 py-3 rounded-lg border border-[#76B900]/40">
                <div className="text-2xl font-bold text-[#76B900]">99.9%</div>
                <div className="text-xs text-gray-400">Uptime</div>
              </div>
              <div className="bg-[#76B900]/20 backdrop-blur-sm px-6 py-3 rounded-lg border border-[#76B900]/40">
                <div className="text-2xl font-bold text-[#76B900]">10K+</div>
                <div className="text-xs text-gray-400">Users</div>
              </div>
              <div className="bg-[#76B900]/20 backdrop-blur-sm px-6 py-3 rounded-lg border border-[#76B900]/40">
                <div className="text-2xl font-bold text-[#76B900]">&lt;100ms</div>
                <div className="text-xs text-gray-400">Response</div>
              </div>
            </div>
          </div>
        </div>

        {/* Floating particles effect */}
        <div className="absolute inset-0 z-5 pointer-events-none">
          <div className="absolute top-1/4 left-1/4 w-2 h-2 bg-[#76B900] rounded-full animate-pulse opacity-60"></div>
          <div className="absolute top-3/4 right-1/3 w-3 h-3 bg-[#76B900] rounded-full animate-pulse opacity-40" style={{ animationDelay: "0.5s" }}></div>
          <div className="absolute top-1/2 right-1/4 w-2 h-2 bg-[#76B900] rounded-full animate-pulse opacity-50" style={{ animationDelay: "1s" }}></div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
