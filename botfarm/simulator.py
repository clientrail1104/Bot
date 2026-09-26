
import random

class CustomerSimulator:
    def __init__(self, persona, scenario, seed=None):
        self.persona = persona
        self.scenario = scenario
        self.random = random.Random(seed)
        self.stage = "initial"
        self.kyc_order = ["mobile", "name", "id_last4", "security_answer"]

    def initial_message(self):
        return self._style(self.scenario.initial_utterance)

    def respond(self, agent_text):
        lower = agent_text.lower()

        if "contact number" in lower or "mobile number" in lower or "nombor telefon" in lower:
            return self._style(self.scenario.kyc_answers["mobile"])

        if "full name" in lower or "nama penuh" in lower or "your name" in lower:
            return self._style(self.scenario.kyc_answers["name"])

        if "last four" in lower or "last 4" in lower or "4 digit" in lower or "empat digit" in lower:
            return self._style(self.scenario.kyc_answers["id_last4"])

        if "security question" in lower or "soalan keselamatan" in lower:
            return self._style(self.scenario.kyc_answers["security_answer"])

        if "human agent" in lower or "officer" in lower or "pegawai" in lower:
            return self._style("Yes, please transfer me.")

        return self._style("Okay.")

    def _style(self, text):
        if self.persona.language == "BM":
            prefix = self.random.choice(["", "Ya, ", "Baik, ", "Okay, "])
        elif self.persona.language == "MIXED":
            prefix = self.random.choice(["", "Okay, ", "Ya, ", "Alright, "])
        else:
            prefix = self.random.choice(["", "Sure, ", "Okay, ", "Alright, "])

        if self.persona.emotion == "angry":
            suffix = self.random.choice([" Please settle this.", " I need this resolved.", " This is frustrating."])
        elif self.persona.emotion == "confused":
            suffix = self.random.choice([" Is that correct?", " I’m not sure.", " Can you explain?"])
        else:
            suffix = ""

        return f"{prefix}{text}{suffix}".strip()
