"""
AI Text Assistant - Main CLI Application
==========================================
A powerful command-line AI assistant with multiple modes and AI provider support.

Features:
- Multiple AI providers (OpenAI, Hugging Face, Ollama)
- Various modes: Chat, Summarize, Translate, Ideas, Code Help
- Chat history management
- Customizable parameters (temperature, max tokens)
- Beautiful CLI interface

Author: Contributed for Hacktoberfest 2025
"""

import os
import sys
import json
from datetime import datetime
from typing import Optional, Dict, Any
import argparse

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False
    
from ai_assistant import AIAssistant
from config import Config
from chat_history import ChatHistory

class AITextAssistantCLI:
    """Main CLI application for AI Text Assistant"""
    
    def __init__(self):
        """Initialize the CLI application"""
        self.config = Config()
        self.assistant = AIAssistant(self.config)
        self.history = ChatHistory()
        self.current_mode = "chat"
        self.running = True
        
    def print_colored(self, text: str, color: str = "white") -> None:
        """Print colored text if colorama is available"""
        if COLORS_AVAILABLE:
            color_map = {
                "red": Fore.RED,
                "green": Fore.GREEN,
                "yellow": Fore.YELLOW,
                "blue": Fore.BLUE,
                "magenta": Fore.MAGENTA,
                "cyan": Fore.CYAN,
                "white": Fore.WHITE,
            }
            print(f"{color_map.get(color, Fore.WHITE)}{text}{Style.RESET_ALL}")
        else:
            print(text)
    
    def print_banner(self) -> None:
        """Print application banner"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║              🤖 AI Text Assistant v1.0                       ║
║                                                              ║
║       Your Intelligent Companion for Text Generation        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """
        self.print_colored(banner, "cyan")
        
    def print_help(self) -> None:
        """Print help information"""
        help_text = """
📚 Available Commands:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 Chat Commands:
  /help              - Show this help message
  /mode <mode>       - Change AI mode (chat, summarize, translate, ideas, code)
  /history           - Show chat history
  /clear             - Clear chat history
  /save <filename>   - Save chat history to file
  /load <filename>   - Load chat history from file
  /config            - Show current configuration
  /temperature <val> - Set temperature (0.0-2.0)
  /tokens <num>      - Set max tokens
  /provider <name>   - Switch AI provider (openai, huggingface, ollama)
  /quit or /exit     - Exit the application

🎯 AI Modes:
  chat      - General conversation (default)
  summarize - Summarize long texts
  translate - Translate between languages
  ideas     - Generate creative ideas
  code      - Programming help and code generation

💡 Tips:
  - Type your message and press Enter to chat
  - Use /mode to switch between different AI capabilities
  - Adjust temperature for more creative (higher) or focused (lower) responses
  - Chat history is automatically saved

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """
        self.print_colored(help_text, "yellow")
    
    def print_status(self) -> None:
        """Print current status"""
        status = f"""
📊 Current Status:
  Mode: {self.current_mode}
  Provider: {self.config.provider}
  Model: {self.config.get_model()}
  Temperature: {self.config.temperature}
  Max Tokens: {self.config.max_tokens}
        """
        self.print_colored(status, "blue")
    
    def handle_command(self, command: str) -> bool:
        """
        Handle user commands
        Returns True if command was handled, False otherwise
        """
        parts = command.split(maxsplit=1)
        cmd = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else None
        
        if cmd == "/help":
            self.print_help()
            return True
            
        elif cmd == "/mode":
            if arg and arg in ["chat", "summarize", "translate", "ideas", "code"]:
                self.current_mode = arg
                self.print_colored(f"✓ Switched to {arg} mode", "green")
            else:
                self.print_colored("✗ Invalid mode. Use: chat, summarize, translate, ideas, code", "red")
            return True
            
        elif cmd == "/history":
            history_data = self.history.get_history()
            if history_data:
                self.print_colored("\n📜 Chat History:", "cyan")
                for i, entry in enumerate(history_data[-10:], 1):  # Show last 10
                    print(f"\n[{i}] {entry['timestamp']}")
                    print(f"You: {entry['user']}")
                    print(f"AI: {entry['assistant']}")
            else:
                self.print_colored("No chat history available.", "yellow")
            return True
            
        elif cmd == "/clear":
            self.history.clear_history()
            self.print_colored("✓ Chat history cleared", "green")
            return True
            
        elif cmd == "/save":
            if arg:
                if self.history.save_to_file(arg):
                    self.print_colored(f"✓ History saved to {arg}", "green")
                else:
                    self.print_colored("✗ Failed to save history", "red")
            else:
                self.print_colored("✗ Please provide a filename", "red")
            return True
            
        elif cmd == "/load":
            if arg:
                if self.history.load_from_file(arg):
                    self.print_colored(f"✓ History loaded from {arg}", "green")
                else:
                    self.print_colored("✗ Failed to load history", "red")
            else:
                self.print_colored("✗ Please provide a filename", "red")
            return True
            
        elif cmd == "/config":
            self.print_status()
            return True
            
        elif cmd == "/temperature":
            if arg:
                try:
                    temp = float(arg)
                    if 0.0 <= temp <= 2.0:
                        self.config.temperature = temp
                        self.print_colored(f"✓ Temperature set to {temp}", "green")
                    else:
                        self.print_colored("✗ Temperature must be between 0.0 and 2.0", "red")
                except ValueError:
                    self.print_colored("✗ Invalid temperature value", "red")
            else:
                self.print_colored("✗ Please provide a temperature value", "red")
            return True
            
        elif cmd == "/tokens":
            if arg:
                try:
                    tokens = int(arg)
                    if tokens > 0:
                        self.config.max_tokens = tokens
                        self.print_colored(f"✓ Max tokens set to {tokens}", "green")
                    else:
                        self.print_colored("✗ Tokens must be positive", "red")
                except ValueError:
                    self.print_colored("✗ Invalid token value", "red")
            else:
                self.print_colored("✗ Please provide a token value", "red")
            return True
            
        elif cmd == "/provider":
            if arg and arg in ["openai", "huggingface", "ollama"]:
                self.config.provider = arg
                self.assistant = AIAssistant(self.config)
                self.print_colored(f"✓ Switched to {arg} provider", "green")
            else:
                self.print_colored("✗ Invalid provider. Use: openai, huggingface, ollama", "red")
            return True
            
        elif cmd in ["/quit", "/exit"]:
            self.running = False
            self.print_colored("\n👋 Thank you for using AI Text Assistant! Goodbye!", "cyan")
            return True
            
        return False
    
    def process_user_input(self, user_input: str) -> None:
        """Process user input and generate AI response"""
        try:
            # Generate response based on mode
            response = self.assistant.generate_response(
                user_input,
                mode=self.current_mode
            )
            
            # Display response
            self.print_colored("\n🤖 AI Assistant:", "magenta")
            print(response)
            print()
            
            # Save to history
            self.history.add_entry(user_input, response)
            
        except Exception as e:
            self.print_colored(f"\n✗ Error: {str(e)}", "red")
            self.print_colored("Tip: Make sure your API keys are configured correctly.", "yellow")
    
    def run(self) -> None:
        """Run the main CLI loop"""
        self.print_banner()
        self.print_colored("Type /help for available commands\n", "yellow")
        self.print_status()
        
        while self.running:
            try:
                # Get user input
                prompt = f"\n{Fore.GREEN if COLORS_AVAILABLE else ''}You [{self.current_mode}]: {Style.RESET_ALL if COLORS_AVAILABLE else ''}"
                user_input = input(prompt).strip()
                
                if not user_input:
                    continue
                
                # Check if it's a command
                if user_input.startswith('/'):
                    self.handle_command(user_input)
                else:
                    # Process as normal chat
                    self.process_user_input(user_input)
                    
            except KeyboardInterrupt:
                self.print_colored("\n\n👋 Interrupted. Use /quit to exit gracefully.", "yellow")
                continue
            except EOFError:
                self.print_colored("\n\n👋 Thank you for using AI Text Assistant! Goodbye!", "cyan")
                break

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="AI Text Assistant - Your intelligent companion for text generation"
    )
    parser.add_argument(
        "--provider",
        choices=["openai", "huggingface", "ollama"],
        help="AI provider to use"
    )
    parser.add_argument(
        "--mode",
        choices=["chat", "summarize", "translate", "ideas", "code"],
        help="Initial AI mode"
    )
    parser.add_argument(
        "--temperature",
        type=float,
        help="Temperature setting (0.0-2.0)"
    )
    
    args = parser.parse_args()
    
    # Create and configure CLI
    cli = AITextAssistantCLI()
    
    if args.provider:
        cli.config.provider = args.provider
        cli.assistant = AIAssistant(cli.config)
    
    if args.mode:
        cli.current_mode = args.mode
    
    if args.temperature is not None:
        cli.config.temperature = args.temperature
    
    # Run the application
    try:
        cli.run()
    except Exception as e:
        print(f"\n✗ Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
