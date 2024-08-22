#!/usr/bin/env python3

import asyncio
import os
import textwrap
from collections import deque
import time
import navel


async def avoid_gaze():
    async with navel.Robot() as robot:

        while True:
            await asyncio.sleep(0.5)
            data = await robot.next_frame()
            if data.persons!=[]:
                print(data.persons)
                person=data.persons[0]
                try:
                    gaze=person.g_gaze[0]
                    #print(gaze)
                    if gaze.x<0:
                        gaze.x=1
                    else:
                        gaze.x=-1
                    if gaze.y<0:
                        gaze.y=1
                    else:
                        gaze.y=-1
                    if gaze.z<0:
                        gaze.z=1
                    else:
                        gaze.z=-1
                    #print(gaze)
                    r=robot.look_at_cart(gaze,0.2)
                except:
                    print("no_gaze detected")
               # print(r)

async def mutual_gaze():
    async with navel.Robot() as robot:

        while True:
            await asyncio.sleep(0.5)
            data = await robot.next_frame()
            if data.persons!=[]:
                print(data.persons)
                person=data.persons[0]
                r=robot.look_at_person(data.persons[0].uuid,0.8)
               # print(r)

if __name__ == "__main__":
    try:
        asyncio.run(avoid_gaze())
    except KeyboardInterrupt:
        pass
