import requests
import random
import xlwt
from lxml import etree

#设置表格样式
def set_style(name,height,bold=False):
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style
#写Excel
def write_excel(row_all):
    f = xlwt.Workbook()
    sheet1 = f.add_sheet('学生',cell_overwrite_ok=True)
    row0 = ["项目名称","需求数量","链接"]
    #写第一行
    for i in range(0,len(row0)):
        sheet1.write(0,i,row0[i],set_style('Times New Roman',220,True))
    #写第二行之后...
    j = 0
    for row_li in row_all:
        j+=1
        for i in range(0,len(row_li)):
            sheet1.write(j,i,row_li[i],set_style('Times New Roman',220,False))
    f.save('test_yidong.xls')  

def main():
    # 中国移动
    url_yidong = "https://b2b.10086.cn/b2b/main/listVendorNoticeResult.html?noticeBean.noticeType=1"

    my_headers = [
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
        'Opera/9.25 (Windows NT 5.1; U; en)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
        'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
        "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
        "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36" 
    ]

    headers = {
        # 加了charset=UTF-8 noticeBean.title 搜索有数据了。。。
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=2',
        'X-Requested-With': 'XMLHttpRequest',
        "User-Agent" : random.choice(my_headers),
        'Host': 'b2b.10086.cn',  
         # 加了cookie没有403的问题了 
        'Cookie': 'saplb_*=(J2EE204289820)204289851; JSESSIONID=Hjllv9x31fcZMIXTmtkbt9lACSEqbgE7Ny0M_SAPu2IWRHCmqZVYU6PyN72iOFPb'
    }
    data = {
        'noticeBean.title': '基站',
        'noticeBean.startDate': '2019-10-01',
        'noticeBean.endDate': '2019-11-10',
        'page.currentPage' : 1,
        # 默认给一个数值吧
        'page.perPageSize' : 30,
        '_qt': 'TN0kDNIzNyYGZmFzMhNjNwEmYjFjMkZmNkRzN5MjZmN'
    }
    response = requests.post(url=url_yidong,data=data,headers=headers)
    db_etree = etree.HTML(response.content)
    # 提取所有id 格式为 selectResult('607041')
    db_onclicks = db_etree.xpath('//table/tr/@onclick')
    list_url = []
    for onclick_str in db_onclicks:
        # 删除字符串中不需要的字符
        id = onclick_str.lstrip('selectResult(\'').rstrip('\')')
        url2 = "https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id="+id 
        list_url.append(url2)
    row_all = []
    for url2 in list_url:
        headers2 = {
            "User-Agent" : random.choice(my_headers)
        }
        response2 = requests.get(url=url2,headers=headers2)
        # 解决乱码问题
        db_etree2 = etree.HTML(response2.content,parser=etree.HTMLParser(encoding='utf8'))
        # 项目名称
        name = db_etree2.xpath('//table//h1/text()')
        for n in name:
            pj_name = n
        # 站址类型 场地租赁 ->微站 站址租赁,机房租赁,铁塔租赁-> 宏站
        # 建设主体 有自建为自建，其他全部为第三方 
        # 需求数量
        sum_list = db_etree2.xpath('//div[@id="ggdiv2"]//table//td[4]/text()')
        # 记录日志
        with open('error.txt',"ab+") as f1:
            err_log = url2 +" sum_list:" + str(sum_list) + "\n" 
            f1.write(err_log.encode("utf-8"))
        sum_res = 0
        for a in sum_list:
            try:
                sum_res += round(float(a))
            except ValueError:
                pass
            continue
        # 区市
        # 供应商名称
        rowli = []
        rowli.append(pj_name)
        rowli.append(sum_res)
        rowli.append(url2)
        row_all.append(rowli)
        # 数据写入txt
        with open("./yidong2.txt", "ab+") as f:
            tmp_data = "项目名称:" + str(pj_name) + "   需求数量:" + str(sum_res) + "链接:" + url2 + "\n"
            f.write(tmp_data.encode("utf-8"))
        # 数据写入excel
    write_excel(row_all)

if __name__ == '__main__':
    main()
    



