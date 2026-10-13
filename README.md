# HEDGEHOG

<!-- ENUMINOUS-NETWORK:START -->
**eNuminous network:** [All repositories](https://enuminous.github.io/EFMW/repositories.html) · [EFMW](https://enuminous.github.io/EFMW/) · [102 equations](https://github.com/enuminous/Monolithic_102_EFMW) · [165 triplets](https://enuminous.github.io/FieldSpace/) · [Zoo](https://enuminous.github.io/Tortoise/) · [Lean](https://enuminous.github.io/Aristotle-102-Monolithic-Lean/) · [Engine](https://enuminous.github.io/Archimedes-Engine/) · [Papers](https://enuminous.github.io/medium/papers-essays-index.html) · [Audit](https://github.com/enuminous/EFMW_Post156_Zoo_Audit/blob/main/portfolio/INTERLOCK_AUDIT.md)

[Repository](https://github.com/enuminous/Hedgehog) · This repository is linked through its source; GitHub Pages is not enabled.

<details>
<summary>Recent repositories (9)</summary>

- [Oroboros](https://github.com/enuminous/Oroboros) · [README](https://github.com/enuminous/Oroboros/blob/main/README.md) · [Page](https://enuminous.github.io/Oroboros/)
- [P-NP](https://github.com/enuminous/P-NP) · [README](https://github.com/enuminous/P-NP/blob/main/README.md) · [Page](https://enuminous.github.io/P-NP/)
- [Research-Program](https://github.com/enuminous/Research-Program) · [README](https://github.com/enuminous/Research-Program/blob/main/README.md) · [Page](https://enuminous.github.io/Research-Program/)
- [I-Have-Guts](https://github.com/enuminous/I-Have-Guts) · [README](https://github.com/enuminous/I-Have-Guts/blob/main/README.md) · [Page](https://enuminous.github.io/I-Have-Guts/)
- [Wrights-Law](https://github.com/enuminous/Wrights-Law) · [README](https://github.com/enuminous/Wrights-Law/blob/main/README.md) · [Page](https://enuminous.github.io/Wrights-Law/)
- [Aristotle-eNuminous](https://github.com/enuminous/Aristotle-eNuminous) · [README](https://github.com/enuminous/Aristotle-eNuminous/blob/main/README.md) · [Page](https://enuminous.github.io/Aristotle-eNuminous/)
- [Multiverse-Simulator](https://github.com/enuminous/Multiverse-Simulator) · [README](https://github.com/enuminous/Multiverse-Simulator/blob/main/README.md) · [Page](https://enuminous.github.io/Multiverse-Simulator/)
- [accelerando-8192](https://github.com/enuminous/accelerando-8192) · [README](https://github.com/enuminous/accelerando-8192/blob/main/README.md) · [Page source](https://github.com/enuminous/accelerando-8192/blob/main/docs/index.html)
- [Codex-888](https://github.com/enuminous/Codex-888) · [README](https://github.com/enuminous/Codex-888/blob/main/README.md) · [Page](https://enuminous.github.io/Codex-888/)

</details>
<!-- ENUMINOUS-NETWORK:END -->

**Held-out Evaluation of Dynamic Generalization, Error, Habitat and Out-of-sample Gain**

HEDGEHOG is the EFMW animal for **generalization**.

Its narrow question is:

> Does an apparent predictive advantage survive genuinely new environments, and can transfer success or failure be explained by preregistered habitat dimensions rather than post-hoc storytelling?

HEDGEHOG is not designed to maximize a benchmark score. It is designed to make overfitting visible.

## Intended uses

- cross-environment validation
- external replication
- AI reliability
- control degradation
- distributed systems
- logistics
- autonomous systems
- forecasting
- any candidate signal developed in one environment and claimed to transfer to another

## Core path

```text
development environments
→ freeze candidate
→ freeze habitat variables
→ untouched environments
→ matched baselines
→ environment-level gain
→ habitat interaction
→ transfer degradation
→ generalization verdict
```

## Canonical habitat dimensions

HEDGEHOG includes the preregisterable dimensions:

- temporal depth
- partial observability
- feedback
- contradiction
- distributed state
- noise

The first five represent structured-complexity dimensions. Noise is treated separately because the habitat hypothesis predicts that useful structure may eventually disappear at a noise ceiling.

## EFMW habitat hypothesis

A testable form is:

> Candidate advantage should tend to increase with structured complexity—temporal depth, partial observability, feedback, contradiction, and distributed state—while eventually degrading under sufficiently high noise.

This is an interaction hypothesis, not permission to explain every result after the fact.

The dimensions, scoring rules, signs, and primary interaction statistic must be frozen before held-out outcomes are examined.

## Flat-stack repository

```text
README.md
LICENSE
CITATION.cff
pyproject.toml
requirements.txt
hedgehog.py
features.py
models.py
metrics.py
freeze.py
environment_schema.json
example_config.yaml
example_data.csv
example_environments.csv
example_run.py
test_hedgehog.py
MANIFEST.sha256
```

## Evaluation levels

HEDGEHOG reports:

1. pooled held-out performance
2. performance in every held-out environment
3. candidate gain over baseline in every environment
4. win rate across environments
5. median environment-level gain
6. worst-environment gain
7. habitat/gain correlations
8. structured-complexity interaction
9. noise interaction
10. transfer degradation from development to held-out environments

## Primary endpoint

The default primary endpoint is:

`median held-out environment ΔBrier`

where:

`ΔBrier = Brier(baseline) - Brier(candidate)`

Positive values favor the candidate.

The habitat analysis is reported separately so a weak overall result cannot be rescued solely by an exploratory subgroup.

## Baseline discipline

The package compares:

- matched raw-state model
- candidate augmented model
- development-only performance
- environment-by-environment held-out performance

For serious use, run HEDGEHOG after BAT has established the conventional baseline set.

## Generalization verdicts

Example verdicts:

- `GENERALIZES`
- `HABITAT-CONDITIONAL`
- `WEAK / INCONCLUSIVE`
- `DOES NOT GENERALIZE`

Thresholds in this repository are demonstration defaults and should be preregistered.

## Installation

```bash
python -m pip install -r requirements.txt
```

## Run

```bash
python example_run.py
```

## Tests

```bash
pytest -q
```

## Freeze

Before observing held-out outcomes, freeze:

- development environment IDs
- held-out environment IDs
- candidate implementation
- conventional baseline
- feature access
- target definition
- habitat dimensions
- habitat scoring rules
- structured-complexity formula
- expected interaction signs
- noise-ceiling hypothesis
- primary endpoint
- minimum material gain
- exclusions
- random seed

Then:

```bash
python freeze.py
```

## Critical warning

Environment metadata can itself leak outcomes.

Habitat scores must describe the environment independently of the candidate's observed performance.

Do not define "high complexity" as "places where EFMW worked."

## Negative results

A failure to generalize is a scientific result.

If development gains disappear on new environments, HEDGEHOG should say so plainly.

## Status

Research software. Experimental.
