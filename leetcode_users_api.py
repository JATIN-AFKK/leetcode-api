from fastapi import FastAPI
import requests
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/leetcode/user/{username}")
def fetch_data(username: str):
    url = "https://leetcode.com/graphql/"
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
        "variables": {"username": username},
        "operationName": "userSessionProgress"
    }

    response = requests.post(url, json=payload)
    
    try:
        data = response.json()  # parse JSON response
    except Exception:
        data = {"error": "Failed to parse response", "raw": response.text}

    return JSONResponse(content=data, status_code=response.status_code)