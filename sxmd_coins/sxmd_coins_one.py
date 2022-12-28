# 202212 可用
# 说明：自动登录并刷帖【书香门第】网站，用来积攒金币下载小说 [回复单个]
# 在系统中设置了每小时的定时任务：
#   1 * * * * python /Users/junqiu/mycode/github/sxmd_coins/sxmd_coins02.py >> /Users/junqiu/mycode/github/sxmd_coins/logs/sxmd_coins02.log
# 参考： https://www.51cto.com/article/715427.html

import time
import random
import datetime
# 导入selenium库
from selenium import webdriver
# 使用By这种定位前要将By类导入
from selenium.webdriver.common.by import By


# 打开下载的浏览器驱动
webdriver_obj = webdriver.Chrome()
# 设置隐式等待
webdriver_obj.implicitly_wait(1)

# 打开登录网页
webdriver_obj.get('http://www.txtnovel.pro/')

# 网页登录的“用户名”输入框
input = webdriver_obj.find_element("xpath", '//*[@id="ls_username"]')
input.send_keys('TODO: 自己的用户名')
# 网页登录的“密码”输入框
passwd = webdriver_obj.find_element("xpath", '//*[@id="ls_password"]')
passwd.send_keys('TODO: 自己的的密码')

# 点击登录按钮
button_login = webdriver_obj.find_element("xpath", '//*[@id="lsform"]/div/div/table/tbody/tr[2]/td[3]/button/em')
button_login.click()
time.sleep(2)  # 等待页面加载, 否则会报错找不到元素

#（有的网站还需要再跳过一个小弹窗, 这边网站不用就不加了）
# webdriver_obj.find_element("xpath", 'XXX弹窗中的关闭键XXX').click()

# 查看下当前的积分, 并打印
before_coins = webdriver_obj.find_element("xpath",'//*[@id="extcreditmenu"]').text
print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " 脚本操作前: " + before_coins)
time.sleep(2)  # 等待页面加载, 否则会报错找不到元素

# # 尝试签到
# try:
# 	webdriver_obj.find_element("xpath", '//*[@id="mn_N462e"]/a').click()
# 	time.sleep(3)  # 等待页面加载, 否则会报错找不到元素
#   XXX
# except:
# 	print("已签到")

# 随便找个板块
webdriver_obj.find_element("xpath", '//*[@id="category_144"]/table/tbody/tr[2]/td[2]/h2/a').click()
time.sleep(3)  # 等待页面加载, 否则会报错找不到元素
# 随便找这个板块下的第一个帖子
# webdriver_obj.find_element("xpath",'//*[@id="normalthread_4041452"]/tr/th/em').click()
webdriver_obj.find_element(By.XPATH, '//*[@id="normalthread_4041432"]/tr/th/a[1]').click()
time.sleep(3)  # 等待页面加载, 否则会报错找不到元素
hui_fu = webdriver_obj.find_element("xpath", '//*[@id="fastpostmessage"]')
# 随机评论一句
comment_list = ['好书抱走~赠人玫瑰，手有余香~','thanks楼主分享','看一看,瞅一瞅,谢谢楼主']
hui_fu.send_keys(random.choice(comment_list))
# 发表回复
webdriver_obj.find_element("xpath", '//*[@id="fastpostsubmit"]/strong').click()
time.sleep(5)  # 等待页面加载, 否则会报错找不到元素

# 查看一下目前的积分, 需要先刷新一下页面，否则数据没有更新
webdriver_obj.refresh()
time.sleep(2)
after_coins = webdriver_obj.find_element("xpath",'//*[@id="extcreditmenu"]').text
print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " 脚本操作后: " + after_coins)

# 最后要记得关闭浏览器窗口
webdriver_obj.quit()
