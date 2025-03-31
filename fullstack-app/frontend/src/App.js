import React, { useEffect, useState } from 'react';

function App() {
    const [message, setMessage] = useState('');
    const [dbMessage, setDbMessage] = useState('');

    useEffect(() => {
        // Fetch data from Flask backend
        fetch('http://localhost:5000/')
            .then(res => res.json())
            .then(data => setMessage(data.message))
            .catch(error => console.error("Error fetching data:", error));  // Error handling

        // Fetch data from PostgreSQL via Flask
        fetch('http://localhost:5000/data')
            .then(res => res.json())
            .then(data => setDbMessage(data.database_message))
            .catch(error => console.error("Error fetching database message:", error));  // Error handling
    }, []);

    return (
        <div style={{ textAlign: 'center', marginTop: '50px', fontFamily: 'Arial, sans-serif' }}>
            <h1 style={{ color: '#007BFF' }}>🌍 Fullstack App</h1>
            <div style={{ background: '#f8f9fa', padding: '20px', borderRadius: '10px', boxShadow: '0px 4px 6px rgba(0, 0, 0, 0.1)', display: 'inline-block' }}>
                <p style={{ fontSize: '18px', fontWeight: 'bold' }}>Backend Mesajı:</p>
                <p style={{ color: '#28a745', fontSize: '16px' }}>{message}</p>
                <hr style={{ width: '80%', margin: '10px auto', borderTop: '1px solid #ccc' }} />
                <p style={{ fontSize: '18px', fontWeight: 'bold' }}>Database Mesajı:</p>
                <p style={{ color: '#dc3545', fontSize: '16px' }}>{dbMessage}</p>
            </div>
        </div>
    );
}

export default App;
