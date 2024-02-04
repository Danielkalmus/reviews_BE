from flask import Flask, render_template, request, send_file
from flask_paginate import Pagination, get_page_args
import sqlite3
import pandas as pd

app = Flask(__name__)
app.template_folder = ''

def get_reviews(sentiment = "all", offset=0, per_page=10):
    query_addition = ""
    conn = sqlite3.connect('your_database.db')
    # merged_df.to_sql('reviews', conn, if_exists='replace', index=False)

    match sentiment:
        case "all":
            query_addition = ""
        case "positive":
            query_addition = "WHERE review = 2"
        case "negative":
            query_addition = "WHERE review = 1"

    query = f"SELECT title, description FROM reviews {query_addition} LIMIT {per_page} OFFSET {offset} "
    result_df = pd.read_sql_query(query, conn)

    # Close the connection
    conn.close()
    return result_df


@app.route('/export_to_excel')
def export_to_excel(sentiment = "all", offset=0, per_page=10):
    result_df = get_reviews(sentiment, offset, per_page)
    result_df.to_excel('reviews.xlsx')
    return send_file('reviews.xlsx', mimetype='application/vnd.ms-excel')


def get_reviews_as_dict(sentiment = "all", offset=0, per_page=10):
    result_df = get_reviews(sentiment, offset, per_page)
    result_list = result_df.to_dict(orient='records')
    print(f'result_list = {result_list}')


def get_total_reviews_number(sentiment = "all"):
    conn = sqlite3.connect('your_database.db')
    query_addition = ""
    query_base = "SELECT COUNT (*) FROM reviews "
    match sentiment:
        case "all":
            query_addition = ""
        case "positive":
            query_addition = "WHERE review = 2"
        case "negative":
            query_addition = "WHERE review = 1"
    print(query_base+query_addition)
    total_reviews_number = pd.read_sql_query(query_base+query_addition, conn)
    count_value = total_reviews_number.values[0][0].item()
    print(count_value)
    return count_value

@app.route('/')
def index():
    sentiment = request.args.get('sentiment')
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    total = get_total_reviews_number(sentiment = sentiment)
    pagination_reviews = get_reviews(sentiment = sentiment, offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4', href="?page={0}&sentiment=" + str(sentiment))
    return render_template('index.html',
                           reviews=pagination_reviews,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


if __name__ == '__main__':
    app.run(debug=True)
