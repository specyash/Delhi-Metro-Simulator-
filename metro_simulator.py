try:
    f = open("metro_data.txt", 'r')
except FileNotFoundError:
    print("Metro data could not be loaded. Ensure the files are in same directory.")
    exit()
lines_data = f.readlines()

f.close()

metro = []

i = 0
# i want to get the data from the file.
while i< len(lines_data) :
    lineName =lines_data[i].strip()
    stn1 =lines_data[i+1].strip()
    stn2 =lines_data[i+2].strip()
    t = lines_data[i+3].strip()
    ch =lines_data[i+4].strip()

    metro.append([lineName, stn1, stn2, t, ch])
    # because there an empty line after each block so i + 6 is required

    i += 6  
# lets get the stations from this raw data
stns = []

for x in metro :
    if x[1] not in stns :
        stns.append(x[1])

    if x[2] not in stns :
        stns.append(x[2])
    # getting the interchange stations
ichg = []
for x in metro :
    if x[4]== "Yes" :
        if x[1] not in ichg:
            ichg.append(x[1])
        if x[2] not in ichg :
            ichg.append(x[2])

#ok i am adding a feature to let the user be free from case senstivity
#plan is to create a function that checks with the user input and tells if the input is valid.
def ver_stn(name):
    for x in stns:
        if x.lower() == name.lower():
            return x
    return None
        
# let's take the user input for the journeyy 
begin = input("Enter the current station: ")
end = input("Enter the final station: ")
t0 = input("Time at the moment: ")
#lets clean the inputs-->
begin = begin.strip()
end = end.strip()
t0 = t0.strip()
#case sensitivity implementation -->
begin = ver_stn(begin)
end = ver_stn(end)

if begin is None or end is  None:
    raise ValueError("Incorrect Station name entered.")

#if the same station is entered --->
if begin == end :
    print("You are already at your destination.")
    exit()

#well, let me put placeholders that will be used to decide the most optimised path for the jouney
#ive take t_same and t_inter to be very high no.s so that the first case always passes
#this is like identical to doing INT_MAX 
t_same = 99999
t_inter = 99999
route_same = []
route_inter = []
ic_final = None
#possible user error while entering time is that they might mess up the format
if ":" not in t0 or not t0.replace(":", "").isdigit():
    raise ValueError("Please enter the time in HH:MM format.")

#another user drive error could be that he might not enter the time in 24 hr format
#in such cases a custom error should be thrown

h,m= map(int, t0.split(":"))
if h< 0 or h>23 or m<0 or m> 59:
    raise ValueError("The time should be entered in 24hr format.")

#lets create simple time converter functions
#this function converts time to minutes
def to_min(t):
    h, m = map(int, t.split(":"))
    return 60*h + m
#this function returns the formatted string of the time
def to_strtime(total):
    #we get float in the final f string returned so lets just use padding and convert to int beforehand
    total = int(total)
    h = total // 60
    m = total %60
    return f"{h}:{m:02d}"
#lets add fare calculation
def fare(t):
    if t<=20:
        return 25
    elif t<=40:
        return 40
    elif t<= 60:
        return 50
    else : 
        return 70
def justnext(t):
    # decoding into hours and minutes
    h, m = t.split(":")
    #now we type convert to int
    m = int(m)
    h = int(h)

    # given constraint is that time can be b/w 6am to 11pm
    if h < 6 or h >= 23 :
        return "No trains available"

    # the trains have a frequency of 4 mins in peak and 8mins otherwise

    if (h >= 8 and h <10) or (h>=17 and h<19):
        frq = 4
    else : 
        frq = 8

    h1=6
    m1 = 0
    
    while True :
        # whenever the metro time becomes greater or equal to user's time input--> return the time!
        if (h1 > h) or (h1 == h and m1 >=m):
            if m1 < 10 :
                return str(h1)+ ":0" + str(m1)
            else :
                return str(h1) + ":" + str(m1)
            
        #again the frequence constraint application
        if (h1 >= 8 and h1 <10) or (h1>=17 and h1<19):
            frq = 4
        else : 
            frq = 8 

        m1 += frq
        # lets configure the timings, ex:84m = 60m(a hr) + (84-60)m
        if m1 >= 60 :
            m1 -=60
            h1+=1
        
        if h1 >=23:
            return "Final metro has left the station!"
    
# lets make a function for finding the line related to a station 
def findline(stn):
    lines = []
    for x in metro :
        if x[1] == stn or x[2] == stn:
            if x[0] not in lines :
                lines.append(x[0])
    
    return lines 
# also creating a function to get stations in ordered manner for a line
def getstns(line):
    s = []
    for x in metro :
        if x[0] == line :
            if x[1] not in s :
                s.append(x[1])
            if x[2] not in s :
                s.append(x[2])

    return s
# figuring out based on starting station and final station based on their lines 
startinglines = findline(begin) 
endlines = findline(end)

#handling error if the user makes a mistake in entering the station name
if startinglines == [] or endlines == []:
    raise ValueError("Invalid Station name entered.")
# we need to find the common stations so as to code for interchange if applicable
#so we type convert the list returned from the above functions to set for the intersection.

common = set(startinglines).intersection(endlines)
# if common's true the same line will be travelled throughout.
# so lets code for the journey that takes place in the same line.

if common :
# we want the common to have only element 
    #type converting back to list
    line = (list(common))[0]
    stns_lst = getstns(line)
    # the index of the stations will be used to figure out the relative posn of one wrt the other
    s_i = stns_lst.index(begin)
    e_i = stns_lst.index(end)
    # if the end station index is to the right of start station index; we set move to 1 else -1
    if s_i < e_i :
        move = 1
    else :
        move = -1
    #now finally lets make the route by setting t=0 and route=[beginning station]
    route = [begin]
    t1 = 0
    x = s_i
    # so traverse the stations list depending on our direction until we reach the 
    # station by appending the stations in between.
    while x !=e_i:
        stn1 = stns_lst[x]
        stn2 = stns_lst[x+move]

        for seg in metro :
            if (seg[1]== stn1 and seg[2]==stn2) or (seg[1]== stn2 and seg[2]==stn1):
                t1 += float(seg[3])
                break

        route.append(stn2)
        x+= move 
    

    # print("|Same Line Journey|")
    # print("Route :", "-->".join(route))
    # print("Total Time : ", t1, "minutes")
    # print("Next metro arrives at:", justnext(t0))
    #instead of printing them inside this block i want that we first see the most optimised path not only just the possible path
    t_start = to_min(t0)
    t_end =t_start +t1
    t_same = t1
    route_same =route[:]
    arrive= to_strtime(t_end)
#now lets code for the interchange part
st_line = startinglines[0]
en_line = endlines[0]
# so ill load the lines for both of the stations and generate the respective
# list of stations.
st_list = getstns(st_line)
en_list = getstns(en_line)
#now since we have the interchange stations with us, lets just find the one which is being used 
# ichg_used = None 
# for x in ichg :
#     if x in st_list and x in en_list :
#         ichg_used = x
#         break 

#the above block of code is incorrect since, it only checks for the first interchange station,
#that occured in both lists and returned that
#now we probably need a better way to do this -->


# find interchange stations separately for start and end lines

# Find valid interchange stations present in both lines
real_ichg = []
for s in ichg:
    if s in st_list and s in en_list:
        real_ichg.append(s)
if real_ichg:
    
# Choose shortest route among those interchange options
    best_time = 99999
    ichg_used = None

    for mid in real_ichg:
        # time from begin to mid
        t_a = 0
        si = st_list.index(begin)
        ei = st_list.index(mid)
        move = 1 if si < ei else -1

        temp = si
        while temp != ei:
            st1 = st_list[temp]
            st2 = st_list[temp+move]
            for seg in metro:
                if (seg[1]==st1 and seg[2]==st2) or (seg[1]==st2 and seg[2]==st1):
                    t_a += float(seg[3])
                    break
            temp += move
        #time from mid to end
        t_b = 0
        si2 =en_list.index(mid)
        ei2= en_list.index(end)
        move2 =1 if si2 < ei2 else -1

        temp2= si2
        while temp2 != ei2:
            st1=en_list[temp2]
            st2= en_list[temp2+move2]
            for seg in metro:
                if (seg[1]== st1 and seg[2] == st2) or (seg[1]== st2 and seg[2] ==st1):
                    t_b+= float(seg[3])
                    break
            temp2 += move2
        #considering the interchange time of 3 minutes
        total= t_a +t_b +3  

        if total< best_time:
            best_time = total
            ichg_used = mid
        #we break the process into beginning station to the interchange station and then
        # the interchange station to the destination station.
    s_i = st_list.index(begin)
    e_i= st_list.index(ichg_used)

    if s_i < e_i :
        move = 1
    else :
        move = -1

    #initialising the route by appending the beginning station 
    route = [begin]
    t2 = 0
    y = s_i

    while y!= e_i :
        stn1 = st_list[y]
        stn2 = st_list[y+move]
    # similar to the previos algorithm we apply it on begin --> ichg_used 
        for seg in metro :
            if (seg[1] == stn1 and seg[2] == stn2) or (seg[1] == stn2 and seg[2] == stn1):
                t2 += float(seg[3])
                break
        
        route.append(stn2)
        y+= move 
    #now lets code for ichg --> destination station
    s_i2 =en_list.index(ichg_used)
    e_i2= en_list.index(end)

    if s_i2 < e_i2:
        go = 1
    else:
        go = -1

    route1 = [ichg_used]
    t3 = 0
    z = s_i2

    while z!= e_i2:
        stn1 =en_list[z]
        stn2 =en_list[z + go]

        for seg in metro:
            if (seg[1] == stn1 and seg[2] == stn2) or (seg[1] == stn2 and seg[2] == stn1):
                t3 += float(seg[3])
                break

        route1.append(stn2)
        z+= go

    full = route + route1[1:]

    st_time = to_min(t0)
    end_mid = st_time + t2
    #now lets find the next train timing on the 2nd line at interchange
    nxt_mid = justnext(to_strtime(end_mid))

    #okay, i have discovered an edge case that takes place when interchange takes place at 23:00
    #in this case justnext() funcn returns either of the strings
    #but to_min() expects HH:MM format and hence the program is expected to crash
    # so lets just code for this specific case !

    if "available" in nxt_mid or "Final metro" in nxt_mid :
        print("Journey not possible-", nxt_mid)
        exit()
    mid_dep = to_min(nxt_mid)
    #this is the final arrival at fter riding the 2nd line
    final_arrive = mid_dep + t3
    t_inter = final_arrive -st_time
    arrive_inter = to_strtime(final_arrive)
    route_inter= full[:]
    ic_final= ichg_used

# print("|Interchange Journey|")
# print("Interchange at: ", ichg_used)
# print("Route: ", "-->".join(full))
# print("Total Time taken: ", final_t, "minutes")
# print("Next metro arrives at:", justnext(t0))
#similarly instead of printing these lets just return the time and see the most optimised path instead of just 
# seeing if the possible....



#now that we have all of the possible cases; we now do the comparision of time taken,
#that is we take the lesser time case.


if t_inter< t_same:
    print("|Interchange journey|")
    print("Interchange at:", ic_final)
    print("Route:", "-->".join(route_inter))
    amt = fare(t_inter)
    print("Total Time taken: ", t_inter, "minutes")
    print("Final Arrival Time:", arrive_inter)
    print("Fare for the trip in inr is: ", amt)


else:
    print("|Same Line Journey|")
    print("Route: ", "-->".join(route_same))
    amt = fare(t_same)
    print("Total Time: ", t_same, "minutes")
    print("Final Arrival Time:", arrive)
    print("Fare for the trip in inr is: ",amt)






            
            


    




                








