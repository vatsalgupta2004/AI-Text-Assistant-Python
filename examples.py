"""
Example Usage Scripts for AI Text Assistant
============================================
Demonstrates various ways to use the AI assistant programmatically.

Author: Contributed for Hacktoberfest 2025
"""

from ai_assistant import AIAssistant
from config import Config
from chat_history import ChatHistory

# =============================================================================
# Example 1: Basic Chat
# =============================================================================

def example_basic_chat():
    """Example: Simple chat interaction"""
    print("\n" + "=" * 60)
    print("Example 1: Basic Chat")
    print("=" * 60)
    
    # Initialize
    config = Config()
    assistant = AIAssistant(config)
    
    # Single query
    response = assistant.generate_response(
        "What is artificial intelligence?",
        mode="chat"
    )
    print(f"\nResponse: {response}")

# =============================================================================
# Example 2: Text Summarization
# =============================================================================

def example_summarization():
    """Example: Summarize long text"""
    print("\n" + "=" * 60)
    print("Example 2: Text Summarization")
    print("=" * 60)
    
    config = Config()
    assistant = AIAssistant(config)
    
    long_text = """
    Artificial intelligence (AI) has made remarkable progress in recent years,
    transforming industries from healthcare to finance. Machine learning algorithms
    can now recognize patterns in data with unprecedented accuracy, while natural
    language processing enables computers to understand and generate human language.
    Deep learning, a subset of machine learning, has revolutionized computer vision,
    enabling applications like facial recognition and autonomous vehicles. However,
    challenges remain in areas like explainability, bias, and ethical considerations.
    The future of AI promises even more advanced capabilities, including artificial
    general intelligence that can match human-level reasoning across diverse tasks.
    """
    
    summary = assistant.generate_response(long_text, mode="summarize")
    print(f"\nOriginal length: {len(long_text)} characters")
    print(f"Summary: {summary}")

# =============================================================================
# Example 3: Translation
# =============================================================================

def example_translation():
    """Example: Translate text"""
    print("\n" + "=" * 60)
    print("Example 3: Translation")
    print("=" * 60)
    
    config = Config()
    assistant = AIAssistant(config)
    
    phrases = [
        ("Hello, how are you?", "Spanish"),
        ("Thank you very much", "French"),
        ("Good morning", "German")
    ]
    
    for phrase, target_lang in phrases:
        query = f"Translate '{phrase}' to {target_lang}"
        translation = assistant.generate_response(query, mode="translate")
        print(f"\n{phrase} → {translation}")

# =============================================================================
# Example 4: Idea Generation
# =============================================================================

def example_idea_generation():
    """Example: Generate creative ideas"""
    print("\n" + "=" * 60)
    print("Example 4: Idea Generation")
    print("=" * 60)
    
    config = Config()
    config.temperature = 0.9  # Higher temperature for creativity
    assistant = AIAssistant(config)
    
    prompt = "Innovative mobile app ideas for students"
    ideas = assistant.generate_response(prompt, mode="ideas")
    print(f"\nIdeas for: {prompt}")
    print(ideas)

# =============================================================================
# Example 5: Code Generation
# =============================================================================

def example_code_generation():
    """Example: Generate code"""
    print("\n" + "=" * 60)
    print("Example 5: Code Generation")
    print("=" * 60)
    
    config = Config()
    assistant = AIAssistant(config)
    
    code_requests = [
        "Write a Python function to calculate factorial",
        "Create a JavaScript function to validate email",
        "Write SQL query to find top 10 customers by sales"
    ]
    
    for request in code_requests:
        print(f"\nRequest: {request}")
        code = assistant.generate_response(request, mode="code")
        print(code)
        print("-" * 60)

# =============================================================================
# Example 6: Batch Processing
# =============================================================================

def example_batch_processing():
    """Example: Process multiple items"""
    print("\n" + "=" * 60)
    print("Example 6: Batch Processing")
    print("=" * 60)
    
    config = Config()
    assistant = AIAssistant(config)
    
    # Multiple texts to summarize
    articles = [
        "Article 1: Climate change is affecting global weather patterns...",
        "Article 2: New breakthrough in quantum computing announced...",
        "Article 3: Social media impact on mental health studied..."
    ]
    
    summaries = []
    for i, article in enumerate(articles, 1):
        print(f"\nProcessing article {i}...")
        summary = assistant.generate_response(article, mode="summarize")
        summaries.append(summary)
        print(f"Summary {i}: {summary[:100]}...")
    
    print(f"\nProcessed {len(summaries)} articles")

# =============================================================================
# Example 7: Chat History Management
# =============================================================================

def example_history_management():
    """Example: Manage chat history"""
    print("\n" + "=" * 60)
    print("Example 7: Chat History Management")
    print("=" * 60)
    
    history = ChatHistory()
    
    # Add conversations
    conversations = [
        ("What is Python?", "Python is a high-level programming language...", "chat"),
        ("Summarize: AI is...", "AI Summary: Machine learning, neural networks...", "summarize"),
        ("Translate hello to Spanish", "Hola", "translate")
    ]
    
    for user_msg, ai_msg, mode in conversations:
        history.add_entry(user_msg, ai_msg, mode=mode)
    
    # Get statistics
    stats = history.get_statistics()
    print(f"\nTotal messages: {stats['total_messages']}")
    print(f"Modes used: {stats['modes_used']}")
    
    # Search history
    results = history.search_history("python")
    print(f"\nSearch 'python': {len(results)} results")
    
    # Save history
    filename = "example_history.json"
    if history.save_to_file(filename):
        print(f"\n✓ Saved to {filename}")
    
    # Export to text
    text_file = "example_history.txt"
    if history.export_to_text(text_file):
        print(f"✓ Exported to {text_file}")

# =============================================================================
# Example 8: Configuration Management
# =============================================================================

def example_configuration():
    """Example: Work with configuration"""
    print("\n" + "=" * 60)
    print("Example 8: Configuration Management")
    print("=" * 60)
    
    config = Config()
    
    # Display current config
    print("\nCurrent Configuration:")
    print(f"  Provider: {config.provider}")
    print(f"  Model: {config.get_model()}")
    print(f"  Temperature: {config.temperature}")
    print(f"  Max Tokens: {config.max_tokens}")
    
    # Modify configuration
    config.temperature = 0.8
    config.max_tokens = 1500
    
    print("\nModified Configuration:")
    print(f"  Temperature: {config.temperature}")
    print(f"  Max Tokens: {config.max_tokens}")
    
    # Validate
    is_valid, error = config.validate()
    print(f"\nValidation: {'✓ Valid' if is_valid else f'✗ {error}'}")
    
    # Convert to dictionary
    config_dict = config.to_dict()
    print(f"\nAs Dictionary: {config_dict}")

# =============================================================================
# Example 9: Error Handling
# =============================================================================

def example_error_handling():
    """Example: Handle errors gracefully"""
    print("\n" + "=" * 60)
    print("Example 9: Error Handling")
    print("=" * 60)
    
    config = Config()
    assistant = AIAssistant(config)
    
    try:
        # This might fail if API key is invalid
        response = assistant.generate_response(
            "Test query",
            mode="chat"
        )
        print(f"\n✓ Success: {response[:100]}...")
    
    except ValueError as e:
        print(f"\n✗ Configuration Error: {e}")
        print("Please check your API keys in .env file")
    
    except Exception as e:
        print(f"\n✗ Unexpected Error: {e}")
        print("Check your internet connection and API status")

# =============================================================================
# Example 10: Custom Workflow
# =============================================================================

def example_custom_workflow():
    """Example: Create custom workflow"""
    print("\n" + "=" * 60)
    print("Example 10: Custom Workflow - Research Assistant")
    print("=" * 60)
    
    config = Config()
    assistant = AIAssistant(config)
    history = ChatHistory()
    
    # Research workflow
    topic = "Quantum Computing"
    
    # Step 1: Generate research questions
    print(f"\nStep 1: Generating research questions about {topic}...")
    questions_query = f"Generate 3 research questions about {topic}"
    questions = assistant.generate_response(questions_query, mode="ideas")
    print(f"Questions:\n{questions}")
    history.add_entry(questions_query, questions, mode="ideas")
    
    # Step 2: Get overview
    print(f"\nStep 2: Getting overview...")
    overview_query = f"Provide a brief overview of {topic}"
    overview = assistant.generate_response(overview_query, mode="chat")
    print(f"Overview: {overview[:200]}...")
    history.add_entry(overview_query, overview, mode="chat")
    
    # Step 3: Summarize findings
    print(f"\nStep 3: Creating summary...")
    summary_query = f"Summarize key points about {topic}"
    summary = assistant.generate_response(summary_query, mode="summarize")
    print(f"Summary: {summary}")
    history.add_entry(summary_query, summary, mode="summarize")
    
    # Save research session
    history.save_to_file(f"{topic.lower().replace(' ', '_')}_research.json")
    print(f"\n✓ Research session saved")

# =============================================================================
# Main Function to Run Examples
# =============================================================================

def main():
    """Run all examples"""
    print("\n" + "=" * 60)
    print("AI Text Assistant - Usage Examples")
    print("=" * 60)
    print("\nNote: These examples require valid API keys in .env file")
    print("Uncomment specific examples to run them\n")
    
    # Uncomment the examples you want to run:
    
    # example_basic_chat()
    # example_summarization()
    # example_translation()
    # example_idea_generation()
    # example_code_generation()
    # example_batch_processing()
    example_history_management()
    example_configuration()
    # example_error_handling()
    # example_custom_workflow()
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()
