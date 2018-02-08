import logging
import subprocess

from funcytaskengine.event_fulfillment.return_values import ValuesContainer
from funcytaskengine.initiators.base import BaseInitiator


logger = logging.getLogger(__name__)


class SubprocessInitiator(BaseInitiator):

    def __init__(self, type, command, overrides=()):
        self.command = command
        self.overrides = overrides

    def apply_overrides(self, event_results):
        """
        Extracts previous values and applies them to the command.

        I'm really not sure of the security implications of this...
        """
        for override in self.overrides:
            event_name, event_value_prop, to_replace = override.split(':')

            v = event_results.return_value_from_name(event_name) \
                .first() \
                .prop(event_value_prop)

            for i, part in enumerate(self.command):
                if part == to_replace:
                    self.command[i] = v

    def execute(self, event_results, *args, **kwargs):
        logger.debug({
            'message': 'executing_command_raw',
            'command': self.command,
        })

        self.apply_overrides(event_results)

        logger.debug({
            'message': 'executing_command_with_overrides',
            'command': self.command,
        })

        p = subprocess.Popen(self.command)
        returncode = p.wait()
        return ValuesContainer(returncode)
