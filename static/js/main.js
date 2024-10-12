document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatMessages = document.getElementById('chat-messages');
    const codePreview = document.getElementById('code-preview');
    const projectNameInput = document.getElementById('project-name');

    chatForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const message = chatInput.value.trim();
        const projectName = projectNameInput.value.trim();

        if (message && projectName) {
            addMessage('user', message);
            generateCode(message, projectName);
            chatInput.value = '';
        }
    });

    function addMessage(sender, content) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', sender);
        messageElement.textContent = content;
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function generateCode(prompt, projectName) {
        fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt, project_name: projectName }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                addMessage('bot', 'Code generated successfully. Check the preview below.');
                // In a real implementation, you'd update the code preview here
                codePreview.textContent = 'Generated code would be displayed here.';
            } else {
                addMessage('bot', 'Error generating code. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            addMessage('bot', 'An error occurred. Please try again later.');
        });
    }
});
