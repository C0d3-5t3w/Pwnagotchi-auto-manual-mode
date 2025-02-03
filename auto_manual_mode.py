import logging
from pwnagotchi.plugins import BasePlugin

class AutoManualMode(BasePlugin):
    __author__ = 'c0d3-5t3w'
    __version__ = '1.0.0'
    __license__ = 'MIT'
    __description__ = 'Switches to manual mode after 15 missed handshakes for use when traveling to fast.'

    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.missed_handshakes = 0
        self.manual_mode_triggered = False

    def on_loaded(self):
        self.log.info("AutoManualMode plugin loaded!")

    def on_epoch(self, agent, epoch_data):
        missed = agent.status.get('missed', 0)
        self.log.debug(f"Missed handshakes: {missed}")

        if missed >= 15 and not self.manual_mode_triggered:
            self.log.info("15 missed handshakes detected. Switching to manual mode.")
            self.switch_to_manual(agent)
            self.manual_mode_triggered = True  # Prevent repeated switches.

        # Reset if missed handshakes drop below threshold.
        if missed < 15 and self.manual_mode_triggered:
            self.manual_mode_triggered = False

    def switch_to_manual(self, agent):
        if agent.mode != 'manual':
            agent.set_mode('manual')
            self.log.info("Pwnagotchi is now in manual mode.")
        else:
            self.log.info("Pwnagotchi is already in manual mode.")
