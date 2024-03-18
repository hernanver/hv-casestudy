
# AI Conversation Prototype Setup Guide

This guide provides the steps to get the AI Conversation Prototype up and running on your machine. The prototype is designed to answer customer questions using OpenAI's GPT model.

## Quick Setup

### 1. Clone the Repository

Clone this repository to your local machine using Git:

```sh
git clone <repository-url>
cd path/to/cloned/repository
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
Obtain an API key from OpenAI.
Create a file named key_openai.txt in the project directory, and paste your API key there.

## Running the Prototype

In your terminal, with the virtual environment activated, run:

```sh
python step02_qa.py
```

## Stopping the Prototype

To stop the prototype, use Ctrl+C in your terminal.



<<STEP01: CSV to JSON Transformation and Embedding Generation>>

This step involves converting a CSV file containing pairs of questions and answers into a JSON format, and generating semantic embeddings for each question and answer. The resulting JSON file organizes the data such that each question-answer pair is accompanied by its corresponding embeddings, facilitating later stages of processing where semantic similarity comparisons are required.

Process

The script reads a CSV file where each row represents a pair of question and answer, separated by a semicolon (;).
For each question and answer pair, the script generates semantic embeddings using OpenAI's GPT-3 model. This involves converting the text into a high-dimensional vector that captures its semantic meaning.
Each question-answer pair, along with its embeddings, is stored in a structured JSON format. This format maintains a direct association between questions, answers, and their respective embeddings, ensuring they are easily accessible for further processing.

Output

The output is a single JSON file containing an array of objects. Each object represents a question-answer pair with the following structure:

json
{
  "question": "Actual question text",
  "question_embedding": [/* array of numbers representing the question's embedding */],
  "answer": "Actual answer text",
  "answer_embedding": [/* array of numbers representing the answer's embedding */]
}

Purpose

The primary goal of this step is to prepare the question-answer data for subsequent stages, where semantic similarity measures will be used to find the most relevant answers based on a user's query. By converting text to embeddings, we enable a machine-understandable format that facilitates comparing the semantic similarity between the user's question and the stored questions.

Usage

To use this script, ensure you have a CSV file formatted with question and answer pairs, separated by semicolons. Set up your OpenAI API key, and run the script. The output will be a JSON file ready for further processing in the next steps of the project.


<<STEP02: Continuous Conversation and CSV Logging>>

This step enhances the interaction with the AI by engaging in a continuous conversation where each question from the user and the corresponding answer from the AI are dynamically processed and responded to in real-time. The key addition is the capability to log each conversation to a CSV file, enabling a persistent record of interactions. This step is crucial for analyzing conversation patterns, improving response quality, and auditing interactions.

Key Features

Dynamic Embedding Generation: For each user question, the script generates semantic embeddings using the GPT model. This facilitates identifying the most semantically similar questions from a preloaded dataset, ensuring the AI's response is contextually relevant.
Continuous Conversation Flow: Unlike a one-off Q&A, this step maintains a running dialogue, allowing for a more natural and engaging user experience. The script listens for user input, processes it, and continues the conversation without interruption until manually stopped.
CSV Logging: Each conversation is uniquely identified and logged into a CSV file with the format ConvID--Question--Answer--TokensUsed. This logging includes the conversation ID, user's question, AI's response, and the number of tokens used for each interaction, providing a comprehensive record of the dialogue.
Implementation Details

Upon each execution, the script initializes a new conversation session, identified by a unique ConvID based on the current timestamp.
User questions are converted into embeddings and compared against a dataset of question-answer pairs to find the most similar questions, which inform the AI's responses.
Responses are generated using OpenAI's GPT model, selected for its semantic comprehension and generation capabilities.
The conversation, including the system's prompts, user's questions, and AI's answers, along with the tokens used for generating responses, are logged into a CSV file. This file serves as a historical record of interactions, useful for analysis and model refinement.
The script runs in a loop, continuously accepting user input and generating responses until manually terminated, facilitating an uninterrupted conversation flow.
Usage

Ensure your OpenAI API key is correctly set up and the necessary Python packages are installed.
Load your dataset of question-answer pairs into the script. This dataset is used to generate contextually relevant AI responses.
Run the script. It will automatically start a new conversation session, listen for user input, generate responses, and log the conversation to a CSV file.
Interact with the script through the terminal by inputting questions and receiving AI-generated answers in real-time.
To end the conversation, simply interrupt the script execution (e.g., Ctrl+C).
