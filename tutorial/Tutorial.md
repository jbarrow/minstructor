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

- getting structured output into a python object
- using pydantic for validation and retries
- using llms as validators

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

This will create a new python package called `minstructor`, with the following structure:

```
minstructor
|- minstructor
|  |- __init__.py
|- tests
|  |- __init__.py
|- poetry.lock
|- pyproject.toml
|- README.md
```

We need two dependencies for this to work, so let's go ahead and get those installed as well:

```sh
poetry add openai pydantic
```

And now we're set!

## Getting Structured Output: Asking for JSON

The simplest way to get structured JSON is to ask the model to return it.
For instance:

```python
from openai import OpenAI

client = OpenAI(api_key=<YOUR_API_KEY>)

client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a world-class information extraction system. Given [X] you extract [Y] must always respond with valid JSON."
        },
        {
            "role": "user",
            "content": ""
        }
    ],
    model="gpt-4-turbo",
    temperature=0
)

print(client.response.choices[0].content)
```

Response:
```

```

As you can see, we're getting back valid json embedded in our message.
However, without some kind of parsing or extracting it's not useful to us in code.
In addition, the format of the JSON isn't fixed -- they model chooses what keys to use.
So we can [...]

## Getting Structured Output: Tool Usage

Thankfully, OpenAI and other LLM providers offer features such as "tool usage," where we can provide a schema to the LLM.

ASIDE: ⚠️ Limitations of Tool Usage

Note, however, that there are differing levels of guardrails.
OpenAI does not promise that we get back an object that _adheres perfectly to our schema_.
Only that we get back a _valid json object_.
This subtlety will lead to some headaches down the line, but we'll look at how to handle those in the validators section [link to validators].

There _are_ providers that will guarantee a return object that adheres to the schema, notably AnyScale and [OTHER PROVIDERS].
They use a constrained generation approach to ensure that the model can only generate tokens that would adhere to the schema.
How that works is a topic for a future post, but is an interesting problem in and of itself.

Going back to OpenAI [...]

## Getting Structured Output: Pydantic

Pydantic will be the interface between the LLM and our code.
We will use it for three things:
1. to **generate the JSON schema** above,
2. to **parse the model response** into a python object, and;
3. to **validate any errors in the model response**.

### Generating JSON Schema

```
model.model_dumps_schema()
```

### Parsing the Model Response

```
model.[]
```

### Validation


## Prompt Engineering Your Pydantic Class

To improve our responses, we can document our object.
Let's take a look at the json schemas that are returned using some different pydantic features.

### Annotating the Object

Add a description to the object itself:

```python
class Model(BaseModel):
    """ comment """

print(model.schema())
```

### Adding Descriptions and Examples

Add a description to each of the fields.
Use the Pydantic `Field` object:

```python
class Model(BaseModel):
    x: int = Field(..., description="")
```

### Chain-of-Thought

A really neat benefit of using this approach is that it's easy to do things like chain of thought prompting.

```python
class Model(BaseModel):
    chain_of_thought: str = Field(..., description="Think step-by-step to arrive at the right answer.")
    x: int
```

## Conclusion

Now we've gotten to a point where we can define a schema in python, prompt the LLM, and get a response back.


## Extension: Modes 101: Supporting AnyScale

This post covers only the core of what instructor does.
If you want to support, say, Claude (which uses xml for tool usage) or other providers/approaches, then the above code wouldn't be sufficient.
For this, `instructor` uses the idea of `MODES`, which I have left out for brevity's sake.

But I think it's worthwhile to look at how to support AnyScale, which offers constrained decoding.

## Extension: LLM Validators

The validators that we've seen are very simple, and provide checks on types and values.
But we can use LLMs to validate the textual/semantic content of values as well.
Doing this requires only writing some custom validators.

## Extension: Metaprogramming Pydantic

