from flask import Flask, render_template
from fetcher import fetch_recent_multifamily, fetch_permit
from datetime import datetime

app = Flask(__name__)


def format_permits(permits):
    for permit in permits:
        format_permit(permit)


def format_permit(permit):
    permit_date = permit["permit_date"].split("T")[0]
    permit["permit_date"] = datetime.strptime(permit_date, "%Y-%m-%d").strftime(
        "%b %d, %Y"
    )
    permit["description_preview"] = permit["job_description"][:75]
    if len(permit["job_description"]) > 75:
        permit["description_preview"] += "..."


@app.route("/")
def index():
    permits = fetch_recent_multifamily(100)
    format_permits(permits)
    return render_template("permits.html", permits=permits, days_ago=100)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/permits/<permit_id>")
def permit_detail(permit_id):
    permit = fetch_permit(permit_id)
    format_permit(permit)
    if permit is None:
        return "No such permit found"
    return render_template("permit_detail.html", permit=permit)
