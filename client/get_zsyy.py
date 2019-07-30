"""中山医院爬虫"""
import re
import os
import requests
import time
from lxml import etree

s = requests.session()
base_url = "http://oa.xmzsh.com/general/file_folder/"
urls_dict = {
    "folders_ids_url": "tree.php?SORT_ID=0&FILE_SORT=1&_=1564106238716",
}
folders_ids_url = base_url + urls_dict.get("folders_ids_url")
headers = {
    'Accept': 'application/json,text/javascript,*/*;q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': f'USER_NAME_COOKIE=zhangql; UI_COOKIE=0; PHPSESSID=7b508c91be542119a24aa087aecb21a7; OA_USER_ID=zhangql; SID_1404=cc15c519; LAST_OPERATION_TIME={time.time()}',
    'Host': 'oa.xmzsh.com',
    'Referer': 'http://oa.xmzsh.com/general/file_folder/index.php?FILE_SORT=1&FROM_TABLE=&BTN_CLOSE=&SORT_ID=&CONTENT_ID=&show_flag=',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }

folders = s.get(url=folders_ids_url, headers=headers).json()
tree_dict = [{"title": f.get("title"), "url":f.get("url").replace("folder.php", "tree.php")} for f in folders]
print(tree_dict)
for t in tree_dict:
    title = t["title"]
    if not os.path.exists(title):
        os.mkdir(title)
    tree_list = s.get(url=base_url + t["url"], headers=headers).json()
    contents_urls = [t.get("url") for t in tree_list]
    for u in contents_urls:
        if u:
            print(u)
            r = re.compile(r"[0-9]+\&").findall(u)
            sort_id = r[0][:-1]
            content = s.get(url=base_url+u+"&start=0&TOTAL_ITEMS=100&PAGE_SIZE=100", headers=headers)
            selector = etree.HTML(content.text)
            ids_nodes = selector.xpath("//input[@type='checkbox']")
            titles_nodes1 = selector.xpath("//a[@title='']")
            titles_nodes2 = selector.xpath("//img[@align='absMiddle']")
            titles = []
            for t1 in titles_nodes1:
                if t1.text:
                    titles.append(t1.text)
            for t2 in titles_nodes2:
                if t2.tail and t2.tail != "签阅":
                    titles.append(t2.tail)
            print(titles)
            ids = [n.attrib.get("value") for n in ids_nodes if n.attrib.get("value")]
            print(ids)
            ids_str = ','.join(ids)
            down_url = f"http://oa.xmzsh.com/general/file_folder/down.php?FILE_SORT=1&SORT_ID={sort_id}&start=0&CONTENT_ID={ids_str}"
            x = s.get(url=down_url, headers=headers, stream=True)
            x.encoding = 'utf-8'
            for chunk in x.iter_content(chunk_size=512):
                i = 0
                with open(f"/home/ihyf/download_test/{titles[0]}", "wb") as f:
                    if chunk:
                        f.write(chunk)
                i += 1
                f.close()







# content = selector.xpath('//div[@id="content"]/ul[@id="ul"]/li/text()')
content = selector.xpath("//span[@class='convert']")
flo_rmb = selector.xpath("//span[@class='convert']")[0].text
flo_usd = selector.xpath("//span[@class='convert']")[1].text
flo_btc = selector.xpath("//span[@class='convert']")[2].text
"http://oa.xmzsh.com/general/file_folder/folder.php?SORT_ID=4796&FILE_SORT=1"
"http://oa.xmzsh.com/general/file_folder/folder.php?SORT_ID=4796&FILE_SORT=1&start=0&TOTAL_ITEMS=12&PAGE_SIZE=100"
"http://oa.xmzsh.com/general/file_folder/down.php?FILE_SORT=1&SORT_ID=4796&start=0&CONTENT_ID=267419"
"http://oa.xmzsh.com/general/file_folder/down.php?FILE_SORT=1&SORT_ID=4796&start=0&CONTENT_ID=267418"
"http://oa.xmzsh.com/general/file_folder/down.php?FILE_SORT=1&SORT_ID=4796&start=0&CONTENT_ID=267419,267418,267417,267416,267415,212653,212652,196268,196267,176470,"

