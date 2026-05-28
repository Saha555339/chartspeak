import json

from chartspeak.spec import ChartSpec

SYSTEM_PROMPT = """\
You are a data visualisation assistant. Given a dataset description and a user request,
output a JSON object that matches the ChartSpec schema exactly.

Rules:
- Use only column names that appear in the dataset description.
- Set 'agg' whenever chart is 'bar' or 'line' and x is categorical or group_by is set.
- For 'histogram' x must be numeric.
- Do not include extra keys.
"""


def build_user_prompt(dataset_description: str, user_request: str) -> str:
    schema_str = json.dumps(ChartSpec.json_schema(), indent=2)
    return f"Dataset:\n{dataset_description}\n\nSchema:\n{schema_str}\n\nRequest: {user_request}"


def build_repair_prompt(
    dataset_description: str,
    user_request: str,
    previous_spec: str,
    error_message: str,
) -> str:
    return (
        f"{build_user_prompt(dataset_description, user_request)}\n\n"
        f"Previous attempt:\n{previous_spec}\n\n"
        f"Validation error: {error_message}\n\n"
        "Fix the spec so it passes validation."
    )
