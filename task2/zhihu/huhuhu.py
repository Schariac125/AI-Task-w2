from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
import json
import random
import os
import csv
import time

if __name__ == "__main__":
    # 知乎似乎升级了反爬机制，现在好像要加上这个才能爬出来
    # Code by Gemini
    options = Options()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Edge(options=options)

    # 注入 JS 屏蔽特征
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        },
    )

    target_url = "https://www.zhihu.com/topic/19551137/unanswered"
    filecookie = "cookies.json"

    # Code by Myself
    if os.path.exists(filecookie):
        driver.get("https://www.zhihu.com")
        time.sleep(2)
        with open(filecookie, "r", encoding="utf-8") as f:
            cookies = json.load(f)
        for cookie in cookies:
            if "expiry" in cookie:
                del cookie["expiry"]
            driver.add_cookie(cookie)
        driver.get(target_url)
    else:
        driver.get(target_url)
        input("扫完按回车")
        cookies = driver.get_cookies()
        with open(filecookie, "w", encoding="utf-8") as f:
            json.dump(cookies, f, ensure_ascii=False)

    time.sleep(8)
    filename = "information.csv"
    already_find = set()
    ids = []

    print("正在获取问题列表...")
    while len(ids) < 25:
        res = driver.find_elements(By.XPATH, '//div[@class="QuestionItem-title"]//a')
        for item in res:
            link = item.get_attribute("href")
            if link and link not in already_find:
                ids.append(link)
                already_find.add(link)
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(random.uniform(2, 4))

    with open(filename, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["标题", "描述", "回答内容"])

        for link in ids:
            try:
                driver.get(link)
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "QuestionHeader-title")
                    )
                )
                title = driver.find_element(
                    By.XPATH, "//h1[@class='QuestionHeader-title']"
                ).text
                try:
                    button = driver.find_element(
                        By.CSS_SELECTOR,
                        ".Button.QuestionRichText-more.FEfUrdfMIKpQDJDqkjte.Button--plain.fEPKGkUK5jyc4fUuT0QP",
                    )
                except:
                    button = None
                if button:
                    button.click()
                    time.sleep(3)
                    description = driver.find_element(
                        By.XPATH, '//span[@class="RichText ztext css-1oz8dhe"]/p'
                    ).text
                    time.sleep(2)
                else:
                    description = "没有详细描述"
                driver.execute_script("window.scrollTo(0, 1000);")
                time.sleep(random.uniform(2, 4))
                user = set()
                attempt = 0
                while len(user) <= 10 and attempt < 15:
                    answers = driver.find_elements(By.CLASS_NAME, "List-item")
                    for answer in answers:
                        try:
                            user_name = answer.find_element(
                                By.CLASS_NAME, "css-1gomreu"
                            ).text
                            if user_name in user:
                                continue
                            else:
                                user.add(user_name)
                                content = answer.find_elements(
                                    By.XPATH,
                                    '//span[@class="RichText ztext CopyrightRichText-richText css-1oz8dhe"]/p',
                                )
                                content_text = ""
                                for c in content:
                                    content_text += c.text + "\n"
                                writer.writerow([title, description, content_text])
                        except Exception as e:
                            print(f"处理答案时出错 {link}: {e}")
                            continue
                    driver.execute_script("window.scrollBy(0, 1000);")
                    attempt += 1
                    time.sleep(random.uniform(8, 10))
                time.sleep(random.uniform(8, 10))
            except WebDriverException as e:
                print(f"连接 {link} 失败: {e}")
                continue

    print("爬好了喵")
