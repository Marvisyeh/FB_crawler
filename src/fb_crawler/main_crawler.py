from random import randint
import json
import time
import re

from requests_soup import chorme_get_page, get_page
from get_contents import get_article_content,get_comments

url= 'https://mbasic.facebook.com/groups/1260448967306807'
soup = chorme_get_page(url)

num = 1
result = list()

while True:
    for i in soup.select('div[id="m_group_stories_container"]')[0].find_all(class_=re.compile(r'[b. ]{2}'))[0]:
        article = dict()
        
        # post timestamp
        post_timestamps = json.loads(i['data-ft'])['page_insights']['1260448967306807']['post_context']['publish_time']
        post_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(post_timestamps))
        print(post_timestamps, post_time)
        article['timestamp']  = post_timestamps
        
        # post id
        story_fbid = json.loads(i['data-ft'])['page_insights']['1260448967306807']['post_context']['story_fbid'][0]
        print(json.loads(i['data-ft'])['page_insights']['1260448967306807']['post_context']['story_fbid'][0])
        article['story_fbid'] = story_fbid
        
        # post username
        posts_user = i.header.select('a')[0].text
        print('Name:', i.header.select('a')[0].text)
        article['postname'] = posts_user
        
        # like
        # likes = i.select('a[class="co cp"]')[0].text
        # print(i.select(f'span[id="like_{story_fbid}"]')[0].text)
        
        # number of comments
        comment_nums = int(i.select('a')[-2].text.split(' ')[0].replace(',',''))
        print(comment_nums)
        article['comment_num'] = comment_nums
        
        # content url
        content_url = i.footer.select('a')[-1]['href']
        article['content_url'] = content_url
        print(content_url)
        
        # get content
        article_contents = get_article_content(content_url)
        article['article_contents'] = article_contents
        print(article_contents)
            
        # get comments
        comment_url = content_url.split('?')[0]
        all_comments = get_comments(comment_url, comment_nums)
        article['all_comments'] = all_comments
        
        result.append(article)

        num += 1
        time.sleep(randint(2,6))

       
        if num % 1000 == 0:
            with open(f'./docs/fb_data_{num}.json', 'w') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            result = list()
        
        else:
            print(num)
    
    next_url = soup.find_all(class_=re.compile(r'([a-z].+ ){4}'))[0].a['href']
    if next_url:
        next_url = 'https://mbasic.facebook.com'+next_url
        soup = get_page(next_url)
    else:
        break
