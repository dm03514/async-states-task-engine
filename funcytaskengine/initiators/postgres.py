import psycopg2

from funcytaskengine.event_fulfillment.return_values import ValuesContainer, EmptyValues
from funcytaskengine.initiators.base import BaseInitiator


class SelectInitiator(BaseInitiator):

    def __init__(self, type, query, connection_string):
        self.query = query
        self.conn = psycopg2.connect(connection_string)
        self.query = query

    def apply_overrides(self, event_results):
        pass

    def execute(self, *args, **kwargs):
        cur = self.conn.cursor()

        results = []

        try:
            cur.execute(self.query)
            results = cur.fetchall()
        finally:
            self.conn.close()
            cur.close()

        return ValuesContainer(results)


class QueryInitiator(BaseInitiator):

    def __init__(self, type, query, connection_string):
        self.query = query
        self.conn = psycopg2.connect(connection_string)
        self.query = query

    def apply_overrides(self, event_results):
        pass

    def execute(self, *args, **kwargs):
        cur = self.conn.cursor()

        try:
            cur.execute(self.query)
        finally:
            self.conn.commit()
            self.conn.close()
            cur.close()

        return EmptyValues()
