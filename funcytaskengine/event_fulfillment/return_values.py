from abc import ABCMeta, abstractmethod


class EventResults(object):
    def __init__(self):
        self.by_event_name = {}
        self.in_order = []

    def add(self, return_value):
        self.in_order.append(return_value)
        self.by_event_name[return_value.event_name] = return_value

    def return_value_from_name(self, event_name):
        return self.by_event_name[event_name]


class Value(object):
    """
    Simple wrapper providing functional accessors and being able to
    smooth over access between different data types?
    """
    def __init__(self, v):
        self.v = v

    def prop(self, name):
        return getattr(self.v, name)


class Valuesable(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def values(self):
        raise NotImplementedError()

    def first(self):
        return Value(self.values()[0])


class EventResult(Valuesable):
    __metaclass__ = ABCMeta

    @abstractmethod
    def success(self):
        pass


class EventSuccessDecoratorResult(EventResult):

    def __init__(self, wrapped):
        self.wrapped = wrapped

    def success(self):
        return True

    def values(self):
        return self.wrapped.values()


class EmptyValues(Valuesable):

    def values(self):
        return ()


class ValuesContainer(Valuesable):
    """
    Wraps any value and exposes it as a `Valuesable` interface.

    This is the primitive of the system and how different components
    communicate.  All values should be wrapped in a ValuesContainer.
    """
    def __init__(self, value):
        self.v = value

    def values(self):
        """
        Returns the value as a tuple.

        If the value is a list or a tuple it will wrap those as a tuple.
        If it is a single value it will wrap it as a tuple.
        :return:
        """
        if self._is_collection(self.v):
            return tuple(self.v)
        else:
            return (self.v,)

    def _is_collection(self, value):
        """
        Determines if a value is a collection, ie list/tuple

        :param value:
        :return:
        """
        return isinstance(value, list) or isinstance(value, tuple)


class EventFailureResult(EventResult):

    def success(self):
        return False

    def values(self):
        return []
