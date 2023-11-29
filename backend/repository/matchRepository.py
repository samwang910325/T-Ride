import psycopg2
from utils.config import ConfigUtil
from repository.models import *


class MatchRepository:
    def __init__(self):
        self.config = ConfigUtil.get('database')
        self.conn = psycopg2.connect(
            database=self.config.get('name'),
            user=self.config.get('user'),
            password=self.config.get('password'),
            host=self.config.get('host'),
            port=self.config.get('port'))

    def send_invitation(self, driver_order_id, passenger_order_id):
        '''
        orders exist and not finished, not matched, not invited
        '''
        sql = f'''INSERT INTO matches (
                      driver_order_id,
                      passenger_order_id,
                      accepted)
                  VALUES (
                      {driver_order_id},
                      {passenger_order_id},
                      false);'''

        # check connection
        try:
            with self.conn.cursor() as cur:
                cur.execute('SELECT 1;')
        except (psycopg2.OperationalError, psycopg2.InterfaceError):
            self.conn = psycopg2.connect(
                database=self.config.get('name'),
                user=self.config.get('user'),
                password=self.config.get('password'),
                host=self.config.get('host'),
                port=self.config.get('port'))

        with self.conn.cursor() as cur:
            cur.execute(sql)
            self.conn.commit()

    def get_driver_invitations(self, order_id):
        '''
        order exists

        passenger orders are sorted by departure time
        '''
        sql = f'''SELECT passenger_orders.*, matches.accepted
                  FROM matches JOIN passenger_orders
                  ON matches.passenger_order_id = passenger_orders.id
                  WHERE matches.driver_order_id = {order_id}
                  ORDER BY passenger_orders.departure_time1 ASC;'''

        # check connection
        try:
            with self.conn.cursor() as cur:
                cur.execute('SELECT 1;')
        except (psycopg2.OperationalError, psycopg2.InterfaceError):
            self.conn = psycopg2.connect(
                database=self.config.get('name'),
                user=self.config.get('user'),
                password=self.config.get('password'),
                host=self.config.get('host'),
                port=self.config.get('port'))

        with self.conn.cursor() as cur:
            cur.execute(sql)
            f2i = {desc[0]: i for i, desc in enumerate(cur.description)}
            rows = cur.fetchall()

        return [InvitationEntity(
            PassengerOrderEntity(
                row[f2i['id']],
                row[f2i['user_id']],
                row[f2i['time1']],
                row[f2i['time2']],
                row[f2i['people']],
                row[f2i['start_point']],
                row[f2i['start_name']],
                row[f2i['end_point']],
                row[f2i['end_name']],
                row[f2i['fee']],
                row[f2i['arrival_time']],
                row[f2i['spot_id']],
                row[f2i['finished']]),
            row[f2i['accepted']]) for row in rows]
