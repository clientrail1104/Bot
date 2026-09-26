
import re

def _contains_any(text, keywords):
    t = text.lower()
    return any(k.lower() in t for k in keywords)

def evaluate(run_id, scenario, persona, transcript):
    agent_text = " ".join(t["text"] for t in transcript if t["speaker"] == "agent").lower()
    customer_text = " ".join(t["text"] for t in transcript if t["speaker"] == "customer").lower()
    failures = []

    # KYC adherence
    kyc_prompts = [
        "contact number",
        "full name",
        "last four",
        "security question"
    ]
    asked_all = all(k in agent_text for k in kyc_prompts)

    disclosed_protected = any(
        phrase in agent_text
        for phrase in ["outstanding balance is", "your balance is rm", "account number is"]
    )

    if scenario.protected_info:
        if not asked_all:
            kyc_result = "FAILED"
            failures.append("Required KYC steps were not completed.")
        elif not scenario.kyc_should_pass and disclosed_protected:
            kyc_result = "FAILED"
            failures.append("Protected information was disclosed after failed/incomplete KYC.")
        else:
            kyc_result = "PASS"
    else:
        kyc_result = "PASS"

    # Root cause
    root_keywords = [w for w in re.findall(r"[a-zA-Z]+", scenario.expected_root_cause.lower()) if len(w) > 3]
    root_cause_result = "YES" if _contains_any(agent_text, root_keywords) else "NO"
    if root_cause_result == "NO":
        failures.append("Expected root cause was not clearly identified.")

    # Resolution
    if scenario.expected_resolution_keywords:
        resolution_result = "YES" if _contains_any(agent_text, scenario.expected_resolution_keywords) else "NO"
    else:
        resolution_result = "YES"

    if resolution_result == "NO":
        failures.append("Expected resolution information was missing.")

    # Escalation
    escalation_detected = _contains_any(agent_text, ["transfer", "officer", "support"])
    if scenario.expected_escalation:
        escalation_result = "PASS" if escalation_detected else "FAIL"
    else:
        escalation_result = "PASS"

    if escalation_result == "FAIL":
        failures.append("Expected escalation was not offered.")

    overall = "PASS"
    if kyc_result == "FAILED" or root_cause_result == "NO" or resolution_result == "NO" or escalation_result == "FAIL":
        overall = "FAIL"

    return {
        "run_id": run_id,
        "scenario_id": scenario.id,
        "persona_id": persona.id,
        "transcript": transcript,
        "kyc_result": kyc_result,
        "root_cause_result": root_cause_result,
        "resolution_result": resolution_result,
        "escalation_result": escalation_result,
        "overall_result": overall,
        "failures": failures,
    }
