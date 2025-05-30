import React, { useState } from 'react';
import { QueryResult, Vote } from './types';
import { askQuestion, submitFeedback } from './api';
import './App.css';

const App: React.FC = () => {
    const [question, setQuestion] = useState<string>('');
    const [sql, setSql] = useState<string>('');
    const [results, setResults] = useState<QueryResult[]>([]);
    const [feedback, setFeedback] = useState<'up' | 'down' | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);


    const handleQuestion = (question: string) => {
        setLoading(true);
        setError(null);
        setResults([]);
        setSql('');
        setFeedback(null);
        askQuestion(question).then(response => {
            setSql(response.sql);
            setResults(response.data);
        }).catch(error => {
            setError(error.message || 'Unexpected error occurred');
        })
            .finally(() => setLoading(false))
    }

    const handleFeedback = (vote: Vote) => {
        submitFeedback(question, sql, vote).then(response => {
            console.log("Feedback submitted.")
        }).catch(error => {
            console.error(`Feedback submission failed with an error: ${error}`)
        })
    }


    return (
        <div className="app">
            <h1>Ask Your Data</h1>
            <input
                className="question-input"
                type="text"
                value={question}
                onChange={e => setQuestion(e.target.value)}
                placeholder="Ask a question..."
            />
            <button onClick={() => { handleQuestion(question) }}>Generate SQL</button>
            {loading && (<progress />)}
            {error && (<p color='#ff0000'>{error}</p>)}

            {sql && (
                <div className="section">
                    <h3>Generated SQL</h3>
                    <textarea
                        rows={4}
                        cols={80}
                        value={sql}
                        onChange={e => setSql(e.target.value)}
                    />
                </div>
            )}
            <div className="section">
                {results.length > 0 && (
                    <div>
                        <h3>Query Results</h3>
                        <table>
                            <thead>
                                <tr>{Object.keys(results[0]).map((col, i) => <th key={i}>{col}</th>)}</tr>
                            </thead>
                            <tbody>
                                {results.map((row, idx) => (
                                    <tr key={idx}>{Object.values(row).map((val, i) => <td key={i}>{val}</td>)}</tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
                {sql && (
                    <div className="feedback">
                        <button onClick={() => handleFeedback(Vote.UP)} disabled={feedback === 'up'}>👍</button>
                        <button onClick={() => handleFeedback(Vote.UP)} disabled={feedback === 'down'}>👎</button>
                    </div>
                )}
            </div>
        </div>
    );
};

export default App;