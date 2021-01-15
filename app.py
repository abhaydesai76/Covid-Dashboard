import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output

data = pd.read_csv("owid-covid-data.csv")
data["date"] = pd.to_datetime(data["date"], format="%Y-%m-%d")
data.sort_values(["iso_code", "date"], inplace=True)

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.title = "Covid Cases by Country"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(children="Covid Cases Analysis", style={"textAlign": "center", "color": "brown",
                                                                "fontWeight": "bold", "fontSize": 36}),
                html.H6(children="(Data Source: https://ourworldindata.org/)",
                        style={"textAlign": "center", "color": "steelblue"})
            ]
        ),
        html.Div(children=[
            html.Div(
                children=[
                    html.Div(children="Country", className="menu-title"),
                    dcc.Dropdown(id="country-filter",
                                 options=[
                                     {"label": country, "value": country}
                                     for country in np.sort(data.location.unique())
                                 ],
                                 value="Afghanistan",
                                 clearable=False,
                                 searchable=True,
                                 className="dropdown")
                ]
            ),
            html.Div(children=[
                html.Div(
                    children=[
                        html.Div(children="Date Range", className="menu-title"),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=data.date.min().date(),
                            max_date_allowed=data.date.max().date(),
                            start_date=data.date.min().date(),
                            end_date=data.date.max().date()
                        )
                    ]
                )]
            ),
            html.Div(children=[
                html.Div(
                    children=[
                        dcc.Graph(id="country-new-cases")
                    ]
                ),
                html.Div(
                    children=[
                        dcc.Graph(id="country-total-cases")
                    ]
                )
            ])
        ]
        )
    ]
)


@app.callback(
    [Output("country-new-cases", "figure"), Output("country-total-cases", "figure")],
    [Input("country-filter", "value"), Input("date-range", "start_date"), Input("date-range", "end_date")]
)
def update_charts(country, start_date, end_date):
    mask = (
        (data.location == country)
        & (data.date >= start_date)
        & (data.date <= end_date)
    )

    filtered_data = data.loc[mask, :]

    country_new_cases_figure = {
        "data": [
            {
                "x": filtered_data["date"],
                "y": filtered_data["new_cases"],
                "type": "bar"
            }
        ]
    }

    country_total_cases_figure = {
        "data": [
            {
                "x": filtered_data["date"],
                "y": filtered_data["total_cases"],
                "type": "bar"
            }
        ]
    }

    return country_new_cases_figure, country_total_cases_figure


if __name__ == "__main__":
    app.run_server(debug=True)
