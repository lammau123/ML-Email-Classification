import { useState } from 'react'
import EmailForm from './components/EmailForm'

import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div>
        <EmailForm></EmailForm>
      </div>
    </>
  )
}

export default App
