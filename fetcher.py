from requests_cache import CachedSession
import datetime

url = "https://data.edmonton.ca/resource/24uj-dj8v.json"


def n_days_ago(n: int) -> datetime.date:
    """Return a date n days ago."""
    return datetime.date.today() - datetime.timedelta(days=n)

# building permits don't get updated that often. we can cache the results for a while
session = CachedSession(cache_name="cache", expire_after=datetime.timedelta(hours=1))

def fetch_recent_multifamily(days_ago=21):
    earliest_date = n_days_ago(days_ago).strftime("%Y-%m-%d")
    # SoQL query parameters
    params = {
        "$order": "permit_date DESC",
        "$where": f"permit_date > '{earliest_date}' AND units_added > 10",
    }
    resp = session.get(url, params=params)
    return resp.json()


def fetch_blatchford_permits(days_ago: int = 365):
    # SoQL query parameters
    earliest_date = n_days_ago(days_ago).strftime("%Y-%m-%d")
    params = {
        "$order": "permit_date DESC",
        "$where": f"permit_date > '{earliest_date}'",
        "neighbourhood": "BLATCHFORD AREA",
    }
    resp = session.get(url, params=params)
    return resp.json()


def fetch_permit(permit_id: str):
    params = {"row_id": permit_id}
    resp = session.get(url, params=params)
    data = resp.json()
    return data[0] if len(data) > 0 else None


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
