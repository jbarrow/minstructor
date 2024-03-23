# `minstructor` Tutorial

In my opinion, perhaps the most useful thing you can do with current LLMs is to convert unstructured information into a structured form.
This is necessary if you want to, say, extract all [...] or [...].
It's the foundation of a lot of the work that I've done over the past year and a half, and I expect I'll be doing a lot more of it in the future.

If you have ever attempted to get structured output from an LLM, you've probably seen Jason Liu's `instructor` library.
It's a small, focused library that enables you to get typed, structured objects back from LLM calls.
Simply define a `pydantic` object (effectively, a typed struct in Python), pass it to a patched OpenAI client (or AnyScale or other provider), and you get back a usable Python object:

```python
import instructor
import openai

from pydantic import BaseModel


client = instructor.patch(openai.OpenAI())

class Test(BaseModel):
    x: int
    y: int

response = client.chat.completions.create(
    messages=[{ "role": "user", "content": "" }],
    response_model=Test,
    temperature=0.0
)


print(response.x)
print(response.y)
```

This is a powerful paradigm, and enables you 
The goal of this tutorial is to build a simpler version of this library, `minstructor`, which walks you through a lot of the core ideas.
This includes:

- getting structured output into a pydantic object
- using pydantic for validation and retries
- using llms as validators
- different "modes", which allow you to prompt other models (e.g. through AnyScale or multimodal via `gpt-4-vision-preview`)

By the end, we'll be able to do something similar to the above:

```python
import minstructor
import openai

from pydantic import BaseModel


class Test(BaseModel):
    x: int
    y: int

client = openai.OpenAI()

response = minstructor.create_chat_completion(
    client,
    messages=[{}],
    response_model=Test
)

print(response.model.x)
print(response.model.y)
```

## Getting Started

I'm going to use `poetry` as a package manager for this, so the first step will be to install it:

```sh
pip install poetry
```

Then, we can create a new project:

```sh
poetry new minstructor
```

## Getting Structured Output: Asking for JSON


## Getting Structured Output: Tool Usage


## Getting Structured Output: Pydantic

## An Aside: Chain-of-Thought

## Getting Structured Output: Validation


## Extension: Better Validators


## Extension: LLM Validation


## Modes: AnyScale


## Modes: Structure from Multimodal Prompts


## Bonus: Dynamic Structured Objects?

## Afterword
