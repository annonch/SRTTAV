#!/usr/bin/python
##########################
#  channon@hawk.iit.edu  #
##########################

'''
State obj

'''
import threading 
import time
import sys

# use python verifier.py state.config init_state

class State:
    'This is the object for states'
    stateCount = 0
    # 0 indexed
    def __init__(self,n,g,trans,times):
        self.ID = State.stateCount
        State.stateCount +=1
        # make ID
        self.name = n
        guar = g.split(',')
        self.guards = dict()
        
        for i in guar:
            j= i.split(':')
            if j[1] == 'int':
                self.guards[j[0]] = int(j[2])
            elif j[1] == 'float':
                self.guards[j[0]] = float(j[2])
            else:
                self.guards[j[0]] = str(j[2])

        t = trans.split(',')
        self.transition_variable = t[0]
        self.transition_var_default = self.guards.get(self.transition_variable)
        self.transition_A = t[1]
        self.transition_B = t[2]

        tim = times.split(',')
        self.reset = int(tim[0])
        self.time_max = int(tim[1])

    def display(self):
        global engine
        print("ID: %s, Name: %s, Variables: %s, Transition Guard: %s, Max Time: %s, Clock Reset: %s "
              % (self.ID,self.name, self.guards,self.transition_variable,self.time_max, self.reset   ) )
        #engine.say("ID: %s, Name: %s, Variables: %s, Transition Guard: %s, Max Time: %s, Clock Reset: %s "
        #      % (self.ID,self.name, self.guards,self.transition_variable,self.time_max, self.reset   ) )

    def str_display(self):
        return("ID: %s, Name: %s, Variables: %s, Transition Guard: %s, Max Time: %s, Clock Reset: %s "
              % (self.ID,self.name, self.guards,self.transition_variable,self.time_max, self.reset   ) )
        
    def transition(self):
        global cur_state,states

        if self.guards.get(self.transition_variable) == self.transition_var_default:
            return 0 #cant transition, variable in default state
        if self.guards.get(self.transition_variable) < self.transition_var_default:
            cur_state = self.transition_A
            return -1 #change state to trans -1
        if self.guards.get(self.transition_variable) > self.transition_var_default:
            cur_state = self.transition_B
            return 1  # change state to trans 1

    def setup(self):
        global clock_time , cur_state
        if self.reset:
            reset_clock()

        if self.time_max:
            now = time.time()
            time_elps = now-clock_time
            time_rem = self.time_max - time_elps
            print('now: %s, elps: %s, rem: %s'
                  % (now,time_elps,time_rem))
            do_every(time_rem/2,    warn ,   cur_state,   2)
            do_every(time_rem - 5 , alert,   cur_state,   2)
            do_every(time_rem,      error_a, cur_state,   2)
        
def do_every(interval, worker_func, cur_state,iterations = 0):
    if iterations !=1:
        threading.Timer (
            interval,
            do_every, [interval, worker_func, cur_state, 0 if iterations == 0 else iterations-1]
        ).start();
    if iterations != 2:
        worker_func(cur_state); 
