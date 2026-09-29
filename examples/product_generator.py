#!/usr/bin/env python3
"""
product_generator.py

Isomorphic Structural Theory (IST) demo:
- semantic intent is noisy and partial
- structural identity is fixed and absolute
- generation is allowed to be probabilistic
- shape enforcement is decoupled from that generation process

This script shows three strategies side-by-side:
1) Pure IST anchor: every missing slot is filled with deterministic validated_token_{index}
2) Rule-based inference: still deterministic, but slightly smarter
3) Probabilistic mock generation: a simulated model "guesses" values, then the schema clamps them

The point:
The model can inspire the idea.
The schema decides the actual identity.
"""

from typing import Dict, Any, List

CANONICAL_SCHEMA = {
    "product_name": "string",
    "core_mechanic": "string",
    "target_audience": "string",
    "price_tier": "string",
    "market_fit_score": "float",
}

FIELD_ORDER = list(CANONICAL_SCHEMA.keys())


def normalize_value(field_name: str, value: Any) -> Any:
    """Coerce values into the contract expected by the canonical structure."""
    if field_name == "market_fit_score":
        try:
            numeric = float(value)
        except (TypeError, ValueError):
            numeric = 0.0
        return round(max(0.0, min(1.0, numeric)), 2)

    text = str(value).strip()
    if not text:
        return ""
    return text


def deterministic_placeholder(field_name: str, index: int) -> Any:
    """Strict IST fallback: shape remains intact with deterministic placeholders."""
    if field_name == "market_fit_score":
        return 0.0
    return f"validated_token_{index}"


def structural_anchor(raw_intent: Dict[str, Any]) -> Dict[str, Any]:
    """
    The structural anchor engine.
    This is the key IST move:
    - the AI may provide sparse, messy intent
    - the schema is fixed
    - missing values are replaced deterministically
    """
    anchored = {}
    for index, field in enumerate(FIELD_ORDER):
        incoming = raw_intent.get(field)

        if incoming is None or str(incoming).strip() == "":
            anchored[field] = deterministic_placeholder(field, index)
        else:
            anchored[field] = normalize_value(field, incoming)

    return anchored


def infer_rule_based(raw_intent: Dict[str, Any]) -> Dict[str, Any]:
    """
    A deterministic but more intentional fallback.
    This is not "the model decides"; it's a rule-based interpretation of the sparse input.
    """
    product_name = str(raw_intent.get("product_name") or "validated_token_0").strip()
    core_mechanic = str(raw_intent.get("core_mechanic") or "context-aware assistance").strip()
    audience = str(raw_intent.get("target_audience") or "knowledge workers").strip()
    price_tier = str(raw_intent.get("price_tier") or "pro").strip()
    market_fit_score = raw_intent.get("market_fit_score", 0.72)

    name_lower = product_name.lower()
    mechanic_lower = core_mechanic.lower()

    if "student" in name_lower or "study" in name_lower:
        audience = "college students"
    elif "manager" in name_lower or "ops" in name_lower or "workflow" in name_lower:
        audience = "operations teams"
    elif "creator" in name_lower or "video" in name_lower:
        audience = "content creators"
    else:
        audience = "knowledge workers"

    if "automation" in mechanic_lower or "workflow" in mechanic_lower:
        core_mechanic = "workflow automation"
    elif "assistant" in mechanic_lower or "copilot" in mechanic_lower:
        core_mechanic = "AI-assisted decision support"
    else:
        core_mechanic = "structured recommendation engine"

    if "enterprise" in name_lower or "team" in name_lower:
        price_tier = "enterprise"
    elif audience == "college students":
        price_tier = "starter"
    elif audience in {"content creators", "knowledge workers"}:
        price_tier = "pro"
    else:
        price_tier = "custom"

    return {
        "product_name": product_name,
        "core_mechanic": core_mechanic,
        "target_audience": audience,
        "price_tier": price_tier,
        "market_fit_score": round(max(0.0, min(1.0, float(market_fit_score))), 2),
    }


def probabilistic_mock(raw_intent: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simulated probabilistic generation.
    This represents a model "guessing" based on a sparse prompt.
    It is intentionally noisy and less stable than the schema.
    """
    product_name = str(raw_intent.get("product_name") or "Northstar").strip()
    seed = product_name.lower()

    name_map = {
        "northstar": "Northstar",
        "atlas": "AtlasPilot",
        "brief": "BriefCanvas",
        "signal": "SignalLoop",
        "orbit": "OrbitOps",
        "luma": "LumaFlow",
    }

    guessed_name = name_map.get(seed, "Northstar")
    guessed_mechanic = "AI-generated summaries + task orchestration"
    guessed_audience = "operations teams"
    guessed_price = "enterprise"
    guessed_score = 0.88

    if "student" in seed or "study" in seed:
        guessed_audience = "college students"
        guessed_price = "starter"
        guessed_score = 0.71
    elif "creator" in seed or "media" in seed:
        guessed_audience = "content creators"
        guessed_price = "pro"
        guessed_score = 0.82
    elif "ops" in seed or "workflow" in seed:
        guessed_audience = "operations teams"
        guessed_price = "enterprise"
        guessed_score = 0.9

    return {
        "product_name": guessed_name,
        "core_mechanic": guessed_mechanic,
        "target_audience": guessed_audience,
        "price_tier": guessed_price,
        "market_fit_score": round(float(guessed_score), 2),
    }


def print_matrix(rows: List[str], headers: List[str]) -> None:
    widths = [max(len(header), max(len(row.split(" | ")[i]) for row in rows)) for i, header in enumerate(headers)]
    print("  ".join(header.ljust(widths[i]) for i, header in enumerate(headers)))
    print("  ".join("-" * widths[i] for i in range(len(headers))))
    for row in rows:
        values = row.split(" | ")
        print("  ".join(values[i].ljust(widths[i]) for i in range(len(headers))))


def main() -> None:
    print("IST Product Idea Generator")
    print("========================================")
    print("Core thesis: the model provides semantic spark; the structure determines identity.")
    print()

    raw_intent = {
        "product_name": "Northstar",
        "core_mechanic": "assistant for teams",
    }

    print("Simulated sparse AI intent (messy semantic spark):")
    print(raw_intent)
    print()

    pure_ist = structural_anchor(raw_intent)
    rule_based = infer_rule_based(raw_intent)
    probabilistic = probabilistic_mock(raw_intent)

    print("1) Pure IST structural anchor (deterministic + schema-enforced)")
    print(pure_ist)
    print()

    print("2) Rule-based inference (still deterministic, a bit smarter)")
    print(rule_based)
    print()

    print("3) Probabilistic mock generation (simulated model guess)")
    print(probabilistic)
    print()

    print("Side-by-side comparison")
    print("======================")
    headers = ["field", "Pure IST", "Rule-based", "Probabilistic"]
    rows = []
    for field in FIELD_ORDER:
        rows.append(
            f"{field} | {pure_ist.get(field)} | {rule_based.get(field)} | {probabilistic.get(field)}"
        )
    print_matrix(rows, headers)
    print()

    print("Interpretation")
    print("--------------")
    print("- The model's input is noisy and incomplete; that is okay.")
    print("- The canonical schema is fixed and non-negotiable.")
    print("- Missing fields are not 'errors' — they are structurally resolved.")
    print("- IST's claim is simple: semantic generation may be uncertain, but identity enforcement is absolute.")
    print("- The structure is the product. The model is only the spark.")


if __name__ == "__main__":
    main()
