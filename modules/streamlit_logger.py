import logging


class StreamlitMemoryHandler(logging.Handler):
    """Custom logging handler to store logs in Streamlit's session state."""

    def __init__(self, st_session_state, *args, **kwargs):
        super(StreamlitMemoryHandler, self).__init__(*args, **kwargs)
        self.st_session_state = st_session_state
        # Initialize logs in session state if not present
        if "logs" not in self.st_session_state:
            self.st_session_state.logs = []

    def emit(self, record):
        # Append the log record to the session state logs
        self.st_session_state.logs.append(self.format(record))
