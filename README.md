# Voicebot QA Bot Farm

A local bot farm for automated Voicebot/AI customer simulation and QA regression testing.

## What it does

- Runs many simulated customer bots concurrently
- Supports BM, English and mixed-language personas
- Tests KYC, root-cause identification, resolution and escalation
- Generates pass/fail results
- Saves detailed JSON results and a CSV summary
- Uses only Python standard library

## Quick start

```bash
python run_bot_farm.py
```

Optional:

```bash
python run_bot_farm.py --workers 10 --repeat 5
```

## Project structure

- `run_bot_farm.py` — main runner
- `botfarm/models.py` — data models
- `botfarm/orchestrator.py` — concurrent bot execution
- `botfarm/simulator.py` — customer simulation
- `botfarm/agent_mock.py` — mock target voicebot
- `botfarm/evaluator.py` — automatic QA scoring
- `config/scenarios.json` — test scenarios
- `config/personas.json` — customer personas
- `results/` — generated reports

## Current scope

This version is intentionally local. It does not place real calls, create accounts, send messages or interact with third-party platforms.

To connect a real Voicebot later, replace `MockVoicebotAgent` with an adapter to your approved telephony or Voicebot API.
