import requests  # 模拟请求
import json  # 轻量级的数据交换格式，易于人阅读和编写
from urllib import parse  # 用于url的解析，合并，编码，解码
import os  # 用于对文件进行操作了模块
import time  # 时间模块


class BaiduImageSpider(object):  # 创建一个类
    def __init__(self):

        self.directory = r"F:\Python\爬虫代码\images_{}"  # 存储目录  这里需要修改为自己希望保存的目录  {}不要丢
        self.json_count = 0  # 请求到的json文件数量（一个json文件包含30个图像文件）
        self.url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&logid=5179920884740494226&ipn=rj&ct' \
                   '=201326592&is=&fp=result&queryWord={' \
                   '}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&hd=&latest=&copyright=&word={' \
                   '}&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&nojc=&pn={' \
                   '}&rn=30&gsm=1e&1635054081427= '
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30 '
        }

    # 获取图像链接可回收物
    def get_image_link(self, url):
        list_image_link = []  # 建立一个图像列表
        strhtml = requests.get(url, headers=self.header)  # Get方式获取网页数据
        jsonInfo = json.loads(strhtml.text)  # json.loads 将已编码的 JSON 字符串解码为 Python 对象
        # 获取图像的链接存到了列表中
        for index in range(30):
            # 将jsonInfo中的数据放到列表中
            list_image_link.append(jsonInfo['data'][index]['thumbURL'])  # 在列表末尾添加新的对象，将图像的链接放在列表中
        return list_image_link

        # 创建存储文件夹

    def create_directory(self, name):
        self.directory = self.directory.format(name)  # 补全文件夹名称
        # 如果目录不存在则创建
        if not os.path.exists(self.directory):  # 如果没有该路径
            os.makedirs(self.directory)  # 使用os 模块创建该目录
        self.directory += r'\{}'

    # 下载图片
    def save_image(self, img_link, filename):
        # img_link为图像的链接
        res = requests.get(img_link, headers=self.header)  # 模拟get请求 返回信息res 对象
        if res.status_code == 404:
            print(f"图片{img_link}下载出错------->")
        with open(filename, "wb") as f:  # 使用二进制形式 覆盖写文件
            f.write(res.content)  # requests模块中的content返回的是二进制的数据
            print("存储路径：" + filename)  # 打印存储路径

    # 入口函数
    def run(self,name):
        searchName_parse = parse.quote(name)  # 编码 将中文转换为url编码格式

        self.create_directory(name)  # 调用创建文件夹的函数，根据查询内容创建文件

        pic_number = 0  # 图像数量
        for index in range(self.json_count):
            pn = (index + 1) * 30  # pn表示一组文件，一组包含30个图像内容
            # 图像网页链接大部分相同，输入的url编码（serrchName_parse）不同，获取的图像类型不同
            # 通过不同的 url 编码获取新的链接
            request_url = self.url.format(searchName_parse, searchName_parse, str(pn))
            # str()函数将整数作为字符串，让其与两侧的字符串类型保持一致

            list_image_link = self.get_image_link(request_url)  # 通过新的 url 调用图像链接函数，获取新的图像链接
            for link in list_image_link:
                pic_number += 1
                self.save_image(link, self.directory.format("img_"+name+"_"+str(pic_number) + '.jpg'))
                time.sleep(0.2)  # 休眠0.2秒，防止封ip
        print(name + "图像下载成功")
        print("图片存入{}".format(self.directory))


if __name__ == '__main__':  # 代码作为模块，在别的文件调用时，不会直接运行整个脚本
    filename = open("./refuse_name.txt", encoding="utf-8")
    str_all = filename.readlines()
    for i in str_all:
        line = i.strip("\n")
        print("正在爬取" + line + "类型的图片")
        spider = BaiduImageSpider()
        spider.json_count = 8  # 默认下载一组图片（30张）
        spider.run(line)
    filename.close()
