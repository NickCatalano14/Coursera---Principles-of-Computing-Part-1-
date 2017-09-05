"""
Cookie Clicker Simulator
"""

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._current_time = 0.0
        self._item_bought = None
        self._item_cost = 0.0
        self._total_cookies = 0.0
        self._lst_history = [(self._current_time, self._item_bought, 
                              self._item_cost, self._total_cookies)]
        
        self._current_cookies = 0.0
        self._current_cps = 1.0
        
        
    def __str__(self):
        """
        Return human readable state
        """
        return "\n" + "Total Cookies: " + str(self._total_cookies) + "\n"\
    "Current Cookies: " + str(self._current_cookies) + "\n"\
    "Current Time: " + str(self._current_time) + "\n"\
    "Current CPS: " + str(self._current_cps) + "\n"
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._current_cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return self._lst_history 

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        
        delta_time = 0
        if self._current_cookies < cookies:
            delta_time = math.ceil((cookies - self._current_cookies) / 
                                      self._current_cps)
        
        return float(delta_time)
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        
        if time > 0:
            self._current_time += time
            self._current_cookies += time * self._current_cps
            self._total_cookies += time * self._current_cps
        
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        cost_flt = float(cost)
        cps_flt = float(additional_cps)
        
        if self._current_cookies >= cost_flt:
            self._item_name = item_name
            self._current_cookies -= cost_flt
            self._current_cps += cps_flt
            his_tuple = (self._current_time, item_name, cost_flt, self._total_cookies)
            self._lst_history.append(his_tuple)
        else:
            pass
        
  
    def get_name(self):
        """
        Return current upgrade item name
        
        Should return None or a string
        """
        return self._item_bought
    
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    
    build_clone = build_info.clone()
    new_state = ClickerState()

    while new_state.get_time() <= duration:
        time = duration - new_state.get_time()
        item_name = new_state.get_name()
        item_name = strategy(new_state.get_cookies(), new_state.get_cps(), new_state.get_history(), time, build_clone)
        if item_name == None:
            break
        if new_state.time_until(build_clone.get_cost(item_name)) > time:
            break 
        else:
            item_name = strategy(new_state.get_cookies(), new_state.get_cps(),new_state.get_history(),  time, build_clone)
            new_state.wait(new_state.time_until(build_clone.get_cost(item_name)))
            new_state.buy_item(item_name, build_clone.get_cost(item_name), build_clone.get_cps(item_name))
            build_clone.update_item(item_name)
    
    new_state.wait(time)
 
    return new_state


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    #cheapest = build_info.build_items()
    #costs = map(build_info.get_cost, cheapest)
    #cheapest_item = costs.index((min(costs)))
    
    #if cookies + cps * time_left > costs[cheapest_item]:
    #    return cheapest_item
    #else:
    #    return None
    
    
    cheapest = build_info.build_items()
    costs = map(build_info.get_cost, cheapest)
    index = costs.index(min(costs))
    cheap_item = cheapest[index]
    if (cookies + cps * time_left) < costs[index]:
        return None
    else:
        return cheap_item
    

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    expensive = build_info.build_items()
    costs = map(build_info.get_cost, expensive)
    
    temp_item = []
    temp_cost = []
    
    for item in range(len(costs)):
        if costs[item] <= cookies + cps * time_left:
            temp_cost.append(costs[item])
            temp_item.append(expensive[item])
            
    if temp_cost == []:
        return None
    else:
        index_ex = temp_cost.index(max(temp_cost))
        return temp_item[index_ex]



def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """


    best = build_info.build_items()
    costs = map(build_info.get_cost, best)
    cps_list = map(build_info.get_cps, best)
    best_list = []
    for item in range(len(best)):
        temp = cps_list[item] / costs[item]
        best_list.append(temp)
    best_idx = best_list.index(max(best_list))
    best_item = best[best_idx] 
    return best_item
    
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    #history = state.get_history()
    #history = [(item[0], item[3]) for item in history]
    #simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    
run()
    

