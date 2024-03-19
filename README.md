# Solution to the AI Case Study of Appinio

For this project, I chose to implement the solution using Python, without the necessity of the LangChain library. This decision was motivated by my proficiency with Python.

This prototype is designed to answer questions using the OpenAI API, drawing upon a database of question-and-answer pairs. These pairs were initially processed and transformed into semantic vectors utilizing OpenAI's 'text-embedding-ada-002' model, enabling the system to understand and match the semantic similarity between user queries and the stored questions.

Question Answering: When a user ask a question, the system retrieves the three most semantically similar questions from the processed database and uses them as context to generate an informed response. This response is formulated by considering the examples and the new query, ensuring that the system's answers are both relevant and accurate.

Python Version: This project is developed with Python 3.11. It is recommended to use Python 3.11 or newer to ensure full compatibility.

## Quick Setup

### 1. Clone the Repository

Clone this repository to your local machine using Git:

```sh
git clone <https://github.com/hernanver/hv-casestudy>
```
### 2. Create a Virtual Environment (Optional but Recommended)
For Unix/macOS:

```sh
python3 -m venv venv
source venv/bin/activate
```
For Windows:

```sh
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies
Install the required Python packages:

```sh
pip install -r requirements.txt
```

### 4. Set Up Your OpenAI API Key

Update .env file with your OpenAI API key as:
OPENAI_API_KEY=''

## Running the Prototype

In your terminal, with the virtual environment activated, run:

```sh
python3 index.py
```

## Stopping the Prototype

To stop the prototype, use Ctrl+C in your terminal.


## About the Process:

## GENERAL DIAGRAM

Below is a flowchart that visually represents the steps involved in our process:

![Diagrama de Flujo del Proceso](https://github.com/hernanver/hv-casestudy/blob/master/diagram.jpg?raw=true)


## STEP01: CSV to JSON Transformation and Embedding Generation


Objective: Transform question-and-answer pairs from a CSV format into JSON and generate semantic embeddings for each pair.

### Process Overview:

The script reads a CSV file where each row corresponds to a question-and-answer pair, delimited by a semicolon (;).
For each pair, it utilizes OpenAI's 'text-embedding-ada-002' model to generate semantic embeddings. This process transforms the textual content into a semantic vector, encapsulating the essence of its meaning.
The pairs, along with their embeddings, are then organized into a structured JSON format, establishing a clear link between the questions, answers, and their corresponding embeddings. This setup facilitates the next stages of processing, particularly for conducting semantic similarity comparisons.

### Output

The output is a single JSON file containing an array of objects. Each object represents a question-answer pair with the following structure:

json
{
  "question": "Question",
  "question_embedding": [/* array of numbers representing the question's embedding */],
  "answer": "Answer",
  "answer_embedding": [/* array of numbers representing the answer's embedding */]
}



## STEP02&3: Continuous Conversation and CSV Logging

Objective: Enhance AI interaction by facilitating a real-time, continuous conversation flow, dynamically addressing each user query with contextually appropriate responses.


### Implementation Details

1-Upon each execution, the script initializes a new conversation session, identified by a unique ConvID based on the current timestamp.
2-User questions are converted into embeddings and compared against a dataset of question-answer pairs to find the most similar questions, which are given as context into the prompt to the 'gpt-3.5-turbo' OpenAI's model to answer correctly.
The script runs in a loop, continuously accepting user input and generating responses until manually terminated, facilitating an uninterrupted conversation flow.




