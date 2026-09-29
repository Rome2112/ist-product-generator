# ist-product-generator

A compact demonstration of Isomorphic Structural Theory (IST): semantic intent is generated probabilistically, but structural identity is enforced deterministically.

## What this repo demonstrates

The goal is to show the core IST claim:

- The model can provide a noisy, partial, creative semantic spark.
- The canonical schema is fixed and non-negotiable.
- Missing fields are not errors; they are structurally resolved.
- Structural identity is enforced before the output is accepted.

This is a proof-of-concept script that compares three strategies side by side:

1. **Pure IST anchoring** with deterministic `validated_token_{index}` fallbacks.
2. **Rule-based inference** that is still deterministic but more intentional.
3. **A simulated probabilistic model guess** that is then normalized into the schema.

## Run the demo

```bash
python examples/product_generator.py
```

## Why IST matters

Traditional AI workflows often couple generation and validation. A model produces an answer, then validation fails, then retries happen, then structure is repaired after the fact.

IST proposes a cleaner boundary:

- **generation** is noisy and creative
- **structure** is fixed and authoritative
- the schema decides the identity, not the model

This repo keeps the demo intentionally small and readable so the philosophy is easy to see.
