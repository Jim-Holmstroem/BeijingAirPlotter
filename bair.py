import twitter
import time,datetime


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
        if(textdata[2]!="no data"):
            self.values=map(lambda i:textdata[i],[2,3]) #pickout the values at 2,3
            self.nodata=False

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

while(len(tweets)!=0):
    tweets=api.GetUserTimeline(id="BeijingAir",max_id=last_id,count=200) #get older

    air_tweets = map(lambda tweet: air_tweet(tweet),tweets)

    ozon_tweets = pickout_valid_measures(air_tweets,"Ozone")
    pm_tweets = pickout_valid_measures(air_tweets,"PM2.5")

    all_pm_tweets.extend(pm_tweets)
    all_ozon_tweets.extend(ozon_tweets)

    for tweet in ozon_tweets:
        print tweet

    for tweet in pm_tweets:
        print tweet

    print "----------------------------------------------"


    last_id=min(map(lambda tweet:tweet.id,tweets))

