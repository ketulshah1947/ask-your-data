import React, { useState, useEffect } from 'react';
// import './App.css';

function App() {
    const [query, setQuery] = useState('');
    const [sql, setSql] = useState('SELECT * FROM orders LIMIT 10;');
    const [data, setData] = useState<string[]>([]);

    useEffect(() => {
        fetch("http://localhost:8000/sample-query")
            .then(res => res.json())
            .then(setData);
    }, []);

    return (
        <div className="App">
            <h1>Ask Your Data</h1>
            <input
                type="text"
                value={query}
                onChange={e => setQuery(e.target.value)}
                placeholder="Ask a question..."
            />
            <textarea
                value={sql}
                onChange={e => setSql(e.target.value)}
                rows={4}
                cols={50}
            />
            <h2>Results</h2>
            <table>
                <thead>
                    <tr>{data.length > 0 && Object.keys(data[0]).map(col => <th key={col}>{col}</th>)}</tr>
                </thead>
                <tbody>
                    {data.map((row, idx) => (
                        <tr key={idx}>{Object.values(row).map((val, i) => <td key={i}>{val}</td>)}</tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default App;