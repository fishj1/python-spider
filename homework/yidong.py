import requests
from lxml import etree

    
def main():
    # 中国移动
    url_yidong = "https://b2b.10086.cn/b2b/main/listVendorNoticeResult.html?noticeBean.noticeType=2"
    headers = {
        'Content-Type':'application/x-www-form-urlencoded',
        'Referer': 'https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=2',
        'X-Requested-With': 'XMLHttpRequest',
        "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36" 
    }
    data = {
        'noticeBean.title': '基站',
        'noticeBean.startDate': '2019-10-01',
        'noticeBean.endDate': '2019-10-31',
        '_qt': '2YkNmZMzM4UDNiJ2NwUWZiNWZlVzNiFGMkNzMwEDNhJ'
    }
    response = requests.post(url=url_yidong,data=data,headers=headers)
    db_etree = etree.HTML(response.content)
    print(db_etree)
    exit()
    # 提取所有id 格式为 selectResult('607041')
    db_onclicks = db_etree.xpath('//table[1]/text()')
    print(db_onclicks)
    exit()
    # db_onclicks = db_etree.xpath('//table[@class="zb_table"]/text()')
    print(db_onclicks)
    exit()
    list_url = []
    for onclick_str in db_onclicks:
        # 删除字符串中不需要的字符
        id = onclick_str.lstrip('selectResult(\'').rstrip('\')')
        url2 = "https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id="+id 
        list_url.append(url2)
    print(list_url)
    exit()
    '''    
    for url2 in list_url:
        headers2 = {
            "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36" 
        }
        print(url2)
        exit()
        response2 = requests.get(url=url2,headers=headers2)
        db_etree = etree.HTML(response2.content)
        print(db_etree)
        exit()
        # 判断数据中是否有 租赁 or 寻源 or 站址 关键词
        # 匹配数据中的供应商
        # 保存数据到文本
    '''

if __name__ == '__main__':
    main()
    



