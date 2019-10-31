import requests
from lxml import etree

    
def main():
    # 中国电信
    url_dianxin = "https://caigou.chinatelecom.com.cn/MSS-PORTAL/announcementjoin/list.do?provinceJT=JT"
    # 中国联通
    url_liantong = "http://www.chinaunicombidding.cn/jsp/cnceb/web/forword.jsp"
    # 中国移动
    url_yidong = "https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=2"
    headers = {
        'Content-Type':'application/x-www-form-urlencoded',
        "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36" 
    }
    data = {
        "provinceJT" : 'JT',
        "docTitle" : '基站',
        'startDate' : '2019-10-01 00:00:00',
        'endDate' : '2019-10-31 23:59:59'
    }
    response = requests.post(url=url_dianxin,data=data,headers=headers)
    db_etree = etree.HTML(response.content)
    # 提取所有公告名称的链接
    db_onclicks = db_etree.xpath('//tr/td[3]/a/@onclick')
    list_url = []
    for onclick_str in db_onclicks:
        # 删除字符串中不需要的字符
        onclick_arr = onclick_str.lstrip('view(').rstrip(')').split(',')
        id = onclick_arr[0].lstrip('\'').rstrip('\'')
        categroyFlag = onclick_arr[1].lstrip('\'').rstrip('\'')
        encryCode = onclick_arr[2].lstrip('\'').rstrip('\'')
        url2 = "https://caigou.chinatelecom.com.cn//MSS-PORTAL/account/viewad.do?category="+categroyFlag+"&id="+id+"&encryCode="+encryCode;
        list_url.append(url2)
       
        '''
        with open("./1.txt","ab+") as f:
            # tmp_data = "公告名称:" + str(gname) + "供应商:" + str(gys) + "\n"
            tmp_data = url2 + "\n"
            f.write(tmp_data.encode('utf-8'))
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

if __name__ == '__main__':
    main()
    



