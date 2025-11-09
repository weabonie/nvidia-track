import LoginForm from "../components/LoginForm";

const LoginPage = () => {
  return (
    <div className="w-full min-h-screen flex animate-fade-in">
      {/* Left Side - Login Form */}
      <div className="bg-gradient-to-b from-lime-900 to-zinc-900 to-lime-800 w-1/2 min-h-screen bg-black flex flex-col justify-center items-center">
        <div className="animate-scale-in opacity-0" style={{ animationDelay: "0.3s" }}>
          <LoginForm/>
        </div>
      </div>

      {/* Right Side - Project Name */}
      <div className="w-1/2 min-h-screen bg-gradient-to-br from-black via-zinc-900 to-black relative overflow-hidden flex items-center justify-center">
        {/* Animated background effects */}
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(118,185,0,0.15)_0%,transparent_70%)]"></div>
        <div className="absolute inset-0 opacity-20">
          <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-[#76B900] rounded-full blur-[120px] animate-pulse"></div>
          <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-[#76B900] rounded-full blur-[120px] animate-pulse" style={{ animationDelay: "1s" }}></div>
        </div>
        
        {/* Project Name */}
        <div className="relative z-10 text-center animate-fade-in-up opacity-0" style={{ animationDelay: "0.2s" }}>
          <h1 className="text-8xl font-bold mb-6">
            <span className="text-[#76B900]">Auto</span>
            <span className="text-[#76B900]">Doc</span>
          </h1>
          <p className="text-2xl text-gray-400 font-light tracking-wide">
            AI-Powered Documentation Assistant
          </p>
          <div className="mt-8 flex justify-center space-x-2">
            <div className="w-2 h-2 bg-[#76B900] rounded-full animate-pulse"></div>
            <div className="w-2 h-2 bg-[#76B900] rounded-full animate-pulse" style={{ animationDelay: "0.2s" }}></div>
            <div className="w-2 h-2 bg-[#76B900] rounded-full animate-pulse" style={{ animationDelay: "0.4s" }}></div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
