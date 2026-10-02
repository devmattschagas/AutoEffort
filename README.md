# AutoEffort

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Language: Python](https://img.shields.io/badge/Language-Python-3776AB?logo=python&logoColor=white)
![Version: 1.0](https://img.shields.io/badge/Version-1.0-orange)
![Classifier: Jev](https://img.shields.io/badge/Classifier-Jev-purple)
![Provider: OpenRouter](https://img.shields.io/badge/Provider-OpenRouter-black)

![AutoEffort logo](AutoEffort.jpeg)

**Automatic reasoning-effort selection for LLM agents and harnesses.**

> “Why do automatic cars change gears for efficiency and speed, but we don't have the same thing for tokens?”
>
> — Matheus das Chagas Santos, Electrical Engineering undergraduate at UFES, 2026. Adapted from the project's original comment.

AutoEffort starts from a simple premise: hard tasks need more reasoning, while easy tasks and casual conversation need less. Manually switching effort levels every time is tedious. Your agent should be able to make that decision for you.

AutoEffort uses **Jev**, through the TypeSafe SDK and OpenRouter, to select a reasoning-effort level based on the context you provide. It is intended to be exposed as a tool in Hermes or other agent harnesses, or called directly from your Python programs.

This is a simple classifier: it passes the supplied context and `reasoning_types` to Jev and returns the selected label. It does not discover which efforts the target model supports, validate compatibility, or configure that model.

**Obtain the supported reasoning-effort values from the target model’s capabilities or documentation and supply them through `reasoning_types`. The built-in `low`, `medium`, and `high` values are only “dumb” presets: they are not a universal standard or a guarantee that a request will work.**

The goal is to help you use reasoning effort more efficiently. Correct selections, compatibility, and token or cost savings are not guaranteed.

## Download

On this GitHub repository's page, select **Code → Download ZIP**, then extract the archive and open a terminal in the extracted folder.

Alternatively, clone the repository using the HTTPS URL shown under **Code**:

```bash
git clone <repository-https-url>
cd AutoEffort
```

Replace `<repository-https-url>` with this repository's actual URL.

## Installation

You need Python 3, pip, and an OpenRouter API key. Run the following commands from the project folder.

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export OPENROUTER_API_KEY="your-openrouter-api-key"
```

### Windows (PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:OPENROUTER_API_KEY = "your-openrouter-api-key"
```

These commands set the key for the current terminal session. Keep your real key out of source files and commits.

Run the included greeting example:

```bash
python autoeffort.py
```

This makes a real API request and prints the returned dictionary.

## Usage

Keep `autoeffort.py` alongside your Python script, or otherwise make it importable:

```python
from autoeffort import AutoEffort

# Populate this mapping using efforts supported by your target model.
# Replace the placeholder below before making a real call.
model_efforts = {"<supported-effort>": "When Jev should select this effort"}

result = AutoEffort(
    reasoning_types=model_efforts,
    messages=[
        {"role": "user", "content": "Help me diagnose this circuit."}
    ],
    goal="Find the cause of the circuit failure",
)

print(result)
```

Context is supplied as keyword arguments. You can include messages, the current goal, the task, and other information Jev needs to make the decision. That context is sent to the external API.

### Built-in presets (not guaranteed to work)

Omitting `reasoning_types` uses the following hard-coded labels and rough criteria. They are placeholders for a basic example, not capabilities obtained from your target model. The included greeting example also uses these presets.

| Effort | Default criterion |
| --- | --- |
| `low` | Casual talk and short conversations |
| `medium` | Simple tasks and short to long conversations |
| `high` | Tasks that need reasoning |

### Supply the target model’s supported efforts

First obtain the accepted effort values for the model and provider you will actually call. Then pass those exact values as the keys of `reasoning_types`, with your selection criteria as the values. AutoEffort does not perform this lookup for you.

The following example is applicable **only if you have verified that your target model accepts `low`, `medium`, and `high`**. Otherwise replace the keys with its supported values:

```python
result = AutoEffort(
    reasoning_types={
        "low": "Greetings and straightforward questions",
        "medium": "Tasks requiring a few reasoning steps",
        "high": "Complex debugging or problems requiring careful analysis",
    },
    messages=[
        {"role": "user", "content": "Find the cause of this intermittent bug."}
    ],
    goal="Diagnose the bug",
)
```

## Tool results

A successful classifier call returns a dictionary such as:

```json
{"status": "success", "reasoning": "low"}
```

`status: "success"` means the classifier returned a choice. It does not mean the target model accepts that effort or that the subsequent model request will succeed.

A missing API key returns:

```json
{"status": "error", "message": "There is no API Key configured"}
```

Caught TypeSafe SDK errors also return `status: "error"`, with the SDK error type and description in `message`. These errors are returned directly so a harness can pass them to the agent. Other exceptions are not converted into this result format.

## Integration with Hermes and other harnesses

Register `AutoEffort` through your harness's Python tool mechanism, or wrap it in the tool interface your harness expects. Obtain the target model’s supported efforts and pass them as `reasoning_types` along with the current messages and goal, then pass the returned dictionary back as the tool result.

On success, your integration applies the selected `reasoning` value to a subsequent LLM request, provided the target model supports it. On error, the agent or harness can decide how to continue based on `message`.

AutoEffort selects the effort; your integration configures the LLM request. This repository contains the Python function and a runnable example; harness-specific adapters are left to the integration.

The current classifier model is `~typesafe/jev-latest`, accessed through `https://openrouter.ai/api`.

## Author and license

Created by **Matheus das Chagas Santos**, Electrical Engineering undergraduate at **UFES**.

Version **1.0**, October 2, 2026.

Released under the [MIT License](LICENSE).
