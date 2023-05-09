def onInput(self):
    import json
    import os

    import openai
    openai.api_key = os.environ["OPENAI_API_KEY"]
    model = "text-embedding-ada-002"
    prompt = self.input
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=100,
        n=100,
        stop=None,
        temperature=0.5,
        presence_penalty=2,
        frequency_penalty=2
    )

    score_str = response.choices[0].text
    print(str(score_str))

onInput(node)