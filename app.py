from flask import Flask, render_template, request, jsonify
import openai
import pandas as pd
import numpy as np
from config import OPENAI_API_KEY
from openai.embeddings_utils import get_embedding
from openai.embeddings_utils import cosine_similarity
import csv

openai.api_key = OPENAI_API_KEY

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('query')
    query_vector = get_embedding(query, engine="text-embedding-ada-002")
    df = pd.read_csv('feeds_embeddings.csv')
    df['embedding'] = df['embedding'].apply(eval).apply(np.array)
    df["similarities"] = df['embedding'].apply(lambda x: cosine_similarity(x, query_vector))
    sorted_by_similarity = df.sort_values("similarities", ascending=False).head(3)
    if not query:
        return render_template('index.html', message='Please enter a search query')
    # Perform the search logic here (e.g. search a database or list of items)
    # For this example, we will simply filter the mock results based on the query
    search_results = sorted_by_similarity['text'].values.tolist()
    return render_template('search.html', results=search_results, query=query)

@app.route('/static/<path:filename>')
def serve_static(filename):
    return app.send_static_file(filename)



# Handing new csv line
@app.route('/save-csv', methods=['POST'])
def save_csv():
    print('received a request')
    data = request.get_json()
    print(data)
    text = data['text']

    # get embedding
    embedding = get_embedding(text, engine="text-embedding-ada-002")

    # get row count
    with open('feeds_embeddings.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        row_count = sum(1 for row in csvreader)

    # write new row
    with open('feeds_embeddings.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([row_count, text, embedding])

    return jsonify(success=True)


if __name__ == '__main__':
    app.run(debug=True)