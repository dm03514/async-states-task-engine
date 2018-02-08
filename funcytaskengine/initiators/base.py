from abc import ABCMeta, abstractmethod


class BaseInitiator(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self, event_results, *args, **kwargs):
        pass

    @abstractmethod
    def apply_overrides(self, event_results):
        pass
