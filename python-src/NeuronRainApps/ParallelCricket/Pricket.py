# -------------------------------------------------------------------------------------------------------
# NEURONRAIN ASFER - Software for Mining Large Datasets
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# --------------------------------------------------------------------------------------------------------
# Copyleft (Copyright+):
# NeuronRain Documentation and Licensing: http://neuronrain-documentation.readthedocs.io/en/latest/
# Personal website(research): https://acadpdrafts.readthedocs.io/en/latest/
# --------------------------------------------------------------------------------------------------------

from collections import deque
import random
import math

run_enum=[0,1,2,3,4,6]

class Player(object):
    def __init__(self,name,teamid):
        self.id = name
        self.teamid = teamid 
        self.state = "Playing"
        self.runs = 0
   
    def ballbatcontact(self,ballcoord,batcoord,bound=100):
        if ballcoord[0] <= batcoord[0] + bound and ballcoord[0] > batcoord[0] - bound and ballcoord[1] <= batcoord[1] + bound and ballcoord[1] > batcoord[1] - bound and ballcoord[2] <= batcoord[2] + bound and ballcoord[2] > batcoord[2] - bound:
            return True
        else:
            return False
       
    def ballstumpcontact(self,ballcoord,stumpcoord,bound=100):
        if ballcoord[0] <= stumpcoord[0] + bound and ballcoord[0] > stumpcoord[1] - bound and ballcoord[1] <= stumpcoord[1] + bound and ballcoord[1] > stumpcoord[1] - bound and ballcoord[2] <= stumpcoord[2] + bound and ballcoord[2] > stumpcoord[2] - bound:
            return True
        else:
            return False

    def play_shot(self,ball):
        ballcoord=[0,0,100]
        batcoord=[0,0,0]
        stumpcoord=[100,100,100]
        run=0
        for i in range(100):
            ballcoord[0] = i
            ballcoord[1] = int(abs(i*math.sin(i)))
            print("Ball trajectory:",ballcoord)
        batcoord[0] = random.randint(1,100)
        batcoord[1] = random.randint(1,100)
        batcoord[2] = random.randint(1,100)
        print("Bat coordinates:",batcoord)
        if self.ballbatcontact(ballcoord,batcoord):
            angle_of_the_shot = random.randint(1,360) % 36 
            run = run_enum[random.randint(0,len(run_enum)-1)] 
            self.runs += run
            print("Ball - ",ball," - Player:",self.id," - Team:",self.teamid," - angle of the shot (in degrees):",angle_of_the_shot)
            print("Ball - ",ball," - Player:",self.id," - run scored:",run)
            return (angle_of_the_shot,run)
        if self.ballstumpcontact(ballcoord,stumpcoord):
            print("Player:",self.id," has been clean-bowled and back in pavilion - score:",self.runs)
            self.state="Out"
            return(0,self.runs)
        else:
            return(0,run)

def print_deque(deq):
    deqstr=[]
    for e in deq:
        deqstr.append(e.id)
    return deqstr

def pricket_sabermetrics(number_of_balls=6,team1=None,team2=None,lowerdegree=3,upperdegree=33):
    ball=1
    player1 = team1.popleft()
    player2 = team2.popleft()
    team1_runs = 0
    team2_runs = 0
    while ball <= number_of_balls:
        shot = player1.play_shot(ball)
        if shot[0] == 0:
            print("Cleanbowled - Player:",player1.id," of team ",player1.teamid)
            if len(team1) > 0:
                player1 = team1.popleft()
                print("Team1 - yet to bat:",print_deque(team1))
            else:
                print("Team1 allout - Number of balls bowled:",ball)
                break 
        if shot[0] < lowerdegree or shot[0] > upperdegree:
            player1.state = "Out"
            print("Shot outside [",lowerdegree," to ",upperdegree,"] degrees range - Player ",player1.id," of team ",player1.teamid," is Out")
            if len(team1) > 0:
                player1 = team1.popleft()
                print("Team1 - yet to bat:",print_deque(team1))
            else:
                print("Team1 allout - Number of balls bowled:",ball)
                break 
        else:
            team1_runs += shot[1] 
        ball+=1
        shot = player2.play_shot(ball)
        if shot[0] == 0:
            print("Cleanbowled - Player:",player2.id," of team ",player2.teamid)
            if len(team2) > 0:
                player2 = team2.popleft()
                print("Team2 - yet to bat:",print_deque(team2))
            else:
                print("Team2 allout - Number of balls bowled:",ball)
                break 
        if shot[0] < lowerdegree or shot[0] > upperdegree:
            player2.state = "Out"
            print("Shot outside [",lowerdegree," to ",upperdegree,"] degrees - Player ",player2.id," of team ",player2.teamid," is Out")
            if len(team2) > 0:
                player2 = team2.popleft()
                print("Team2 - yet to bat:",print_deque(team2))
            else:
                print("Team2 allout - Number of balls bowled:",ball)
                break 
        else:
            team2_runs += shot[1] 
        ball+=1
    print("Team1 runs:",team1_runs)
    print("Team2 runs:",team2_runs)
    if team1_runs > team2_runs:
        print("Team1 wins")
    if team2_runs > team1_runs:
        print("Team2 wins")
    if team1_runs == team2_runs:
        print("Team1 and Team2 tied")

if __name__=="__main__":
    p1=Player("player1","team1")
    p2=Player("player2","team1")
    p3=Player("player3","team1")
    p4=Player("player4","team1")
    p5=Player("player5","team1")
    p6=Player("player6","team1")
    p7=Player("player7","team1")
    p8=Player("player8","team1")
    p9=Player("player9","team1")
    p10=Player("player10","team1")
    p11=Player("player11","team1")
    p12=Player("player12","team2")
    p13=Player("player13","team2")
    p14=Player("player14","team2")
    p15=Player("player15","team2")
    p16=Player("player16","team2")
    p17=Player("player17","team2")
    p18=Player("player18","team2")
    p19=Player("player19","team2")
    p20=Player("player20","team2")
    p21=Player("player21","team2")
    p22=Player("player22","team2")
    team1=deque()
    team2=deque()
    team1.append(p1)
    team1.append(p2)
    team1.append(p3)
    team1.append(p4)
    team1.append(p5)
    team1.append(p6)
    team1.append(p7)
    team1.append(p8)
    team1.append(p9)
    team1.append(p10)
    team1.append(p11)
    team2.append(p12)
    team2.append(p13)
    team2.append(p14)
    team2.append(p15)
    team2.append(p16)
    team2.append(p17)
    team2.append(p18)
    team2.append(p19)
    team2.append(p20)
    team2.append(p21)
    team2.append(p22)
    pricket_sabermetrics(number_of_balls=300,team1=team1,team2=team2)
