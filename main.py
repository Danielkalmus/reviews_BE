import pandas as pd
from flask import Flask, request, jsonify
import sqlite3
import streamlit as st



app = Flask(__name__)

#merged_df = pd.read_csv('merged_file.csv', dtype={'review': str, 'title': str, 'description': str})
#merged_df.reset_index(drop=True, inplace=True)

@app.route('/get_similar_results_by_word', methods=['GET'])
def find_similar_word(word):
    word = request.args.get('word')


def load_from_sql_server(review_value):
    conn = sqlite3.connect('your_database.db')
    # merged_df.to_sql('reviews', conn, if_exists='replace', index=False)
    query = f"SELECT title, description FROM reviews WHERE review = '{review_value}' LIMIT 3"
    result_df = pd.read_sql_query(query, conn)

    result_list = result_df.to_dict(orient='records')
    print(f'result_list = {result_list}')

    # Close the connection
    conn.close()
    return result_list


@app.route('/get_result_by_review_number', methods=['GET'])
def get_reviews():
    # Get the review value from the UI (assuming it's sent as a query parameter)
    review_value = request.args.get('review')
    result_df = load_from_sql_server(review_value)
    return result_df


if __name__ == '__main__':
    app.run(debug=True)
