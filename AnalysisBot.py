import requests, json

OPENROUTER_API_KEY = "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"

if OPENROUTER_API_KEY is None:
    print("Please set the OPENROUTER_API_KEY")
    exit(1)

def chat(prompt): 
    system_message = "Please answer from a professional perspective in software engineering, giving answers and explanations. Please do not make up data."

    msg = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
    ]

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}"},
        data=json.dumps({
            "messages": msg,
            "model": "mistralai/mistral-7b-instruct:free"
        })
    )
    
    resp =  response.json()['choices'][0]['message']['content'] # extract the bot's response from the JSON
    print(f"--------\n{resp}\n") # print the bot's response to the console

    #return "Your prompt is: "+prompt
    return resp

