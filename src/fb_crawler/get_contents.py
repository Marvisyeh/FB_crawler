from requests_soup import chorme_get_page
from user_agent import generate_user_agent
from bs4 import BeautifulSoup
from random import randint
import requests
import time
import re

# Full article
def get_article_content(content_url):
    headers = {'User-Agent':generate_user_agent()}
    
    # article_res = requests.get(content_url, headers=headers)
    # article_soup = BeautifulSoup(article_res.text, 'html.parser')
    article_soup = chorme_get_page(content_url)

    article_contents = article_soup.select('div[style=""]')[0].text
    
    return article_contents

# All comments
def get_comments(comment_url, comment_nums):
    all_comments = list()
    
    for i in range(0, comment_nums, 10):
        headers = {'User-Agent':generate_user_agent()}
        payload = {
            'p':i,
            'refid':'18'
        }

        res_comments = requests.get(comment_url, headers=headers, params=payload)
        soup_comment = BeautifulSoup(res_comments.text, 'html.parser')
        
        for com in soup_comment.find_all(id=re.compile(r'^\d{10,17}')):
            
            # if comment in comments
            more_comments = com.find_all(id=re.compile('comment_replies_more.+'))
            
            if more_comments:
                
                more_comments = 'https://mbasic.facebook.com'+com.find_all(id=re.compile('comment_replies_more.+'))[0].a['href']
    #             print(more_comments)
                time.sleep(randint(3,6))

                res_more = requests.get(more_comments, headers=headers)
                soup_more = BeautifulSoup(res_more.text, 'html.parser')

                for m in soup_more.find_all(id=re.compile(r'\d{10,17}')):
                    per_comment = {}

                    reponse_id = m['id']
                    per_comment['id']=reponse_id
                    # print(m['id'], end=', ')

                    response_name = m.a.text
                    per_comment['name'] = response_name
                    # print(m.a.text, end=', ')

                    # 如果留言中的留言超過10筆，會有額外的url
                    try:
                        response_content = m.div.div.text
                        per_comment['comment'] = response_content
                        # print(m.div.div.text)
                    except AttributeError as e:
                        print(e)
                        pass
                    all_comments.append(per_comment)
                
            
            else:
                
                per_comment = {}
                
                reponse_id = com['id']
                per_comment['id']=reponse_id
                # print(com['id'])

                response_name = com.a.text
                per_comment['name'] = response_name
                # print(com.a.text, end=":")

                response_content = com.select('div')[0].text.split('讚')[0].replace(response_name,'')
                per_comment['comment'] = response_content
                # print(com.select('div')[0].text.split('讚')[0].replace(com.a.text,''))

                all_comments.append(per_comment)

                
                
                
            time.sleep(randint(3,7))
        time.sleep(randint(2,8))
        

    return all_comments

if __name__ == '__main__':
    url = 'https://mbasic.facebook.com/comment/replies/?ctoken=5413685551983107_5416909204994075&count=11&curr&pc=1&ft_ent_identifier=5413685551983107&gfid=AQCCwRAMTgknIVNB_EU&refid=18&__tn__=R'
    get_comments(url, 2115)