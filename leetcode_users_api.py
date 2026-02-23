from fastapi import FastAPI
import requests
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/leetcode/user/{username}")
def fetch_data(username: str):
    url = "https://leetcode.com/graphql/"
    

    userList : str = username.split(',')
    output = {}
    for user in userList:
        payload = {
        "query": """
            query userSessionProgress($username: String!) {
              allQuestionsCount {
                difficulty
                count
              }
              matchedUser(username: $username) {
                submitStats {
                  acSubmissionNum {
                    difficulty
                    count
                    submissions
                  }
                  totalSubmissionNum {
                    difficulty
                    count
                    submissions
                  }
                }
              }
            }
            """,
            "variables": {"username": user},
            "operationName": "userSessionProgress"
        }
        response = requests.post(url, json = payload, headers = {
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/json"
          }
        )

        try:
            data = response.json()
        except Exception:
            data = {"error": "Failed to parse response", "raw": response.text}
        output[user] = data
    return JSONResponse(content = output)