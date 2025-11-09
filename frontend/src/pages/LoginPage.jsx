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
      <div className="w-1/2 min-h-screen bg-black relative overflow-hidden">
        {/* Background overlay with gradient */}
        <div className="absolute inset-0 bg-gradient-to-br from-black/80 via-[#76B900]/10 to-black/80 z-10 pointer-events-none"></div>
        
        {/* Main GPU Image */}
        <img
          src="https://images.unsplash.com/photo-1591488320449-011701bb6704?w=1920&q=80&fit=crop"
          alt="NVIDIA GPU Technology"
          className={`w-full h-full object-cover transition-all duration-700 ${
            imageLoaded ? 'scale-100 opacity-100' : 'scale-110 opacity-0'
          }`}
          onLoad={() => setImageLoaded(true)}
        />
      </div>
    </div>
  );
};

export default LoginPage;
