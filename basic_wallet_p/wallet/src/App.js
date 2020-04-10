import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { Form, DataCheck } from './components'

function App() {
  const [id, setID] = useState('0')
  const [newID, setNewID] = useState('')
  const [chain, setChain] = useState([])

  useEffect(() => {
    axios
      .get('http://localhost:5000/chain')
      .then(({ data }) => {
        setChain(data.chain)
        console.log(data)
      })
      .catch((err) => console.log(err))
  }, [id])

  const handleChange = (e) => setNewID(e.target.value)

  const handleSubmit = (e) => {
    e.preventDefault()
    setID(newID)
  }

  return (
    <div>
      <Form submit={handleSubmit} change={handleChange} id={newID} />
      <h1>Wallet {id}</h1>
      <DataCheck data={chain} />
    </div>
  )
}

export default App
