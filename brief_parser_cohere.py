import os
import json
import cohere

def parse_brief(brief_text):
    cohere_api_key = os.environ.get("COHERE_API_KEY")
    if not cohere_api_key:
        return {
            "goals": [],
            "deliverables": [],
            "key_dates": [],
            "responsibilities": [],
            "raw_response": "",
            "error": "Missing COHERE_API_KEY environment variable."
        }

    co = cohere.Client(cohere_api_key)

    prompt = f"""
Extract this creative brief into structured JSON.

Brief:
{brief_text}

Return only valid JSON in the following format:
{{
  "goals": [...],
  "deliverables": [...],
  "key_dates": [...],  // must be a list of strings, not a dictionary
  "responsibilities": [{{"person": "...", "role": "..."}}]
}}

Notes:
- Use double quotes in JSON keys/values.
- Do NOT return key_dates as an object with named keys.
- Only return the JSON object. No markdown, no explanation.
"""

    try:
        response = co.chat(
            model="command-r",
            message=prompt,
            temperature=0.3
        )

        raw_response = response.text.strip()

        # Attempt to parse JSON
        result = json.loads(raw_response)

        # Normalize key_dates if it's a dict instead of list
        if isinstance(result.get("key_dates"), dict):
            result["key_dates"] = list(result["key_dates"].values())

        return result

    except json.JSONDecodeError as e:
        return {
            "goals": [],
            "deliverables": [],
            "key_dates": [],
            "responsibilities": [],
            "raw_response": raw_response,
            "error": f"Invalid JSON in response: {str(e)}"
        }

    except Exception as e:
        return {
            "goals": [],
            "deliverables": [],
            "key_dates": [],
            "responsibilities": [],
            "raw_response": "",
            "error": str(e)
        }
