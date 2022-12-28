#!/usr/bin/python
# 202212 可用
# 功能说明：自动登录并刷帖【书香门第】网站，用来积攒金币下载小说 [签到 + 批量回复刷金币]
# 参考： https://www.51cto.com/article/715427.html

import sys
import time
import random
import datetime
import logging
# 导入selenium库
from selenium import webdriver
# 使用By这种定位前要将By类导入
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


# 定义参数日志：
# 第一个参数：日志文件名称
# 第二个参数：控制台日志输出最小等级（默认：logging.INFO）
# 第三个参数：文件日志输出最小等级(默认：logging.DEBUG)
def config_logging(file_name: str, console_level: int = logging.INFO, file_level: int = logging.DEBUG):
    file_handler = logging.FileHandler(file_name, mode='a', encoding="utf8")
    file_handler.setFormatter(
        logging.Formatter('%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                          datefmt="%Y-%m-%d %H:%M:%S"))
    file_handler.setLevel(file_level)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(
        logging.Formatter('%(asctime)s - line:%(lineno)d - %(levelname)s - %(message)s', datefmt="%Y-%m-%d %H:%M:%S"))
    console_handler.setLevel(console_level)
    logging.basicConfig(level=min(console_level, file_level), handlers=[file_handler, console_handler])


# 尝试签到
def try_sign():
    try:
        webdriver_obj.get('http://www.txtnovel.pro/plugin.php?id=dsu_paulsign:sign')
        webdriver_obj.find_element("xpath", '//*[@id="kx"]').click()
        webdriver_obj.find_element("xpath", '//*[@id="qiandao"]/table/tbody/tr/td/div/a').click()
        time.sleep(3)  # 等待页面加载, 否则会报错找不到元素
        logger.info("签到成功，当前积分：%s", webdriver_obj.find_element("xpath", '//*[@id="extcreditmenu"]').text)
    except Exception as e:
        logger.error("签到异常，跳过...")


def get_coin_sxmd():
    """
    登录网站，并回复评论，用来刷金币
    """
    # 打开登录网页
    webdriver_obj.get('http://www.txtnovel.pro/')
    # 网页登录的“用户名”输入框
    input = webdriver_obj.find_element("xpath", '//*[@id="ls_username"]')
    input.send_keys('TODO: 自己的用户名')
    # 网页登录的“密码”输入框
    passwd = webdriver_obj.find_element("xpath", '//*[@id="ls_password"]')
    passwd.send_keys('TODO: 自己的的密码')
    # 点击登录按钮
    webdriver_obj.find_element("xpath", '//*[@id="lsform"]/div/div/table/tbody/tr[2]/td[3]/button/em').click()
    time.sleep(2)  # 等待页面加载, 否则会报错找不到元素
    # 查看下当前的积分, 并打印
    before_count = webdriver_obj.find_element("xpath", '//*[@id="extcreditmenu"]').text
    logger.info("脚本操作前: " + before_count)
    # 尝试签到
    try_sign()
    # 随便找个板块
    webdriver_obj.get('http://www.txtnovel.pro/forum-17-1.html')
    # webdriver_obj.get('http://www.txtnovel.pro/')
    # webdriver_obj.find_element("xpath", '//*[@id="category_144"]/table/tbody/tr[2]/td[2]/h2/a').click()
    time.sleep(2)  # 等待页面加载, 否则会报错找不到元素
    # 获取这个版本下的第一页的所有小说列表
    tbody_ids = webdriver_obj.find_elements(
        "xpath", "//*[@id='moderate']/table/tbody[starts-with(@id,'normalthread_')]/tr/th/a[1]")
    href_list = []
    # 把所有小说页面都记录下来， 用来后面直接跳转遍历刷评论
    for a_href in tbody_ids:
        logger.debug("[for test]: %s", a_href.text)
        logger.debug("[for test]: %s", a_href.get_attribute("href"))
        href_list.append(a_href.get_attribute("href"))
    logger.info("准备评论回复: %s个小说资源", len(href_list))
    # 计数, 依次回复每一个小说资源
    count = 1
    for one_href in href_list:
        logger.info("第%s个", count)
        logger.info("第%s个: %s", count, one_href)
        # 进入这个页面
        webdriver_obj.get(one_href)
        time.sleep(2)
        # 随机发表回复
        comment_list = ['好书抱走~赠人玫瑰，手有余香~', 'thanks for sharing', '看一看,瞅一瞅,谢谢楼主', '谢谢楼主分享^^',
                        '路过路过，谢谢排雷^_^', '共有してくれてありがとう', '谢谢分享文文٩(๑❛ᴗ❛๑)۶']
        comment_one = random.choice(comment_list)
        webdriver_obj.find_element("xpath", '//*[@id="fastpostmessage"]').send_keys(comment_one)
        webdriver_obj.find_element("xpath", '//*[@id="fastpostsubmit"]/strong').click()
        logger.info("第%s个: 评论: %s", count, comment_one)
        time.sleep(2)
        # 刷新后查看当前的积分
        webdriver_obj.refresh()
        time.sleep(2)
        logger.info("第%s个, 评论回复后: %s", count,
                    webdriver_obj.find_element("xpath", '//*[@id="extcreditmenu"]').text)
        count += 1
        # 由于网站要求两次评论之间间隔必须大于15s，所以这里随机等待一段时间
        time.sleep(random.randint(15, 20))
    logger.info("总计评论: %s次", count)
    after_count = webdriver_obj.find_element("xpath", '//*[@id="extcreditmenu"]').text
    logger.info("脚本操作后: %s", after_count)
    logger.info("总计评论: %s次，操作前%s, 操作后%s", count, before_count, after_count)


if __name__ == '__main__':
    # 定义日志打印
    config_logging("./logs/sxmd_coins_batch.log", logging.INFO, logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("开始执行自动登录[书香门第]论坛，并刷金币.....")
    # 打开下载的浏览器驱动, 并设置不显示运行的浏览器
    options = Options()
    options.add_argument('--headless')
    webdriver_obj = webdriver.Chrome(options=options)
    # 设置隐式等待, 声明后对整个webdriver的生命周期都有效, 后面不用重复声明
    webdriver_obj.implicitly_wait(3)
    # 登录论坛网站，并批量刷金币
    get_coin_sxmd()
    # 最后要记得关闭浏览器窗口
    webdriver_obj.quit()
    logger.info("====== END ======")
