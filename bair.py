import twitter
import time,datetime

import numpy
import matplotlib.pyplot as plt


api=twitter.Api()

class air_tweet:
    t=0 # time in seconds when created
    measure_type="no data" #the type of the measure
    values=[-1,-1] #[concentration,AQI] 
    nodata=True
    """
    Your a grownup right? dont write too this private field
    """

    def __init__(self,tweet):
        self.t=tweet.created_at_in_seconds
        #Split and strip the textdata
        textdata=map(lambda data: data.strip().encode('ascii','replace'),tweet.text.split(";"))
        self.measure_type=textdata[1].split()[0] #overnight measures is contains some clutter
        if(not textdata[2].startswith("no data")):
            try:
                self.values=map(lambda i:float(textdata[i]),[2,3]) #pickout the values at 2,3
                self.nodata=False
            except: #if the data is invlid (damn you twitteruser) (this actually happens for many data)
                if(len(textdata)>3):
                    if(not textdata[3].startswith("no data")):
                        try:
                            self.values=map(lambda i:float(textdata[i]),[3,4]) #pickout the values at 2,3
                            self.nodata=False
                        except:    
                            print ("the twitter data is invalid:"+tweet.text)
                else:
                    print ("the twitter data is invalid:"+tweet.text)

    def __str__(self):
        return str(self.measure_type)+"="+str(self.values)+"@"+str(self.t)

def pickout_valid_measures(air_tweets,measure_type=None):
    """
    Filters out all the valid air_tweets with the specified measure_type
    If measure type is left out the measure type wont be considered
    """
    return filter(lambda tweet: not tweet.nodata and (measure_type is None or tweet.measure_type == measure_type),air_tweets)

all_pm_tweets=[]
all_ozon_tweets=[]

last_id=None
tweets=[0]

trycounter=5

while(True): #will be breaked by last statement
    try:
        tweets=api.GetUserTimeline(id="BeijingAir",max_id=last_id,count=200) #get older
    except twitter.TwitterError:
        trycounter-=1
        if(trycounter>0):
            print("TwitterError trying again in 5")
            print("reseting API")
            api=twitter.Api()
            time.sleep(5)
            print("continue;")
            continue #tries again
        else:
            break;
    air_tweets = map(lambda tweet: air_tweet(tweet),tweets)

    ozon_tweets = pickout_valid_measures(air_tweets,"Ozone")
    pm_tweets = pickout_valid_measures(air_tweets,"PM2.5")

    all_pm_tweets.extend(pm_tweets)
    all_ozon_tweets.extend(ozon_tweets)

    print "Fetched tweets:",len(tweets)
    
    tweetids=map(lambda tweet:tweet.id,tweets);
    if(len(tweetids)==0):
        break; #we are done here, nuttin more to see
    last_id=min(tweetids)

#for tweet in all_pm_tweets:
#    print tweet

x=numpy.array(map(lambda tweet:tweet.t,all_pm_tweets))
y0=numpy.array(map(lambda tweet:tweet.values[0],all_pm_tweets))
y1=numpy.array(map(lambda tweet:tweet.values[1],all_pm_tweets))

plt.plot(x,y0,'r-')
plt.plot(x,y1,'g-')
plt.show()
