import json

import logging
import pprint

from nose.tools import assert_dict_equal

from .base import BaseTransitionCondition


logger = logging.getLogger(__name__)


class DictEqual(BaseTransitionCondition):
    def __init__(self, type, expected):
        self.expected = expected

    def apply(self, vs):
        logger.info({
            'class': self.__class__,
            'expected': self.expected,
        })
        expected = json.loads(self.expected)

        for v in vs.values():
            logger.info(pprint.pformat(expected))
            logger.info(pprint.pformat(v))
            logger.info({
                'class': self.__class__,
                'expected': expected,
                'received': json.dumps(v),
            })
            assert_dict_equal(v, expected, '{} != {}'.format(v, expected))

        return vs


class LengthEqual(BaseTransitionCondition):

    def __init__(self, type, length):
        self.length = length

    def apply(self, vs):
        logger.info({
            'class': self.__class__,
            'collection': vs,
            'length': self.length,
        })
        assert len(vs.values()) == self.length, 'collection ({}) != expected ({})'.format(
            len(vs.values()), self.length
        )
        return vs


class HasKeys(BaseTransitionCondition):

    def __init__(self, type, value_property=None, keys=()):
        self.keys = keys
        self.value_property = value_property

    def apply(self, vs):
        for v in vs.values():
            to_assert = v
            if self.value_property:
                to_assert = getattr(v, self.value_property)

            logger.info({
                'type': self,
                'to_assert': to_assert,
                'keys': self.keys,
            })
            assert set(to_assert) == set(self.keys)
        return vs


class Equal(BaseTransitionCondition):
    def __init__(self, type, to_equal, value_property=None):
        self.value_property = value_property
        self.to_equal = to_equal

    def apply(self, vs):
        for v in vs.values():
            to_assert = v
            if self.value_property:
                to_assert = getattr(v, self.value_property)
            assert self.to_equal == to_assert, '{} != {}, {}'.format(
                self.to_equal, to_assert, v)
        return vs

