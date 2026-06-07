import requests

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiYXVkIjoiaHR0cDovLzIwLjI0NC41Ni4xNDQvZXZhbHVhdGlvbi1zZXJ2aWNlIiwiZW1haWwiOiJmaXJkb3NhbGlsZW81NkBnbWFpbC5jb20iLCJleHAiOjE3ODA4MTU5NzQsImlhdCI6MTc4MDgxNTA3NCwiaXNzIjoiQWZmb3JkIE1lZGljYWwgVGVjaG5vbG9naWVzIFByaXZhdGUgTGltaXRlZCIsImp0aSI6IjU2MzYwNjU4LTY0YjQtNGI3MS04YmVmLTFmMWMwNjU2Mjg3OCIsImxvY2FsZSI6ImVuLUlOIiwibmFtZSI6ImttIGZpcmRvcyBhbGkiLCJzdWIiOiI5MmQyNjc3Yy1hODU4LTQ3MjQtOGU3YS02ZDUzMmFjZjViZWYifSwiZW1haWwiOiJmaXJkb3NhbGlsZW81NkBnbWFpbC5jb20iLCJuYW1lIjoia20gZmlyZG9zIGFsaSIsInJvbGxObyI6IjIwMjMwMDM0MDYiLCJhY2Nlc3NDb2RlIjoid2dLdGdaIiwiY2xpZW50SUQiOiI5MmQyNjc3Yy1hODU4LTQ3MjQtOGU3YS02ZDUzMmFjZjViZWYiLCJjbGllbnRTZWNyZXQiOiJxckhjQ0dOcmpZZmJzTWZEIn0.1CLeRcgKuihk4jtFaq7sqjTqYldGKSq7DP4QXGALEsI"

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
            n = len(vehicles)

            dp = [[0] * (capacity + 1) for _ in range(n + 1)]

            for i in range(1, n + 1):

                duration = vehicles[i - 1]["Duration"]
                impact = vehicles[i - 1]["Impact"]

                for h in range(capacity + 1):

                    if duration <= h:
                        dp[i][h] = max(
                            dp[i - 1][h],
                            dp[i - 1][h - duration] + impact
                        )
                    else:
                        dp[i][h] = dp[i - 1][h]

            selected_tasks = []
            h = capacity

            for i in range(n, 0, -1):

                if dp[i][h] != dp[i - 1][h]:

                    selected_tasks.append(vehicles[i - 1])

                    h -= vehicles[i - 1]["Duration"]

            selected_tasks.reverse()

            total_duration = sum(
                task["Duration"] for task in selected_tasks
            )

            total_impact = sum(
                task["Impact"] for task in selected_tasks
            )

            print("\n" + "=" * 60)
            print(f"Depot ID: {depot['ID']}")
            print(f"Available Mechanic Hours: {capacity}")
            print(f"Maximum Impact Score: {total_impact}")
            print(f"Total Hours Used: {total_duration}")
            print(f"Number of Selected Tasks: {len(selected_tasks)}")

            print("\nSelected Tasks:")

            for task in selected_tasks:
                print(
                    f"TaskID: {task['TaskID']} | "
                    f"Duration: {task['Duration']} | "
                    f"Impact: {task['Impact']}"
                )

    else:
        print("Unable to fetch API data")

except Exception as e:
    print("Error:", e)
