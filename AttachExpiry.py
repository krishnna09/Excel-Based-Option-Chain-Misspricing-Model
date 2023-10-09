from pymongo import MongoClient
from datetime import datetime

def get_expiry_names(symbol, instrument):
    myClient = MongoClient( "mongodb://192.168.1.110:27017/" )
    mydb = myClient['Details'] # The strategy orders will be stored in database named MockStrategySignal 
    coll = mydb['expiries']

    temp = coll.find_one()
    current_exp = datetime.strptime(temp["current"], "%Y-%m-%d")

    next_exp = datetime.strptime(temp["next"], "%Y-%m-%d")
    far_exp = datetime.strptime(temp["far"], "%Y-%m-%d")

    s_current= current_exp.strftime("%Y-%b-%d").upper()
    s_next = next_exp.strftime("%Y-%b-%d").upper()
    s_far = far_exp.strftime("%Y-%b-%d").upper()

    current_mon = s_current[5:8]
    next_mon = s_next[5:8]
    far_mon = s_far[5:8]

    current_expiry_symbol = ''
    next_expiry_symbol = ''
    names_with_expiry = []

    #print("s_current",s_current)
    #print("s_next", s_next) 

    if(instrument=="OPT"):

        if(current_mon==next_mon):
            if(current_mon=="JAN"):
                current_expiry_symbol = symbol + s_current[2:4] +"1" +s_current[-2:]

            elif(current_mon=="FEB"):
                current_expiry_symbol = symbol + s_current[2:4] +"2" +s_current[-2:]

            elif(current_mon=="MAR"):
                current_expiry_symbol = symbol + s_current[2:4] +"3" +s_current[-2:]

            elif(current_mon=="APR"):
                current_expiry_symbol = symbol + s_current[2:4] +"4" +s_current[-2:]

            elif(current_mon=="MAY"):
                current_expiry_symbol = symbol + s_current[2:4] +"5" +s_current[-2:]

            elif(current_mon=="JUN"):
                current_expiry_symbol = symbol + s_current[2:4] +"6" +s_current[-2:]

            elif(current_mon=="JUL"):
                current_expiry_symbol = symbol + s_current[2:4] +"7" +s_current[-2:]

            elif(current_mon=="AUG"):
                current_expiry_symbol = symbol + s_current[2:4] +"8" +s_current[-2:]

            elif(current_mon=="SEP"):
                current_expiry_symbol = symbol + s_current[2:4] +"9" +s_current[-2:]


            else:
                current_expiry_symbol = symbol + s_current[2:4] +current_mon[0] +s_current[-2:]
            

        else:
            current_expiry_symbol = symbol + s_current[2:4] +current_mon


        if(next_mon==far_mon):

            if(next_mon=="JAN"):
                next_expiry_symbol = symbol + s_next[2:4] +"1" +s_next[-2:]

            elif(next_mon=="FEB"):
                next_expiry_symbol = symbol + s_next[2:4] +"2" +s_next[-2:]

            elif(next_mon=="MAR"):
                next_expiry_symbol = symbol + s_next[2:4] +"3" +s_next[-2:]
            elif(next_mon=="APR"):
                next_expiry_symbol = symbol + s_next[2:4] +"4" +s_next[-2:]

            elif(next_mon=="MAY"):
                next_expiry_symbol = symbol + s_next[2:4] +"5" +s_next[-2:]

            elif(next_mon=="JUN"):
                next_expiry_symbol = symbol + s_next[2:4] +"6" +s_next[-2:]

            elif(next_mon=="JUL"):
                next_expiry_symbol = symbol + s_next[2:4] +"7" +s_next[-2:]

            elif(next_mon=="AUG"):
                next_expiry_symbol = symbol + s_next[2:4] +"8" +s_next[-2:]

            elif(next_mon=="SEP"):
                next_expiry_symbol = symbol + s_next[2:4] +"9" +s_next[-2:]


            else:
                next_expiry_symbol = symbol + s_next[2:4] + next_mon[0] +s_next[-2:]
            

        else:
            next_expiry_symbol = symbol + s_next[2:4] +next_mon

    


        

        
        names_with_expiry = [current_expiry_symbol, next_expiry_symbol]  
        

    # For old data format

    if(instrument=="FUT"):
        current_expiry_symbol = symbol + s_current[2:4] +current_mon + "FUT"
        names_with_expiry = [current_expiry_symbol]


    return(names_with_expiry)


