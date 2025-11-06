import { useState, useEffect, useRef } from 'react';

/**
 * Custom hook for streaming task status via Server-Sent Events (SSE).
 *
 * Automatically connects to SSE endpoint and updates state in real-time.
 * Handles connection lifecycle, cleanup, and error recovery.
 *
 * @param {string} taskId - Celery task ID to monitor
 * @returns {{status: string, result: any, error: string, isConnected: boolean}}
 *
 * @example
 * const { status, result, error, isConnected } = useTaskStream(taskId);
 *
 * if (status === 'SUCCESS') {
 *   console.log('Task completed:', result);
 * }
 */
export function useTaskStream(taskId) {
  const [status, setStatus] = useState('PENDING');
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [isConnected, setIsConnected] = useState(false);

  // Store EventSource in ref to avoid recreating on re-renders
  const eventSourceRef = useRef(null);

  useEffect(() => {
    if (!taskId) {
      return;
    }

    // Get API base URL from environment or default
    const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    const streamUrl = `${API_BASE}/api/async/tasks/${taskId}/stream`;

    console.log(`[useTaskStream] Connecting to SSE: ${streamUrl}`);

    // Create EventSource connection
    const eventSource = new EventSource(streamUrl);
    eventSourceRef.current = eventSource;

    // Handle incoming messages
    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log(`[useTaskStream] Received update:`, data);

        setStatus(data.state);
        setIsConnected(true);

        // Handle SUCCESS state
        if (data.state === 'SUCCESS' && data.result) {
          setResult(data.result);
          setError(null);
          eventSource.close();
          console.log(`[useTaskStream] Task completed successfully`);
        }

        // Handle FAILURE state
        if (data.state === 'FAILURE') {
          setError(data.error || 'Task failed');
          setResult(null);
          eventSource.close();
          console.error(`[useTaskStream] Task failed:`, data.error);
        }
      } catch (err) {
        console.error('[useTaskStream] Error parsing SSE message:', err);
      }
    };

    // Handle connection open
    eventSource.onopen = () => {
      console.log(`[useTaskStream] SSE connection opened`);
      setIsConnected(true);
    };

    // Handle errors
    eventSource.onerror = (err) => {
      console.error('[useTaskStream] SSE connection error:', err);
      setIsConnected(false);

      // Close connection on error
      eventSource.close();

      // Set error state if not already complete
      if (status !== 'SUCCESS' && status !== 'FAILURE') {
        setError('Connection lost. Please refresh to check task status.');
      }
    };

    // Cleanup function - close connection when component unmounts or taskId changes
    return () => {
      console.log(`[useTaskStream] Cleaning up SSE connection`);
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
        eventSourceRef.current = null;
      }
      setIsConnected(false);
    };
  }, [taskId]);

  return {
    status,
    result,
    error,
    isConnected
  };
}

export default useTaskStream;
