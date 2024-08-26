import requests

def fetch_google_ads_data(access_token):
    url = "https://googleads.googleapis.com/vX/customers/{customer_id}/googleAds:searchStream"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    params = {
        "query": "SELECT campaign.id, ad_group.id, ad_group_ad.ad.id, ad_group_ad.ad.name FROM ad_group_ad"
    }
    response = requests.post(url, headers=headers, json=params)
    response.raise_for_status()
    return response.json()

# Exemple d’utilisation
if __name__ == "__main__":
    access_token = 'YOUR_GOOGLE_ACCESS_TOKEN'
    data = fetch_google_ads_data(access_token)
    print(data)
