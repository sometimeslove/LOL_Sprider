#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@author:Chris iven
#Python version 3.6


#1.分析LOL官网行为!
#发现这个网页的所有数据都是经过js生成的!意思就是说 他的数据全部不在该网页里面,而是在一个JS文件里面!
#所以我们获取JS文件即可!

import requests
import json,re,os
class LOL_Spider(object):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"}
    def __init__(self,url):
        self.url = url

    def get_hero_data(self):
        response = requests.get(self.url,headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 BIDUBrowser/8.7 Safari/537.36"},timeout=10)
        if response.status_code == 200:
            with open("hero_data.json","w")as f:
                f.write(json.dumps(response.text, indent=2))

        #打开文件
        with open("hero_data.json","r")as f:
            string = f.read()
        data = json.loads(string)

        hero_name = []#英雄的名字
        hero_id = []#英雄的图片id
        pattern1 = re.compile('"keys":{(.*?)},"data".*?')
        #匹配出第一段数据!
        first_data = re.findall(pattern1,data)[0]
        pattern2 = re.compile('"(.*?)":"(.*?)"')
        for i in re.findall(pattern2,first_data):
            hero_id.append(i[0])#id
            hero_name.append(i[1])#名字
        print(hero_name,"\n",hero_id)
        return hero_name,hero_id


    def download_pic(self,hero_name,hero_id):
        i = 0
        while i <len(hero_id):
            j = 0
            while j < 15:
                url = "http://ossweb-img.qq.com/images/lol/web201310/skin/big"+hero_id[i]+"00"+str(j)+".jpg"
                #print(url)
                print("下载链接是:",url)
                response = requests.get(url,headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 BIDUBrowser/8.7 Safari/537.36"},timeout=10)

                detail_line = 'https://game.gtimg.cn/images/lol/act/img/js/hero/' + hero_id[i] + '.js'
                res = requests.get(detail_line, headers=self.headers).json()
                for skin in res["skins"]:
                    if not skin["mainImg"]:
                        continue
                    item = {}
                    item["heroName"] = skin["heroName"]  # 英雄的名字
                    item["skinName"] = skin["name"].replace("/", "_")  # 皮肤的名字并将名字中出现的斜线/用下划线代替_
                    item["skinImage"] = skin["mainImg"]  # 皮肤的图片链接
                    print(item)

                if "404 page not found" in response.text:
                    print(hero_name[i], "下的皮肤已经下载完毕!!")
                    break
                # else:
                    # try:
                    #     os.mkdir("英雄联盟各英雄和皮肤/"+hero_name[i])
                    # except FileExistsError:
                    #     pass
                    # with open("英雄联盟各英雄和皮肤/"+hero_name[i]+"/"+str(j)+".jpg","wb")as f:
                    #     f.write(response.content)
                j+=1
            i+=1
    def Start_Spider(self):
        hero_name,hero_id = self.get_hero_data()
        self.download_pic(hero_name,hero_id)


if __name__=="__main__":
    url = "http://lol.qq.com/biz/hero/champion.js"
    lol = LOL_Spider(url)
    lol.Start_Spider()