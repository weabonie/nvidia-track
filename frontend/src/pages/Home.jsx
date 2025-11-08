const Home = () => {
  return (
    <div className="max-w-4xl mx-auto text-center">
      <h1
        className="text-6xl md:text-7xl font-bold text-white mb-6 tracking-tight animate-fade-in-up opacity-0"
        style={{ animationDelay: "0.1s" }}
      >
        Welcome to NVIDIA Track
      </h1>
      <p
        className="text-xl md:text-2xl text-gray-400 mb-12 leading-relaxed animate-fade-in-up opacity-0"
        style={{ animationDelay: "0.3s" }}
      >
        Modern GPU monitoring and tracking solutions for developers
      </p>
      <div
        className="flex justify-center animate-fade-in-up opacity-0"
        style={{ animationDelay: "0.5s" }}
      >
        <button className="bg-white text-black px-10 py-4 rounded-lg font-semibold hover:bg-gray-200 transition-all transform hover:scale-105 text-lg">
          Get Started
        </button>
      </div>
    </div>
  );
};

export default Home;
