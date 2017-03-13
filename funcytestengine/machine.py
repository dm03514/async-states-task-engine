from collections import namedtuple, OrderedDict

import gevent
import logging

from gevent import Timeout
from transitions import Machine

from funcytestengine.event_fulfillment import EventFulfillmentFactory
from funcytestengine.initiators import InitiatorFactory

### This file needs to generically operation on ANY subclasses
from funcytestengine.transition_conditions import TransitionConditions

STATES = namedtuple('States', ['PENDING', 'FINISHED'])('pending', 'finished')
EVENT_RESULT = namedtuple('EventResult', ['SUCCESS', 'FAILURE'])('success', 'failure')


logger = logging.getLogger(__name__)
FIVE_MINUTES = 60 * 5


class EventResult(object):

    def __init__(self, status, context):
        self.status = status
        self.context = context


class Event(object):
    def __init__(self,
                 name,
                 transition_conditions,
                 initiator,
                 event_fulfillment_strategy=None,
                 timeout=FIVE_MINUTES):
        self.name = name
        self.initiator = InitiatorFactory.build(initiator)
        self.fulfillment = EventFulfillmentFactory.build(event_fulfillment_strategy)
        self.conditions = TransitionConditions(config_conditions=transition_conditions)
        self.timeout = timeout

    def execute(self):
        """
        Runs the fulfillment strategy on the initiator until the conditions are met.

        :return:
        """
        with gevent.Timeout(self.timeout):
            return self.fulfillment.run(self.initiator, self.conditions)


class Events(object):
    def __init__(self, events_list):
        self.events_dict = OrderedDict([(e.name, e) for e in events_list])

    def states(self):
        return self.events_dict.keys()

    def first_state(self):
        return self.states()[0]

    def teardown_current(self):
        pass

    def run(self, event_name, event_result_q):
        # TODO per event timeout
        # get the current event,
        event = self.events_dict[event_name]
        try:
            event.execute()
        except (Exception, Timeout) as e:
            logger.error('%s', {
                'message': 'event_execution_error',
                'exception': e
            })
            event_result_q.put(EVENT_RESULT.FAILURE)
        else:
            event_result_q.put(EVENT_RESULT.SUCCESS)


class TaskMachine(object):

    def __init__(self, machine_dict):
        # self.machine_dict = machine_dict
        self.events = Events([Event(**e) for e in machine_dict['events']])
        self.machine = Machine(
            model=self,
            states=self.states(),
            initial=STATES.PENDING
        )
        self.machine.add_ordered_transitions()

    def states(self):
        pre_states = [STATES.PENDING]
        # scheduled?
        # pre-flight resource checks? if a db or an integration
        # is not accessible, fail early option
        post_states = [STATES.FINISHED]
        return pre_states + self.events.states() + post_states

    def is_running(self):
        return True

    # can event fulfillment strategy decorate?
    # noop strategy by default
    def run_current_event(self, event_result_q):
        """
        Executes the current event, using the provided fulfilment strategy
        until the transition conditions are met.

        TODO, errors, timeouts, etc.

        :param next_state_q:
        :return:
        """
        # right now sleep then trigger completion
        gevent.spawn(self.events.run, self.state, event_result_q)

