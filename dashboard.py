# dashboard.py
from qtpylib.reports import Reports


class Dashboard(Reports):
    pass  # we just need the name


# open web to http://localhost:5000
if __name__ == "__main__":
    dashboard = Dashboard(
        port=5000,
        blotter="MainBlotter"
    )
    dashboard.run()
