# TFI101_pythonETL_104

104人力銀行<br>

功課內容<br>
公司名稱、職缺、工作內容整理成CSV格式，其餘欄位自由新增，量力而為即可。


繳交方式<br>
截圖或 輸出CSV、Excel等檔案 上傳即可，也可以將作品上傳到GitHub並提供網址。

kyword=設定成要做為在104上搜尋的關鍵字<br>
公司資訊、職缺名稱、聯絡資訊、所需技能

pages=抓取的頁數(0為全部)<br>

save_separately=爬取結果的檔案存放份數(設0代表全部資料輸出成同一份Excel，其他數字代表要分開存，此欄位不可輸入負數。)<br>

cache=設定爬蟲抓取幾頁搜尋結果就存成一份新的Excel<br>

1. Packages:
   1. requests
   2. bs4
   3. time
   4. json
   5. pandas
   6. xlsxwriter(for excel)
2. HTTP Method: GET
3. URL: https://www.104.com.tw/jobs/search/
4. Parameter:
   1. ro=0
   2. kwop=7
   3. keyword=<user_input>
   4. expansionType=area, spec,com, job, wf, wktm
   5. order=12
   6. asc=0
   7. page=<auto_increment>
   8. mode=s
   9. jobsource=2018indexpoc
   10. lanfFlag=0
5. JS render solution:
   1. url: https://www.104.com.tw/job/ajax/content/<jobID>
   2. headers: { "Referer": "https://www.104.com.tw/job/ajax/content/<jobID>" }
