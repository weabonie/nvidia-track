import { useState } from 'react'
import Layout from './Layout'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <Layout>
      <div className='container mx-auto px-4 py-20'>
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-6xl md:text-7xl font-bold text-white mb-6 tracking-tight animate-fade-in-up opacity-0" style={{ animationDelay: '0.1s' }}>
            Welcome to <span className="block mt-2">NVIDIA Track</span>
          </h1>
          <p className="text-xl md:text-2xl text-gray-400 mb-12 leading-relaxed animate-fade-in-up opacity-0" style={{ animationDelay: '0.3s' }}>
            Modern GPU monitoring and tracking solutions for developers
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center animate-fade-in-up opacity-0" style={{ animationDelay: '0.5s' }}>
            <button className="bg-white text-black px-10 py-4 rounded-lg font-semibold hover:bg-gray-200 transition-all transform hover:scale-105 text-lg">
              Get Started
            </button>
            <button className="bg-transparent border-2 border-white text-white px-10 py-4 rounded-lg font-semibold hover:bg-white hover:text-black transition-all text-lg">
              Learn More
            </button>
          </div>
        </div>
      </div>
    </Layout>
  )
}

export default App
