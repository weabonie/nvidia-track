import { Link } from "react-router-dom";

const Home = () => {
  return (
    <div className="w-full">
      {/* Hero Section */}
      <div className="relative bg-black py-32 md:py-48 w-full min-h-[calc(100vh-5rem)] flex items-center justify-center overflow-hidden">
        {/* NVIDIA Background Image */}
        <div className="absolute inset-0">
          <div 
            className="absolute inset-0 opacity-20"
            style={{
              backgroundImage: "url('https://images.unsplash.com/photo-1591488320449-011701bb6704?q=80&w=2070&auto=format&fit=crop')",
              backgroundSize: "cover",
              backgroundPosition: "center",
              backgroundRepeat: "no-repeat",
            }}
          ></div>
          <div className="absolute inset-0 bg-gradient-to-br from-black/80 via-black/90 to-black/80"></div>
          <div className="absolute inset-0 bg-gradient-to-tr from-transparent via-[#76B900]/5 to-transparent"></div>
        </div>
        
        {/* Hero Content */}
        <div className="relative max-w-4xl mx-auto text-center px-6 z-10 space-y-8">
          <h1
            className="text-5xl md:text-7xl font-bold text-white mb-4 tracking-tight animate-fade-in-up opacity-0"
            style={{ animationDelay: "0.1s" }}
          >
            Monitor GPUs, <span className="text-[#76B900]">Maximize Performance</span>
          </h1>
          <p
            className="text-lg md:text-xl text-gray-300 max-w-2xl mx-auto animate-fade-in-up opacity-0"
            style={{ animationDelay: "0.3s" }}
          >
            Track GPU metrics in real-time and optimize your workloads effortlessly
          </p>
          <div
            className="flex justify-center pt-4 animate-fade-in-up opacity-0"
            style={{ animationDelay: "0.5s" }}
          >
            <Link 
              to={"/login"} 
              className="bg-[#76B900] text-white px-12 py-4 rounded-lg font-semibold hover:bg-[#5d9100] transition-all transform hover:scale-105 text-lg shadow-2xl"
            >
              Get Started
            </Link>
          </div>
        </div>
      </div>

      {/* Key Benefits Section */}
      <div className="bg-black py-24 px-6">
        <div className="max-w-6xl mx-auto">
          <div className="grid md:grid-cols-3 gap-12">
            {/* Benefit 1 */}
            <div 
              className="text-center space-y-4 animate-fade-in-up opacity-0"
              style={{ animationDelay: "0.2s" }}
            >
              <div className="flex justify-center mb-4">
                <div className="w-16 h-16 bg-[#76B900]/10 rounded-full flex items-center justify-center">
                  <svg className="w-8 h-8 text-[#76B900]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
              </div>
              <h3 className="text-xl font-semibold text-white">Real-Time Monitoring</h3>
              <p className="text-gray-400">Track GPU performance metrics instantly</p>
            </div>

            {/* Benefit 2 */}
            <div 
              className="text-center space-y-4 animate-fade-in-up opacity-0"
              style={{ animationDelay: "0.4s" }}
            >
              <div className="flex justify-center mb-4">
                <div className="w-16 h-16 bg-[#76B900]/10 rounded-full flex items-center justify-center">
                  <svg className="w-8 h-8 text-[#76B900]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                </div>
              </div>
              <h3 className="text-xl font-semibold text-white">Smart Analytics</h3>
              <p className="text-gray-400">Get insights to optimize your workloads</p>
            </div>

            {/* Benefit 3 */}
            <div 
              className="text-center space-y-4 animate-fade-in-up opacity-0"
              style={{ animationDelay: "0.6s" }}
            >
              <div className="flex justify-center mb-4">
                <div className="w-16 h-16 bg-[#76B900]/10 rounded-full flex items-center justify-center">
                  <svg className="w-8 h-8 text-[#76B900]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                </div>
              </div>
              <h3 className="text-xl font-semibold text-white">Enterprise Ready</h3>
              <p className="text-gray-400">Secure and scalable for teams of any size</p>
            </div>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-gradient-to-b from-black to-gray-900 py-20 px-6 border-t border-gray-800">
        <div className="max-w-3xl mx-auto text-center space-y-6">
          <h2 className="text-3xl md:text-4xl font-bold text-white">
            Ready to optimize your GPU performance?
          </h2>
          <p className="text-gray-400 text-lg">
            Join thousands of developers already using NVIDIA Track
          </p>
          <Link 
            to={"/login"} 
            className="inline-block bg-[#76B900] text-white px-12 py-4 rounded-lg font-semibold hover:bg-[#5d9100] transition-all transform hover:scale-105 text-lg shadow-2xl"
          >
            Get Started Free
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Home;
