const Home = () => {
  return (
    <div className="w-full">
      {/* Hero Banner Section */}
      <div className="relative bg-gradient-to-br from-gray-900 via-black to-gray-900 border-y border-gray-800 py-20 mb-16">
        {/* Subtle grid pattern overlay */}
        <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.02)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.02)_1px,transparent_1px)] bg-[size:50px_50px] [mask-image:radial-gradient(ellipse_at_center,black_50%,transparent_100%)]"></div>
        
        <div className="relative max-w-4xl mx-auto text-center px-4">
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
            <button className="bg-white text-black px-10 py-4 rounded-lg font-semibold hover:bg-[#76B900] hover:text-black transition-all transform hover:scale-105 text-lg shadow-lg border-2 border-white hover:border-[#76B900]">
              Get Started
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
