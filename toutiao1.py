import json

import requests
import execjs  # pip install PyExecJS


class NewToutiao:
    def __init__(self, url, type_="全部"):
        if type_ == "全部":
            self.type = "profile_all"
        elif type_ == "文章":
            self.type = "pc_profile_article"
        elif type_ == "视频":
            self.type = "pc_profile_video"
        elif type_ == "微头条":
            self.type = "pc_profile_ugc"
        elif type_ == "合集":
            self.type = "profile_collection"
        elif type_ == "问答":
            self.type = "profile_wenda"
        self.js = execjs.compile(open("new_sign.js", "r",encoding="utf-8").read())
        self.max_behot_time = 0
        self.url = url
        self.token = self.url.split('/')[-1]
        self.session = requests.Session()
        # 这个就是返回数据的地方，可以自己封装一下
        while True:
            try:
                content = self.get_data()
                print(content)
            except Exception as e:
                print('已经没有数据了，或者被封IP了')

    def get_signature(self, url):
        signature = self.js.call("get_sign", url)
        return f"&_signature={signature}"

    # 获取结果
    def get_data(self):
        base_url = 'https://www.toutiao.com/toutiao'
        path = f'/api/pc/feed/?category={self.type}&utm_source=toutiao&visit_user_token={self.token}&max_behot_time={self.max_behot_time}'
        base_url += path
        signature = self.get_signature(base_url)
        base_url += signature
        headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
        }
        response = requests.get(base_url, headers=headers)
        content = json.loads(response.text)
        self.max_behot_time = content['next']['max_behot_time']
        return content


if __name__ == '__main__':
    # 修改用户链接就可以直接获取了，type是你要爬取的类型，比如：全部，文章，视频，微头条等
    NewToutiao('https://www.toutiao.com/c/user/token/MS4wLjABAAAAmWcWyIWzrIhrj9-KxDUTVV3GWfXyDNTggj90GsKgNfM',
               type_="全部")
