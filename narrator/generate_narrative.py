generate_scr_narrative

from google import genai
import json


def generate_narrative(findings):
    client = genai.Client()

    system_instruction = """
You are a senior data analyst writing for Mamaearth's regional ops and finance heads.

Write the narrative using exactly three labeled sections:
Situation
Complication
Resolution

Every number in the output must come from the supplied findings and must appear with the same value.
Do not invent, estimate, calculate, round, or introduce any statistics that are not present in the supplied findings.
"""

    contents = f"""
Using the supplied verified findings below, write a concise business narrative.

Supplied findings:
{json.dumps(findings, indent=2)}

Make sure the narrative contains the three required sections:
Situation
Complication
Resolution
"""
      try
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents,
        config={
            "system_instruction": system_instruction
        }
    )

    return response.text









parameter locking and error handling

from google import genai
import json


def generate_narrative(findings):
    client = genai.Client()

    system_instruction = """
You are a senior data analyst writing for Mamaearth's regional ops and finance heads.

Write the narrative using exactly three labeled sections:
Situation
Complication
Resolution

Every number in the output must come from the supplied findings and must appear with the same value.
Do not invent, estimate, calculate, round, or introduce any statistics that are not present in the supplied findings.
"""



Supplied findings:
{json.dumps(findings, indent=2)}

Make sure the narrative contains the three required sections:
Situation
Complication
Resolution
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config={
                "system_instruction": system_instruction,
                # Temperature 0.0 makes the factual business report deterministic,
                # rather than treating it like creative writing.
                "temperature": 0.0,
                "max_output_tokens": 500,
            },
            timeout=30,
        )

        return {
            "status": "success",
            "narrative": response.text,
            "tokens": getattr(response.usage_metadata, "total_token_count", None)
        }

    except Exception as err:
        return {
            "status": "error",
            "narrative": None,
            "message": str(err)
        }






offline fallback path task 4

def generate_scr_narrative_offline(findings: dict) -> dict:
    """
    Fallback function that generates SCR sections deterministically
    using f-strings without making network calls or requiring API keys.
    """
    situation = (
        f"Analysis indicates an initial operational state with key baseline "
        f"metrics recorded at {findings.get('baseline_metric', 'N/A')} across "
        f"the targeted systems."
    )

    complication = (
        f"However, an observed variance of {findings.get('variance', 'N/A')} was "
        f"detected, leading to {findings.get('impact_count', 0)} identified issues "
        f"that impact system performance."
    )

    resolution = (
        f"To resolve this, execute step {findings.get('recommended_step', 1)} "
        f"to achieve the target threshold of {findings.get('target_metric', 'N/A')} "
        f"and restore full stability."
    )

    return {
        "situation": situation,
        "complication": complication,
        "resolution": resolution
    }


def generate_scr_narrative(findings: dict, api_key: str | None = None) -> dict:
    """
    Main function attempting API generation, falling back to offline mode
    if no API key is set or if the API call returns an error.
    """
    if not api_key:
        return generate_scr_narrative_offline(findings)

    try:
        # Example primary API call logic
        response = call_external_scr_api(findings, api_key)

        # Check if the API response itself signals an error status
        if response.get("status") == "error":
            return generate_scr_narrative_offline(findings)

        return {
            "situation": response["data"]["situation"],
            "complication": response["data"]["complication"],
            "resolution": response["data"]["resolution"]
        }

    except Exception:
        # Fallback on network errors, exceptions, or timeouts
        return generate_scr_narrative_offline(findings)



task 5

def check_narrative_figures(narrative: str) -> bool:
    """
    Check that the generated narrative contains all five required findings.
    Commas are ignored when checking numeric values.
    """
    normalized = narrative.replace(",", "")

    checks = {
        "Cleaned revenue 97,358.30": "97358.3",
        "COD return rate 44.4%": "44.4",
        "COD + Tier-2 return rate 54.5%": "54.5",
        "Duplicate reconciliation delta 2,501.90": "2501.9",
        "March peak revenue 20,318.90": "March",
    }

    # March must also appear with the peak revenue figure.
    checks["March peak revenue 20,318.90"] = (
        "March" if "March" in narrative and "20318.9" in normalized else None
    )

    all_passed = True

    for label, value in checks.items():
        passed = value is not None and value in normalized
        print(f"{'PASS' if passed else 'FAIL'} — {label}")
        if not passed:
            all_passed = False

    return all_passed
2. Make the March check specifically require both values


def check_narrative_figures(narrative: str) -> bool:
    normalized = narrative.replace(",", "")

    checks = [
        ("Cleaned revenue", "97358.3"),
        ("COD return rate", "44.4"),
        ("COD + Tier-2 highest-risk rate", "54.5"),
        ("Duplicate reconciliation delta", "2501.9"),
    ]

    all_passed = True

    for label, figure in checks:
        passed = figure in normalized
        print(f"{'PASS' if passed else 'FAIL'} — {label}: {figure}")
        if not passed:
            all_passed = False

    march_peak_passed = "March" in narrative and "20318.9" in normalized
    print(
        f"{'PASS' if march_peak_passed else 'FAIL'} — "
        "March peak revenue: March + 20318.9"
    )

    if not march_peak_passed:
        all_passed = False

    return all_passed
3. Save the actual online Gemini output

After Gemini produces the narrative:

with open("narrator/sample_output.txt", "w", encoding="utf-8") as f:
    f.write(result["narrative"])

print("\nNarrative figure checker:")
check_narrative_figures(result["narrative"])

Then you can also verify exactly what the grader will see:

with open("narrator/sample_output.txt", "r", encoding="utf-8") as f:
    saved_narrative = f.read()

print("\nSaved sample_output.txt checker:")
check_narrative_figures(saved_narrative)

You want the output to look like:

Narrative figure checker:
PASS — Cleaned revenue: 97358.3
PASS — COD return rate: 44.4
PASS — COD + Tier-2 highest-risk rate: 54.5
PASS — Duplicate reconciliation delta: 2501.9
PASS — March peak revenue: March + 20318.9

Saved sample_output.txt checker:
PASS — Cleaned revenue: 97358.3
PASS — COD return rate: 44.4
PASS — COD + Tier-2 highest-risk rate: 54.5
PASS — Duplicate reconciliation delta: 2501.9
PASS — March peak revenue: March + 20318.9

