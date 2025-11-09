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
            className="flex flex-col space-y-2 text-2xl! sm:text-3xl! md:text-4xl! lg:text-6xl! font-normal! leading-tight mb-6 animate-fade-in-up opacity-0"
            style={{ animationDelay: "0.1s" }}
          >
            <span className="text-[#76B900]">Say hello to your</span>
            <span className="text-white">AI-Powered <TypingText words={["Project Assistant.", "Coding Assistant.", "Design Assistant.", "Research Assistant."]} typingSpeed={80} deletingSpeed={40} pause={1400} className="text-white inline-block" /></span>
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
        {/* Preview image (served from public/home-preview.png). Hidden on small screens. Anchored bottom-right of the hero on md+. */}
        <img
          src="/home-preview.png"
          alt="Home preview"
          aria-hidden="true"
          className="pointer-events-none hidden md:block absolute right-30 bottom-0 z-20 w-56 md:w-140 lg:w-192 rounded-2xl shadow-2xl opacity-95 animate-fade-in-up opacity-0"
          style={{ }}
        />
      </section>

      {/* Key Benefits Section - Rule of Three */}
      <section id="benefits" className="bg-gradient-to-b from-black to-gray-900 py-24 px-6 relative">
        <div className="max-w-7xl mx-auto">
          {/* Section Header */}
          <div className="text-center mb-16 opacity-0 animate-fade-in-up">
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
              className="group bg-gray-900/50 backdrop-blur-sm border border-gray-800 rounded-2xl p-8 hover:border-[#76B900]/50 transition-all duration-300 hover:transform hover:scale-105 opacity-0 animate-fade-in-up"
              style={{ animationDelay: "0.2s" }}
            >
              <div className="flex justify-center mb-6">
                <div className="w-16 h-16 bg-[#76B900]/10 rounded-2xl flex items-center justify-center group-hover:bg-[#76B900]/20 transition-colors">
                  <svg className="w-8 h-8 text-[#76B900]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    {/* Database / Ingestion icon */}
                    <ellipse cx="12" cy="6" rx="7" ry="2.5" strokeWidth={2} />
                    <path d="M5 6v3c0 1.38 3.134 2.5 7 2.5s7-1.12 7-2.5V6" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" />
                    <path d="M5 12v3c0 1.38 3.134 2.5 7 2.5s7-1.12 7-2.5v-3" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                </div>
              </div>
              <h3 className="text-xl font-bold text-white mb-3 text-center">Smart Ingestion</h3>
              <p className="text-gray-400 text-center leading-relaxed">
                Automatically analyze repositories, code comments, and architecture notes to build structured context before writing.
              </p>
            </div>

            {/* Benefit 2 - Smart Analytics */}
            <div 
              className="group bg-gray-900/50 backdrop-blur-sm border border-gray-800 rounded-2xl p-8 hover:border-[#76B900]/50 transition-all duration-300 hover:transform hover:scale-105 opacity-0 animate-fade-in-up"
              style={{ animationDelay: "0.3s" }}
            >
              <div className="flex justify-center mb-6">
                <div className="w-16 h-16 bg-[#76B900]/10 rounded-2xl flex items-center justify-center group-hover:bg-[#76B900]/20 transition-colors">
                  <svg className="w-8 h-8 text-[#76B900]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    {/* Flow / Planning icon */}
                    <rect x="3" y="3" width="6" height="6" rx="1.5" strokeWidth={2} />
                    <rect x="15" y="3" width="6" height="6" rx="1.5" strokeWidth={2} />
                    <rect x="9" y="15" width="6" height="6" rx="1.5" strokeWidth={2} />
                    <path d="M6 9v6h6" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" />
                    <path d="M18 9v6h-6" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                </div>
              </div>
              <h3 className="text-xl font-bold text-white mb-3 text-center">Autonomous Planning</h3>
              <p className="text-gray-400 text-center leading-relaxed">
                Agents map the documentation hierarchy, ensuring logical flow and linking related sections seamlessly.
              </p>
            </div>

            {/* Benefit 3 - Enterprise Ready */}
            <div 
              className="group bg-gray-900/50 backdrop-blur-sm border border-gray-800 rounded-2xl p-8 hover:border-[#76B900]/50 transition-all duration-300 hover:transform hover:scale-105 opacity-0 animate-fade-in-up"
              style={{ animationDelay: "0.4s" }}
            >
              <div className="flex justify-center mb-6">
                <div className="w-16 h-16 bg-[#76B900]/10 rounded-2xl flex items-center justify-center group-hover:bg-[#76B900]/20 transition-colors">
                  <svg className="w-8 h-8 text-[#76B900]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    {/* Upload / Publish icon */}
                    <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" />
                    <path d="M17 8l-5-5-5 5" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" />
                    <path d="M12 3v12" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                </div>
              </div>
              <h3 className="text-xl font-bold text-white mb-3 text-center">Fast Publishing</h3>
              <p className="text-gray-400 text-center leading-relaxed">
                Deploys directly to Docusaurus with pre-built navigation, visuals, and styling. Ready for production.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonial Section - Social Proof */}

      {/* Final CTA Section - Repeated Conversion */}
      <section className="bg-gradient-to-b from-gray-900 via-black to-black py-24 px-6 border-t border-gray-800">
        <div className="max-w-4xl mx-auto text-center space-y-8">
          <h2 className="text-4xl md:text-5xl font-bold text-white leading-tight">
            <span className="text-[#76B900]">One-Link</span> Setup
          </h2>
          <p className="text-xl text-gray-300 max-w-3xl mx-auto">
            Skip the setup. Just paste your GitHub repository link, and our multi-agent system takes care of the rest.
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
