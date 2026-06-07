import requests

TOKEN = input("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiYXVkIjoiaHR0cDovLzIwLjI0NC41Ni4xNDQvZXZhbHVhdGlvbi1zZXJ2aWNlIiwiZW1haWwiOiJmaXJkb3NhbGlsZW81NkBnbWFpbC5jb20iLCJleHAiOjE3ODA4MTUxNTIsImlhdCI6MTc4MDgxNDI1MiwiaXNzIjoiQWZmb3JkIE1lZGljYWwgVGVjaG5vbG9naWVzIFByaXZhdGUgTGltaXRlZCIsImp0aSI6IjUzNDgzNmI5LWNkZWMtNDMyOS04Y2E1LWY1N2QyOTQwNGRjOCIsImxvY2FsZSI6ImVuLUlOIiwibmFtZSI6ImttIGZpcmRvcyBhbGkiLCJzdWIiOiI5MmQyNjc3Yy1hODU4LTQ3MjQtOGU3YS02ZDUzMmFjZjViZWYifSwiZW1haWwiOiJmaXJkb3NhbGlsZW81NkBnbWFpbC5jb20iLCJuYW1lIjoia20gZmlyZG9zIGFsaSIsInJvbGxObyI6IjIwMjMwMDM0MDYiLCJhY2Nlc3NDb2RlIjoid2dLdGdaIiwiY2xpZW50SUQiOiI5MmQyNjc3Yy1hODU4LTQ3MjQtOGU3YS02ZDUzMmFjZjViZWYiLCJjbGllbnRTZWNyZXQiOiJxckhjQ0dOcmpZZmJzTWZEIn0.oJU62jdmgPhPr_aXNNSped5WN2vbPQtAFFj5podChi0")

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
                    dp[h] = max(dp[h], dp[h - duration] + impact)

            print(
                f"Depot {depot['ID']} -> Maximum Impact Score = {dp[capacity]}"
            )

    else:
        print("Unable to fetch API data")

except Exception as e:
    print("Error:", e)
