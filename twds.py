from bs4 import BeautifulSoup as btu
import requests as req
from datetime import datetime

"""
twepy module is a simple module that collects information about tweets and users on Twitter

What the module does: Collects information about tweets, searches and displays tweets on a specific tag, collects information from users

"""
__Author__ = "Naci Caner"

class TagNotFound(Exception):
     """
     If there is no tag or tag you entered, it returns a TagNotFound Error
     
     Examplem:
         tag="Pqpzmxkdk"
     output:
         TagNotFound -> Error
         .
     """
     def __init__(self) -> None:
        super().__init__("Tag Not Found")
        
        
class BrokenDate(Exception):
    """
    BrokenDate Error is for DateFiltre function If user enters a date after today's date, this error is returned
    
    Todays_date = 2023-03-19
    Examplem:
        date_filtre(stime="2023-03-24")
    Output:
        BrokenDate -> Error
        
    """
    def __init__(self) -> None:
        super().__init__("Broken Date:{self.date}")


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
   
def tag_all(tag):
    global headers
    """
     tag_all: function Finds the most recent tweets about the entered tag and gives you a Liste
     
     Args:
         tag_all(tag="Cyber")
     
     
     Returns:
         [links1,links2,links3]
     
     Error -> TagNotFound
    """
    output = []
    urlNiter = f"https://nitter.net/search?f=tweets&q=%23{tag}&since=&until=&near="
    requestsNiter = req.get(urlNiter,headers=headers)
    htmlNiter = requestsNiter.text
    soupNiter = btu(htmlNiter,"lxml")
    divtweetclass = soupNiter.find_all("div",{"class":"timeline"})
    for iNiter in divtweetclass:
        none_ = iNiter.find("h2",{"class":"timeline-none"})
        if none_ == None:
             pass
        else:
             raise TagNotFound()
        spantweetNiter = iNiter.find_all("span",attrs={"class":"tweet-date"})
    for hreftweetNiter in spantweetNiter:
         linktweetNiter = "https://twitter.com"+hreftweetNiter.find("a").get("href")
         output.append(linktweetNiter)
    return output
         
         
         

def date_filtre(tag,stime,etime,**kwargs):
    global headers
    """
    date_filtre: Finds Tweets between two entered dates.
    
    Examplem:
        date_filtre(tag="cyber",stime="2023-03-17",etime="2023-03-16")
    
    Returns:
        [links1,links2,links3...]
    
    Error: -> BrokenDate
    Error: -> ValueError
    
    The date_filter returns two errors, first BrokenDate and second ValueError.  Returns ValueError because Date Entered is in Wrong format
    
    Examplem:
        date_filtre(tag="cyber",stime="2023.02.12")
    
    Returns:
        ValueError
    
    stime: Tells the desired Tweets to start from
    etime: Specifies the date until which the tweet will be searched.
    """
    FiltreOutput= []
    urlfiltre = f"https://nitter.net/search?f=tweets&q=%23{tag}&since={stime}&until={etime}&near="
    from datetime import datetime
    date_obj = datetime.strptime(stime, '%Y-%m-%d')
    formatted_date = date_obj.strftime('%d.%m.%Y')
    today = datetime.today().date()
    if date_obj.date() > today: # Error code runs if entered date is greater than today's date
        raise BrokenDate() # Error

    requestsfiltre = req.get(urlfiltre,headers=headers)
    htmlfiltre = requestsfiltre.text
    soupFiltre = btu(htmlfiltre,"lxml")
    DivTimeİtemClass = soupFiltre.find_all("div",{"class":"timeline-item"})
    none__ = soupFiltre.find_all("h2",{"class":"timeline-none"})
    if none__ == []: # If this Divclass exists, the requested Tag does not exist and an error is returned.
         pass
    else:
         raise TagNotFound() # Error
    for iFiltre in DivTimeİtemClass:
         Tweet_Link_Class ="https://twitter.com"+ iFiltre.find("a").get("href")
         FiltreOutput.append(Tweet_Link_Class)
    return FiltreOutput
    
    

def tw_info(TweetLink,**kwargs):
    TweetLink += "?cxt="
    global headers
    LinkListeİmg = []
    dicti_output = {}
    """
     tw_info: Collects information about the entered tweet
     
     Information Collected: Collects Tweet Content,Tweet IMG , Tweet Date
     
     Examplem:
         tw_info(linksTweet)
     
     Returns:
         {"Link":TweetLink,"Date":İnfoDateP,"Content":İnfoContentDiv,"İmg":LinkListeİmg}
         
         
     
 
    """
    NitterReplace = TweetLink.replace("https://twitter.com","https://nitter.net").split("?cxt")[0]
    İnfoTweetRequests = req.get(NitterReplace,headers=headers)
    İnfoTweetHtml = İnfoTweetRequests.text
    İnfoSoup = btu(İnfoTweetHtml,"lxml")
    İnfoContentDiv = İnfoSoup.find("div",{"class":"tweet-content media-body"}).text
    İnfoDateP = İnfoSoup.find("p",{"class":"tweet-published"}).text    
    İnfoİmg = İnfoSoup.find_all("div",{"class":"attachment image"})
    for İnfoİmgHref in İnfoİmg:
        İnfoİmgLink = "https://nitter.net"+İnfoİmgHref.find("a").get("href")
        LinkListeİmg.append(İnfoİmgLink)   
    dicti_output = {"Link":TweetLink,"Date":İnfoDateP,"Content":İnfoContentDiv,"İmg":LinkListeİmg}
    return dicti_output
    
    
    
    
def user_info(userL,**kwargs):
       """
  user_info: Collects Information About the Entered User
  
  Examplem:
       user_info("elonmusk")
  
  Returns:
       {'Username': 'Elon Musk', 'Tweets Num': '23,756', 'Following': '185', 'followers': '131,931,126', 'Like': '19,733'}

       
       """
       output_user = {}
       userLink = f"https://nitter.net/{userL}"
       userRequests = req.get(userLink)
       userHtml = userRequests.text
       soup = btu(userHtml, "html.parser")
       user = soup.find("a", {"class":"profile-card-fullname"}).text
       tweets_num = soup.find("span",{"class":"profile-stat-num"}).text
       following = soup.find("li",{"class":"following"}).find("span",{"class":"profile-stat-num"}).text
       followers = soup.find("li",{"class":"followers"}).find("span",{"class":"profile-stat-num"}).text
       likes = soup.find("li",{"class":"likes"}).find("span",{"class":"profile-stat-num"}).text
       img = soup.find("div",{"class":"profile-card"}).find("div",{"class":"profile-card-info"}).find("a", {"class":"profile-card-avatar"}).get("href")
       output_user = {"Username":user,"Tweets Num":tweets_num,"Following":following,"followers":followers,"Like":likes}
       return output_user
       
      