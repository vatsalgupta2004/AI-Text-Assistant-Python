"""
Chat History Management Module
================================
Handles saving, loading, and managing chat conversation history.

Author: Contributed for Hacktoberfest 2025
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path

class ChatHistory:
    """Manages chat conversation history"""
    
    def __init__(self, history_dir: str = "chat_history"):
        """
        Initialize chat history manager
        
        Args:
            history_dir: Directory to store chat history files
        """
        self.history_dir = Path(history_dir)
        self.history: List[Dict[str, Any]] = []
        self._ensure_history_dir()
    
    def _ensure_history_dir(self) -> None:
        """Create history directory if it doesn't exist"""
        self.history_dir.mkdir(parents=True, exist_ok=True)
    
    def add_entry(self, user_message: str, assistant_response: str, 
                  mode: str = "chat", metadata: Optional[Dict] = None) -> None:
        """
        Add a new chat entry to history
        
        Args:
            user_message: User's input message
            assistant_response: AI assistant's response
            mode: Current AI mode
            metadata: Additional metadata (optional)
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "user": user_message,
            "assistant": assistant_response,
            "mode": mode,
            "metadata": metadata or {}
        }
        self.history.append(entry)
    
    def get_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get chat history
        
        Args:
            limit: Maximum number of entries to return (None for all)
        
        Returns:
            List of chat entries
        """
        if limit:
            return self.history[-limit:]
        return self.history
    
    def get_conversation_context(self, num_messages: int = 5) -> List[Dict[str, str]]:
        """
        Get recent conversation context for AI
        
        Args:
            num_messages: Number of recent messages to include
        
        Returns:
            List of message dictionaries with 'role' and 'content'
        """
        recent = self.history[-num_messages:]
        context = []
        
        for entry in recent:
            context.append({"role": "user", "content": entry["user"]})
            context.append({"role": "assistant", "content": entry["assistant"]})
        
        return context
    
    def clear_history(self) -> None:
        """Clear all chat history"""
        self.history = []
    
    def save_to_file(self, filename: Optional[str] = None) -> bool:
        """
        Save chat history to JSON file
        
        Args:
            filename: Name of file to save (auto-generates if None)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"chat_history_{timestamp}.json"
            
            filepath = self.history_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump({
                    "saved_at": datetime.now().isoformat(),
                    "total_messages": len(self.history),
                    "history": self.history
                }, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error saving history: {e}")
            return False
    
    def load_from_file(self, filename: str) -> bool:
        """
        Load chat history from JSON file
        
        Args:
            filename: Name of file to load
        
        Returns:
            True if successful, False otherwise
        """
        try:
            filepath = self.history_dir / filename
            
            if not filepath.exists():
                print(f"File not found: {filepath}")
                return False
            
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.history = data.get("history", [])
            
            return True
        except Exception as e:
            print(f"Error loading history: {e}")
            return False
    
    def list_saved_files(self) -> List[str]:
        """
        List all saved history files
        
        Returns:
            List of filenames
        """
        try:
            return [f.name for f in self.history_dir.glob("*.json")]
        except Exception:
            return []
    
    def export_to_text(self, filename: str) -> bool:
        """
        Export chat history to readable text file
        
        Args:
            filename: Name of text file to create
        
        Returns:
            True if successful, False otherwise
        """
        try:
            filepath = self.history_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write("AI Text Assistant - Chat History\n")
                f.write("=" * 60 + "\n\n")
                
                for i, entry in enumerate(self.history, 1):
                    f.write(f"[{i}] {entry['timestamp']}\n")
                    f.write(f"Mode: {entry.get('mode', 'chat')}\n")
                    f.write(f"\nYou: {entry['user']}\n")
                    f.write(f"\nAI: {entry['assistant']}\n")
                    f.write("\n" + "-" * 60 + "\n\n")
            
            return True
        except Exception as e:
            print(f"Error exporting to text: {e}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about chat history
        
        Returns:
            Dictionary with various statistics
        """
        if not self.history:
            return {
                "total_messages": 0,
                "modes_used": {},
                "first_message": None,
                "last_message": None
            }
        
        # Count modes
        modes = {}
        for entry in self.history:
            mode = entry.get("mode", "chat")
            modes[mode] = modes.get(mode, 0) + 1
        
        return {
            "total_messages": len(self.history),
            "modes_used": modes,
            "first_message": self.history[0]["timestamp"],
            "last_message": self.history[-1]["timestamp"],
            "total_characters": sum(len(e["user"]) + len(e["assistant"]) for e in self.history)
        }
    
    def search_history(self, query: str, case_sensitive: bool = False) -> List[Dict[str, Any]]:
        """
        Search chat history for a query string
        
        Args:
            query: Search query
            case_sensitive: Whether search should be case-sensitive
        
        Returns:
            List of matching entries
        """
        results = []
        
        if not case_sensitive:
            query = query.lower()
        
        for entry in self.history:
            user_text = entry["user"] if case_sensitive else entry["user"].lower()
            assistant_text = entry["assistant"] if case_sensitive else entry["assistant"].lower()
            
            if query in user_text or query in assistant_text:
                results.append(entry)
        
        return results
    
    def __len__(self) -> int:
        """Return number of entries in history"""
        return len(self.history)
    
    def __repr__(self) -> str:
        """String representation"""
        return f"ChatHistory(entries={len(self.history)}, dir={self.history_dir})"
