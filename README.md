# DynRow
DynRow connects to the Concept2 Ergometer and shows a birds-eye view of you rowing versus bots.

Here are some vieos to get a basic idea of how it looks like and what it does:
* [0.1: First Prototype](http://youtu.be/gBvpYNmO__Y)
* [0.2: Initially uploaded version](http://youtu.be/8LIEzyJB_4k)
* [0.3: First version with stats being shown](http://youtu.be/3XJ9Eh7riac)
* [0.4: Introducing Boomerang Bots](https://www.youtube.com/watch?v=pUSHYbpO-0I)

My goal is to create a rowing application which displays thorough statistics about your current workout. In addition to that there should be a variety of bots available. Here are a few ideas:
* *Constant pace:* This is useful if you want to row in a certain tempo
* *Boomerang:* They're rowing at a constant pace, but if they get behind you they will row faster. If they get too far in front, they'll decelerate to let you keep up with them. They're almost like the constant pace boats, but they'll always be around. This leads to having opponents around even at the longest training sessions
* *Heartrate:* You set up your desired target heart rate and the bot will row faster/slower according to your current heart rate
* *Ghostrider:* This bot replays a previously rowing session of yourself
* *Intervals:* Usually this bot runs on a constant pace, but it'll push the tempo from time to time. Try to keep pace
* ... There are a lot of different bots possible, time will tell what bots are the most useful

Another idea is to implement a logic which adds additional boats to your workout. So besides the bots you specifially set up there will a lot different boats with randomized behaviour. The goal is to have a widely populated environment instead of simply the same 2 boats you row with your entire session. We'll see how this works out.

The software uses a slightly modified version of  [PyRow](http://www.newhavenrowingclub.org/pyrow/) and has been tested to work on a Xubuntu 14.04 machine connected to a PM5 monitor. I'm open sourcing this software to allow people to adopt it to their own machines. It also could be useful to have as much different bots as possible.

The modifications of PyRow are made to be able to work with my PM5 monitor. There's also some additional exception handling added. I haven't made much effort to keep it portable to PM3/4 monitors, it's currently just set up to get it up and running on my system.
