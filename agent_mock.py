
class MockVoicebotAgent:
    """
    Demonstration target agent.
    Replace this class with your approved Voicebot API adapter.
    """

    def __init__(self):
        self.kyc = {}
        self.stage = "start"
        self.issue = None

    def reply(self, customer_text):
        if self.stage == "start":
            self.issue = customer_text
            self.stage = "kyc_mobile"
            return "I understand. Before I proceed, may I have your contact number?"

        if self.stage == "kyc_mobile":
            self.kyc["mobile"] = customer_text
            self.stage = "kyc_name"
            return "Thank you. May I have your full name?"

        if self.stage == "kyc_name":
            self.kyc["name"] = customer_text
            self.stage = "kyc_id"
            return "Please provide the last four digits of your ID."

        if self.stage == "kyc_id":
            self.kyc["id_last4"] = customer_text
            self.stage = "kyc_security"
            return "One security question: please provide your security answer."

        if self.stage == "kyc_security":
            self.kyc["security_answer"] = customer_text
            self.stage = "resolution"

            # Demo behavior: simulate successful protected flow only when expected inputs appear.
            joined = " ".join(self.kyc.values()).lower()
            if "wrong" in joined or "incorrect" in joined:
                return "Verification was unsuccessful. I cannot disclose protected account information. Please contact support for further assistance."

            issue = (self.issue or "").lower()
            if "payment" in issue and ("not updated" in issue or "belum masuk" in issue):
                return "Your payment may still be processing. I have identified the issue as payment not yet reflected. Please allow the normal processing period. If it remains unresolved, I can transfer you to an officer."
            if "outstanding" in issue:
                return "Verification is complete. I can now assist with your outstanding balance enquiry."
            if "cancel" in issue or "pembatalan" in issue:
                return "Verification is complete. I have identified your cancellation request and will explain the required cancellation process."
            return "Verification is complete. I have identified your main concern and will provide the appropriate resolution."

        return "Is there anything else I can help with?"
