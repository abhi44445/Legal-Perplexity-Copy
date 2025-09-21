<img width="1889" height="920" alt="Screenshot 2025-09-15 000922" src="https://github.com/user-attachments/assets/57ae0e3a-3208-489f-94fa-c7f3f6ce7be9" />

<img width="1884" height="906" alt="Screenshot 2025-09-15 000935" src="https://github.com/user-attachments/assets/cc894948-8adb-443e-aa8a-db64464b8605" />

<img width="1895" height="956" alt="Screenshot 2025-09-15 000906" src="https://github.com/user-attachments/assets/a9ffd777-cad2-404d-b22b-b7b616ab24ed" />


# Legal Perplexity 2.0 - Constitutional AI Assistant

An advanced AI-powered legal assistant specialized in Indian Constitutional Law. This project provides comprehensive constitutional analysis with citation-backed responses using cutting-edge RAG (Retrieval-Augmented Generation) technology.

## 🚀 Key Features

### 🏛️ Constitution Chat
Expert constitutional analysis with citation-backed responses, user type adaptation, and comprehensive coverage of Indian constitutional law.

### ⚖️ Know Your Rights (NEW)
Real-world legal guidance for citizens facing situations like:
- **Bribery & Corruption**: Police demanding bribes, government office corruption
- **Threats & Intimidation**: Personal safety threats, illegal eviction attempts  
- **Harassment**: Workplace harassment, public space safety, online harassment
- **Constitutional Violations**: Understanding and asserting your fundamental rights

**Key Benefits:**
- Constitutional foundation for all advice
- Urgency classification with emergency guidance
- Actionable recommendations with evidence collection
- Multi-scenario support with specialized prompts

📚 **[Know Your Rights Documentation](./features/know_your_rights/docs/README.md)**

## 🏛️ Constitution Chat Feature

The **Constitution Chat** is our flagship feature that provides:

- **Expert Constitutional Analysis**: Deep insights into Indian Constitution articles (1-395)
- **Citation-Backed Responses**: Every answer includes verifiable constitutional references
- **User Type Adaptation**: Tailored responses for General Public, Legal Professionals, and Students
- **Comprehensive Coverage**: Fundamental Rights, Directive Principles, governance structures, and more
- **Legal Precedent Integration**: Supreme Court landmark cases and judicial interpretations

### Quick Start for Constitution Chat

1. **Start Backend Server**:
   ```bash
   uvicorn main:app --host 127.0.0.1 --port 8000 --reload
   ```

2. **Start Frontend Application**:
   ```bash
   cd frontend && npm run dev
   ```

3. **Access the Application**: 
   - Constitution Chat: http://localhost:5174/constitution
   - Know Your Rights: http://localhost:5174/know-your-rights

4. **Ask Constitutional Questions**: 
   - "What is Article 14 and its key principles?"
   - "Explain fundamental freedoms under Article 19"
   - "How do Directive Principles guide governance?"

📚 **[View Complete Constitution Chat Documentation](./constitution_chat/CONSTITUTION_CHAT_DOCUMENTATION.md)**

---

## Table of Contents
1. [Constitution Chat Feature](#constitution-chat-feature)
2. [Environment Setup](#environment-setup)
    - [Using Pipenv](#using-pipenv)
    - [Using Conda](#using-conda)
    - [Using Pip](#using-pip)
3. [Running the Project](#running-the-project)
4. [Legacy Phase-based Execution](#legacy-phase-based-execution)

---

## Environment Setup

### Using Pipenv
Pipenv is a tool that manages dependencies and virtual environments for Python projects.

1. Install Pipenv if you don't have it:
    ```
    pip install pipenv
    ```

2. Navigate to the project directory and create a virtual environment:
    ```
    pipenv install
    ```

3. Activate the virtual environment:
    ```
    pipenv shell
    ```

4. (Optional) Install any additional dependencies:
    ```
    pipenv install <package_name>
    ```

---

### Using Conda
Conda is an open-source package management system and environment management system.

1. Create a new conda environment:
    ```
    conda create -n myenv python=3.9
    ```

2. Activate the environment:
    ```
    conda activate myenv
    ```

3. Install dependencies from `requirements.txt` (if available):
    ```
    pip install -r requirements.txt
    ```

---

### Using Pip
Pip is the standard package installer for Python.

1. Install virtualenv if you don't have it:
    ```
    pip install virtualenv
    ```

2. Create a virtual environment:
    ```
    virtualenv venv
    ```

3. Activate the virtual environment:
    - On Windows:
        ```
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```
        source venv/bin/activate
        ```

4. Install dependencies from `requirements.txt` (if available):
    ```
    pip install -r requirements.txt
    ```

---

## Running the Project

### Modern FastAPI + React Application (Recommended)

The main application runs as a modern web service with separate backend and frontend:

#### Backend (FastAPI)
```bash
# Install Python dependencies
pip install -r requirements-fastapi.txt

# Start the FastAPI server
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

#### Frontend (React + Vite)
```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Start the development server
npm run dev
```

#### Access the Application
- **Frontend**: http://localhost:5174
- **Backend API**: http://localhost:8000
- **Constitution Chat**: http://localhost:5174/chat
- **API Documentation**: http://localhost:8000/docs

### Configuration
Create a `.env` file in the project root:
```env
OPENROUTER_API_KEY=your_api_key_here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
```

---

## Legacy Phase-based Execution

The project consists of three Python files, each corresponding to a different phase of the project:

### To run the App directly
```
streamlit run main.py
```

### To run app in different phases

1. Phase 1: Run the first phase using:
    ```
    streamlit run frontend.py
    ```

2. Phase 2: Run the second phase using:
    ```
    python vector_database.py
    ```

3. Phase 3: Run the third phase using:
    ```
    python rag_pipeline.py
    ```

Ensure that all dependencies are installed before running the scripts.

---

## 🚀 Features Overview

- **Constitution Chat**: AI-powered constitutional law assistant
- **Rights Explorer**: Interactive fundamental rights exploration
- **Cases Database**: Searchable legal case repository
- **Research Workspace**: Advanced legal research tools
- **Advanced Search**: Semantic search across legal documents

## 📋 System Requirements

- **Python**: 3.10 or higher
- **Node.js**: 16.0 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 2GB for vector database and dependencies

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For technical support or questions:
- Create an issue on GitHub
- Check the [Constitution Chat Documentation](./constitution_chat/CONSTITUTION_CHAT_DOCUMENTATION.md)
- Review the API documentation at http://localhost:8000/docs

---

If you encounter any issues, feel free to reach out or check the documentation for the tools mentioned above.
