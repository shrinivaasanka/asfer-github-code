import serpapi
import json

def google_finance_search_quote(apikey,ticker):
    client = serpapi.Client(api_key=apikey)
    results = client.search({ "engine": "google_finance", "q": ticker })
    jsonfile=open("testlogs/GoogleSearchSerpApi.json","w")
    print(results.data)
    json.dump(results.data,jsonfile)

if __name__=="__main__":
    google_finance_search_quote(apikey="794c4cb1585ed9d90908972adb14fbd4e6fcec9204a6fcc2a90468dbba53c983",ticker="ICICIBANK:NSE")
