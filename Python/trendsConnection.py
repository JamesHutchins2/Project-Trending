from pytrends.request import TrendReq
import pandas as pd

def get_top_queries(keyword):
    #define vaiables
    topic_titles = []
    top_queries = []

    topics_fail = False
    queries_fail = False



    pytrends = TrendReq(hl='en-US',timeout=(20,35))
    kwlist = [keyword]
    pytrends.build_payload(kwlist,timeframe='today 1-m', geo='', gprop='')
    related_topics = pytrends.related_topics()
    if related_topics.get(keyword):
        top_topics = related_topics[keyword]['top']
        #arrange the topics in descending order
        top_topics = top_topics.sort_values(by='value',ascending=False)
        #remove all where hasData is false
        top_topics = top_topics[top_topics['hasData']==True]
        #remove the hasData column
        top_topics = top_topics.drop(columns=['hasData'])
        #remove formattedValue column, and topic_type column
        top_topics = top_topics.drop(columns=['formattedValue','topic_type'])
        topic_titles = top_topics['topic_title'].tolist()
    else:
        topics_fail = True


    related_queries = pytrends.related_queries()

    if related_queries.get(keyword):
        top_queries = related_queries[keyword]['top']
        if not top_queries.empty:
            #drop rows where value < 20
            top_queries = top_queries[top_queries['value']>=20]

        else:
            queries_fail = True
    else:
        queries_fail = True


    if topics_fail and queries_fail:
        return 404 #no data found
    elif topics_fail:
        return top_queries
    elif queries_fail:
        return topic_titles
    else:
        return [topic_titles,top_queries]
    

def main():
    keyword = input("Enter a keyword: ")
    print(get_top_queries(keyword))


main()
print("Done")