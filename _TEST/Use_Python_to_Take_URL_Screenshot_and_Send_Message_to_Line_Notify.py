#!/usr/bin/env python
# coding: utf-8

# In[1]:


# 網頁畫面批次擷取工具
# 在Anaconda Powershell 上執行
# 檢查現有的模組
# conda list
# 加入下載頻道
# conda config --append channels conda-forge
# conda config --add channels loopbio
# 安裝chromedriver相關函式庫
# conda install -c conda-forge python-chromedriver-binary
# conda install -c anaconda chromedriver-binary
# conda install -c jhedrick selenium-chromedriver
# conda install -c dhirschfeld chromedriver
# 安裝selenium相關函式庫
# conda install -c conda-forge selenium

# 結果發現chromedriver需要對應目前本機安裝的Chrome 版本
# 到這裡 https://chromedriver.chromium.org/downloads 下載對應版本的chromedriver.exe
# 直接改成放到子目錄底下抓
# wd = webdriver.Chrome(options=options , executable_path='./chromedriver.exe')

# 定期執行
# jupyter nbconvert --ExecutePreprocessor.timeout=600 --to notebook --execute _TEST/Use_Python_to_Take_URL_Screenshot_and_Send_Message_to_Line_Notify.ipynb


# In[2]:



# 匯入相關函式庫

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from time import sleep 
from PIL import Image
import numpy as np
from datetime import datetime
import requests
import os


# In[3]:



# 初始化設定
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument("--window-size=1280x1024")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-certificate-errors-spki-list')
options.add_argument('--ignore-ssl-errors')
options.add_argument('--disable-dev-shm-usage')


# In[1]:


# ====================================
# 請根據需求修改此段落的相關設定

# 請依照範例設定所需要產製的網站畫面網址列表
# 目前擷取的只有不會導進SSO登入頁面的有掛連結在入口的網頁
urls = [
	"https://www.ntust.edu.tw/",#校首頁
	"https://i.ntust.edu.tw/student",#校務行政資訊系統-學生專區
	"https://i.ntust.edu.tw/faculty",#校務行政資訊系統-教職員工專區
	"https://i.ntust.edu.tw/AccountManagement/QueryAccountId", #現有教職員帳號查詢
	"https://i.ntust.edu.tw/AccountManagement/OldEmployeeRegistration",#5 現有教職員帳號申請
	"https://i.ntust.edu.tw/NTUSTSSOServ/SSO/ChangePWD",#變更密碼
	"https://stuinfosys.ntust.edu.tw/NTUSTSSOServ/SSO/ChangePWD",#學生變更密碼
	"https://stuinfosys.ntust.edu.tw/NTUSTSSOServ/SSO/Login/CourseSelection",#選課系統
	"https://interuniversity.ntust.edu.tw/",#校際選課系統
	"https://cour01.ntust.edu.tw/DMP_student/", #10 學分學程申請系統
	"https://stu.ntust.edu.tw/exchange_stu/login.aspx",#交換生資訊系統
	"https://eportfolio.ntust.edu.tw/",#學生學習歷程資訊網
	"https://donate1.ntust.edu.tw/",#捐款系統
	"https://dss17.ntust.edu.tw/TriangleChoose/Login_SSO.aspx",#三校選課交換系統
	"https://tstudy.ntust.edu.tw/industrystudy/CheckMember.aspx",#15 教師赴產業研習登錄系統
	"http://ae.ntust.edu.tw/",#學術研究倫理課程報名系統
	"https://sp.cge.ntust.edu.tw/",#社會實踐課程系統
	"https://cardsystem.ntust.edu.tw/std/index.php/user/login",#學生證掛失暨補發申請系統
	"https://sa.ntust.edu.tw/WebCounseling/",#諮商預約系統
	"https://sa.ntust.edu.tw/Dorm/", #20 學生宿舍系統
	"https://emp.ntust.edu.tw/authorizecode/Emp_Main.aspx",#課程授權碼列印
	"https://querycourse.ntust.edu.tw/querycourse/",#課程查詢系統
	"https://dss20.ntust.edu.tw/NTUTR/", #三校聯盟課程交換
	"https://hr.ntust.edu.tw/NTUSTEIP/",#線上簽到退系統-主要
	"https://pa.ntust.edu.tw/NTUSTEIP/",#25 線上簽到退系統-次要
	"https://hreip1.ntust.edu.tw/EIP/Login/LoginNtust.resource.aspx",#電子表單差勤系統
	"https://pa.ntust.edu.tw/Intranet/",#人事室內部資訊網
	"https://ccdoc.ntust.edu.tw/docmgsystem/login.aspx", #校內文件管理系統
	"https://emp.ntust.edu.tw/abroadplan/login.aspx",#出國計畫資訊系統
	"http://hr.ntust.edu.tw/Salary/",#30 舊薪資系統
	"https://dss18.ntust.edu.tw/QryPay/",#薪資查詢
	"https://sa02.ntust.edu.tw/StuScoreApply",#學雜費減免申請系統
	"https://studentpay.ntust.edu.tw/",#服務學習獎學金(工讀金)系統
	"https://sa.ntust.edu.tw/Scholarship/",#獎助學金系統
	"https://dss18.ntust.edu.tw/Employee/tax_login.aspx",#35 扣繳憑單列印及所得查詢
	"https://dss18.ntust.edu.tw/employee/Pay_login.aspx",#出納請款系統
	"https://dss20.ntust.edu.tw/pension/login.aspx", #勞退金系統
	"https://hrm.ntust.edu.tw/EmployeePromotion/Account/login",#約用人員升遷評比系統
	"https://hirehr.ntust.edu.tw/ContractedStaff/", #專案計畫人員聘僱系統
	"https://dss21.ntust.edu.tw/PTAssis/",#40 兼任助理及臨時人員聘僱系統
	"https://tea.ntust.edu.tw/tengage/Login.aspx",#教師聘任系統
	"https://dss18.ntust.edu.tw/employee/Hinsu_login.aspx",#二代健保系統
	"https://e-service.ntust.edu.tw/emp/index.aspx", #舊教職員工資訊網站
	"https://cour01.ntust.edu.tw/DMP_Management/",#輔系、雙主修及學分學程系統
	"https://tpro.ntust.edu.tw/promotion/Login.aspx",#45 教師升等審查系統
	"https://tpro.ntust.edu.tw/Award/",#教師教學獎系統
	"https://tpro.ntust.edu.tw/review/",#講座教授暨特聘教授、傑出研究獎外審作業系統
	"https://stuinfosys.ntust.edu.tw/Q_Questionnaire/", #校友流向問卷調查系統
	"https://hrm.ntust.edu.tw/HRVote/",#線上投票系統
	"https://hrm.ntust.edu.tw/HRVoteManage/HR_Manage.aspx",#50 線上投票系統-管理者登入
	"https://www.cc.ntust.edu.tw/p/412-1050-8352.php",#R-PAGE電算中心校園授權軟體頁面
	"https://software.ntust.edu.tw/websoftware/login.aspx", #校園授權軟體系統
	"https://netservice.ntust.edu.tw/", #電子郵件系統入口
	"https://cash.ntust.edu.tw/Login.aspx",#出納組-出納支付網路查詢系統
	"https://property.ntust.edu.tw/sys_AMSIS/login.aspx",#55 總務處-財產管理系統
	"https://ssoam.ntust.edu.tw/nidp/app/login", #AMSSO Access Manager
	"https://140.118.242.152:8443/nps/servlet/portalservice", #NetIQ Access Manager主要
	"https://140.118.242.158:8443/nps/servlet/portalservice", #NetIQ Access Manager次要
	"https://front.test.sss.ntust.edu.tw/WebSoftWare", #新版授權軟體系統測試頁
	"https://education-web.ntust.edu.tw/AcademicEducation/Home/Index",#60 論文指導教授系統-系所端
]

# LINE Notify 權杖
Line_tokens = ['改成自己的LINE Notify 權杖', # 1st token
               #'your_line_notify_token_2', # 2st token
]

# Discord Webhook URL（換成你自己的 Webhook）
WEBHOOK_URL = "改成自己的Discord Webhook URL"


# 最後輸出檔的檔案名稱
PATH = './OutPutTemp/'
fname_out = "output.jpg"
fname_out_resize = "output_resize.jpg"

# 圖片中每一列的網站數目
num_of_col = 5


# In[5]:


# ====================================
# 依照輸入的網址列表，依序產製個別的網站截圖

fnames = []
#chrome_options = None
#chrome_options = Options()
wd = webdriver.Chrome(options=options , executable_path='./Driver/chromedriver.exe')
#wd = webdriver.Chrome(options=chrome_options)
wd.set_page_load_timeout(30)
for i in range(0, len(urls)):
  try:
    wd.get(urls[i])
    sleep(1)
    wd.get_screenshot_as_file(PATH + str(i) + ".png") 
    print(i+1, "/", len(urls), urls[i], "Screenshot Success!")
    fnames.append(PATH + str(i) + ".png")
  except Exception as e:
    print(i,urls[i], "Screenshot Error!")
    print(e)

if len(fnames) % num_of_col:
  white_img = Image.new('RGB', (1280, 1024), color = (255,255,255))
  white_img.save(PATH + "white.png")
  for i in range(0, num_of_col - len(fnames) % num_of_col):
    fnames.append(PATH + "white.png")


# In[6]:


# 將個別的網站截圖彙整成一張大圖
def pil_grid(images, max_horiz=np.iinfo(int).max):
    n_images = len(images)
    n_horiz = min(n_images, max_horiz)
    h_sizes, v_sizes = [0] * n_horiz, [0] * (n_images // n_horiz)
    for i, im in enumerate(images):
        h, v = i % n_horiz, i // n_horiz
        h_sizes[h] = max(h_sizes[h], im.size[0])
        v_sizes[v] = max(v_sizes[v], im.size[1])
    h_sizes, v_sizes = np.cumsum([0] + h_sizes), np.cumsum([0] + v_sizes)
    im_grid = Image.new('RGB', (h_sizes[-1], v_sizes[-1]), color='white')
    for i, im in enumerate(images):
        im_grid.paste(im, (h_sizes[i % n_horiz], v_sizes[i // n_horiz]))
    return im_grid

imgs    = [ Image.open(i) for i in fnames ]
final_img = pil_grid(imgs, num_of_col)
final_img.save(PATH + fname_out)
fnames.append(PATH + fname_out)
#Image.close()
#imgs = Image.open(i)
#imgs.close(i)
#final_img
resize_img = final_img.resize((3200,6144))
resize_img.save(PATH + fname_out_resize)
fnames.append(PATH + fname_out_resize)


# In[9]:


# 全部網頁合成單張圖片發送
## 要發送的訊息
now = datetime.now()
message = now.strftime("\n%Y/%m/%d %H:%M:%S\n" )

for Line_token in Line_tokens:
# HTTP 標頭參數與資料
    headers = { "Authorization": "Bearer " + Line_token }
    data = { 'message': message }

# 要傳送的圖片檔案
#image = open(PATH + fname_out_resize, 'rb')

# 改成使用 with open 來關閉已開啟的圖檔
with open(PATH + fname_out_resize, 'rb' ) as image :
 files = { 'imageFile': image }

    
# 以 requests 發送 POST 請求到LINE
# requests.post("https://notify-api.line.me/api/notify",
# headers = headers, data = data, files = files)
    
	
# 改成Discord Webhook 用的格式
	data = { "content": message }
	files = { "file": open(PATH + fname_out_resize, "rb") }
# 發送 Webhook 到Discord 
response = requests.post(WEBHOOK_URL, data=data, files=files)

	
# 手動關閉
image.close()
    
# 關閉chromedriver及相關已開啟網頁
wd.close()
wd.quit()



# 將過程中產製的中繼圖片刪除
# sleep(1)
for fname in fnames:
    if os.path.exists(fname):   
     os.remove(fname)


# In[11]:


# 寫入執行成功時間
import pandas, numpy
# 取得現在時間
now = datetime.now()
txt = '上次更新時間為：' + str(now)

# 轉成df
df = pandas.DataFrame([txt], index=['UpdateTime'])

# 存出檔案
# df.to_csv('log.csv', header=False)
df.to_csv('log.txt', header=False)


# In[ ]:




