document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('code-generator-form');
    const codeContainer = document.getElementById('generated-code');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const projectDescription = document.getElementById('project-description').value;

        try {
            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ project_description: projectDescription }),
            });

            if (!response.ok) {
                throw new Error('Failed to generate code');
            }

            const data = await response.json();
            codeContainer.textContent = data.code;
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while generating code. Please try again.');
        }
    });
});
