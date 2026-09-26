
class RealVoicebotAdapter:
    """
    Template for connecting an approved Voicebot API.

    Implement:
      - start_session()
      - send_text(text)
      - close_session()

    Keep credentials outside source code, e.g. environment variables.
    """

    def start_session(self):
        raise NotImplementedError

    def send_text(self, text):
        raise NotImplementedError

    def close_session(self):
        raise NotImplementedError
