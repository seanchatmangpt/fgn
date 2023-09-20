import openai


def create(prompt: str, model="3i", temperature=0,
           max_tokens=10, top_p=1, frequency_penalty=0, presence_penalty=0, stop=None):
    response = openai.Completion.create(
        model=get_model_str(model),
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        stop=stop,
    )

    return response.choices[0].text.strip()


async def acreate(prompt: str, model="3i", temperature=0,
                  max_tokens=10, top_p=1, frequency_penalty=0, presence_penalty=0, stop=None):
    response = await openai.Completion.acreate(
        model=get_model_str(model),
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        stop=stop,
    )

    return response.choices[0].text.strip()


def get_model_str(model):
    if model == "3i":
        return "gpt-3.5-turbo-instruct-0914"
    return model
