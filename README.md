# MentalHealthAI

An AI-powered mental health support application built with LangChain, Ollama, and Streamlit.

[![Deploy on Render](https://img.shields.io/badge/Render-Deploy-blue?logo=render)](https://render.com)

## 📋 Features

- Mental health support chatbot powered by Ollama/LLM
- Vector database for contextual information retrieval
- Streamlit web interface for easy interaction
- Conversation history tracking

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Ollama (for local LLM)
- SQLite3

### Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/MentalHealthAI.git
cd MentalHealthAI
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/Scripts/activate  # Windows
# or
source venv/bin/activate  # Linux/Mac
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure environment variables
```bash
cp .env.example .env
# Edit .env with your settings
```

### Running the Application

```bash
streamlit run src/app.py
```

## 📁 Project Structure

```
MentalHealthAI/
├── src/
│   ├── app.py           # Streamlit application
│   ├── engine.py        # LLM engine logic
│   ├── main.py          # Main entry point
│   └── utils.py         # Utility functions
├── data/
│   └── mental_health_india.json  # Dataset
├── db/                  # Database files
├── requirements.txt     # Python dependencies
├── README.md           # Project documentation
└── .env.example        # Environment variables template
```

## 🔧 Configuration

See `.env.example` for all available configuration options.

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For issues and questions, please open an issue on GitHub.