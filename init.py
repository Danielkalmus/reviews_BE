import pandas as pd
import sqlite3

def init_db():
    # merged_df = pd.read_csv('merged_file.csv', dtype={'review': str, 'title': str, 'description': str})
    # merged_df.reset_index(drop=True, inplace=True)
    column_names = ['review', 'title', 'description']
    file_train = pd.read_csv('train.csv', dtype={'review': str, 'title': str, 'description': str})
    file_train.columns = column_names
    file_test = pd.read_csv('test.csv', dtype={'review': str, 'title': str, 'description': str})
    file_test.columns = column_names
    conn = sqlite3.connect('reviews.db')

    if not table_exists(conn, 'reviews'):
        file_train.to_sql('reviews', conn, if_exists='append', index=False)
        file_test.to_sql('reviews', conn, if_exists='append', index=False)

        conn.execute("CREATE INDEX idx_review ON reviews (review);")
        conn.execute("""
         CREATE VIRTUAL TABLE reviews_fts USING fts5(review, title, description);
        """)
        cursor = conn.cursor()
        # Retrieve data from the original 'reviews' table
        cursor.execute("SELECT review, title, description FROM reviews")
        original_data = cursor.fetchall()

        # Insert data into the FTS5 virtual table 'reviews_fts'
        for row in original_data:
            review, title, description = row
            cursor.execute("INSERT INTO reviews_fts (review, title, description) VALUES (?, ?, ?)",
                           (review, title, description))
        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        print("Data transferred successfully to the FTS5 virtual table.")


def table_exists(conn, table_name):
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", [table_name])
    return c.fetchall() != []


if __name__ == "__main__":
    init_db()
