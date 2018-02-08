from funcytaskengine.event_fulfillment.return_values import EmptyValues
from funcytaskengine.initiators.base import BaseInitiator


class NoopInitiator(BaseInitiator):

    def __init__(self, *args, **kwargs):
        pass

    def apply_overrides(self, event_results):
        pass

    def execute(self, *args, **kwargs):
        return EmptyValues()
