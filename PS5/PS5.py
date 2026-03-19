# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

# TODO: NewsStory
class NewsStory(object):
    def __init__(self,guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate
        self.pubdate = self.pubdate.replace(tzinfo=pytz.timezone("EST"))


    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_link(self):
        return self.link

    def get_pubdate(self):
        return self.pubdate
    
#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError
# PHRASE TRIGGERS
# Problem 2
# TODO: PhraseTrigger
def clean_text(text):
    ret_str =''
    for char in text:
        if char in string.ascii_letters:
            ret_str+=char.lower()
        else:
            if len(ret_str)>1 and ret_str[-1]!=' ':
                ret_str+=' '
    return ret_str     
class PhraseTrigger(Trigger):
    def __init__(self,phrase):
        self.phrase =clean_text(phrase)

    def is_phrase_in(self,text_input):
        c_text = clean_text(text_input)
        start_index =c_text.find(self.phrase)
        if start_index!=-1:
            if (start_index+len(self.phrase))==len(c_text) or c_text[start_index+ len(self.phrase)] not in string.ascii_letters:
                return True
        return False

# Problem 3
# TODO: TitleTrigger
class TitleTrigger(PhraseTrigger):
    def evaluate(self, story):
        return self.is_phrase_in(story.get_title())

# Problem 4
# TODO: DescriptionTrigger
class DescriptionTrigger(PhraseTrigger):
    def evaluate(self, story):
        return self.is_phrase_in(story.get_description())
# TIME TRIGGERS
# Problem 5
# TODO: TimeTrigger
class TimeTrigger(Trigger):
    def __init__(self,string):
        self.date = datetime.strptime(string,"%d %b %Y %H:%M:%S")
        self.date = self.date.replace(tzinfo=pytz.timezone("EST"))
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.

# Problem 6
# TODO: BeforeTrigger and AfterTrigger
class BeforeTrigger(TimeTrigger):
    def evaluate(self,story):
        return story.pubdate < self.date

class AfterTrigger(TimeTrigger):
    def evaluate(self,story):
        return story.pubdate > self.date

# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger
class NotTrigger(Trigger):
    def __init__(self,T):
        self.T  = T
    def evaluate(self,story):
        return not self.T.evaluate(story)
# Problem 8
# TODO: AndTrigger
class AndTrigger(Trigger):
    def __init__(self,T1,T2):
        self.T1  = T1
        self.T2 = T2 
    def evaluate(self,story):
        return self.T1.evaluate(story) and self.T2.evaluate(story)

# Problem 9
# TODO: OrTrigger
class OrTrigger(Trigger):
    def __init__(self,T1,T2):
        self.T1  = T1
        self.T2 = T2 
    def evaluate(self,story):
        return self.T1.evaluate(story) or self.T2.evaluate(story)


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.
    
    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)
    ret_stories=[]
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                ret_stories.append(story)
                break
    return ret_stories

def get_title_trigger(arg_list,l):
    return (arg_list[0],TitleTrigger(arg_list[2]))

def get_before_trigger(arg_list,l):
    return (arg_list[0],BeforeTrigger(arg_list[2]))
def get_after_trigger(arg_list,l):
    return (arg_list[0],AfterTrigger(arg_list[2]))
def get_description_trigger(arg_list,l):
    return (arg_list[0],DescriptionTrigger(arg_list[2]))

def get_composite_trigger(arg_list,trigger_list):
    if arg_list[1]=='OR' or arg_list[1]=='AND':
        title1 = arg_list[2]
        title2 = arg_list[3]
        t1,t2 =None,None 
        for trig in trigger_list:
            if title1== trig[0]:
                t1 =trig[1]
            if title2 ==trig[0]:
                t2 =trig[1]
        if arg_list[1] =='OR':
            return (arg_list[0],OrTrigger(t1,t2))
        else:
            return (arg_list[0],AndTrigger(t1,t2))
    else:
        t1 =None
        for trig in trigger_list:
            if trig[0]==arg_list[0]:
                return (arg_list[0],NotTrigger(trig[1]))


#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers
    ret_triggers =[]
    trig_dict ={'OR':get_composite_trigger,'AND':get_composite_trigger,'NOT':get_composite_trigger,
                'TITLE':get_title_trigger,'BEFORE':get_before_trigger,'AFTER':get_after_trigger,
                'DESCRIPTION':get_description_trigger}
    for line in lines:
        arg_list = line.split(',')
        if arg_list[0] !='ADD':
            trig_type = arg_list[1]
            #print(line)
            ret_triggers.append(trig_dict[trig_type](arg_list,ret_triggers))

        else:
            trig_list_names = arg_list[1:]
            sub_list =[]
            for t1 in trig_list_names:
                for t2 in ret_triggers:
                    if t1 ==t2[0]:
                        sub_list.append(t2[1])
            ret_triggers.append(sub_list)

    ret_l =[]
    for item in ret_triggers :
        if type(item)==tuple:
            ret_l.append(item[1])
        else:
            ret_l.append([item[:]])


    return ret_l

#read_trigger_config(filename='triggers.txt')

SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

