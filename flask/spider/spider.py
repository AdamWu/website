import os
import shutil
import requests
from lxml import etree
import time

 
class MZiTu:
 
    # 初始化对象属性
    def __init__(self):
        self.index_url = "https://www.mzitu.com/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
            "Referer": "https://www.mzitu.com/"
        }
        self.path = "meizitu"


        self.urls_finish = []
        self.urls_downloads = []

        self.file = open('finished.txt','a+')
        self.file.seek(0, 0)
        lines = self.file.readlines()
        for line in lines:
            self.urls_finish.append(line.strip())

        self.urls_downloads.append(self.index_url)
        

    # 发送request请求
    def send_request(self, url):
        counter = 0
        while True:
            response = requests.get(url, headers=self.headers, allow_redirects=False)
            if response.status_code == 200:
                return response.content
            
            counter = counter + 1
            if counter > 1000:
                print("*" * 10, 'request too many fail!!', "*" * 10)
                return None

            time.sleep(0.1)
 

    def add_url(self, url):
        if url in self.urls_finish:
            return
        if url in self.urls_downloads:
            return
        self.urls_downloads.append(url)

    # 解析每页的数据
    def parse(self, html_str):
        html = etree.HTML(html_str)

        # 写真集
        titles = html.xpath('//img[@class="lazy"]')
        for title in titles:
            href = title.xpath('../@href')[0]
            self.add_url(href)
        
        # 下一页
        next_page_url = html.xpath('//a[@class="next page-numbers"]/@href')
        for url in next_page_url:
            self.add_url(url)

        # 是否写真集首页
        title = html.xpath('//h2[@class="main-title"]')
        return title[0].text if title else None
 
    # 获取每张写真集的img_url
    def get_img_url(self, detail_html):
        html = etree.HTML(detail_html)
        lst = html.xpath('//div[@class="main-image"]/p/a/img/@src')
        img_url = lst[0] if lst else None

        next_img_url = html.xpath('//span[contains(text(),"下一页")]/../@href')
        next_url = next_img_url[0] if next_img_url else None
        return img_url, next_url
 
    # 保存img
    def save_image(self, title, img_url_list):
        
        total_image = len(img_url_list)
        final_dir = self.path + '/' + '[{}P]'.format(str(total_image)) + title

        if os.path.exists(final_dir):
            shutil.rmtree(final_dir)
        os.makedirs(final_dir)

        for img_url in img_url_list:
            image_data = self.send_request(img_url)
            if image_data == None:
                continue

            file_name = final_dir + '/' + img_url[-9:]
            try:
                f = open(file_name, 'wb+')
                f.write(image_data)
                f.close()
            except:
                print("*" * 10, 'io error', "*" * 10)
                continue
            
            print("*" * 10, img_url, 'finish', "*" * 10)
 
 
    def run(self):

        while True:

            if len(self.urls_downloads) > 0:
                url = self.urls_downloads.pop(0)
                print("-" * 10 + "parse url: {} (left:{})".format(url,len(self.urls_downloads)) + "-" * 10)

                if url in self.urls_finish:
                    print("-" * 10 + "already finished" + "-" * 10)
                    continue

                while True:
                    content = self.send_request(url)
                    if content == None:
                        break
                    html_str = content.decode()

                    # 搜索新的写真集
                    title = self.parse(html_str)

                    # 获取写真集详情
                    img_url_list = []
                    if title != None:
                        next_url = url

                        while True:    
                            content = self.send_request(next_url)
                            if content == None:
                                break
                            detail_html = content.decode()

                            img_url, next_url2 = self.get_img_url(detail_html)
                            if img_url != None:
                                next_url = next_url2
                                img_url_list.append(img_url)
                            if next_url is None:
                                break

                    print("-" * 10 + "images count: {}".format(len(img_url_list)) + "-" * 10)
                
                    # 保存图片
                    if img_url_list:
                        
                        self.save_image(title, img_url_list)
                    
                        # 保存结果
                        self.urls_finish.append(url)
                        self.file.write(url+'\n')
                        self.file.flush()

                    break

                # 结束
                print('\n\n')
 
 
def main():
    mz = MZiTu()
    mz.run()

if __name__ == '__main__':
    main()