def check_battleship_number(exp_ships, filled_spaces):
#Test we have the correct amount of ships
    if (filled_spaces == exp_ships):
        print "SUCCESS correct amount of ships"
        return True
    else :
        print "FAIL exp ships %d actual %d" % (exp_ships, filled_spaces)
        ship_gen_error_flg = 1
        return False

def check_result_of_shot (actual, exp, msg) :
    if (actual == exp):
        print "SUCCESS: " + msg
    else:
        print "FAIL" + msg
    
