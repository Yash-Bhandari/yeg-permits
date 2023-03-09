import requests
import datetime

url = "https://data.edmonton.ca/resource/24uj-dj8v.json"


def n_days_ago(n: int) -> datetime.date:
    """Return a date n days ago."""
    return datetime.date.today() - datetime.timedelta(days=n)


def fetch_recent_multifamily():
    # SoQL query parameters
    days_ago = 7 * 3
    earliest_date = n_days_ago(days_ago).strftime("%Y-%m-%d")
    params = {
        "$order": "permit_date DESC",
        "$where": f"permit_date > '{earliest_date}' AND units_added > 10",
    }
    resp = requests.get(url, params=params)
    return resp.json()


def fetch_blatchford_permits(days_ago: int = 365):
    # SoQL query parameters
    earliest_date = n_days_ago(days_ago).strftime("%Y-%m-%d")
    params = {
        "$order": "permit_date DESC",
        "$where": f"permit_date > '{earliest_date}'",
        "neighbourhood": "BLATCHFORD AREA",
    }
    resp = requests.get(url, params=params)
    return resp.json()


# permits = fetch_permits()
# print(*permits[:5], sep="\n")

display_columns = [
    "permit_date",
    "construction_value",
    "units_added",
    "neighbourhood",
    "address",
    "job_description",
    "work_type",
    "floor_area",
]

if __name__ == "__main__":
    import pandas as pd
    from pandasgui import show

    permits = fetch_blatchford_permits()
    if not permits:
        print("No permits found")
        exit(0)
    print(f"Found {len(permits)} permits")
    df = pd.DataFrame(permits)
    df.columns = [x.lower() for x in df.columns]
    show(df[display_columns])
