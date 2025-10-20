"""
Web UI for AI Text Assistant using Flask
=========================================
Provides a user-friendly web interface for the AI assistant.

Features:
- Real-time chat interface
- Mode switching
- Chat history visualization
- Settings configuration
- Export/import chat history

Author: Contributed for Hacktoberfest 2025
"""

from flask import Flask, render_template, request, jsonify, send_file, session
from flask_cors import CORS
import os
import secrets
from datetime import datetime
from pathlib import Path

from ai_assistant import AIAssistant
from config import Config
from chat_history import ChatHistory

# Initialize Flask app
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
CORS(app)

# Initialize components
config = Config()
try:
    assistant = AIAssistant(config)
except (ValueError, ImportError) as e:
    print(f"Warning: AI assistant initialization failed: {e}")
    print("Web UI will start but AI features may not work without valid API keys.")
    assistant = None
history = ChatHistory()

@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Handle chat requests
    
    Expected JSON:
        {
            "message": "user message",
            "mode": "chat|summarize|translate|ideas|code"
        }
    
    Returns:
        {
            "response": "AI response",
            "mode": "current mode",
            "timestamp": "ISO timestamp"
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({"error": "No message provided"}), 400
        
        if not assistant:
            return jsonify({"error": "AI assistant not initialized. Please configure API keys."}), 503
        
        user_message = data['message']
        mode = data.get('mode', 'chat')
        
        # Generate AI response
        response = assistant.generate_response(user_message, mode=mode)
        
        # Save to history
        history.add_entry(user_message, response, mode=mode)
        
        return jsonify({
            "response": response,
            "mode": mode,
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    """
    Get chat history
    
    Query params:
        limit: Maximum number of entries to return
    
    Returns:
        {
            "history": [...],
            "total": number
        }
    """
    try:
        limit = request.args.get('limit', type=int)
        history_data = history.get_history(limit=limit)
        
        return jsonify({
            "history": history_data,
            "total": len(history)
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/history/clear', methods=['POST'])
def clear_history():
    """Clear chat history"""
    try:
        history.clear_history()
        return jsonify({"success": True, "message": "History cleared"})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/history/export', methods=['GET'])
def export_history():
    """
    Export chat history as JSON file
    
    Returns:
        File download
    """
    try:
        filename = f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = history.history_dir / filename
        
        if history.save_to_file(filename):
            return send_file(filepath, as_attachment=True, download_name=filename)
        else:
            return jsonify({"error": "Failed to export history"}), 500
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/history/import', methods=['POST'])
def import_history():
    """
    Import chat history from JSON file
    
    Expected: multipart/form-data with 'file' field
    
    Returns:
        {
            "success": true,
            "message": "...",
            "entries": number
        }
    """
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Save uploaded file
        filename = f"import_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = history.history_dir / filename
        file.save(filepath)
        
        # Load history
        if history.load_from_file(filename):
            return jsonify({
                "success": True,
                "message": "History imported successfully",
                "entries": len(history)
            })
        else:
            return jsonify({"error": "Failed to import history"}), 500
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/config', methods=['GET'])
def get_config():
    """
    Get current configuration (excluding sensitive data)
    
    Returns:
        {
            "provider": "...",
            "model": "...",
            "temperature": 0.7,
            "max_tokens": 1000,
            ...
        }
    """
    try:
        config_dict = config.to_dict()
        
        # Remove sensitive information
        safe_config = {k: v for k, v in config_dict.items() 
                      if 'key' not in k.lower() and 'secret' not in k.lower()}
        
        return jsonify(safe_config)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/config', methods=['POST'])
def update_config():
    """
    Update configuration
    
    Expected JSON:
        {
            "temperature": 0.8,
            "max_tokens": 1500,
            ...
        }
    
    Returns:
        {
            "success": true,
            "message": "...",
            "config": {...}
        }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Update configuration
        config.update_from_dict(data)
        
        # Validate
        is_valid, error = config.validate()
        if not is_valid:
            return jsonify({"error": f"Invalid configuration: {error}"}), 400
        
        return jsonify({
            "success": True,
            "message": "Configuration updated",
            "config": config.to_dict()
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """
    Get chat statistics
    
    Returns:
        {
            "total_messages": number,
            "modes_used": {...},
            "first_message": "...",
            "last_message": "...",
            ...
        }
    """
    try:
        stats = history.get_statistics()
        return jsonify(stats)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/search', methods=['POST'])
def search_history():
    """
    Search chat history
    
    Expected JSON:
        {
            "query": "search term",
            "case_sensitive": false
        }
    
    Returns:
        {
            "results": [...],
            "count": number
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({"error": "No query provided"}), 400
        
        query = data['query']
        case_sensitive = data.get('case_sensitive', False)
        
        results = history.search_history(query, case_sensitive=case_sensitive)
        
        return jsonify({
            "results": results,
            "count": len(results)
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    return jsonify({"error": "Internal server error"}), 500

def create_templates():
    """Create templates directory and HTML file"""
    templates_dir = Path("templates")
    templates_dir.mkdir(exist_ok=True)
    
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Text Assistant</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .chat-container { max-width: 1000px; margin: 50px auto; background: white; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); }
        .chat-header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 15px 15px 0 0; }
        .chat-body { height: 500px; overflow-y: auto; padding: 20px; background: #f8f9fa; }
        .message { margin-bottom: 15px; padding: 10px 15px; border-radius: 10px; max-width: 80%; }
        .user-message { background: #007bff; color: white; margin-left: auto; text-align: right; }
        .ai-message { background: #e9ecef; color: #333; }
        .chat-input { padding: 20px; border-top: 1px solid #dee2e6; }
        .mode-badge { cursor: pointer; transition: all 0.3s; }
        .mode-badge:hover { transform: scale(1.1); }
        .mode-badge.active { background: #28a745 !important; }
    </style>
</head>
<body>
    <div class="container">
        <div class="chat-container">
            <div class="chat-header">
                <h2 class="mb-0"><i class="fas fa-robot"></i> AI Text Assistant</h2>
                <p class="mb-0">Your intelligent companion for text generation</p>
            </div>
            
            <div class="p-3 border-bottom">
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <span class="badge bg-primary mode-badge active me-2" data-mode="chat">💬 Chat</span>
                        <span class="badge bg-secondary mode-badge me-2" data-mode="summarize">📝 Summarize</span>
                        <span class="badge bg-secondary mode-badge me-2" data-mode="translate">🌐 Translate</span>
                        <span class="badge bg-secondary mode-badge me-2" data-mode="ideas">💡 Ideas</span>
                        <span class="badge bg-secondary mode-badge" data-mode="code">💻 Code</span>
                    </div>
                    <div>
                        <button class="btn btn-sm btn-outline-danger" onclick="clearHistory()">
                            <i class="fas fa-trash"></i> Clear
                        </button>
                        <button class="btn btn-sm btn-outline-primary" onclick="exportHistory()">
                            <i class="fas fa-download"></i> Export
                        </button>
                    </div>
                </div>
            </div>
            
            <div class="chat-body" id="chatBody">
                <div class="text-center text-muted">
                    <i class="fas fa-comments fa-3x mb-3"></i>
                    <p>Start a conversation with the AI assistant!</p>
                </div>
            </div>
            
            <div class="chat-input">
                <form id="chatForm">
                    <div class="input-group">
                        <input type="text" class="form-control" id="userInput" placeholder="Type your message..." required>
                        <button class="btn btn-primary" type="submit">
                            <i class="fas fa-paper-plane"></i> Send
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>

    <script>
        let currentMode = 'chat';
        
        // Mode switching
        document.querySelectorAll('.mode-badge').forEach(badge => {
            badge.addEventListener('click', function() {
                document.querySelectorAll('.mode-badge').forEach(b => {
                    b.classList.remove('active', 'bg-primary');
                    b.classList.add('bg-secondary');
                });
                this.classList.remove('bg-secondary');
                this.classList.add('active', 'bg-primary');
                currentMode = this.dataset.mode;
            });
        });
        
        // Chat form submission
        document.getElementById('chatForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const userInput = document.getElementById('userInput');
            const message = userInput.value.trim();
            
            if (!message) return;
            
            // Add user message
            addMessage(message, 'user');
            userInput.value = '';
            
            // Show loading
            const loadingId = addMessage('Thinking...', 'ai');
            
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message, mode: currentMode })
                });
                
                const data = await response.json();
                
                // Remove loading, add response
                document.getElementById(loadingId).remove();
                addMessage(data.response, 'ai');
                
            } catch (error) {
                document.getElementById(loadingId).remove();
                addMessage('Error: ' + error.message, 'ai');
            }
        });
        
        function addMessage(text, type) {
            const chatBody = document.getElementById('chatBody');
            const messageDiv = document.createElement('div');
            const id = 'msg-' + Date.now();
            messageDiv.id = id;
            messageDiv.className = 'message ' + (type === 'user' ? 'user-message' : 'ai-message');
            messageDiv.textContent = text;
            chatBody.appendChild(messageDiv);
            chatBody.scrollTop = chatBody.scrollHeight;
            return id;
        }
        
        async function clearHistory() {
            if (!confirm('Clear all chat history?')) return;
            
            try {
                await fetch('/api/history/clear', { method: 'POST' });
                document.getElementById('chatBody').innerHTML = '<div class="text-center text-muted"><i class="fas fa-comments fa-3x mb-3"></i><p>History cleared. Start a new conversation!</p></div>';
            } catch (error) {
                alert('Error clearing history: ' + error.message);
            }
        }
        
        async function exportHistory() {
            try {
                const response = await fetch('/api/history/export');
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'chat_history.json';
                a.click();
            } catch (error) {
                alert('Error exporting history: ' + error.message);
            }
        }
        
        // Load history on page load
        window.addEventListener('load', async function() {
            try {
                const response = await fetch('/api/history?limit=20');
                const data = await response.json();
                
                if (data.history && data.history.length > 0) {
                    document.getElementById('chatBody').innerHTML = '';
                    data.history.forEach(entry => {
                        addMessage(entry.user, 'user');
                        addMessage(entry.assistant, 'ai');
                    });
                }
            } catch (error) {
                console.error('Error loading history:', error);
            }
        });
    </script>
</body>
</html>"""
    
    with open(templates_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

def main():
    """Run the Flask web server"""
    # Create templates if they don't exist
    create_templates()
    
    # Run server
    print("\n" + "=" * 60)
    print("🤖 AI Text Assistant Web UI")
    print("=" * 60)
    print(f"\n🌐 Server starting on http://{config.web_host}:{config.web_port}")
    print("\n💡 Press Ctrl+C to stop the server\n")
    
    app.run(
        host=config.web_host,
        port=config.web_port,
        debug=config.debug_mode
    )

if __name__ == "__main__":
    main()
