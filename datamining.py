import sys
import operator


Country_arg=sys.argv[1]
apps_file = sys.argv[2]
user_file = sys.argv[3]
jobs_file= sys.argv[4]
user_history_file=sys.argv[5]


users={}
jobs={}
apps={}
user_history={}
job_list = []
fin_job=[]
location={}
jobsdim={}


#Import the files below

with open(jobs_file,'rw') as job:
    for row in job.readlines():
        row= row.split('\t')
        try:
            row[0]=int(row[0])
            jobs[int(row[0])]=row
        except ValueError:
            x=1
        

with open(user_history_file,'rw') as user_his:
    for row in user_his.readlines():
        row= row.split('\t')
        try:    
            user_history[int(row[0])]=row
        except ValueError:
            x=1
        

with open(user_file,'rw') as user:
    for row in user.readlines():
        row= row.split('\t')
        try:
            row[0]=int(row[0])
            users[int(row[0])]=row
        except ValueError:
            x=1
        


with open(apps_file,'rw') as app:
    for row in app.readlines():
        row= row.split('\t')
        try:
            row[0]=int(row[0])
            row[2]=int(row[2])
            apps[int(row[0]),int(row[2])]=row
        except ValueError:
            x=1
    
    

def firsttask(a1,b1):
    
    #Join User and apps tables 
    
    user_apps={}
    
    for k1,k2 in b1.keys():
        user_apps[k1,k2]=users[k1]+b1[k1,k2]
    
    #---------------------------------------------------
    
    
    state_list={}
    
    for key1,key2 in user_apps.keys(): #For each user ID,Job ID combination
        a=user_apps[key1,key2][15] #store job id in a variable for it to be used later
        b=user_apps[key1,key2][2] # store state id thats to be fed to the state collection dictionary
        if(b in state_list.keys()): #check if the entry for that state already exists in the state dictionary
            state_list[b].append(a)
        else:
            state_list[b]=[a] #if not create a list for that state and add first value
    
    #Create a location dimension 
    
    for k in a1.keys():
        a=a1[k][2]
        b=a1[k][3]
        location[a]=b
        
    #Create job dimension
    
    for k in jobs.keys():
        a=int(jobs[k][0])
        b=jobs[k][1]
        jobsdim[a]=b
        
    
    # till here, perfectly fine. Print state_list to get a dict with....
    #cont.....State_ID as key and different application IDs applied in that state       
    
    for key in state_list.keys():
        u={}
        ho=state_list[key]
        for word in ho:
            cnt=ho.count(word)
            while(word not in u.keys()):
                u[word]=cnt
            state_list[key]=u
                
    tr=state_list.copy()
    #print tr
    
    for state in tr:
        for job_id in tr[state]:
            job_list.append([state, job_id, tr[state][job_id]])
    
    
               
    y=sorted(job_list, key=lambda k: k[2], reverse=True)[:5]
    
    
      # Prints top 5 jobs by state
    for i in range(0,len(y)):
        if(i==0):
            print 'StateID'+ '\t'+'JobID'+'\t'+'\t'+'NumbOfApps'
        print str(y[i][0]) + '\t' + str(y[i][1])+ '\t'+'\t' + str(y[i][2])


firsttask(users,apps) #CALLING FIRSTTASK function


def secondtask(a):
    # From the cuboid obtained above, perform slicing Country= argument passed
    country=[]
    
    #------------------------------Slice on Country---------------------------------
    #The following loop makes a list of all the jobs with state ID and their respective counts obtained from materialised cuboid
    for(s_id,j_id,cnt) in a:
        if(location[s_id]==Country_arg):
            u=[]
            u.append(s_id)
            u.append(j_id)
            u.append(str(cnt))
            country.append(u)
    
    
    #------------------------------------------------------------------------------------        
    
    #-------------------------Roll-UP from JobID to Title_ID on Job dimension---------------

    country_top={}
    
    # Roll up on to CountryID from StateID
    
    for each in country:
        job_id=each[1]
        count=int(each[2])
        title=jobs[int(job_id)][1]
        try:
            country_top[title]+=count
        except KeyError:
            country_top[title]=count
   

    
    #Top 5 
    x=sorted(country_top.iteritems(), key=operator.itemgetter(1), reverse=True)[:5]
    
    
    print '\n'+'\n'
    
    for i in range(0,len(x)):
        if(i==0):
            print 'CountryID'+ '\t'+'JobID'+'\t''\t'+'NumbOfApps'
        print str(Country_arg + '\t' + str(x[i][0])+ '\t'+ str(x[i][1]))



secondtask(job_list) #CALLING SECONDTASK FUNCTION

