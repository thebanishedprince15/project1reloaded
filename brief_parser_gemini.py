import os
import json
import re
import google.generativeai as genai

def parse_brief(brief_text):
    gemini_api_key = os.environ.get("GOOGLE_GEMINI_API_KEY")
    if not gemini_api_key:
        return {
            "goals": [],
            "deliverables": [],
            "key_dates": [],
            "responsibilities": [],
            "raw_response": "",
            "error": "Missing GOOGLE_GEMINI_API_KEY environment variable."
        }

    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""
Extract the following from this creative brief and return only valid JSON:
- goals: list of strings
- deliverables: list of strings
- key_dates: list of strings
- responsibilities: list of dicts with 'person' and 'role'

Brief:
{brief_text}

Format:
{{
  "goals": [...],
  "deliverables": [...],
  "key_dates": [...],
  "responsibilities": [{{"person": "...", "role": "..."}}]
}}

Rules:
- Use double quotes for all keys and values.
- Do NOT include explanations or markdown. Only return the JSON object.
"""

    try:
        response = model.generate_content(prompt)
        raw_response = response.text.strip()

        # Remove Markdown wrapping if present
        if raw_response.startswith("```"):
            raw_response = re.sub(r"^```(?:json)?\s*", "", raw_response)
            raw_response = re.sub(r"\s*```$", "", raw_response)

        # Parse the JSON safely
        result = json.loads(raw_response)

        # Normalize key_dates if returned as a dict
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
