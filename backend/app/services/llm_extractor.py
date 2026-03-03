import json
import re
from app.core.config import settings

MOCK_RESPONSES = [
    {"confidence_score": 0.82, "hedging_score": 0.21, "guidance_score": 0.78, "risk_score": 0.31, "composite_score": 0.73, "signal_label": "bullish", "reasoning": "Strong confidence, raised guidance, minimal hedging."},
    {"confidence_score": 0.45, "hedging_score": 0.68, "guidance_score": 0.41, "risk_score": 0.72, "composite_score": 0.34, "signal_label": "bearish", "reasoning": "Excessive hedging, withdrawn guidance, many risks flagged."},
    {"confidence_score": 0.61, "hedging_score": 0.44, "guidance_score": 0.58, "risk_score": 0.49, "composite_score": 0.55, "signal_label": "neutral", "reasoning": "Mixed signals, guidance maintained but not raised."},
]

def _build_prompt(transcript):
    return (
        "You are a quantitative analyst extracting sentiment signals from an earnings call transcript. "
        "Score the following on axes 0.0-1.0: "
        "confidence_score (1=very confident), hedging_score (1=lots of hedging), "
        "guidance_score (1=raised guidance), risk_score (1=many risks). "
        "Compute composite_score = (confidence + guidance + (1-hedging) + (1-risk)) / 4. "
        "Set signal_label to bullish if composite>0.6, bearish if <0.4, else neutral. "
        "Transcript: " + transcript[:2000] +
        " Respond ONLY with valid JSON: "
        '{"confidence_score":0.0,"hedging_score":0.0,"guidance_score":0.0,'
        '"risk_score":0.0,"composite_score":0.0,"signal_label":"neutral","reasoning":"brief"}'
    )

async def extract_signal(transcript_content: str, ticker: str) -> dict:
    if settings.anthropic_api_key and settings.anthropic_api_key != "your_anthropic_key_here":
        return await _extract_anthropic(transcript_content)
    if settings.openai_api_key and settings.openai_api_key != "your_openai_key_here":
        return await _extract_openai(transcript_content)
    return _mock_extract(ticker)

def _mock_extract(ticker: str) -> dict:
    import hashlib
    idx = int(hashlib.md5(ticker.encode()).hexdigest(), 16) % len(MOCK_RESPONSES)
    return MOCK_RESPONSES[idx]

async def _extract_anthropic(transcript: str) -> dict:
    import anthropic
    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
    response = client.messages.create(
        model="claude-haiku-20240307", max_tokens=400,
        messages=[{"role": "user", "content": _build_prompt(transcript)}]
    )
    text = response.content[0].text
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return json.loads(match.group())
    raise ValueError(f"Could not parse: {text}")

async def _extract_openai(transcript: str) -> dict:
    from openai import OpenAI
    client = OpenAI(api_key=settings.openai_api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini", max_tokens=400,
        messages=[{"role": "user", "content": _build_prompt(transcript)}]
    )
    text = response.choices[0].message.content
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return json.loads(match.group())
    raise ValueError(f"Could not parse: {text}")
