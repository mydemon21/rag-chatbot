let docCount = 0;
let chunkCount = 0;

function addMessage(content, isUser, sources = []) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;
    
    let html = isUser ? content : `<i class="fas fa-robot" style="margin-right: 0.5rem;"></i>${content}`;
    if (sources && sources.length > 0) {
        html += `<div class="sources"><i class="fas fa-file-alt"></i> Sources: ${sources.join(', ')}</div>`;
    }
    messageDiv.innerHTML = html;
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showTyping() {
    document.getElementById('typingIndicator').style.display = 'block';
    const chatMessages = document.getElementById('chatMessages');
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function hideTyping() {
    document.getElementById('typingIndicator').style.display = 'none';
}

async function sendMessage() {
    const input = document.getElementById('messageInput');
    const query = input.value.trim();
    if (!query) return;
    
    addMessage(query, true);
    input.value = '';
    showTyping();
    
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query })
        });
        
        const data = await response.json();
        hideTyping();
        addMessage(data.answer, false, data.sources);
    } catch (error) {
        hideTyping();
        addMessage('❌ Error: ' + error.message, false);
    }
}

async function uploadFiles() {
    const fileInput = document.getElementById('fileInput');
    const files = fileInput.files;
    
    if (files.length === 0) return;
    
    for (let file of files) {
        const formData = new FormData();
        formData.append('file', file);
        
        try {
            showTyping();
            const response = await fetch('/ingest', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            hideTyping();
            addMessage(`✅ ${data.message}`, false);
            docCount++;
            updateStats();
        } catch (error) {
            hideTyping();
            addMessage(`❌ Error uploading ${file.name}: ${error.message}`, false);
        }
    }
    
    fileInput.value = '';
}

async function ingestFolder() {
    try {
        showTyping();
        const response = await fetch('/ingest_folder', { method: 'POST' });
        const data = await response.json();
        hideTyping();
        addMessage(`✅ ${data.message}`, false);
        
        // Extract chunk count from message
        const match = data.message.match(/(\d+) chunks/);
        if (match) {
            chunkCount += parseInt(match[1]);
            updateStats();
        }
    } catch (error) {
        hideTyping();
        addMessage('❌ Error: ' + error.message, false);
    }
}

function clearChat() {
    const chatMessages = document.getElementById('chatMessages');
    chatMessages.innerHTML = `
        <div class="message bot">
            <i class="fas fa-robot" style="margin-right: 0.5rem;"></i>
            Hello! I'm your AI document assistant. Upload some documents and start asking questions about them.
        </div>
    `;
}

function updateStats() {
    document.getElementById('docCount').textContent = docCount;
    document.getElementById('chunkCount').textContent = chunkCount;
}

function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

// File upload handler
document.getElementById('fileInput').addEventListener('change', uploadFiles);

// Auto-resize input
document.getElementById('messageInput').addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 120) + 'px';
});

// Welcome animation
window.addEventListener('load', function() {
    setTimeout(() => {
        addMessage('💡 Tip: Upload documents using the sidebar or drag & drop files here!', false);
    }, 2000);
});