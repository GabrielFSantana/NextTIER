import requests

url = "https://exercisedb.p.rapidapi.com/exercises"

querystring = {"limit":"10","offset":"0"}

headers = {
	"x-rapidapi-key": "5face91d51msh8dd0e2cd75f71d4p1a8b67jsnba852f929a59",
	"x-rapidapi-host": "exercisedb.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())