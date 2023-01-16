from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st

"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""
#@title
import requests
import pandas as pd
import json

token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJ1c2VyIjp7ImlkIjozMDIwNzMyNjQsImVtYWlsIjoibG9pYy5jYWx2eUBibG9vbWF5cy5jb20iLCJhcHBsaWNhdGlvbiI6MzAwMjIyNjM1fX0.Vex1LoYSDbQmQf_wgsU4sQ-GBduO-cFUkRBNmx_2jluJafRPxKfp9BxNYTBewYeWnCUkxjYIp3aTj5VofCSSRQ'

url = "https://api.pipefy.com/graphql"

file_name = 'pipefy'

#payload = "{\"query\":\"{ allCards (pipeId:X) { edges { node { id title fields { name report_value updated_at value } } } }} \"}"
payload = "{\"query\":\"{ allCards (pipeId:X) {     edges {       node {         id         title         fields {           name           report_value           updated_at           value         }       }     }     pageInfo {       endCursor     }   } }"


headers = {
    "authorization": f"Bearer {token}",
    "content-type": "application/json"
    }
has_next_page = True
first_query = True
pipe_id = "302417396"
json_data = {}
records_df = pd.DataFrame()
while(has_next_page):
  if first_query:
    payload = {"query": "{ allCards (pipeId:\""+pipe_id+"\") { edges { node { id title fields { name report_value updated_at value } } } pageInfo {endCursor hasNextPage}}}"}
    first_query = False
  else:
    payload = {"query": "{ allCards (pipeId:\""+pipe_id+"\",after:\""+end_cursor+"\") { edges { node { id title fields { name report_value updated_at value } } } pageInfo {endCursor hasNextPage}}}"}


  response = requests.request("POST", url, json=payload, headers=headers)
  json_data = json.loads(response.text)
  end_cursor =json_data['data']['allCards']["pageInfo"]["endCursor"] 
  has_next_page = json_data["data"]["allCards"]["pageInfo"]["hasNextPage"]
  total_records_pg = len(json_data["data"]["allCards"]["edges"])
  for i in range(total_records_pg):
        card_title = json_data["data"]["allCards"]["edges"][i]["node"]["title"]
        card_data_d = json_data["data"]["allCards"]["edges"][i]["node"]["fields"]
        card_data = {x['name']:x['value'] for x in card_data_d}
        records_df = records_df.append(card_data, ignore_index=True)

records_df.info()

job = records_df

job.drop(['Commentaire ✪','Monday Sprint Planning'], axis=1, inplace=True) 
job['Raison de la perte'] = job['Raison de la perte'].fillna('Autre')
job['Canal de communication du client'].unique() 
job['Validé en interne'].unique() 
job.drop(['Confirmer la publication','Détails'], axis=1, inplace=True)
job['Date pour débriefing CV'] = job['Date pour débriefing CV'].fillna(0)

print(job)

with st.echo(code_location='below'):
    total_points = st.slider("Number of points in spiral", 1, 5000, 2000)
    num_turns = st.slider("Number of turns in spiral", 1, 100, 9)

    Point = namedtuple('Point', 'x y')
    data = []

    points_per_turn = total_points / num_turns

    for curr_point_num in range(total_points):
        curr_turn, i = divmod(curr_point_num, points_per_turn)
        angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
        radius = curr_point_num / total_points
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        data.append(Point(x, y))

    st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
        .mark_circle(color='#0068c9', opacity=0.5)
        .encode(x='x:Q', y='y:Q'))
