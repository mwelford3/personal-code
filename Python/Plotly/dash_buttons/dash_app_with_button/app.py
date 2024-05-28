from dash import Dash, html, Input, Output, State
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.PULSE])

form = dbc.FormFloating(
    [
        dbc.Input(id="username"),
        dbc.Label("Enter username.")
    ]
)
button = dbc.Button("Submit")
output_container = html.Div(className="mt-4")

app.layout = dbc.Container([form, button, output_container], fluid=True)

@app.callback(
    Output(output_container, "children"),
    Input(button, "n_clicks"),
    State("username", "value"),
    prevent_initial_call=True
)
def greet(_, name):
    return f"Welcome {name}!" if name else "Please enter username."


if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=False)