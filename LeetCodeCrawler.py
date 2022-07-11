# -*- coding:UTF-8 -*-
import os
import time
from pathlib import Path
import requests
import json

"""
类说明:下载
Parameters:
    无
Returns:
    无
Modify:
    2019-02-28
"""


class downloader(object):
    def __init__(self):
        self.server = 'https://leetcode.cn/'
        self.target = 'https://leetcode.cn/problemset/all/?page=1'
        self.title = []  # 存放章节名
        self.titleSlug = []  # 存放章节名
        self.nums = 0  # 章节数

    """
    函数说明:获取下载链接
    Parameters:
        无
    Returns:
        无
    Modify:
        2019-02-28
    """
    # 54 页 每页50
    def get_download_url(self):
        count = 0
        for skip in range(54):
            cookie = "gr_user_id=13bf8bb7-48e4-4145-8917-f6dc1e8f426b; _bl_uid=Ojlmv3hUd9Invaaq1qC7mbFeCqtC; a2873925c34ecbd2_gr_last_sent_cs1=yltrcc; _ga=GA1.2.302401184.1653632797; Hm_lvt_fa218a3ff7179639febdb15e372f411c=1656772954,1657351226; csrftoken=ZAbkkXaXbPWlZAyN6eZlQDhfi1kSODbTtnL2wF6yc3f1SUJnv8XPGBYgt8R5Setr; aliyungf_tc=0d8091b88414963b9bfc64c795b1d9323b3407fbdde74472c1b426757c47c3bd; NEW_PROBLEMLIST_PAGE=1; a2873925c34ecbd2_gr_session_id=19c12105-056d-4008-a9c1-5df9471e985e; a2873925c34ecbd2_gr_last_sent_sid_with_cs1=19c12105-056d-4008-a9c1-5df9471e985e; a2873925c34ecbd2_gr_session_id_19c12105-056d-4008-a9c1-5df9471e985e=true; a2873925c34ecbd2_gr_cs1=yltrcc; LEETCODE_SESSION=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiMTYyNDQyNSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImF1dGhlbnRpY2F0aW9uLmF1dGhfYmFja2VuZHMuUGhvbmVBdXRoZW50aWNhdGlvbkJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3ZjJiM2U4N2QwZWU0NTQ1ZWZkZmY3MTg3MzQ0NTQwZTAzYzRlMzY4MjViNWEzNzIzZTc4NDAxNzYyZDM5NTI2IiwiaWQiOjE2MjQ0MjUsImVtYWlsIjoiIiwidXNlcm5hbWUiOiJ5bHRyY2MiLCJ1c2VyX3NsdWciOiJ5bHRyY2MiLCJhdmF0YXIiOiJodHRwczovL2Fzc2V0cy5sZWV0Y29kZS5jbi9hbGl5dW4tbGMtdXBsb2FkL3VzZXJzL2Rhcmtsb3Z5LTkvYXZhdGFyXzE2MzUzNjk5OTEucG5nIiwicGhvbmVfdmVyaWZpZWQiOnRydWUsIl90aW1lc3RhbXAiOjE2NTczNTI4MzIuOTQwMjA0NiwiZXhwaXJlZF90aW1lXyI6MTY1OTg5ODgwMCwidmVyc2lvbl9rZXlfIjoxLCJsYXRlc3RfdGltZXN0YW1wXyI6MTY1NzQzNzkwOH0.ZEd-TVQzL-zwN5L109fPx5cWEHCe6G6WxehcaN5aIbQ"
            header = {
                "cookie": cookie,
                "Content-Type": "application/json",
                "x-csrftoken": "ZAbkkXaXbPWlZAyN6eZlQDhfi1kSODbTtnL2wF6yc3f1SUJnv8XPGBYgt8R5Setr"
            }
            # 发送字典
            postBody = "{\"query\":\"\\n    query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {\\n  problemsetQuestionList(\\n    categorySlug: $categorySlug\\n    limit: $limit\\n    skip: $skip\\n    filters: $filters\\n  ) {\\n    hasMore\\n    total\\n    questions {\\n         difficulty\\n   frontendQuestionId\\n          title\\n      titleCn\\n      titleSlug\\n      topicTags {\\n        name\\n        nameTranslated\\n        id\\n        slug\\n      }\\n      extra {\\n        hasVideoSolution\\n        topCompanyTags {\\n          imgUrl\\n          slug\\n          numSubscribed\\n        }\\n      }\\n    }\\n  }\\n}\\n    \",\"variables\":{\"categorySlug\":\"\",\"skip\": " + str(skip * 50) + ",\"limit\":50,\"filters\":{}}}"

            r1 = requests.post("https://leetcode.cn/graphql/", data=postBody, headers=header)
            # print("r1返回的内容为-->" + r1.content.decode())
            text = json.loads(r1.text)
            for question in text['data']['problemsetQuestionList']['questions']:
                self.title.append(question['frontendQuestionId'] + "." + question['titleCn'])
                self.titleSlug.append(question['titleSlug'])
                count += 1
            #time.sleep(5)
        self.nums = count



    """
    函数说明:获取章节内容
    Parameters:
        target - 下载连接(string)
    Returns:
        texts - 章节内容(string)
    Modify:
        2019-02-28
    """

    def get_contents(self, target, title):
        cookie = "gr_user_id=13bf8bb7-48e4-4145-8917-f6dc1e8f426b; _bl_uid=Ojlmv3hUd9Invaaq1qC7mbFeCqtC; a2873925c34ecbd2_gr_last_sent_cs1=yltrcc; _ga=GA1.2.302401184.1653632797; Hm_lvt_fa218a3ff7179639febdb15e372f411c=1656772954,1657351226; csrftoken=ZAbkkXaXbPWlZAyN6eZlQDhfi1kSODbTtnL2wF6yc3f1SUJnv8XPGBYgt8R5Setr; aliyungf_tc=0d8091b88414963b9bfc64c795b1d9323b3407fbdde74472c1b426757c47c3bd; NEW_PROBLEMLIST_PAGE=1; a2873925c34ecbd2_gr_session_id=19c12105-056d-4008-a9c1-5df9471e985e; a2873925c34ecbd2_gr_last_sent_sid_with_cs1=19c12105-056d-4008-a9c1-5df9471e985e; a2873925c34ecbd2_gr_session_id_19c12105-056d-4008-a9c1-5df9471e985e=true; a2873925c34ecbd2_gr_cs1=yltrcc; LEETCODE_SESSION=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiMTYyNDQyNSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImF1dGhlbnRpY2F0aW9uLmF1dGhfYmFja2VuZHMuUGhvbmVBdXRoZW50aWNhdGlvbkJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3ZjJiM2U4N2QwZWU0NTQ1ZWZkZmY3MTg3MzQ0NTQwZTAzYzRlMzY4MjViNWEzNzIzZTc4NDAxNzYyZDM5NTI2IiwiaWQiOjE2MjQ0MjUsImVtYWlsIjoiIiwidXNlcm5hbWUiOiJ5bHRyY2MiLCJ1c2VyX3NsdWciOiJ5bHRyY2MiLCJhdmF0YXIiOiJodHRwczovL2Fzc2V0cy5sZWV0Y29kZS5jbi9hbGl5dW4tbGMtdXBsb2FkL3VzZXJzL2Rhcmtsb3Z5LTkvYXZhdGFyXzE2MzUzNjk5OTEucG5nIiwicGhvbmVfdmVyaWZpZWQiOnRydWUsIl90aW1lc3RhbXAiOjE2NTczNTI4MzIuOTQwMjA0NiwiZXhwaXJlZF90aW1lXyI6MTY1OTg5ODgwMCwidmVyc2lvbl9rZXlfIjoxLCJsYXRlc3RfdGltZXN0YW1wXyI6MTY1NzQzNzkwOH0.ZEd-TVQzL-zwN5L109fPx5cWEHCe6G6WxehcaN5aIbQ"
        header = {
            "cookie": cookie,
            "Content-Type": "application/json",
            "x-csrftoken": "ZAbkkXaXbPWlZAyN6eZlQDhfi1kSODbTtnL2wF6yc3f1SUJnv8XPGBYgt8R5Setr"
        }
        # 发送字典
        postBody = "{\"operationName\":\"questionData\",\"variables\":{\"titleSlug\":\""+ target + "\"},\"query\":\"query questionData($titleSlug: String!) {\\n  question(titleSlug: $titleSlug) {translatedTitle\\n   translatedContent\\n  difficulty\\n         topicTags {\\n      name\\n      slug\\n      translatedName\\n      __typename\\n    }\\n  }\\n}\\n\"}"

        r1 = requests.post("https://leetcode.cn/graphql/", data=postBody, headers=header)
        # print("r1返回的内容为-->" + r1.content.decode())
        text = json.loads(r1.text)
        # 增加分类
        topicTags = text['data']['question']['topicTags']
        text = str(text['data']['question']['translatedContent'])

        # 替换 <p> </p>
        text = text.replace("<p>", "")
        text = text.replace("</p>", "")
        # 替换 <code> </code>
        text = text.replace("<code>", "`")
        text = text.replace("</code>", "`")
        # 加粗 ** <strong>
        text = text.replace("<strong>", "")
        text = text.replace("</strong>", " ")
        # em
        text = text.replace("<em>", "")
        text = text.replace("</em>", " ")
        # <pre> </pre>
        text = text.replace("<pre>", "```")
        text = text.replace("</pre>", "\n```")
        # <sup> </sup>
        text = text.replace("<sup>", "^")
        text = text.replace("</sup>", "")
        # <ul> </ul>
        text = text.replace("<ul>", "")
        text = text.replace("</ul>", "")
        # <ol> </ol>
        text = text.replace("<ol>", "")
        text = text.replace("</ol>", "")
        # <li> <li>
        text = text.replace("	<li>", "* ")
        text = text.replace("</li>", "")
        # &lt; <
        text = text.replace("&lt;", "<")
        text = text.replace("&gt;", ">")
        # &nbsp;  \n
        text = text.replace("&nbsp;", " ")
        # <u> </u>
        text = text.replace("<u>", "")
        text = text.replace("</u>", "")
        # print(text)
        text = "## " + title + "\n## 题目链接\n[" + self.server + target + "](" + self.server + target +")\n## 题目描述\n" + text
        text = text.replace("示例 1", "## 示例\n示例 1")
        text = text.replace("提示", "## 提示")
        categoryName = ""
        for category in topicTags:
            if categoryName == "":
                if category['translatedName'] is not None:
                    categoryName += "`" + category['translatedName'] + "`"
            else:
                if category['translatedName'] is not None:
                    categoryName += ", `" + category['translatedName'] + "`"
        text = text + "## 题解\n**分类标签：**" + categoryName + "\n"
        text = text + "### 题解一：\n"
        ## 分类下载
        for category in topicTags:
            if category['translatedName'] is not None:
                dl.writer(title, category['translatedName'] + "/" + title + '.md', text, category['translatedName'])
        return text


    """
    函数说明:将爬取的文章内容写入文件
    Parameters:
        name - 章节名称(string)
        path - 当前路径下,小说保存名称(string)
        text - 章节内容(string)
    Returns:
        无
    Modify:
        2019-02-28
    """

    def writer(self, name, path, text, dir):
        write_flag = True
        if dir is not None:
            # 判断目录存在否
            my_file = Path(dir)
            if my_file.is_dir():
                # 存在 就不操作
                print("目录存在哦")
            else:
                os.mkdir(dir)
        with open(path, 'a', encoding='utf-8') as f:
            f.write("## " + name + '\n')
            f.writelines(text)
            f.write('\n\n')


if __name__ == "__main__":
    dl = downloader()
    dl.get_download_url()
    print('LeetCode 开始下载：')
    for i in range(dl.nums):
        dl.writer(dl.title[i], dl.title[i] + '.md',
                  dl.get_contents(dl.titleSlug[i], dl.title[i]), None)
    print('\r', '已下载：  100%', end='', flush=True)
    print('\n下载完成!')
