# Price Tracker Advance

An advanced AI-powered grocery price tracking agent built with LangChain, LangGraph, and Hugging Face. This project combines large language models (LLMs) with model context protocol (MCP) to provide intelligent price tracking and product comparison capabilities.

## Overview

Price Tracker Advance is a conversational AI agent that leverages:
- **LangChain** - Framework for building language model applications
- **LangGraph** - Orchestration framework for managing complex workflows
- **Hugging Face Models** - State-of-the-art language models for processing queries
- **MCP Client** - Model Context Protocol for accessing external tools and data

The agent can analyze grocery prices, compare products, track price changes, and provide intelligent recommendations through a natural language interface.

## Features

- 🤖 **Conversational AI Agent** - Natural language interface for price tracking queries
- 📊 **Graph-based Workflow** - Intelligent state management and routing using LangGraph
- 🛠️ **Tool Integration** - MCP client integration for accessing external data sources
- 📈 **Data Visualization** - Graph generation capabilities for price trends
- 🔄 **Async Support** - Fully asynchronous execution for improved performance
- 🤗 **Hugging Face Integration** - Access to powerful open-source language models

## Requirements

- Python 3.8 or higher
- All dependencies listed in `requirement.txt`

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/JiteshPL/price_tracker_advance.git
cd price_tracker_advance
```

### 2. Create a Virtual Environment (Recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirement.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root directory:

```env
# Hugging Face API Token (Required)
HUGGINGFACEHUB_API_TOKEN=your_huggingface_api_token_here

# Model Configuration (Optional)
MODEL_PROVIDER=huggingface
HF_MODEL=Qwen/Qwen2.5-7B-Instruct
```

**Getting your Hugging Face API Token:**
1. Visit [Hugging Face](https://huggingface.co/)
2. Sign up or log in to your account
3. Go to Settings → Access Tokens
4. Create a new token with read access
5. Copy the token and paste it into your `.env` file

## Usage

### Running the Agent

```bash
python app.py
```

This will start the interactive Grocery AI Agent. You'll see:

```
============================================================
 Grocery AI Agent 
============================================================

You : 
```

### Example Queries

Try asking the agent questions like:

```
You : What are the current prices for organic milk?
Agent: [Response with current prices and recommendations]

You : Compare prices for whole wheat bread across different stores
Agent: [Comparison chart and analysis]

You : Show me the price trends for eggs over the last month
Agent: [Price trend visualization and insights]

You : Which vegetables are on sale this week?
Agent: [List of sale items with prices]
```

### Exiting the Agent

To exit the agent, type:
```
You : exit
```
or
```
You : quit
```

## Project Structure

```
price_tracker_advance/
├── app.py                  # Main entry point - runs the interactive agent
├── graph.py               # LangGraph workflow definition
├── model.py               # LLM configuration and initialization
├── mcp_client.py          # Model Context Protocol client
├── prompts.py             # Prompt templates for the agent
├── state.py               # State management for the graph
├── graph.py               # Price trend visualization
├── requirement.txt        # Python dependencies
├── nodes/                 # Directory for LangGraph nodes
│   └── agent.py          # Agent node implementation
└── README.md             # This file
```

### File Descriptions

- **app.py** - Main application entry point that initializes the agent and handles user interactions
- **graph.py** - Defines the LangGraph workflow with nodes and edges for processing queries
- **model.py** - Manages LLM initialization and configuration, currently using Hugging Face Qwen model
- **mcp_client.py** - Handles communication with MCP servers for data retrieval
- **prompts.py** - Contains prompt templates used by the agent
- **state.py** - Defines the state schema for the LangGraph workflow
- **nodes/agent.py** - Implements the core agent logic and tool binding

## Dependencies

The project uses the following key libraries:

| Package | Version | Purpose |
|---------|---------|---------|
| `langgraph` | ≥0.6.5 | Graph-based workflow orchestration |
| `langchain` | ≥0.3.27 | Core LLM framework |
| `langchain-core` | ≥0.3.74 | Core components |
| `langchain-huggingface` | ≥0.3.1 | Hugging Face integration |
| `langchain-mcp-adapters` | ≥0.1.9 | MCP protocol support |
| `huggingface_hub` | ≥0.34.4 | Hugging Face Hub access |
| `transformers` | ≥4.55.0 | Transformer models |
| `python-dotenv` | ≥1.1.1 | Environment variable management |
| `pydantic` | ≥2.11.7 | Data validation |

## Configuration

### Model Selection

The agent uses Hugging Face for language model capabilities. You can configure which model to use by setting the `HF_MODEL` environment variable:

```env
HF_MODEL=Qwen/Qwen2.5-7B-Instruct  # Default
HF_MODEL=mistralai/Mistral-7B-Instruct-v0.3
HF_MODEL=meta-llama/Llama-2-7b-chat-hf
```

### Performance Tuning

In `model.py`, you can adjust:

```python
temperature=0.2,        # Lower = more deterministic (0.0-1.0)
max_new_tokens=1024     # Maximum response length
```

## Troubleshooting

### Issue: "HUGGINGFACEHUB_API_TOKEN not found"

**Solution:** Make sure you've created a `.env` file with your Hugging Face API token. See [Set Up Environment Variables](#4-set-up-environment-variables).

### Issue: "Module not found" errors

**Solution:** Ensure all dependencies are installed:
```bash
pip install -r requirement.txt
```

### Issue: Slow response times

**Solution:** This is normal for the first query as the model is being loaded. Subsequent queries will be faster.

### Issue: Connection errors to Hugging Face

**Solution:** 
1. Check your internet connection
2. Verify your API token is valid
3. Check if Hugging Face servers are operational

## Architecture

The project uses a **LangGraph-based architecture** with the following flow:

1. **Input** - User query received through command-line interface
2. **Agent** - LLM processes query with available tools
3. **Tool Calling** - MCP client accesses external data sources
4. **Processing** - Results aggregated and formatted
5. **Output** - Response presented to user
6. **Loop** - Maintains conversation history for context

## Future Enhancements

- 📱 Web interface for better UX
- 📊 Advanced analytics and reporting
- 💾 Database integration for persistent storage
- 🔔 Price alert notifications
- 📍 Location-based price tracking
- 🌐 Multi-language support
- ⚡ Caching for improved performance

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is currently unlicensed. Please add a LICENSE file if you plan to share it publicly.

## Support

If you encounter any issues or have questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review the LangChain documentation: https://python.langchain.com/
3. Check LangGraph documentation: https://langchain-ai.github.io/langgraph/
4. Visit Hugging Face docs: https://huggingface.co/docs

## Author

**JiteshPL** - [GitHub Profile](https://github.com/JiteshPL)

## Acknowledgments

- LangChain team for the excellent framework
- Hugging Face for providing powerful language models
- LangGraph for workflow orchestration capabilities
