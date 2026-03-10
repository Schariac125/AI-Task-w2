import requests
import re
import csv
import os
from lxml import etree

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
}

#Code by Gemini
def get_download_count(file_link, file_id):
    owner_match = re.search(r"owner=(\d+)", file_link)
    if not owner_match:
        return ""

    owner = owner_match.group(1)
    count_url = (
        "https://jwch.fzu.edu.cn/system/resource/code/news/click/clicktimes.jsp"
        f"?wbnewsid={file_id}&owner={owner}&type=wbnewsfile&randomid=nattach{file_id}"
    )
    response = requests.get(url=count_url, headers=headers)
    return str(response.json().get("wbshowtimes", ""))

#Code by Myself
if __name__ == "__main__":
    filename = "imformation.csv"
    with open(filename, "w", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        for idx in range(180, 209):
            url = f"https://jwch.fzu.edu.cn/jxtz/{idx}.htm"
            page = requests.get(url=url, headers=headers)
            page.encoding = "utf-8"
            tree = etree.HTML(page.text)
            data = tree.xpath('//ul[@class="list-gl"]/li')
            for i in data:
                # 日期
                date = "".join(i.xpath('./span[@class="doclist_time"]//text()'))
                # 发布单位
                department = "".join(i.xpath("./text()")).replace('【','').replace('】','').strip()
                # 标题
                title = i.xpath("./a/@title")[0]
                # 链接
                link = i.xpath("./a/@href")[0]
                # 完整的拼接链接
                true_link = f"https://jwch.fzu.edu.cn/{link}"
                res = requests.get(url=true_link, headers=headers)
                res = res.text
                tree2 = etree.HTML(res)
                data2 = tree2.xpath('//ul[@style="list-style-type:none;"]/li')
                if data2:
                    for j in data2:
                        # 文件下载链接
                        file_link = f"https://jwch.fzu.edu.cn{j.xpath('./a/@href')[0]}"
                        # 文件名
                        raw_name = "".join(j.xpath("./a//text()")).strip()
                        try:
                            name = raw_name.encode("iso-8859-1").decode("gbk")
                        except:
                            try:
                                name = raw_name.encode("iso-8859-1").decode("utf-8")
                            except:
                                name = raw_name  
                        # 文件id
                        result = re.search(r"wbfileid=(\d+)", file_link).group(1)
                        # 文件下载次数
                        download_num = get_download_count(file_link, result)
                        file_data = requests.get(url=file_link, headers=headers).content
                        full_path = os.path.join("all_file", name)
                        with open(full_path, "wb") as f1:
                            f1.write(file_data)
                        writer.writerow([date, department, title, true_link,name,result,download_num])
                else:
                    writer.writerow([date, department, title, true_link,"无附件"])
    print("爬好了喵")
