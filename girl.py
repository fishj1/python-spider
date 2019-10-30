import requests
import json
import os

def getData():
    try:
        gank_content = requests.get("http://gank.io/api/data/福利/1000/1").content
    except:
        print("获取信息失败")

    gank_json = json.loads(gank_content.decode("utf-8"))
    print(gank_json["error"])
    if (gank_json["error"] == False):
        return gank_json["results"]
    return []

def saveImg(img_info_list):
    if os.path.exists("./gank_images/"):
        pass
    else:
        os.makedirs("./gank_images/")
    for img_info in img_info_list:

        try:
            img_data = requests.get(img_info["url"]).content
            file_name = img_info["url"].split("/")[-1]
            path_name = "./gank_images/"+file_name
            if (os.path.exists(path_name) == False):
                with open (path_name, "wb+") as e:
                    e.write(img_data)
                    print(path_name, "保存成功!")
        except:
            print(img_info["url"], "保存失败")
            pass

def main():
    img_info_list = getData()
    saveImg(img_info_list)


if __name__ == '__main__':
    main()