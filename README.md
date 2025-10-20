# 🤖 AI Text Assistant (Python + Gen AI)# AI-Text-Assistant-Python



[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)# 🤖 AI Text Assistant (Python + Gen AI)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[![Hacktoberfest](https://img.shields.io/badge/Hacktoberfest-2025-orange.svg)](https://hacktoberfest.com/)A beginner-friendly **Python + Gen AI** project for **Hacktoberfest**!  

This simple command-line chatbot uses an AI model (OpenAI or Hugging Face API) to generate responses for your prompts.  

A comprehensive **Python + Generative AI** project for **Hacktoberfest 2025**!  

This intelligent assistant uses advanced AI models (OpenAI, Hugging Face, or Ollama) to provide versatile text generation capabilities through both CLI and Web interfaces.You can chat, generate ideas, write content, or even add your own AI-powered features! 🌟  



Chat, summarize, translate, generate ideas, get coding help, and more - all powered by state-of-the-art AI! 🌟---



---## ✨ Features

- 🧠 Ask anything and get AI-powered responses  

## ✨ Features- 💬 Simple CLI interface, if possible then you can add web UI 

- 💾 Saves chat history locally  

### 🎯 Multiple AI Modes- ⚙️ Customizable temperature/creativity level  

- **💬 Chat** - Natural conversation with context awareness- 🧩 Extendable — add new modes (summarizer, translator, idea generator, etc.)

- **📝 Summarize** - Intelligent text summarization with key points

- **🌐 Translate** - Multi-language translation with context preservation---

- **💡 Ideas** - Creative idea generation and brainstorming

- **💻 Code** - Programming assistance and code generation## 🚀 Getting Started



### 🔧 Powerful Capabilities### 1️⃣ Clone this repository

- 🤖 **Multi-Provider Support** - OpenAI, Hugging Face, Ollama (local models)```bash

- 🖥️ **Dual Interface** - Beautiful CLI and modern Web UIgit clone https://github.com/<your-username>/ai-text-assistant.git

- 💾 **Smart History** - Automatic chat history with search and export
- ⚙️ **Highly Configurable** - Temperature, tokens, models, and more
- 📊 **Usage Statistics** - Track your interactions and patterns
- 🔒 **Privacy-Focused** - Local storage, no data collection

### 🎨 User Experience
- Beautiful colored CLI with emoji indicators
- Responsive web interface with real-time updates
- Keyboard shortcuts and intuitive commands
- Export/import chat sessions
- Full conversation context

---

## 🚀 Quick Start

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/vatsalgupta2004/AI-Text-Assistant-Python.git
cd AI-Text-Assistant-Python
```

### 2️⃣ Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure API Keys
```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your API keys
# For OpenAI: Get key from https://platform.openai.com/api-keys
# For Hugging Face: Get key from https://huggingface.co/settings/tokens
```

Example `.env` configuration:
```env
AI_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here
TEMPERATURE=0.7
MAX_TOKENS=1000
```

### 5️⃣ Run the Application

**CLI Interface:**
```bash
python main.py
```

**Web Interface:**
```bash
python web_ui.py
# Open browser to http://127.0.0.1:5000
```

---

## 📖 Usage Guide

### CLI Commands

Once you start the CLI interface, you can use these commands:

| Command | Description | Example |
|---------|-------------|---------|
| `/help` | Show all available commands | `/help` |
| `/mode <mode>` | Switch AI mode | `/mode summarize` |
| `/history` | View chat history | `/history` |
| `/clear` | Clear chat history | `/clear` |
| `/save <file>` | Save history to file | `/save my_chat.json` |
| `/load <file>` | Load history from file | `/load my_chat.json` |
| `/config` | Show current configuration | `/config` |
| `/temperature <val>` | Set temperature (0.0-2.0) | `/temperature 0.9` |
| `/tokens <num>` | Set max tokens | `/tokens 1500` |
| `/provider <name>` | Switch provider | `/provider huggingface` |
| `/quit` or `/exit` | Exit application | `/quit` |

### CLI Mode Examples

**Chat Mode (Default):**
```
You [chat]: Tell me about artificial intelligence
🤖 AI Assistant: Artificial intelligence (AI) refers to...
```

**Summarize Mode:**
```
You [summarize]: Summarize this article: [paste long text]
🤖 AI Assistant: Key Points:
• Main idea 1
• Main idea 2
...
```

**Translate Mode:**
```
You [translate]: Translate "Hello, how are you?" to Spanish
🤖 AI Assistant: "Hola, ¿cómo estás?"
```

**Ideas Mode:**
```
You [ideas]: Give me startup ideas for sustainable fashion
🤖 AI Assistant: Here are innovative ideas:
1. Clothing rental subscription service...
```

**Code Mode:**
```
You [code]: Write a Python function to calculate fibonacci numbers
🤖 AI Assistant: Here's an optimized implementation...
```

### Web Interface

The web UI provides:
- Real-time chat interface
- Mode switching with visual indicators
- Chat history visualization
- Export/import functionality
- Configuration panel
- Search capabilities

Access at: `http://127.0.0.1:5000` after running `python web_ui.py`

---

## 🔧 Configuration

### AI Providers

**1. OpenAI (Recommended for beginners)**
```env
AI_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here
AI_MODEL=gpt-3.5-turbo  # or gpt-4
```

**2. Hugging Face (Free tier available)**
```env
AI_PROVIDER=huggingface
HUGGINGFACE_API_KEY=hf_your-key-here
AI_MODEL=mistralai/Mistral-7B-Instruct-v0.2
```

**3. Ollama (Local, no API key needed)**
```env
AI_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
AI_MODEL=llama2
```

For Ollama, first install Ollama from [ollama.ai](https://ollama.ai) and run:
```bash
ollama pull llama2
```

### Generation Parameters

- **Temperature** (0.0 - 2.0): Controls creativity
  - `0.0-0.3`: Focused, deterministic
  - `0.4-0.7`: Balanced (recommended)
  - `0.8-2.0`: Creative, varied

- **Max Tokens**: Maximum response length
  - `500-1000`: Short responses
  - `1000-2000`: Medium responses
  - `2000+`: Long, detailed responses

---

## 📁 Project Structure

```
AI-Text-Assistant-Python/
├── main.py              # CLI application entry point
├── web_ui.py            # Web interface server
├── ai_assistant.py      # Core AI logic and providers
├── config.py            # Configuration management
├── chat_history.py      # History management
├── requirements.txt     # Python dependencies
├── .env.example         # Environment template
├── .gitignore          # Git ignore rules
├── README.md           # This file
├── CONTRIBUTING.md     # Contribution guidelines
├── LICENSE             # MIT License
├── templates/          # Web UI templates
│   └── index.html
└── chat_history/       # Saved chat sessions (auto-created)
```

---

## 🤝 Contributing

We love contributions! This project is perfect for:
- 🆕 First-time contributors
- 🎃 Hacktoberfest participants
- 🐍 Python enthusiasts
- 🤖 AI/ML learners

### Ways to Contribute

1. **Add new AI modes** (sentiment analysis, content generation)
2. **Improve UI/UX** (better styling, animations)
3. **Add features** (voice input, file upload)
4. **Fix bugs** (check issues tab)
5. **Improve documentation** (tutorials, examples)
6. **Add tests** (unit tests, integration tests)
7. **Optimize performance** (caching, async operations)

### Contribution Steps

1. **Fork** the repository
2. **Clone** your fork
   ```bash
   git clone https://github.com/YOUR_USERNAME/AI-Text-Assistant-Python.git
   ```
3. **Create a branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
4. **Make changes** and test thoroughly
5. **Commit** with clear messages
   ```bash
   git commit -m "Add: Amazing new feature"
   ```
6. **Push** to your fork
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request** with detailed description

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 🐛 Troubleshooting

### Common Issues

**1. API Key Errors**
```
Error: OPENAI_API_KEY not found
```
**Solution:** Make sure you created `.env` file and added your API key.

**2. Import Errors**
```
ModuleNotFoundError: No module named 'openai'
```
**Solution:** Install dependencies: `pip install -r requirements.txt`

**3. Ollama Connection Error**
```
Error: Ollama API error: Connection refused
```
**Solution:** Make sure Ollama is running: `ollama serve`

**4. Rate Limiting**
```
Error: Rate limit exceeded
```
**Solution:** Wait a moment or switch to different provider/model.

---

## 📚 Advanced Usage

### Command-Line Arguments

```bash
# Start with specific provider
python main.py --provider huggingface

# Start in specific mode
python main.py --mode code

# Set temperature
python main.py --temperature 0.9

# Combine arguments
python main.py --provider ollama --mode ideas --temperature 1.2
```

### Programmatic Usage

```python
from ai_assistant import AIAssistant
from config import Config

# Initialize
config = Config()
config.provider = "openai"
assistant = AIAssistant(config)

# Generate response
response = assistant.generate_response(
    "Explain quantum computing",
    mode="chat"
)
print(response)
```

### Batch Processing

```python
from ai_assistant import AIAssistant
from config import Config

config = Config()
assistant = AIAssistant(config)

# Process multiple texts
texts = ["Text 1...", "Text 2...", "Text 3..."]
summaries = []

for text in texts:
    summary = assistant.generate_response(text, mode="summarize")
    summaries.append(summary)
```

---

## 🎓 Learning Resources

### For Beginners
- [Python Basics](https://docs.python.org/3/tutorial/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Hugging Face Hub](https://huggingface.co/docs/hub)

### Advanced Topics
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [LangChain Documentation](https://python.langchain.com/)
- [Flask Web Development](https://flask.palletsprojects.com/)

---

## 📊 Features Roadmap

- [ ] Voice input/output support
- [ ] Image generation capabilities
- [ ] Multi-user sessions
- [ ] API endpoint for integration
- [ ] Docker containerization
- [ ] Database storage for history
- [ ] Authentication system
- [ ] Plugin architecture
- [ ] Mobile app (React Native)
- [ ] Real-time collaboration

---

## 🌟 Examples

### Example 1: Content Creation
```
Mode: Ideas
Input: "Content ideas for a tech blog"
Output: 
1. "The Future of AI in Healthcare" - Explore how AI is revolutionizing...
2. "Quantum Computing Explained Simply" - Break down complex concepts...
3. "Sustainable Tech: Green Computing Solutions" - Discuss eco-friendly...
```

### Example 2: Code Assistant
```
Mode: Code
Input: "Create a REST API with Flask"
Output:
from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({"message": "Hello, API!"})
...
```

### Example 3: Learning Aid
```
Mode: Summarize
Input: [Paste research paper]
Output:
Key Findings:
• The study examined X with sample size Y
• Results showed significant correlation (p < 0.05)
• Implications for Z industry
• Limitations: A, B, C
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Vatsal Gupta**
- GitHub: [@vatsalgupta2004](https://github.com/vatsalgupta2004)
- Contribution: Hacktoberfest 2025

---

## 🙏 Acknowledgments

- OpenAI for GPT models
- Hugging Face for model hosting
- Ollama for local model support
- Flask for web framework
- Colorama for terminal colors
- All contributors and Hacktoberfest participants!

---

## 📞 Support

- 🐛 [Report Bug](https://github.com/vatsalgupta2004/AI-Text-Assistant-Python/issues)
- 💡 [Request Feature](https://github.com/vatsalgupta2004/AI-Text-Assistant-Python/issues)
- 💬 [Discussions](https://github.com/vatsalgupta2004/AI-Text-Assistant-Python/discussions)

---

## ⭐ Star History

If you find this project useful, please consider giving it a star! ⭐

---

**Happy Coding! 🚀** Made with ❤️ for Hacktoberfest 2025
