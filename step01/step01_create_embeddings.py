import os
import openai
import json
import csv
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Reads and returns the content of a file
def open_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as infile:
            return infile.read()
    except FileNotFoundError as e:
        print(f"File not found: {filepath}")
        raise e

# Saves payload to a JSON file
def save_json(filepath, payload):
    try:
        with open(filepath, 'w', encoding='utf-8') as outfile:
            json.dump(payload, outfile, ensure_ascii=False, sort_keys=True, indent=4)
    except Exception as e:
        print(f"Error saving JSON: {e}")
        raise e

# Generates and returns GPT-3 embedding for given content.
def gpt3_embedding(content, engine='text-embedding-ada-002'):
    try:
        print('CONTENT TO EMBED:', content)
        content = content.encode(encoding='ASCII', errors='ignore').decode()
        response = openai.Embedding.create(input=content, engine=engine)
        vector = response['data'][0]['embedding']
        return vector
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None

# Processes a CSV file to generate embeddings and saves them in a JSON file
def process_csv_file(csv_path, json_directory, json_filename='qa_embeddings.json', delimiter=';'):
    if not os.path.exists(json_directory):
        os.makedirs(json_directory)
    json_path = os.path.join(json_directory, json_filename)
    qa_list = []
    try:
        with open(csv_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=delimiter)
            next(reader, None)  
            for row in reader:
                if len(row) == 2:
                    question, answer = row
                    question_embedding = gpt3_embedding(question)
                    answer_embedding = gpt3_embedding(answer)
                    qa_list.append({
                        "question": question,
                        "question_embedding": question_embedding,
                        "answer": answer,
                        "answer_embedding": answer_embedding
                    })
                else:
                    print(f"Skipping row due to unexpected format: {row}")
        save_json(json_path, qa_list)
    except Exception as e:
        print(f"Error processing CSV file: {e}")
        raise e
    
if __name__ == "__main__":
    openai.api_key = os.getenv('OPENAI_API_KEY')
    csv_path = "papers_csv/aichallenge.csv"
    out_path = "qa_json/"

    # Process the CSV file and save to a single JSON file
    process_csv_file(csv_path, out_path)

