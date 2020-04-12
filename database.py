#!/usr/bin/env python

# -----------------------------------------------------------------------
# database.py
# Author:
# -----------------------------------------------------------------------

import os
import psycopg2
from config import config
import json
from letter import Letter
from random import randint


DATABASE_URL = os.environ['DATABASE_URL']

# -----------------------------------------------------------------------


class Database:

    def __init__(self):
        self._conn = None

    # connect to the PostgreSQL server
    def connect(self):
        try:
            # read connection parameters
            params = config()
            self._conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            # self._conn = psycopg2.connect(**params)
            # psycopg2.connect()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    # close connection to the PostgreSQL server
    def disconnect(self):
        if self._conn is not None:
            self._conn.close()
            print('Database connection closed.')

    def user_exist(self, username):
        cur = self._conn.cursor()
        cmd = "SELECT id FROM public.\"Users\" WHERE id = CAST((%s) as text)"
        cur.execute(cmd, (username,))
        if cur.fetchone() is None:
            cur.close()
            return False

        cur.close()
        return True

    # add a letter to the PostgreSQL database
    def submit_letter(self, username, letter, letter_name, time_submitted, path):
        try:
            cur = self._conn.cursor()
            cmd0 = "INSERT INTO letter (l_name, date_m, user_id, path) VALUES ((%s), (%s), (%s), (%s))"
            cur.execute(cmd0, [letter_name, time_submitted, username, path, ])
            self._conn.commit()
            cur.close()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def letter_queue(self):
        try:
            cur = self._conn.cursor()
            cmd = "SELECT * FROM public.\"letter\""
            cur.execute(cmd)
            letters = []
            rows = cur.fetchall()
            for row in rows:
                letters.append(Letter(row[0], row[2], row[1], row[3], row[4], row[5], row[6], row[7]))

            cur.close()
            return letters
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def letter_receive(self):
        try:
            cur = self._conn.cursor()
            cmd = "SELECT * FROM public.\"letter\""
            cur.execute(cmd)
            letters = []
            rows = cur.fetchall()
            for row in rows:
                letters.append(Letter(row[0], row[2], row[1], row[3], row[4], row[5], row[6], row[7]))

            cur.close()
            return letters
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def send_out(self):
        try:
            cur = self._conn.cursor()

            # get the letters and users from the database
            cmd = "SELECT l_name, user_id FROM public.\"letter\" WHERE l_approved1 = true"
            cur.execute(cmd)
            letters_n = []
            users = {}
            row = cur.fetchone()
            # while row is not None:
            #  letters_n.append(row[0])
            # users.append(row[1])
            # row = cur.fetchone()

            # a list of letters to send out
            # make a dictionary with keys=users and values=[letters_composed_by_user_list]
            while row is not None:
                letters_n.append(row[0])
                x = users.get(row[1])
                print(row[1])
                if x is not None:
                    x.append(row[0])
                    users[row[1]] = x
                else:
                    users.update({row[1]: [row[0]]})

                row = cur.fetchone()
            n = len(letters_n)
            # list tracks which letters a given user shall receive
            send = []
            i = 0
            # SHOULD PROBABLY HAVE TO DO SOMETHING IN CASE A USER MADE ALL THE LETTERS OR IF THERE AREN'T ENOUGH LETTERS
            # TO GO AROUND
            for user in users:
                # user receives letters in accordance with how many they sent, currently 1:1 ratio
                while i < len(users[user]):
                    # randomly select a letter
                    x = randint(0, n - 1)
                    # make sure user didn't write the letter and hasn't already received the letter
                    if letters_n[x] not in users[user] and letters_n[x] not in send:
                        send.append(letters_n[x])
                        i += 1

                # update the database
                cmd = "SELECT l_received FROM public.\"Users\" WHERE id = CAST((%s) as text)"
                cur.execute(cmd, [user, ])
                receives = cur.fetchone()
                if receives[0] is not None:
                    receives = list(receives[0]) + send
                else:
                    receives = send
                cmd = "UPDATE public.\"Users\" SET l_received = (%s) WHERE id = CAST((%s) as text)"
                cur.execute(cmd, [receives, user, ])

                self._conn.commit()

                i = 0
                send = []



            # # set a list that generates the number of times each user should receive a letter.
            # times = []
            # for i in range(n):
            #     times.append(randint(1, n/2))
            #
            # cmd1 = "INSERT INTO User (json_test) WHERE l_name = CAST((%s) TO TEXT) VALUES ((%s))"
            # send = []
            # for i in range(n):
            #     for j in range(times[i]):
            #         letter_n = random.choice(letters)
            #         # don't want the user that sent the letter to receive it
            #         if i != letters.index(letter_n):
            #             # make sure not to send the same letter twice
            #             if letter_n not in send:
            #                 send.append(letter_n)

            # for i in range(n):
            # concentrating on the letters:
            # repeat a random number of times

            # randomly generate an index
            # check if user already sent it

            # while letters_n:
            #   letter_n = letters_n.pop()
            #  i = 0
            #  while i is not index and len(letter_n) is not 1:
            #     i = randint(i, len(letters_n))
            # user = users.pop(i)
            # get the l_received list

            # append the letter to the list

            cur.close()
            return
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)


# -----------------------------------------------------------------------

if __name__ == '__main__':
    connect()
