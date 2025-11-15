import React from 'react';
import { useState, useEffect } from 'react';
import { MCQChallenge } from '../challenge/MCQChallenge.jsx';
import { useApi } from '../utils/api.js';

export function HistoryPanel() {
    const [history, setHistory] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const { makeRequest } = useApi();

    const fetchHistory = async () => {
        setIsLoading(true);
        setError(null);
        try {
            const data = await makeRequest('challenges/my-history');
            setHistory(data.challenges);
        } catch (err) {
            setError('Failed to fetch history.');
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        fetchHistory();
    }, []);

    if (isLoading) {
        return (
            <div className="loading">
                <p>Loading history...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div>
                <p>Error loading history: {error}</p>
                <button onClick={fetchHistory}>Retry</button>
            </div>
        );
    }

    return (
        <div className='history-panel'>
            <h2>Challenge History</h2>
            {history.length === 0 ? (
                <p>No history available.</p>
            ) : (
                <div className='history-list'>
                    {history.map((challenge) => (
                        <MCQChallenge key={challenge.id} challenge={challenge} showExplanation={true} />
                    ))}
                </div>
            )}
        </div>
    );
}
