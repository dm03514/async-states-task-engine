import unittest

from mock import MagicMock

from funcytaskengine.event_fulfillment.return_values import EventResults, EventSuccessDecoratorResult, ValuesContainer
from funcytaskengine.initiators.base import ExtractPreviousResults, PreviousResultOverride


class OverridesTestCase(unittest.TestCase):

    def test_previous_results_no_overrides(self):

        class StubExecutor(object):
            @ExtractPreviousResults()
            def execute(self, **kwargs):
                return 'complete'

        self.assertEqual(
            'complete',
            StubExecutor().execute(event_results=EventResults()),
        )

    def test_previous_results_single_override(self):

        class StubExecutor(object):
            def __init__(self, url=''):
                self.url = url

            @ExtractPreviousResults(
                PreviousResultOverride(
                    event_name='last_test',
                    target_attr='url',
                    value_prop=None,
                ),
            )
            def execute(self, **kwargs):
                return 'complete'

        se = StubExecutor()
        results = EventResults()
        result = EventSuccessDecoratorResult(
            ValuesContainer(value='previous_url_value')
        )
        result.event_name = 'last_test'
        results.add(result)

        self.assertEqual(
            'complete',
            se.execute(event_results=results),
        )
        self.assertEqual('previous_url_value', se.url)

    def test_previous_results_multiple_overrides_different_results(self):

        class StubExecutor(object):
            def __init__(self, url='', first_url=''):
                self.url = url
                self.first_url = first_url

            @ExtractPreviousResults(
                PreviousResultOverride(
                    event_name='last_test',
                    target_attr='url',
                    value_prop=None,
                ),
                PreviousResultOverride(
                    event_name='first_test',
                    target_attr='first_url',
                    value_prop=None,
                ),
            )
            def execute(self, **kwargs):
                return 'complete'

        se = StubExecutor()
        results = EventResults()
        result = EventSuccessDecoratorResult(
            ValuesContainer(value='previous_url_value')
        )
        result.event_name = 'last_test'
        results.add(result)

        result = EventSuccessDecoratorResult(
            ValuesContainer(value='first_url_value')
        )
        result.event_name = 'first_test'
        results.add(result)

        self.assertEqual(
            'complete',
            se.execute(event_results=results),
        )
        self.assertEqual('previous_url_value', se.url)
        self.assertEqual('first_url_value', se.first_url)

    def test_previous_results_multiple_overrides_same_results(self):

        class StubExecutor(object):
            def __init__(self, url='', first_url=''):
                self.url = url
                self.first_url = first_url

            @ExtractPreviousResults(
                PreviousResultOverride(
                    event_name='last_test',
                    target_attr='url',
                    value_prop='event_prev_url',
                ),
                PreviousResultOverride(
                    event_name='last_test',
                    target_attr='first_url',
                    value_prop='event_first_url',
                ),
            )
            def execute(self, **kwargs):
                return 'complete'

        se = StubExecutor()
        results = EventResults()
        result = EventSuccessDecoratorResult(
            ValuesContainer(value=MagicMock(
                event_prev_url='previous_url_value',
                event_first_url='first_url_value'
            ))
        )
        result.event_name = 'last_test'
        results.add(result)

        self.assertEqual(
            'complete',
            se.execute(event_results=results),
        )
        self.assertEqual('previous_url_value', se.url)
        self.assertEqual('first_url_value', se.first_url)
