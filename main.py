from dash import Dash, dcc, html, Input, Output
from dash_bootstrap_components.themes import BOOTSTRAP
import plotly.express as px
from src.components.layout import create_layout
import pandas as pd
from bs4 import BeautifulSoup
import requests


def main() -> None:
    app = Dash(
         __name__,
        external_stylesheets=[BOOTSTRAP],
        routes_pathname_prefix='/dash/'
        )
    app.title = "Diasoft dashboard"
    app.layout = create_layout(app)

    app.run_server(debug=True)


if __name__ == "__main__":
    main()
