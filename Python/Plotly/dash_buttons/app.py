from dash import Dash, html
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME, dbc.icons.BOOTSTRAP])

buttons = html.Div(
    [
        dbc.Button("Primary", color="primary", className="me-1" ),
        dbc.Button("Secondary", color="secondary", className="me-1"),
        dbc.Button("Success", color="success", className="me-1"),
        dbc.Button("Warning", color="warning", className="me-1"),
        dbc.Button("Danger", color="danger", className="me-1"),
        dbc.Button("Info", color="info"),
    ], className= "m-4"
)

button_2 = html.Div(
    [
        dbc.Button("Regular", className="me-1"),
        dbc.Button("Outline", outline=True, color="primary", className="me-1"),
        dbc.Button("Disabled", disabled=True, className="me-1"),
        dbc.Button("Large", size="lg", className="me-1"),
        dbc.Button("Small", size="sm", className="me-1"),
        dbc.Button("Link", color="link")
    ], className="me-4"
)

# Adding icons.
FA_icon = html.I(className="fa-solid fa-cloud-arrow-down me-2")
FA_button = dbc.Button([FA_icon, "Download"], className="me-2")

BS_icon = html.I(className="bi bi-cloud-arrow-down-fill me-2")
BS_button = dbc.Button([BS_icon, "Download"]
                       )


# Dash iconify
from dash_iconify import DashIconify
download_icon = DashIconify(icon="bi:cloud-download", style={"marginRight":5})
download_button = dbc.Button([download_icon, "Download"], className="me-2")

settings_icon = DashIconify(icon="carbon:settings-check", style={"marginRight":5})
settings_button = dbc.Button([settings_icon, "Settings"])


app.layout = dbc.Container([buttons, button_2, FA_button, BS_button,
                            download_button, settings_button])

if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=False)
