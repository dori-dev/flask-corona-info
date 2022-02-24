"""Flask Application
"""
from multiprocessing import Process
from flask import Flask, render_template
from get_info import read_info, read_old_info
from run_spider import run_spider

Process(target=run_spider).start()

app = Flask(__name__)


@app.route("/")
def crawl_info():
    """crawl inforamation
    """
    try:
        info: dict = read_info()
    except IOError:
        info: dict = read_old_info()
    table: dict = info['table_info']
    return render_template(
        "index.html",
        cases=info.get("cases"),
        deaths=info.get("deaths"),
        recovered=info.get("recovered"),
        country=table.get("country"),
        total_cases=table.get("total_cases"),
        new_cases=table.get("new_cases"),
        total_deaths=table.get("total_deaths"),
        new_deaths=table.get("new_deaths"),
        total_recovered=table.get("total_recovered"),
        new_recovered=table.get("new_recovered"),
        active_cases=table.get("active_cases"),
        population=table.get("population")
    )


if __name__ == "__main__":
    app.run()
