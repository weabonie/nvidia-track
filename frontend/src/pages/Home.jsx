import { Link } from "react-router-dom";
import TypingText from "../components/TypingText"

const Home = () => {
  return (
    <div className="w-full">
      {/* Hero Section - Full Viewport */}
      <section className="relative bg-black min-h-[calc(100vh-5rem)] flex py-12 justify-center overflow-hidden">
        {/* Optimized Background */}
        <div className="absolute inset-0">
          <div 
            className="absolute inset-0 opacity-15"
            style={{
              backgroundImage: "url('https://images.unsplash.com/photo-1591488320449-011701bb6704?q=80&w=1920&auto=format&fit=crop&ixlib=rb-4.0.3')",
              backgroundSize: "cover",
              backgroundPosition: "center",
              backgroundRepeat: "no-repeat",
            }}
          ></div>
          <div className="absolute inset-0 bg-gradient-to-br from-black via-black/95 to-black"></div>
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(118,185,0,0.1)_0%,transparent_70%)]"></div>
        </div>
        
        {/* Hero Content - Z-Pattern Layout */}
        <div className="relative w-[90%] max-w-8xl mx-auto text-left px-2 z-10">
          {/* Main Headline - Clear Value Prop */}
          <h1
            className="flex flex-col space-y-2 text-5xl sm:text-6xl md:text-7xl lg:text-8xl font-normal! leading-tight mb-6 animate-fade-in-up opacity-0"
            style={{ animationDelay: "0.1s" }}
          >
            <span className="text-[#76B900]">Say hello to your</span>
            <span className="text-white">AI-Powered <TypingText words={["Project Management Assistant.", "Coding Assistant.", "Design Assistant.", "Research Assistant."]} typingSpeed={80} deletingSpeed={40} pause={1400} className="text-white inline-block" /></span>
          </h1>

          {/* Subheadline - Benefit-Driven */}
          <p
            className="text-lg text-left sm:text-xl md:text-2xl text-gray-300 mx-auto mb-10 leading-relaxed animate-fade-in-up opacity-0"
            style={{ animationDelay: "0.2s" }}
          >
            Where productivity meets intelligence.
          </p>

          {/* Primary CTA */}
          <div
            className="flex flex-col sm:flex-row gap-4 animate-fade-in-up opacity-0"
            style={{ animationDelay: "0.3s" }}
          >
            <Link 
              to={"/login"} 
              className="group bg-[#76B900] text-white px-10 py-4 rounded-lg font-semibold hover:bg-[#5d9100] transition-all duration-300 transform hover:scale-105 text-lg shadow-md hover:shadow-[#76B900]/50 w-full sm:w-auto"
            >
              Get Started Free
              <svg className="inline-block ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </Link>
            <a 
              href="#benefits" 
              className="text-gray-300 px-10 py-4 rounded-lg font-semibold border-2 border-gray-700 hover:border-[#76B900] hover:text-white transition-all duration-300 w-full sm:w-auto"
            >
              Learn More
            </a>
          </div>

          {/* Social Proof Indicators */}
          {/* <div 
            className="flex flex-wrap justify-center items-center gap-8 mt-16 animate-fade-in opacity-0"
            style={{ animationDelay: "0.4s" }}
          >
            <div className="text-center">
              <div className="text-3xl font-bold text-[#76B900]">99.9%</div>
              <div className="text-sm text-gray-400">Uptime</div>
            </div>
            <div className="h-8 w-px bg-gray-800"></div>
            <div className="text-center">
              <div className="text-3xl font-bold text-[#76B900]">10K+</div>
              <div className="text-sm text-gray-400">Active Users</div>
            </div>
            <div className="h-8 w-px bg-gray-800"></div>
            <div className="text-center">
              <div className="text-3xl font-bold text-[#76B900]">&lt;100ms</div>
              <div className="text-sm text-gray-400">Response Time</div>
            </div>
          </div> */}
        </div>
      </section>

      {/* Key Benefits Section - Rule of Three */}
      <section id="benefits" className="bg-gradient-to-b from-black to-gray-900 py-24 px-6">
        <div className="max-w-7xl mx-auto">
          {/* Section Header */}
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-5xl font-bold text-white mb-4">
              Save <span className="text-[#76B900]">hours</span> of manual writing.
            </h2>
            <p className="text-lg text-gray-400 max-w-2xl mx-auto">
              Powered by multiple Nemotron models, each agent specializes in technical writing, diagram explanation, and user guidance.
            </p>
          </div>

          {/* Benefits Grid */}
          <div className="grid md:grid-cols-3 gap-8 lg:gap-12">
            {/* Benefit 1 - Real-Time Monitoring */}
            <div 
              className="group bg-gray-900/50 backdrop-blur-sm border border-gray-800 rounded-2xl p-8 hover:border-[#76B900]/50 transition-all duration-300 hover:transform hover:scale-105 animate-fade-in-up opacity-0"
              style={{ animationDelay: "0.1s" }}
            >
              <div className="flex justify-center mb-6">
                <div className="w-16 h-16 bg-[#76B900]/10 rounded-2xl flex items-center justify-center group-hover:bg-[#76B900]/20 transition-colors">
                  <svg className="w-8 h-8 text-[#76B900]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
              </div>
              <h3 className="text-xl font-bold text-white mb-3 text-center">Real-Time Monitoring</h3>
              <p className="text-gray-400 text-center leading-relaxed">
                Track GPU utilization, memory, and temperature instantly
              </p>
            </div>

            {/* Benefit 2 - Smart Analytics */}
            <div 
              className="group bg-gray-900/50 backdrop-blur-sm border border-gray-800 rounded-2xl p-8 hover:border-[#76B900]/50 transition-all duration-300 hover:transform hover:scale-105 animate-fade-in-up opacity-0"
              style={{ animationDelay: "0.2s" }}
            >
              <div className="flex justify-center mb-6">
                <div className="w-16 h-16 bg-[#76B900]/10 rounded-2xl flex items-center justify-center group-hover:bg-[#76B900]/20 transition-colors">
                  <svg className="w-8 h-8 text-[#76B900]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                </div>
              </div>
              <h3 className="text-xl font-bold text-white mb-3 text-center">AI-Powered Insights</h3>
              <p className="text-gray-400 text-center leading-relaxed">
                Get intelligent recommendations to maximize efficiency
              </p>
            </div>

            {/* Benefit 3 - Enterprise Ready */}
            <div 
              className="group bg-gray-900/50 backdrop-blur-sm border border-gray-800 rounded-2xl p-8 hover:border-[#76B900]/50 transition-all duration-300 hover:transform hover:scale-105 animate-fade-in-up opacity-0"
              style={{ animationDelay: "0.3s" }}
            >
              <div className="flex justify-center mb-6">
                <div className="w-16 h-16 bg-[#76B900]/10 rounded-2xl flex items-center justify-center group-hover:bg-[#76B900]/20 transition-colors">
                  <svg className="w-8 h-8 text-[#76B900]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                  </svg>
                </div>
              </div>
              <h3 className="text-xl font-bold text-white mb-3 text-center">Enterprise Security</h3>
              <p className="text-gray-400 text-center leading-relaxed">
                Bank-grade encryption and compliance for peace of mind
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonial Section - Social Proof */}
      <section className="bg-gray-900 py-20 px-6">
        <div className="max-w-4xl mx-auto">
          <div className="bg-gradient-to-br from-gray-800 to-gray-900 rounded-2xl p-8 md:p-12 border border-gray-700">
            <div className="flex items-start gap-4 mb-6">
              <svg className="w-12 h-12 text-[#76B900] flex-shrink-0" fill="currentColor" viewBox="0 0 24 24">
                <path d="M14.017 21v-7.391c0-5.704 3.731-9.57 8.983-10.609l.995 2.151c-2.432.917-3.995 3.638-3.995 5.849h4v10h-9.983zm-14.017 0v-7.391c0-5.704 3.748-9.57 9-10.609l.996 2.151c-2.433.917-3.996 3.638-3.996 5.849h3.983v10h-9.983z" />
              </svg>
            </div>
            <p className="text-xl md:text-2xl text-white mb-6 leading-relaxed">
              "NVIDIA Track transformed how we monitor our ML infrastructure. Real-time insights helped us reduce GPU costs by 40%."
            </p>
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-[#76B900] rounded-full flex items-center justify-center text-white font-bold text-lg">
                JD
              </div>
              <div>
                <div className="text-white font-semibold">Jane Doe</div>
                <div className="text-gray-400 text-sm">ML Engineer, Tech Corp</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Final CTA Section - Repeated Conversion */}
      <section className="bg-gradient-to-b from-gray-900 via-black to-black py-24 px-6 border-t border-gray-800">
        <div className="max-w-4xl mx-auto text-center space-y-8">
          <h2 className="text-4xl md:text-5xl font-bold text-white leading-tight">
            Ready to <span className="text-[#76B900]">supercharge</span> your GPUs?
          </h2>
          <p className="text-xl text-gray-300 max-w-2xl mx-auto">
            Join thousands of developers optimizing their GPU workloads today
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4">
            <Link 
              to={"/login"} 
              className="bg-[#76B900] text-white px-12 py-4 rounded-lg font-semibold hover:bg-[#5d9100] transition-all duration-300 transform hover:scale-105 text-lg shadow-2xl hover:shadow-[#76B900]/50"
            >
              Get Started Free
            </Link>
            <a 
              href="mailto:contact@nvidiatrack.com" 
              className="text-gray-300 px-12 py-4 rounded-lg font-semibold border-2 border-gray-700 hover:border-[#76B900] hover:text-white transition-all duration-300"
            >
              Contact Sales
            </a>
          </div>
          <p className="text-sm text-gray-500">
            No credit card required • Free 14-day trial • Cancel anytime
          </p>
        </div>
      </section>
    </div>
  );
};

export default Home;
