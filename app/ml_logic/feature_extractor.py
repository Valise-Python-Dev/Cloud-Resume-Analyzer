from typing import Dict, Any
import re

DATE_RE = re.compile(r'(\d{4})')

def estimate_years_experience(parsed: Dict[str, Any]) -> float:
    # Simple heuristic: 1 year per experience block found
    # You can improve this logic later if needed
    exp_blocks = parsed.get("experience", [])
    if not exp_blocks:
        # Fallback: Count mentions of years in text
        raw = parsed.get("raw_text", "")
        dates = DATE_RE.findall(raw)
        if len(dates) >= 2:
            try:
                return float(int(max(dates)) - int(min(dates)))
            except:
                pass
        return 1.0
    return float(len(exp_blocks)) * 2.0

def count_skills(parsed: Dict[str, Any]) -> int:
    return len(parsed.get("skills", []))

def formatting_score(parsed: Dict[str, Any]) -> float:
    score = 0.0
    n_sections = len(parsed.get("sections", []))
    score += min(n_sections, 5) * 2.0
    if parsed.get("emails"): score += 3.0
    if parsed.get("phones"): score += 2.0
    return score

def extract_features(parsed: Dict[str, Any]) -> Dict[str, float]:
    feats = {}
    feats["years_exp"] = estimate_years_experience(parsed)
    feats["skill_count"] = count_skills(parsed)
    feats["format_score"] = formatting_score(parsed)
    feats["num_experience_items"] = len(parsed.get("experience", [])) if "experience" in parsed else 0
    return feats