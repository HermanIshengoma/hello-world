#!/usr/bin/env python
import time
from timeloop import Timeloop
from datetime import timedelta
import schedule

t1 = Timeloop()


@t1.job(interval=timedelta(seconds=2))
def sample_job_every_2s():
    print("2s job current time : {}".format(time.ctime()))


@t1.job(interval=timedelta(seconds=5))
def sample_job_every_2s():
    print("5s job current time : {}".format(time.ctime()))


@t1.job(interval=timedelta(seconds=10))
def sample_job_every_2s():
    print("10s job current time : {}".format(time.ctime()))

t1.start(block=True)