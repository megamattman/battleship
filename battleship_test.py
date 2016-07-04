import sys

def function_name():
    return sys._getframe().f_back.f_code.co_name

def check_battleship_number(exp_ships, filled_spaces):
#Test we have the correct amount of ships
    if (filled_spaces == exp_ships):
        print "SUCCESS correct amount of ships"
        return True
    else :
        print "FAIL exp ships %d actual %d" % (exp_ships, filled_spaces)
        ship_gen_error_flg = 1
        return False

def check_result (actual, exp, msg) :
    if (actual == exp):
        print "SUCCESS: " + function_name() + " " + msg
    else:
        print output_fail_string(actual, exp, function_name(), msg)
    
def check_grid_pos (board, row, col, exp_val, msg) :
    actual = board.board[row][col]
    if ( actual == exp_val):
        print ("SUCCESS: check_grid_pos " + msg)
    else:
        extra_information = "Location " + str(row) +"," + str(col) + " - " + msg
        output_fail_string(actual, exp_val, function_name(), extra_information)

def output_fail_string (actual, exp, func_name, msg):
    print "FAIL: %s, got %s expected %s - %s" %(func_name, actual, exp, msg)

