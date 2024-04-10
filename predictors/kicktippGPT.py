"""
Predictor who asks ChatGPT to predict the outcome.
"""
from .config import OPENAI_API_KEY
from openai import OpenAI
from helper.match import Match
from .base import PredictorBase

class kicktippGPT(PredictorBase):

    def predict(self, match: Match):
        client = OpenAI(api_key=OPENAI_API_KEY)

        team_a = match.hometeam
        team_b = match.roadteam

        messages=[
            {"role": "system", "content": "You are a predictor of football games of the german Bundesliga. For Your predictions You use the performance of the teams in their recent matches."},
            {"role": "user", "content": "Please give me a prediction for the number of goals scored by " + team_a + " and " + team_b + " in their next match, listing " + team_a + "'s goals first. Answer only with the numbers, separated by a colon."}
        ]

        completion = client.chat.completions.create(model="gpt-4",messages=messages)

        answer = completion.choices[0].message.content

        try:
            score_a = int(answer.split(":")[0])
            score_b = int(answer.split(":")[1])
        except:
            messages.append({"role": "assistant", "content": answer })
            messages.append({"role": "user", "content": "In this case, just give a guess. Answer only with the numbers, separated by a colon and listing " + team_a + "'s goals first."})
            completion = client.chat.completions.create(model="gpt-4",messages=messages)
            answer = completion.choices[0].message.content
            score_a = int(answer.split(":")[0])
            score_b = int(answer.split(":")[1])

        return (score_a,score_b)