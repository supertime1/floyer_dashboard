import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Output, Input
import plotly.graph_objects as go

data = pd.read_csv("joint_table.csv")

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]


VALID_USERNAME_PASSWORD_PAIRS = {
    'lu.zhang@sonova.com': 'FloyerSSV123!'
}

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
                html.P(children="❤️", className="header-emoji"),
                html.H1(
                    children="Floyer Dashboard", className="header-title"
                ),
                html.P(
                    children="Dashboard to view the on-going clinical study in"
                             "SSV",
                    className="header-description",
                ),
            ],
            className="header",
        ),

        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Gender", className="menu-title"),
                        dcc.Dropdown(
                            id="gender-filter",
                            options=[
                                {"label": gender, "value": gender}
                                for gender in list(data.gender.unique()) + ['all']
                            ],
                            value="all",
                            clearable=False,
                            className="dropdown",
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(children="Person", className="menu-title"),
                        dcc.Dropdown(
                            id="person-filter",
                            options=[
                                {"label": person, "value": person}
                                for person in list(data.person.unique()) + ['all']
                            ],
                            value="all",
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ],
                ),
            ],
            className='menu'
        ),

        html.Div(
            children=[
                html.Div(
                    children="Age Range",
                    id='output-container-range-slider',
                    className="menu-title"
                ),
                dcc.RangeSlider(
                    id="age-range",
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
                    },
                    className='margin180'
                ),
            ],
            className='wrapper'
        ),

        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="mape-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="data-availability-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)


@app.callback(
    [Output("mape-chart", "figure"), Output("data-availability-chart", "figure"),
     Output('output-container-range-slider', 'children')],
    [
        Input("gender-filter", "value"),
        Input("person-filter", "value"),
        Input("age-range", "value")
    ],
)
def update_charts(gender, person, age):
    if gender == 'all':
        gender = data.gender.unique()
    else:
        gender = [gender]

    if person == 'all':
        person = data.person.unique()

        mask = (
                (data.gender.isin(gender))
                & (data.person.isin(person))
                & ((data.age <= age[1]) & (data.age >= age[0]))
        )
        filtered_data = data.loc[mask, :]

        mape_chart_figure = {
            "data": [
               go.Box(
                   x=filtered_data['activity'],
                   y=filtered_data['mape']
               )
            ],
            "layout":
                go.Layout(title='MAPE vs Activity')
            ,
        }

        da_chart_figure = {
            "data": [
               go.Box(
                   x=filtered_data['activity'],
                   y=filtered_data['da']
               )
            ],
            "layout":
                go.Layout(title='Data Availability vs Activity')
            ,
        }

    else:
        person = [person]
        mask = (
                (data.gender.isin(gender))
                & (data.person.isin(person))
                & ((data.age <= age[1]) & (data.age >= age[0]))
        )
        filtered_data = data.loc[mask, :]

        mape_chart_figure = {
            "data": [
                go.Bar(
                    x=filtered_data['activity'],
                    y=filtered_data['mape']
                )
            ],
            "layout":
                go.Layout(title='MAPE vs Activity')
            ,
        }

        da_chart_figure = {
            "data": [
                go.Bar(
                    x=filtered_data['activity'],
                    y=filtered_data['da']
                )
            ],
            "layout":
                go.Layout(title='Data Availability vs Activity')
            ,
        }

    return mape_chart_figure, da_chart_figure, 'Selected Age Range {}'.format(age)

if __name__ == "__main__":
    app.run_server(debug=True)