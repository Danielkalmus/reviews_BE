from flask import Flask, render_template
from flask_paginate import Pagination, get_page_args
import sqlite3
import pandas as pd

app = Flask(__name__)
app.template_folder = ''


def get_reviews(offset=0, per_page=10):
    conn = sqlite3.connect('your_database.db')
    # merged_df.to_sql('reviews', conn, if_exists='replace', index=False)
    query = f"SELECT title, description FROM reviews LIMIT {per_page} OFFSET {offset}"
    result_df = pd.read_sql_query(query, conn)

    result_list = result_df.to_dict(orient='records')
    print(f'result_list = {result_list}')

    # Close the connection
    conn.close()
    return result_list


def get_total_reviews_number():
    conn = sqlite3.connect('your_database.db')
    query = "SELECT COUNT (*) FROM reviews"
    total_reviews_number = pd.read_sql_query(query, conn)
    count_value = total_reviews_number.values[0][0].item()
    print(count_value)
    return count_value



@app.route('/')
def index():
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    total = get_total_reviews_number()
    pagination_users = get_reviews(offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')
    return render_template('index.html',
                           users=pagination_users,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


if __name__ == '__main__':
    app.run(debug=True)
