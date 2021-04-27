import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Output, Input
import plotly.graph_objects as go
import plotly.express as px
import json

with open('user_lst.json', ) as f:
    VALID_USERNAME_PASSWORD_PAIRS = json.load(f)

data = pd.read_csv("joint_table.csv")

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)
server = app.server
app.title = "Floyer Dashboard!"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children='❤️', className='header-emoji'),
                html.H1(
                    children='Floyer Dashboard', className='header-title'
                ),
                html.P(
                    children='Dashboard to view the on-going clinical study in SSV',
                    className='header-description',
                ),
            ],
            className='header',
        ),

        html.Div(
            children=[
                html.Div(
                    children=[
                        html.H2(children='Project', className='menu-title'),
                        dcc.Dropdown(
                            id='project-filter',
                            options=[
                                {'label': project, 'value': project}
                                for project in list(data.project.unique()) + ['all']
                            ],
                            value='all',
                            multi=False,
                            clearable=False,
                        )
                    ]
                ),
                html.Div(
                    children=[
                        html.H2(children='Subject', className='menu-title'),
                        dcc.Dropdown(
                            id='subject-filter',
                            options=[
                                {'label': subject, 'value': subject}
                                for subject in list(data.person.unique()) + ['all']
                            ],
                            value='all',
                            multi=True,
                            clearable=False,
                        ),
                    ],
                )
            ],
            className='menu'
        ),

        html.Div(
            children=[
                html.H2(children='Project Demographic Overview', className='block-title'),
                html.Div(
                    children=[
                        dcc.Graph(
                            id='pie_gender',
                            className='plot'
                            ),
                        dcc.Graph(
                            id='pie_race',
                            className='plot'
                            ),
                        dcc.Graph(
                            id='hist_age',
                            className='plot'
                            ),
                    ],
                    className='flex-block'
                )
            ],
            className='block'
        ),

        html.Div(
            children=[
                html.H2(children='Data Filter', className='block-title'),
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.H3(children='Demographic Filter', className='block-title'),
                                html.H4(children='Gender', className='block-title'),
                                dcc.Dropdown(
                                    id='gender-filter',
                                    options=[
                                        {'label': gender, 'value': gender}
                                        for gender in list(data.gender.unique()) + ['all']
                                    ],
                                    value='all',
                                    multi=False,
                                    clearable=False,
                                ),
                                html.H4(children='Race', className='block-title'),
                                dcc.Dropdown(
                                    id='race-filter',
                                    options=[
                                        {'label': race, 'value': race}
                                        for race in list(data.race.unique()) + ['all']
                                    ],
                                    value='all',
                                    multi=True,
                                    clearable=False,
                                ),
                                html.H4(children='Age Range', className='block-title'),
                                dcc.RangeSlider(
                                    id='age-range',
                                    min=20,
                                    max=80,
                                    step=5,
                                    value=[20, 80],
                                    marks={
                                        20: {'label': '20'},
                                        30: {'label': '30'},
                                        40: {'label': '40'},
                                        50: {'label': '50'},
                                        60: {'label': '60'},
                                        70: {'label': '70'},
                                        80: {'label': '80'}
                                    }
                                ),
                            ],
                            className='sub-block'
                        ),
                        html.Div(
                            children=[
                                html.H3(children='Firmware & Algorithm Filter', className='block-title'),
                                html.H4(children='Firmware Version', className='block-title'),
                                dcc.Dropdown(
                                    id='firmware-filter',
                                    # options=[
                                    #     {'label': firmware, 'value': firmware}
                                    #     for firmware in list(data.firmware.unique())
                                    # ],
                                    multi=False,
                                    clearable=False,
                                ),
                                html.H4(children='Algorithm Version', className='block-title'),
                                dcc.Dropdown(
                                    id='algorithm-filter',
                                    # options=[
                                    #     {'label': algorithm, 'value': algorithm}
                                    #     for algorithm in list(data.algorithm.unique())
                                    # ],
                                    multi=False,
                                    clearable=False,
                                ),
                                html.H4(children='Quality Factor', className='block-title'),
                                dcc.RangeSlider(
                                    id='quality-factor-range',
                                    min=0,
                                    max=100,
                                    step=5,
                                    marks={
                                        0: {'label': '0'},
                                        10: {'label': '10'},
                                        20: {'label': '20'},
                                        30: {'label': '30'},
                                        40: {'label': '40'},
                                        50: {'label': '50'},
                                        60: {'label': '60'},
                                        70: {'label': '70'},
                                        80: {'label': '80'},
                                        90: {'label': '90'},
                                        100: {'label': '100'}
                                    }
                                ),
                            ],
                            className='sub-block'
                        ),
                    ],
                    className='flex-block'
                ),
            ],
            className='block'
        ),

        html.Div(
            children=[
                html.H2(children='Statistics Overview', className='block-title'),
                html.Div(
                    children=[
                        html.Div(
                            dcc.Graph(
                                id="mape-chart", config={"displayModeBar": False},
                            ),
                            className='sub-block'
                        ),
                        html.Div(
                            dcc.Graph(
                                id="data-availability-chart", config={"displayModeBar": False},
                            ),
                            className='sub-block'
                        ),
                    ],
                    className='flex-block'
                ),
            ],
            className='block',
        ),
    ]
)

@app.callback(
    [
        Output('hist_age', 'figure'),
        Output('pie_gender', 'figure'),
        Output('pie_race', 'figure')
    ],
    [
        Input('project-filter', 'value'),
        Input('subject-filter', 'value')
    ]
)
def update_demographic(project, subject):
    if project == 'all':
        project = data.project.unique()
    else:
        project = [project]

    if not subject:
        return px.histogram(), px.pie(), px.pie()
    elif 'all' in subject:
        subject = data.person.unique()
    else:
        subject = subject

    mask = (data.project.isin(project)) & (data.person.isin(subject))
    filter_data = data.loc[mask, :]
    age = filter_data.drop_duplicates(['project', 'person']).age
    gender = filter_data.drop_duplicates(['project', 'person']).groupby('gender').size().reset_index(
        name='counts')
    race = filter_data.drop_duplicates(['project', 'person']).groupby('race').size().reset_index(
            name='counts')

    hist_age_figure = {
        'data': [go.Histogram(x=age)],
        'layout': go.Layout(title='Age', height=350, bargap=0.1)
    }
    pie_gender_figure = {
        'data': [go.Pie(values=gender['counts'], labels=gender['gender'])],
        'layout': go.Layout(title='Gender', height=350)
    }
    pie_race_figure = {
        'data': [go.Pie(values=race['counts'], labels=race['race'])],
        'layout': go.Layout(title='Race', height=350)
    }
    return hist_age_figure, pie_gender_figure, pie_race_figure


@app.callback(
    [
        Output('mape-chart', 'figure'),
        Output('data-availability-chart', 'figure')
    ],
    [
        Input('project-filter', 'value'),
        Input('subject-filter', 'value'),
        Input('gender-filter', 'value'),
        Input('race-filter', 'value'),
        Input('age-range', 'value'),
        # Input('firmware-filter', 'value'),
        # Input('algorithm-filter', 'value'),
        # Input('quality-factor-range', 'value')
    ],
)
def update_statistics_charts(project, subject, gender, race, age):
    if project == 'all':
        project = data.project.unique()
    else:
        project = [project]

    if not subject:
        return px.box(), px.box()
    elif 'all' in subject:
        subject = data.person.unique()
    else:
        subject = subject

    if gender == 'all':
        gender = data.gender.unique()
    else:
        gender = [gender]

    if not race:
        return px.box(), px.box()
    elif 'all' in race:
        race = data.race.unique()
    else:
        race = race

    mask = (
            (data.project.isin(project)) &
            (data.person.isin(subject)) &
            (data.gender.isin(gender)) &
            (data.race.isin(race)) &
            ((data.age <= age[1]) & (data.age >= age[0]))
    )

    filtered_data = data.loc[mask, :]

    mape_chart_figure = {
        "data": [
            go.Box(
                x=filtered_data['mape'],
                y=filtered_data['activity'],
                orientation='h'
            )
        ],
        "layout":
            go.Layout(title='MAPE vs Activity')
        ,
    }

    da_chart_figure = {
        "data": [
            go.Box(
                x=filtered_data['da'],
                y=filtered_data['activity'],
                orientation='h'
            )
        ],
        "layout":
            go.Layout(title='Data Availability vs Activity')
        ,
    }

    return mape_chart_figure, da_chart_figure

if __name__ == "__main__":
    app.run_server(debug=True)