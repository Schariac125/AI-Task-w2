from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    while len(ids) < 20:
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
                print(f"正在爬取: {link}")
                driver.get(link)
                wait = WebDriverWait(driver, 10)

                # 显式等待标题出现
                title_el = wait.until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "QuestionHeader-title")
                    )
                )
                title_text = title_el.text

                try:
                    detail_el = driver.find_element(
                        By.CSS_SELECTOR, "span[itemprop='text']"
                    )
                    inf = detail_el.text.strip()
                except:
                    inf = "该问题无详细描述"

                # 2. 边滚动边抓取回答
                all_answers = []
                seen_answers = set()
                attempts = 0
                stagnant_rounds = 0

                # 设定抓取目标：比如抓到 10 个不同的回答，或者滚动 10 次
                # 我实在不会写这个逻辑了，因为知乎有些回答非常长，这样子会让selenium非常难搞
                # 已被懒加载打败
                while len(all_answers) < 10 and attempts < 10 and stagnant_rounds < 3:
                    before_count = len(all_answers)
                    elements = driver.find_elements(
                        By.CSS_SELECTOR,
                        ".List-item .RichContent-inner .RichText.ztext, "
                        ".AnswerItem .RichContent-inner .RichText.ztext",
                    )

                    for el in elements:
                        text = el.text.strip()
                        if not text or text in seen_answers:
                            continue
                        seen_answers.add(text)
                        all_answers.append(text)
                        if len(all_answers) >= 10:
                            break

                    if len(all_answers) == before_count:
                        stagnant_rounds += 1
                    else:
                        stagnant_rounds = 0

                    if len(all_answers) >= 10:
                        break

                    # 连续几轮没有新回答时，说明已经基本到底或选择器失效
                    driver.execute_script("window.scrollBy(0, 1200);")
                    time.sleep(random.uniform(8, 10))
                    attempts += 1

                # 3. 将所有抓到的回答合并成一个字符串，存入 CSV 的一格中
                # 这样 CSV 里一个问题就只占一行，结构清晰
                final_ans_str = "\n\n--- 下一个回答 ---\n\n".join(list(all_answers))

                writer.writerow([title_text, inf, final_ans_str])
                print(f"成功爬取标题: {title_text}，抓到回答数: {len(all_answers)}")

                time.sleep(random.uniform(8, 10))  # 休息一下再爬下一个链接

            except Exception as e:
                print(f"连接 {link} 失败: {e}")
                continue

    print("爬好了喵")
