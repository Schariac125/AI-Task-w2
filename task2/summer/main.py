import requests
import json
import os
import csv

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
}

if __name__ == "__main__":
    url = "https://summer-ospp.ac.cn/api/getProList"
    os.makedirs("project", exist_ok=True)

    for i in range(1, 13):
        body = {
            "difficulty": [],
            "lang": "zh",
            "orgName": [],
            "pageNum": f"{i}",
            "pageSize": "50",
            "programName": "",
            "programmingLanguageTag": [],
            "supportLanguage": [],
            "techTag": [],
        }

        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        data = response.json()
        filename = os.path.join("project", f"inf{i}.json")
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    print("数据已保存到 project 文件夹中。")

    inf_file = "information.csv"
    with open(inf_file, "w", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["项目名", "项目难度", "技术领域标签", "项目简述", "项目产出要求"]
        )
        for i in range(1, 13):
            file = os.path.join("project", f"inf{i}.json")
            with open(file, "r", encoding="utf-8") as js:
                data = json.load(js)
                project_list = data.get("rows", [])
                for data in project_list:
                    body = {"programId": data.get("programCode"), "type": "org"}
                    url = "https://summer-ospp.ac.cn/api/getProDetail"
                    response = requests.post(url, headers=headers, json=body)
                    response.raise_for_status()
                    result = response.json()
                    project_name = data.get("programName")
                    project_difficulty = data.get("difficulty")
                    project_tech_tags = "".join(data.get("techTag", [])).replace(",","")
                    project_description = result.get("programDesc")
                    project_requirements = result.get("programReq")
                    writer.writerow(
                        [
                            project_name,
                            project_difficulty,
                            project_tech_tags,
                            project_description,
                            project_requirements,
                        ]
                    )
                    project_pdf=f"https://summer-ospp.ac.cn/previewPdf/{data.get("proId")}"
                    safe_project_name=project_name.replace("/", "_").replace("\\", "_").replace(":", "_").replace("*", "_").replace("?", "_").replace('"', "_").replace("<", "_").replace(">", "_").replace("|", "_")
                    pdf_filepath=os.path.join("pdf_file", f"{safe_project_name}.pdf")
                    pdf_data=requests.get(url=project_pdf, headers=headers).content
                    os.makedirs("pdf_file", exist_ok=True)
                    try:
                        with open(pdf_filepath, "wb") as f1:
                            f1.write(pdf_data)
                    except Exception as e:
                        print(f"下载 {project_name} 的 PDF 文件时发生错误: {e}")
                        continue
    print(f"项目信息已保存到 {inf_file} 文件中。")