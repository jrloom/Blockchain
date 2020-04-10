import React from 'react'

const Form = ({ submit, change, id }) => {
  return (
    <form onSubmit={submit}>
      <label>
        Set ID: <input value={id} onChange={change} />
      </label>
      <button type='submit'>submit</button>
    </form>
  )
}

export default Form
