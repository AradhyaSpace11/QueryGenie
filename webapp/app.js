document.getElementById('submitQuery').addEventListener('click', async () => {
    const query = document.getElementById('queryInput').value;
    if (!query.trim()) {
        alert('Please enter a query.');
        return;
    }

    // Clear previous results
    document.getElementById('relevantInfo').textContent = 'Loading...';
    document.getElementById('aiResponse').textContent = '';

    try {
        // Send query to backend API
        const response = await fetch('/api/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query }),
        });

        if (response.ok) {
            const data = await response.json();
            document.getElementById('relevantInfo').textContent = data.relevantInfo;
            document.getElementById('aiResponse').textContent = data.aiResponse;
        } else {
            document.getElementById('relevantInfo').textContent = 'Error retrieving information.';
            document.getElementById('aiResponse').textContent = '';
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('relevantInfo').textContent = 'An error occurred. Please try again.';
        document.getElementById('aiResponse').textContent = '';
    }
});
