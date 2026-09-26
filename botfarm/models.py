
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional

@dataclass
class Persona:
    id: str
    language: str
    emotion: str
    speaking_style: str
    interrupt_probability: float = 0.0

@dataclass
class Scenario:
    id: str
    name: str
    initial_utterance: str
    protected_info: bool
    expected_root_cause: str
    expected_resolution_keywords: List[str]
    expected_escalation: bool
    kyc_answers: Dict[str, str]
    kyc_should_pass: bool

@dataclass
class Turn:
    speaker: str
    text: str

@dataclass
class TestResult:
    run_id: str
    scenario_id: str
    persona_id: str
    transcript: List[Dict[str, str]]
    kyc_result: str
    root_cause_result: str
    resolution_result: str
    escalation_result: str
    overall_result: str
    failures: List[str]

    def to_dict(self):
        return asdict(self)
