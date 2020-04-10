import React from 'react'

const DataCheck = (data) => (
  <pre
    style={{
      padding: '20px',
      backgroundColor: 'lightgrey',
      fontSize: '20px',
    }}
  >
    {JSON.stringify(data, null, 2)}
  </pre>
)

export default DataCheck
