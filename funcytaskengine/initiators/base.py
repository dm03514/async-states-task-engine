from abc import ABCMeta, abstractmethod

import functools
from collections import namedtuple

from funcytaskengine.event_fulfillment.return_values import EventResults


class BaseInitiator(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self, **kwargs):
        pass


PreviousResultOverride = namedtuple(
    'PreviousResultOverride',
    ['event_name', 'target_attr', 'value_prop'],
)


class ExtractPreviousResults(object):
    def __init__(self, *overrides):
        self.overrides = overrides

    def __call__(self, fn):
        @functools.wraps(fn)
        def decorated(wrapped_self, event_results=None, **kwargs):
            assert isinstance(event_results, EventResults)

            for override in self.overrides:
                setattr(
                    wrapped_self,
                    override.target_attr,
                    event_results
                        .return_value_from_name(override.event_name)
                        .first(override.value_prop)
                )

            result = fn(wrapped_self, **kwargs)
            return result
        return decorated

