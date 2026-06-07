import requests

TOKEN = "PASTE_YOUR_ACCESS_TOKEN_HERE"

headers = {
    "Authorization": f"Bearer {TOKEN}"
}

try:
    depots_response = requests.get(
        "http://4.224.186.213/evaluation-service/depots",
        headers=headers
    )

    vehicles_response = requests.get(
        "http://4.224.186.213/evaluation-service/vehicles",
        headers=headers
    )

    print("Depots API Status:", depots_response.status_code)
    print("Vehicles API Status:", vehicles_response.status_code)

    if depots_response.status_code == 200 and vehicles_response.status_code == 200:

        depots = depots_response.json()["depots"]
        vehicles = vehicles_response.json()["vehicles"]

        for depot in depots:

            capacity = depot["MechanicHours"]

            dp = [0] * (capacity + 1)

            for vehicle in vehicles:

                duration = vehicle["Duration"]
                impact = vehicle["Impact"]

                for h in range(capacity, duration - 1, -1):
                    dp[h] = max(
                        dp[h],
                        dp[h - duration] + impact
                    )

            print(
                f"Depot {depot['ID']} -> Maximum Impact Score = {dp[capacity]}"
            )

    else:
        print("Unable to fetch data from APIs")
        print(depots_response.text)
        print(vehicles_response.text)

except Exception as e:
    print("Error:", e)
