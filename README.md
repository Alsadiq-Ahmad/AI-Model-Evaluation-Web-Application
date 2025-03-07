# AI Model Evaluation Web Application

## Overview

This project is a **web application** for evaluating responses from multiple **Large Language Models (LLMs)**, including:

- **GPT-3.5 Turbo** (OpenAI)
- **GPT-4** (OpenAI)
- **Llama-2-70B-Chat** (Meta via Replicate API)
- **Falcon-40B-Instruct** (via Replicate API)

The system utilizes **a vector database** (Pinecone) to retrieve relevant search results and enhance the model responses. It also integrates **WebSockets/SSE** for real-time streaming of responses to the frontend.
![RAG2](https://github.com/user-attachments/assets/4c4519e8-26b2-4963-8296-be7a8080dfc2)
## Features

- **Multi-LLM Response Comparison**: Compare how different models respond to the same query.
- **Vector Database Querying**: Uses **Pinecone** to retrieve relevant search results.
- **WebSockets/SSE for Streaming**: Real-time updates for model responses.
- **Web Scraping Integration**: Uses **BeautifulSoup** to scrape and store data in Pinecone.
- **Flask-Based API**: A backend built with **Flask**, handling query processing and LLM interaction.
- **Bootstrap-Based UI**: A simple and user-friendly interface for inputting queries and viewing model responses.

---

## Installation

### Prerequisites

Ensure you have the following installed:

- Python 3.8+
- Redis (for Flask-SSE)

### Setup


1. **Clone the Repository:**

   ```sh
   git clone <repository_url>
   cd <repository_folder>
   ```

2. **Create a Virtual Environment (Optional but Recommended):**

   ```sh
   python -m venv venv
   source venv/bin/activate   # On macOS/Linux
   venv\Scripts\activate      # On Windows
   ```

3. **Install Dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

4. **Start Redis Server:**

   ```sh
   redis-server
   ```

5. **Run the Application:**

   ```sh
   python main.py
   ```

6. **Access the Web Application:** Open your browser and visit:

   ```
   http://127.0.0.1:5000/
   ```

---

## API Endpoints

### `GET /`

- **Description**: Renders the main web page.

### `POST /submit`

- **Description**: Accepts a user query, retrieves search results, sends prompts to LLMs, and streams responses.
- **Request Body**:
  ```json
  {
    "query": "What is machine learning?"
  }
  ```
- **Response**:
  ```json
  {
    "status": "processing"
  }
  ```

### Streaming Updates

- **Endpoint**: `/stream`
- **Event Type**: `response`
- **Data Format**:
  ```json
  {
    "model": "gpt-4",
    "response": "Machine learning is a branch of AI..."
  }
  ```

---

## File Structure

```
├── app/
│   ├── __init__.py    # Flask app initialization
│   ├── main.py        # Main application logic
│   ├── querying.py    # Functions for querying models & vector DB
│   ├── scraping.py    # Web scraping module
│   ├── templates/
│   │   ├── index.html  # Frontend UI
├── requirements.txt    # Dependencies
├── README.md           # Project documentation
```

---

## Environment Variables

Ensure you set up your API keys before running the project:

```sh
export OPENAI_API_KEY="your_openai_api_key"
export REPLICATE_API_KEY="your_replicate_api_key"
export PINECONE_API_KEY="your_pinecone_api_key"
```

For Windows (PowerShell):

```powershell
$env:OPENAI_API_KEY="your_openai_api_key"
$env:REPLICATE_API_KEY="your_replicate_api_key"
$env:PINECONE_API_KEY="your_pinecone_api_key"
```

---

## Future Improvements

- **Enhance UI** with better visualization of model responses.
- **Optimize Query Processing** to reduce latency.
- **Integrate More LLMs** for better comparison.
- **Deploy on a Cloud Platform** for production use.

---

## License

This project is licensed under the **MIT License**. See the LICENSE file for details.

