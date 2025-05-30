import { Answer, Vote } from "./types";

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:8000";


export const askQuestion = async (question: string): Promise<Answer> => {
    const res = await fetch(`${API_BASE_URL}/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question })
    });
    if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.detail || 'Failed to generate SQL');
    }
    const response = await res.json();
    if (response.error) {
        throw new Error(`SQL generation faced an error: ${response.error}. SQL: ${response.sql}`);
    }
    return { data: response.results, sql: response.sql };
};

export const submitFeedback = async (question: string, sql: string, vote: Vote) => {
    await fetch(`${API_BASE_URL}/feedback`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question, generated_sql: sql, feedback: vote })
    });
};