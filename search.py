#python搜索关键词 统计数量脚本
import os
import xlrd
import xlwt
from xlutils.copy import copy
from docx import Document

#读取目录下所有文件名
def ListFilesToTxt(dir, extype):
    exts = extype.split(" ")
    to_list = []
    files = os.listdir(dir)
    for name in files:
        for ext in exts:
            if (name.endswith(ext)):
                to_list.append(name)
    return to_list
    
#数据写入excel中
def write_excel_xls_append(path, value):
    index = len(value)  # 获取需要写入数据的行数
    workbook = xlrd.open_workbook(path)  # 打开工作簿
    sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
    worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
    rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
    new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
    new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格
    for row in range(1,rows_old):
        case_name = worksheet.cell_value(row, 1)   #获取单元格值
        for i in range(0, index):
            if value[i][0] == case_name:
                for k in range(1, len(value[i])):             
                    new_worksheet.write(row, 12+k, value[i][k])  # 统计数据从N开始 14
                break
    new_workbook.save(path)  # 保存工作簿
    print("xls格式表格【追加】写入数据成功！")

if __name__ == '__main__':
    #列名 案例名称
    cloumn = ['序号','案例名称','单位名称','案例来源','所属行业','云计算','大数据','人工智能','物联网','机器人/无人机','区块链','AR/VR','移动通信']
    bigdata = ['大数据','数据挖掘','数据分析']
    ai = ['人工智能','图像识别', '人脸识别' ,'语音识别', '深度学习', '机器学习', '联邦学习','语义分析']
    robot = ['机器人','无人机']
    vr_ar = ['VR','AR','虚拟现实','增强现实']
    blockchain = ['区块链','以太坊','智能合约','比特币','加密货币','去中心化' ]
    mobileconnect = ['移动通信','移动互联']
    
    dir_path = "./"   #目录名
    all_files = ListFilesToTxt(dir_path,"docx")
    print("找到docx文件数量:")
    print(len(all_files))
    serial_num = 1
    dic_word = []
    search_file = []
    for path in all_files:
        document = Document(path)
        tables = document.tables #获取文件中的表格集
        if tables is None or len(tables) == 0:
            continue
        else:
            table0 = tables[0]     #获取文件中的第一个表格
            dic = []
            #序号
            search_file.append(path)
            # 案例名称
            name = table0.cell(0,1).text
            dic.append(name)
            # 单位名称
            #company_name = table0.cell(1,1).text
            #dic.append(company_name)
            #dic.append("案例征集")
            #所属行业
            #industry = table0.cell(4,1).text
            #dic.append(industry)

            result = ""
            for i in range(1,len(table0.rows)):
                #读取第2列的数据   
                try :
                    result += table0.cell(i,1).text
                except IndexError:
                    pass
            #1.云计算
            if result.find('云计算') != -1:
                dic.append(1)
            else:
                dic.append(" ")
            #2.大数据
            big_flag = " "
            for j in bigdata:
                if result.find(j) != -1:
                    big_flag = 1
                    break
            dic.append(big_flag)
            #3.人工智能
            ai_flag = " "
            for h in ai:
                if result.find(h) != -1:
                    ai_flag = 1
                    break
            dic.append(ai_flag)
            #4.物联网
            if result.find('物联网') != -1:
                dic.append(1)
            else :
                dic.append(" ")
            #5.机器人/无人机
            rb_flag = " "
            for k in robot:
                if result.find(k) != -1:
                    rb_flag = 1
            dic.append(rb_flag)
            #6.区块链
            blockchain_falg = " "
            for b in blockchain:
                if result.find(b) != -1:
                    blockchain_falg = 1
            dic.append(blockchain_falg)
            #7.VR/AR
            va_falg = " "
            for l in vr_ar:
                if result.find(l) != -1:
                    va_falg = 1
            dic.append(va_falg)
            #8.移动通信
            mobile_co_falg = " "
            for m in mobileconnect:
                if result.find(m) != -1:
                    mobile_co_falg = 1
            dic.append(mobile_co_falg)
            serial_num += 1
            dic_word.append(dic)
    xlsx_path = ".\案例分析-阶段-汇总test1.xlsx"
    write_excel_xls_append(xlsx_path,dic_word)
    print("一共找到匹配的数据总数:")
    print(len(dic_word))
    print(dic_word)

