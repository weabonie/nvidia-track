import { useState } from 'react'
import Layout from './Layout'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <Layout>
      <div className='container mx-auto px-4'>
        <p className="text-3xl text-red-600">Copilot Helper</p>
      </div>
    </Layout>
  )
}

export default App
