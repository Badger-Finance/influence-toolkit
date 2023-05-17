import requests

from influence_toolkit.constants import LLAMA_DASHBOARD_URL


def get_usd_vlaura_hh():
    r = requests.post(
        LLAMA_DASHBOARD_URL,
        json={"id": "bribes-overview-aura"},
    ).json()

    dollar_per_lock_asset = r["dashboard"]["epochs"][-1]["dollarPerVlAsset"]

    return dollar_per_lock_asset
