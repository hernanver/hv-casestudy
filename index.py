from openai import OpenAI
import openai
import json
import numpy as np
from scipy.spatial.distance import cosine
from typing import List
import csv
import os
from datetime import datetime
from step01.step01_create_embeddings import open_file
from time import sleep
from dotenv import load_dotenv

# Load .env 
load_dotenv()

# Compute and return the cosine similarity between two vectors
def cosine_similarity(a: List[float], b: List[float]) -> float:
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Generate and return GPT embedding for the provided text
def get_embedding(text, model='text-embedding-ada-002'):
    response = openai.embeddings.create(input=text, model=model)
    return response.data[0].embedding

# Load and return the JSON content from the given file.
def load_json(filepath: str) -> dict:
    try:
        with open(filepath, 'r', encoding='utf-8') as infile:
            return json.load(infile)
    except json.JSONDecodeError as e:
        print(f"Error loading JSON: {e}")
        raise
    

# Log conversation details to a CSV file
def save_conversation_to_csv(conv_id, question, response, tokens_used, filename="conversations.csv"):
    """
    Save Conversation into a CSV file.
    """
    # Verifica si el archivo ya existe para determinar si se debe escribir el encabezado
    file_exists = os.path.isfile(filename)
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['ConvID', 'Question', 'Answer', 'TokensUsed']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            'ConvID': conv_id,
            'Question': question,
            'Answer': response,
            'TokensUsed': tokens_used
        })

# Find and return the top N most similar questions based on cosine similarity
def find_most_similar_questions(user_embedding, questions, top_n=3):
    similarities = []
    for question in questions:
        sim = cosine_similarity(user_embedding, question["question_embedding"])
        similarities.append((question, sim))
    similarities.sort(key=lambda x: x[1], reverse=True)
    # Return top_n examples
    return similarities[:top_n]

# Generate a context string from the most similar questions and their answers
def generate_answer_context(questions):
    context = "### EXAMPLES:"
    for i, (question, sim) in enumerate(questions, start=1):
        context += f"# QUESTION {i}: {question['question']}\ANSWER {i}: {question['answer']}\n\n"
    return context


# Generate a response from OpenAI based on the given conversation
def chatbot(conversation, model="gpt-3.5-turbo-16k", max_tokens=150, temperature=0.5):

    while True:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=conversation, 
                temperature=temperature,
                max_tokens=max_tokens
            )
            text = response.choices[0].message.content
            return text, response.usage.total_tokens
        
        except Exception as e:
            print(f"Error communicating with OpenAI: {e}")
            exit(1)


if __name__ == "__main__":

    # LOAD API KEY
    openai.api_key = os.getenv('OPENAI_API_KEY')
    client = OpenAI(api_key=openai.api_key)

    # Load questions and answers dataset
    qa_data = load_json('step01/qa_json/qa_embeddings.json')
    # Initialize conversation
    conversation = []
    # Unique conversation ID
    conv_id = datetime.now().strftime("%Y%m%d%H%M%S")

    try:
        while True:
            user_input = input("Please enter your question: ")

            user_embedding = get_embedding(user_input)

            similar_questions = find_most_similar_questions(user_embedding, qa_data)

            context = generate_answer_context(similar_questions)
            
            # print("CONTEXT:", context)

            # Prepare the chatbot prompt with context
            system_message = "You should be able to answer a potential customer's question that might be asked through Live Chat or email. Please use the following three examples to answer the user's question."
            conversation = [{'role': 'system', 'content': system_message + context}, {'role': 'user', 'content': user_input}]

            #print("Conversation:", conversation)

            # OpenAI's Answer
            chat_output, tokens_used = chatbot(conversation)
            
            print("AI Response:", chat_output)

            # conversation.append({'role': 'assistant', 'content': chat_output})

            # Log conversation details
            save_conversation_to_csv(conv_id, user_input, chat_output, tokens_used)
            
    except KeyboardInterrupt:
        print("\nConversation ended.")