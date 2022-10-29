from dash import Dash, dcc, html, Input, Output, State
import plotly.express as px
import os
from dotenv import load_dotenv
import praw
from datetime import datetime
import pandas as pd

app = Dash(__name__, suppress_callback_exceptions=True)

load_dotenv()
reddit = praw.Reddit(
    client_id=os.environ["PERSONAL_USE_SCRIPT"],
    client_secret=os.environ["SECRET"],
    user_agent="Unwrap AI Coding Challenge",
)


app.layout = html.Div([
    dcc.Input(id='input-on-submit', type='text', value="politics"),
    html.Button('Submit', id='submit-val', n_clicks=0),
    dcc.Loading(
        id="loading",
        children=[
            html.Div(
                id='btn_output',
                children='Enter a value and press submit'
            ),
            html.H6('Hello?')
        ],
        type="circle",
    )
    
])

def days_of_week_chart(submissions):
    result = [0] * 7
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for timestamp in submissions['created_utc']:
        date = datetime.fromtimestamp(timestamp)
        result[(date.weekday())] += 1

    return dcc.Graph(figure=px.bar(x=days, y=result))

def serialized_subs(subs):
    result = {
        'post_id': [],
        'created_utc': []
    }
    for sub in subs:
        result['post_id'].append(sub.id)
        result['created_utc'].append(sub.created_utc)
    return result


@app.callback(
    # Output('filter', 'test'),
    Output('btn_output', 'children'),
    Input('submit-val', 'n_clicks'),
    State('input-on-submit', 'value')
)
def update_output(n_clicks, value):
    print('HERE')
    try:
        subs = reddit.subreddit(value).top(limit=20)
    except Exception as e:
        return "Subreddit not found."


    return [days_of_week_chart(serialized_subs(subs))]

# @app.callback(
#     # Output('btn_output', 'children'),
#     Output('filter', 'test')
# )
# def filter_output(query):
#     return html.Div([days_of_week_chart(query)])



if __name__ == '__main__':
    app.run_server(debug=True)