import sys

from Boats.BoatRollingAverage import BoatRollingAverage
from Boats.BoatConstant import BoatConstant
import unittest

def testReset():
    "simple test for the framework as much as the reset"
    b = BoatRollingAverage( "test", BoatConstant("constant"))
    b.pace = 120
    b.reset()
    assert b.pace == BoatRollingAverage.DEFAULT_PACE

def testConstantAverage():
    "test rolling pace when other boat moves at a constant rate"
    ob = BoatConstant("constant")
    b = BoatRollingAverage( "test", ob, 100)
    ob.pace = 90
    time = 1
    for distance in xrange(1, 111):
        ob.distance = distance
        b.move(time)
        time += 1
    assert b.pace==90, "b.pace was %s"%b.pace

def testAverageAfterBufferHasRolled():
    "test that the rolling boat pace is the average of the last 100 paces' when set to update every meter"
    # so the other pat pace goes from 0 to 200, we set rolling to look average the last 100, therefore rolling pace should be 150
    ob = BoatConstant("constant")
    b = BoatRollingAverage( "test", ob, 100, 1)
    ob.pace = 0
    time = 1
    for distance in xrange(0, 200):
        ob.distance = distance
        b.move(time)
        time += 1
        ob.pace += 1
    assert b.pace==150, "b.pace is:%s, ob.pace is %s, ave=%s"%(b.pace , ob.pace, b.buffer.average)



