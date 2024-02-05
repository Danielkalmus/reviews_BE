'''import pandas as pd
import sqlite3

def most_common_words():

  conn = sqlite3.connect('reviews.db')
  result_df = pd.read_sql_query("""
  select word, count(*) from (
  select (case when instr(substr(reviews.description, nums.n+1), ' ') then substr(reviews.description, nums.n+1)
             else substr(reviews.description, nums.n+1, instr(substr(reviews.description, nums.n+1), ' ') - 1)
        end) as word
  from (select ' '||description as description
      from reviews
     )reviews cross join
     (select 1 as n union all select 2 union all select 3
     ) nums
  where substr(reviews.description, nums.n, 1) = ' ' and substr(reviews.description, nums.n, 1) <> ' '
  ) w
  group by word
  order by count(*) desc
  """, conn)
  return result_df

if __name__ == "__main__":
  most_common_words()'''
