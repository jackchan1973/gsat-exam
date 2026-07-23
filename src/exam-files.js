const EXAM_FILES = [
  {
    "id": "113一模-數學A-試題內容",
    "year": "113一模",
    "subject": "數學A",
    "type": "試題內容",
    "title": "113 全國高中一模 數學",
    "file": "測試用試題/113全國一模.pdf"
  },
  {
    "id": "115-國綜-試題內容-1",
    "year": "115",
    "subject": "國綜",
    "type": "試題內容",
    "title": "01-115學測國綜試卷",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0q054337448417166461/01-115%e5%ad%b8%e6%b8%ac%e5%9c%8b%e7%b6%9c%e8%a9%a6%e5%8d%b7.pdf",
    "file": "資料/大考中心官方PDF/115學年度/國綜/115學測-國綜-試題內容-01-115學測國綜試卷.pdf"
  },
  {
    "id": "115-國綜-答題卷-2",
    "year": "115",
    "subject": "國綜",
    "type": "答題卷",
    "title": "01-115學測國綜答題卷",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0q054338219695914416/01-115%e5%ad%b8%e6%b8%ac%e5%9c%8b%e7%b6%9c%e7%ad%94%e9%a1%8c%e5%8d%b7.pdf",
    "file": "資料/大考中心官方PDF/115學年度/國綜/115學測-國綜-答題卷-01-115學測國綜答題卷.pdf"
  },
  {
    "id": "115-國綜-選擇題答案-3",
    "year": "115",
    "subject": "國綜",
    "type": "選擇題答案",
    "title": "01-115學測國語文綜合能力測驗答案",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0q040596675162309932/01-115%e5%ad%b8%e6%b8%ac%e5%9c%8b%e8%aa%9e%e6%96%87%e7%b6%9c%e5%90%88%e8%83%bd%e5%8a%9b%e6%b8%ac%e9%a9%97%e7%ad%94%e6%a1%88.pdf",
    "file": "資料/大考中心官方PDF/115學年度/國綜/115學測-國綜-選擇題答案-01-115學測國語文綜合能力測驗答案.pdf"
  },
  {
    "id": "115-國綜-非選擇題評分原則-4",
    "year": "115",
    "subject": "國綜",
    "type": "非選擇題評分原則",
    "title": "115學測國文考科(國綜)非選擇題參考答案與評分原則",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0q054334089673796864/115%e5%ad%b8%e6%b8%ac%e5%9c%8b%e6%96%87%e8%80%83%e7%a7%91%28%e5%9c%8b%e7%b6%9c%29%e9%9d%9e%e9%81%b8%e6%93%87%e9%a1%8c%e5%8f%83%e8%80%83%e7%ad%94%e6%a1%88%e8%88%87%e8%a9%95%e5%88%86%e5%8e%9f%e5%89%87.pdf",
    "file": "資料/大考中心官方PDF/115學年度/國綜/115學測-國綜-非選擇題評分原則-115學測國文考科(國綜)非選擇題參考答案與評分原則.pdf"
  },
  {
    "id": "115-國寫-試題內容-5",
    "year": "115",
    "subject": "國寫",
    "type": "試題內容",
    "title": "07-115學測國寫試卷",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0q054338512775247597/07-115%e5%ad%b8%e6%b8%ac%e5%9c%8b%e5%af%ab%e8%a9%a6%e5%8d%b7.pdf",
    "file": "資料/大考中心官方PDF/115學年度/國寫/115學測-國寫-試題內容-07-115學測國寫試卷.pdf"
  },
  {
    "id": "115-國寫-答題卷-6",
    "year": "115",
    "subject": "國寫",
    "type": "答題卷",
    "title": "07-115學測國寫答題卷",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0q054339053954085532/07-115%e5%ad%b8%e6%b8%ac%e5%9c%8b%e5%af%ab%e7%ad%94%e9%a1%8c%e5%8d%b7.pdf",
    "file": "資料/大考中心官方PDF/115學年度/國寫/115學測-國寫-答題卷-07-115學測國寫答題卷.pdf"
  },
  {
    "id": "115-國寫-非選擇題評分原則-7",
    "year": "115",
    "subject": "國寫",
    "type": "非選擇題評分原則",
    "title": "115學測國文考科(國寫)非選擇題評分原則",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0q054334768025403359/115%e5%ad%b8%e6%b8%ac%e5%9c%8b%e6%96%87%e8%80%83%e7%a7%91%28%e5%9c%8b%e5%af%ab%29%e9%9d%9e%e9%81%b8%e6%93%87%e9%a1%8c%e8%a9%95%e5%88%86%e5%8e%9f%e5%89%87.pdf",
    "file": "資料/大考中心官方PDF/115學年度/國寫/115學測-國寫-非選擇題評分原則-115學測國文考科(國寫)非選擇題評分原則.pdf"
  },
  {
    "id": "115-英文-試題內容-8",
    "year": "115",
    "subject": "英文",
    "type": "試題內容",
    "title": "02-115學測英文試卷",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0q054532302653501476/02-115%e5%ad%b8%e6%b8%ac%e8%8b%b1%e6%96%87%e8%a9%a6%e5%8d%b7.pdf",
    "file": "資料/大考中心官方PDF/115學年度/英文/115學測-英文-試題內容-02-115學測英文試卷.pdf"
  },
  {
    "id": "115-英文-答題卷-9",
    "year": "115",
    "subject": "英文",
    "type": "答題卷",
    "title": "02-115學測英文答題卷",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0q054339832930771045/02-115%e5%ad%b8%e6%b8%ac%e8%8b%b1%e6%96%87%e7%ad%94%e9%a1%8c%e5%8d%b7.pdf",
    "file": "資料/大考中心官方PDF/115學年度/英文/115學測-英文-答題卷-02-115學測英文答題卷.pdf"
  },
  {
    "id": "115-英文-選擇題答案-10",
    "year": "115",
    "subject": "英文",
    "type": "選擇題答案",
    "title": "02-115學測英文答案",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0q040594609847120321/02-115%e5%ad%b8%e6%b8%ac%e8%8b%b1%e6%96%87%e7%ad%94%e6%a1%88.pdf",
    "file": "資料/大考中心官方PDF/115學年度/英文/115學測-英文-選擇題答案-02-115學測英文答案.pdf"
  },
  {
    "id": "115-英文-非選擇題評分原則-11",
    "year": "115",
    "subject": "英文",
    "type": "非選擇題評分原則",
    "title": "115學測英文考科非選擇題參考答案與評分原則",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0q054335046832331817/115%e5%ad%b8%e6%b8%ac%e8%8b%b1%e6%96%87%e8%80%83%e7%a7%91%e9%9d%9e%e9%81%b8%e6%93%87%e9%a1%8c%e5%8f%83%e8%80%83%e7%ad%94%e6%a1%88%e8%88%87%e8%a9%95%e5%88%86%e5%8e%9f%e5%89%87.pdf",
    "file": "資料/大考中心官方PDF/115學年度/英文/115學測-英文-非選擇題評分原則-115學測英文考科非選擇題參考答案與評分原則.pdf"
  },
  {
    "id": "115-數學A-試題內容-12",
    "year": "115",
    "subject": "數學A",
    "type": "試題內容",
    "title": "03-115學測數學a試卷",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0q054344158947111283/03-115%e5%ad%b8%e6%b8%ac%e6%95%b8%e5%ad%b8a%e8%a9%a6%e5%8d%b7.pdf",
    "file": "資料/大考中心官方PDF/115學年度/數學A/115學測-數學A-試題內容-03-115學測數學a試卷.pdf"
  },
  {
    "id": "115-數學A-答題卷-13",
    "year": "115",
    "subject": "數學A",
    "type": "答題卷",
    "title": "03-115學測數學a答題卷",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0q054340566198842071/03-115%e5%ad%b8%e6%b8%ac%e6%95%b8%e5%ad%b8a%e7%ad%94%e9%a1%8c%e5%8d%b7.pdf",
    "file": "資料/大考中心官方PDF/115學年度/數學A/115學測-數學A-答題卷-03-115學測數學a答題卷.pdf"
  },
  {
    "id": "115-數學A-選擇(填)題答案-14",
    "year": "115",
    "subject": "數學A",
    "type": "選擇(填)題答案",
    "title": "03-115學測數學a答案",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0q040592802409726233/03-115%e5%ad%b8%e6%b8%ac%e6%95%b8%e5%ad%b8a%e7%ad%94%e6%a1%88.pdf",
    "file": "資料/大考中心官方PDF/115學年度/數學A/115學測-數學A-選擇(填)題答案-03-115學測數學a答案.pdf"
  },
  {
    "id": "115-數學A-非選擇題評分原則-15",
    "year": "115",
    "subject": "數學A",
    "type": "非選擇題評分原則",
    "title": "115學測數學a考科非選擇題參考答案與評分原則",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0q054335289912664889/115%e5%ad%b8%e6%b8%ac%e6%95%b8%e5%ad%b8a%e8%80%83%e7%a7%91%e9%9d%9e%e9%81%b8%e6%93%87%e9%a1%8c%e5%8f%83%e8%80%83%e7%ad%94%e6%a1%88%e8%88%87%e8%a9%95%e5%88%86%e5%8e%9f%e5%89%87.pdf",
    "file": "資料/大考中心官方PDF/115學年度/數學A/115學測-數學A-非選擇題評分原則-115學測數學a考科非選擇題參考答案與評分原則.pdf"
  },
  {
    "id": "115-數學B-試題內容-16",
    "year": "115",
    "subject": "數學B",
    "type": "試題內容",
    "title": "04-115學測數學b試卷",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0q054533256912682493/04-115%e5%ad%b8%e6%b8%ac%e6%95%b8%e5%ad%b8b%e8%a9%a6%e5%8d%b7.pdf",
    "file": "資料/大考中心官方PDF/115學年度/數學B/115學測-數學B-試題內容-04-115學測數學b試卷.pdf"
  },
  {
    "id": "115-數學B-答題卷-17",
    "year": "115",
    "subject": "數學B",
    "type": "答題卷",
    "title": "04-115學測數學b答題卷",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0q054341330457922198/04-115%e5%ad%b8%e6%b8%ac%e6%95%b8%e5%ad%b8b%e7%ad%94%e9%a1%8c%e5%8d%b7.pdf",
    "file": "資料/大考中心官方PDF/115學年度/數學B/115學測-數學B-答題卷-04-115學測數學b答題卷.pdf"
  },
  {
    "id": "115-數學B-選擇(填)題答案-18",
    "year": "115",
    "subject": "數學B",
    "type": "選擇(填)題答案",
    "title": "04-115學測數學b答案",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0q040592403413040721/04-115%e5%ad%b8%e6%b8%ac%e6%95%b8%e5%ad%b8b%e7%ad%94%e6%a1%88.pdf",
    "file": "資料/大考中心官方PDF/115學年度/數學B/115學測-數學B-選擇(填)題答案-04-115學測數學b答案.pdf"
  },
  {
    "id": "115-數學B-非選擇題評分原則-19",
    "year": "115",
    "subject": "數學B",
    "type": "非選擇題評分原則",
    "title": "115學測數學b考科非選擇題參考答案與評分原則",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0q054335782082987960/115%e5%ad%b8%e6%b8%ac%e6%95%b8%e5%ad%b8b%e8%80%83%e7%a7%91%e9%9d%9e%e9%81%b8%e6%93%87%e9%a1%8c%e5%8f%83%e8%80%83%e7%ad%94%e6%a1%88%e8%88%87%e8%a9%95%e5%88%86%e5%8e%9f%e5%89%87.pdf",
    "file": "資料/大考中心官方PDF/115學年度/數學B/115學測-數學B-非選擇題評分原則-115學測數學b考科非選擇題參考答案與評分原則.pdf"
  },
  {
    "id": "115-社會-試題內容-20",
    "year": "115",
    "subject": "社會",
    "type": "試題內容",
    "title": "05-115學測社會試卷",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0q054534130270752519/05-115%e5%ad%b8%e6%b8%ac%e7%a4%be%e6%9c%83%e8%a9%a6%e5%8d%b7.pdf",
    "file": "資料/大考中心官方PDF/115學年度/社會/115學測-社會-試題內容-05-115學測社會試卷.pdf"
  },
  {
    "id": "115-社會-答題卷-21",
    "year": "115",
    "subject": "社會",
    "type": "答題卷",
    "title": "05-115學測社會答題卷",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0q054342054715193114/05-115%e5%ad%b8%e6%b8%ac%e7%a4%be%e6%9c%83%e7%ad%94%e9%a1%8c%e5%8d%b7.pdf",
    "file": "資料/大考中心官方PDF/115學年度/社會/115學測-社會-答題卷-05-115學測社會答題卷.pdf"
  },
  {
    "id": "115-社會-選擇題答案-22",
    "year": "115",
    "subject": "社會",
    "type": "選擇題答案",
    "title": "05-115學測社會答案",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0q040582211712162219/05-115%e5%ad%b8%e6%b8%ac%e7%a4%be%e6%9c%83%e7%ad%94%e6%a1%88.pdf",
    "file": "資料/大考中心官方PDF/115學年度/社會/115學測-社會-選擇題答案-05-115學測社會答案.pdf"
  },
  {
    "id": "115-社會-非選擇題評分原則-23",
    "year": "115",
    "subject": "社會",
    "type": "非選擇題評分原則",
    "title": "115學測社會考科非選擇題參考答案與評分原則",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0q054335965162309932/115%e5%ad%b8%e6%b8%ac%e7%a4%be%e6%9c%83%e8%80%83%e7%a7%91%e9%9d%9e%e9%81%b8%e6%93%87%e9%a1%8c%e5%8f%83%e8%80%83%e7%ad%94%e6%a1%88%e8%88%87%e8%a9%95%e5%88%86%e5%8e%9f%e5%89%87.pdf",
    "file": "資料/大考中心官方PDF/115學年度/社會/115學測-社會-非選擇題評分原則-115學測社會考科非選擇題參考答案與評分原則.pdf"
  },
  {
    "id": "115-自然-試題內容-24",
    "year": "115",
    "subject": "自然",
    "type": "試題內容",
    "title": "06-115學測自然試卷",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0q054346117821958325/06-115%e5%ad%b8%e6%b8%ac%e8%87%aa%e7%84%b6%e8%a9%a6%e5%8d%b7.pdf",
    "file": "資料/大考中心官方PDF/115學年度/自然/115學測-自然-試題內容-06-115學測自然試卷.pdf"
  },
  {
    "id": "115-自然-答題卷-25",
    "year": "115",
    "subject": "自然",
    "type": "答題卷",
    "title": "115學測自然答題卷",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0q054342730331869130/115%e5%ad%b8%e6%b8%ac%e8%87%aa%e7%84%b6%e7%ad%94%e9%a1%8c%e5%8d%b7.pdf",
    "file": "資料/大考中心官方PDF/115學年度/自然/115學測-自然-答題卷-115學測自然答題卷.pdf"
  },
  {
    "id": "115-自然-選擇題答案-26",
    "year": "115",
    "subject": "自然",
    "type": "選擇題答案",
    "title": "06-115學測自然答案",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0q040579122726476606/06-115%e5%ad%b8%e6%b8%ac%e8%87%aa%e7%84%b6%e7%ad%94%e6%a1%88.pdf",
    "file": "資料/大考中心官方PDF/115學年度/自然/115學測-自然-選擇題答案-06-115學測自然答案.pdf"
  },
  {
    "id": "115-自然-非選擇題評分原則-27",
    "year": "115",
    "subject": "自然",
    "type": "非選擇題評分原則",
    "title": "115學測自然考科非選擇題參考答案與評分原則",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0q054336274158996445/115%e5%ad%b8%e6%b8%ac%e8%87%aa%e7%84%b6%e8%80%83%e7%a7%91%e9%9d%9e%e9%81%b8%e6%93%87%e9%a1%8c%e5%8f%83%e8%80%83%e7%ad%94%e6%a1%88%e8%88%87%e8%a9%95%e5%88%86%e5%8e%9f%e5%89%87.pdf",
    "file": "資料/大考中心官方PDF/115學年度/自然/115學測-自然-非選擇題評分原則-115學測自然考科非選擇題參考答案與評分原則.pdf"
  },
  {
    "id": "114-國綜-試題內容-28",
    "year": "114",
    "subject": "國綜",
    "type": "試題內容",
    "title": "01-114學測國綜試題",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0p056424313827932684/01-114%e5%ad%b8%e6%b8%ac%e5%9c%8b%e7%b6%9c%e8%a9%a6%e9%a1%8c.pdf",
    "file": "資料/大考中心官方PDF/114學年度/國綜/114學測-國綜-試題內容-01-114學測國綜試題.pdf"
  },
  {
    "id": "114-國綜-答題卷-29",
    "year": "114",
    "subject": "國綜",
    "type": "答題卷",
    "title": "01-114學測國綜答題卷-定稿",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0p051548371966937352/01-114%e5%ad%b8%e6%b8%ac%e5%9c%8b%e7%b6%9c%e7%ad%94%e9%a1%8c%e5%8d%b7-%e5%ae%9a%e7%a8%bf.pdf",
    "file": "資料/大考中心官方PDF/114學年度/國綜/114學測-國綜-答題卷-01-114學測國綜答題卷-定稿.pdf"
  },
  {
    "id": "114-國綜-選擇題答案-30",
    "year": "114",
    "subject": "國綜",
    "type": "選擇題答案",
    "title": "01-114學測國語文綜合能力測驗答案",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0p051548831591816379/01-114%e5%ad%b8%e6%b8%ac%e5%9c%8b%e8%aa%9e%e6%96%87%e7%b6%9c%e5%90%88%e8%83%bd%e5%8a%9b%e6%b8%ac%e9%a9%97%e7%ad%94%e6%a1%88.pdf",
    "file": "資料/大考中心官方PDF/114學年度/國綜/114學測-國綜-選擇題答案-01-114學測國語文綜合能力測驗答案.pdf"
  },
  {
    "id": "114-國綜-非選擇題評分原則-31",
    "year": "114",
    "subject": "國綜",
    "type": "非選擇題評分原則",
    "title": "01-114學測國綜非選擇題參考答案與評分原則",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0p055377938076732468/01-114%e5%ad%b8%e6%b8%ac%e5%9c%8b%e7%b6%9c%e9%9d%9e%e9%81%b8%e6%93%87%e9%a1%8c%e5%8f%83%e8%80%83%e7%ad%94%e6%a1%88%e8%88%87%e8%a9%95%e5%88%86%e5%8e%9f%e5%89%87.pdf",
    "file": "資料/大考中心官方PDF/114學年度/國綜/114學測-國綜-非選擇題評分原則-01-114學測國綜非選擇題參考答案與評分原則.pdf"
  },
  {
    "id": "114-國寫-試題內容-32",
    "year": "114",
    "subject": "國寫",
    "type": "試題內容",
    "title": "07-114學測國寫試題",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0p056425983094832020/07-114%e5%ad%b8%e6%b8%ac%e5%9c%8b%e5%af%ab%e8%a9%a6%e9%a1%8c.pdf",
    "file": "資料/大考中心官方PDF/114學年度/國寫/114學測-國寫-試題內容-07-114學測國寫試題.pdf"
  },
  {
    "id": "114-國寫-答題卷-33",
    "year": "114",
    "subject": "國寫",
    "type": "答題卷",
    "title": "07-114學測國寫答題卷-定稿",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0p051547366164997308/07-114%e5%ad%b8%e6%b8%ac%e5%9c%8b%e5%af%ab%e7%ad%94%e9%a1%8c%e5%8d%b7-%e5%ae%9a%e7%a8%bf.pdf",
    "file": "資料/大考中心官方PDF/114學年度/國寫/114學測-國寫-答題卷-07-114學測國寫答題卷-定稿.pdf"
  },
  {
    "id": "114-國寫-非選擇題評分原則-34",
    "year": "114",
    "subject": "國寫",
    "type": "非選擇題評分原則",
    "title": "02-114學測國寫閱卷評分原則說明",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0p055378361790934567/02-114%e5%ad%b8%e6%b8%ac%e5%9c%8b%e5%af%ab%e9%96%b1%e5%8d%b7%e8%a9%95%e5%88%86%e5%8e%9f%e5%89%87%e8%aa%aa%e6%98%8e.pdf",
    "file": "資料/大考中心官方PDF/114學年度/國寫/114學測-國寫-非選擇題評分原則-02-114學測國寫閱卷評分原則說明.pdf"
  },
  {
    "id": "114-英文-試題內容-35",
    "year": "114",
    "subject": "英文",
    "type": "試題內容",
    "title": "02-114學測英文試題",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0p056425554473267580/02-114%e5%ad%b8%e6%b8%ac%e8%8b%b1%e6%96%87%e8%a9%a6%e9%a1%8c.pdf",
    "file": "資料/大考中心官方PDF/114學年度/英文/114學測-英文-試題內容-02-114學測英文試題.pdf"
  },
  {
    "id": "114-英文-答題卷-36",
    "year": "114",
    "subject": "英文",
    "type": "答題卷",
    "title": "114學測英文答題卷-定稿",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0p051546347999453841/114%e5%ad%b8%e6%b8%ac%e8%8b%b1%e6%96%87%e7%ad%94%e9%a1%8c%e5%8d%b7-%e5%ae%9a%e7%a8%bf.pdf",
    "file": "資料/大考中心官方PDF/114學年度/英文/114學測-英文-答題卷-114學測英文答題卷-定稿.pdf"
  },
  {
    "id": "114-英文-選擇題答案-37",
    "year": "114",
    "subject": "英文",
    "type": "選擇題答案",
    "title": "02-114學測英文答案",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0p051545433631383724/02-114%e5%ad%b8%e6%b8%ac%e8%8b%b1%e6%96%87%e7%ad%94%e6%a1%88.pdf",
    "file": "資料/大考中心官方PDF/114學年度/英文/114學測-英文-選擇題答案-02-114學測英文答案.pdf"
  },
  {
    "id": "114-英文-非選擇題評分原則-38",
    "year": "114",
    "subject": "英文",
    "type": "非選擇題評分原則",
    "title": "03-114學測英文考科非選擇題參考答案與評分原則",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0p055378620142741052/03-114%e5%ad%b8%e6%b8%ac%e8%8b%b1%e6%96%87%e8%80%83%e7%a7%91%e9%9d%9e%e9%81%b8%e6%93%87%e9%a1%8c%e5%8f%83%e8%80%83%e7%ad%94%e6%a1%88%e8%88%87%e8%a9%95%e5%88%86%e5%8e%9f%e5%89%87.pdf",
    "file": "資料/大考中心官方PDF/114學年度/英文/114學測-英文-非選擇題評分原則-03-114學測英文考科非選擇題參考答案與評分原則.pdf"
  },
  {
    "id": "114-數學A-試題內容-39",
    "year": "114",
    "subject": "數學A",
    "type": "試題內容",
    "title": "03-114學測數學a試題",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0p056503510203248955/03-114%e5%ad%b8%e6%b8%ac%e6%95%b8%e5%ad%b8a%e8%a9%a6%e9%a1%8c.pdf",
    "file": "資料/大考中心官方PDF/114學年度/數學A/114學測-數學A-試題內容-03-114學測數學a試題.pdf"
  },
  {
    "id": "114-數學A-答題卷-40",
    "year": "114",
    "subject": "數學A",
    "type": "答題卷",
    "title": "03-114學測數學a答題卷-定稿",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0p051544143566849267/03-114%e5%ad%b8%e6%b8%ac%e6%95%b8%e5%ad%b8a%e7%ad%94%e9%a1%8c%e5%8d%b7-%e5%ae%9a%e7%a8%bf.pdf",
    "file": "資料/大考中心官方PDF/114學年度/數學A/114學測-數學A-答題卷-03-114學測數學a答題卷-定稿.pdf"
  },
  {
    "id": "114-數學A-選擇(填)題答案-41",
    "year": "114",
    "subject": "數學A",
    "type": "選擇(填)題答案",
    "title": "03-114學測數學a答案",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0p051544393000727284/03-114%e5%ad%b8%e6%b8%ac%e6%95%b8%e5%ad%b8a%e7%ad%94%e6%a1%88.pdf",
    "file": "資料/大考中心官方PDF/114學年度/數學A/114學測-數學A-選擇(填)題答案-03-114學測數學a答案.pdf"
  },
  {
    "id": "114-數學A-非選擇題評分原則-42",
    "year": "114",
    "subject": "數學A",
    "type": "非選擇題評分原則",
    "title": "04-114學測數學a考科非選擇題參考答案與評分原則",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0p055379013856943041/04-114%e5%ad%b8%e6%b8%ac%e6%95%b8%e5%ad%b8a%e8%80%83%e7%a7%91%e9%9d%9e%e9%81%b8%e6%93%87%e9%a1%8c%e5%8f%83%e8%80%83%e7%ad%94%e6%a1%88%e8%88%87%e8%a9%95%e5%88%86%e5%8e%9f%e5%89%87.pdf",
    "file": "資料/大考中心官方PDF/114學年度/數學A/114學測-數學A-非選擇題評分原則-04-114學測數學a考科非選擇題參考答案與評分原則.pdf"
  },
  {
    "id": "114-數學B-試題內容-43",
    "year": "114",
    "subject": "數學B",
    "type": "試題內容",
    "title": "04-114學測數學b試題",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0p056503860912551449/04-114%e5%ad%b8%e6%b8%ac%e6%95%b8%e5%ad%b8b%e8%a9%a6%e9%a1%8c.pdf",
    "file": "資料/大考中心官方PDF/114學年度/數學B/114學測-數學B-試題內容-04-114學測數學b試題.pdf"
  },
  {
    "id": "114-數學B-答題卷-44",
    "year": "114",
    "subject": "數學B",
    "type": "答題卷",
    "title": "04-114學測數學b答題卷-定稿",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0p051541760865961655/04-114%e5%ad%b8%e6%b8%ac%e6%95%b8%e5%ad%b8b%e7%ad%94%e9%a1%8c%e5%8d%b7-%e5%ae%9a%e7%a8%bf.pdf",
    "file": "資料/大考中心官方PDF/114學年度/數學B/114學測-數學B-答題卷-04-114學測數學b答題卷-定稿.pdf"
  },
  {
    "id": "114-數學B-選擇(填)題答案-45",
    "year": "114",
    "subject": "數學B",
    "type": "選擇(填)題答案",
    "title": "04-114學測數學b答案",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0p051541901400830673/04-114%e5%ad%b8%e6%b8%ac%e6%95%b8%e5%ad%b8b%e7%ad%94%e6%a1%88.pdf",
    "file": "資料/大考中心官方PDF/114學年度/數學B/114學測-數學B-選擇(填)題答案-04-114學測數學b答案.pdf"
  },
  {
    "id": "114-數學B-非選擇題評分原則-46",
    "year": "114",
    "subject": "數學B",
    "type": "非選擇題評分原則",
    "title": "05-114學測數學b考科非選擇題參考答案與評分原則",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0p055377000559491425/05-114%e5%ad%b8%e6%b8%ac%e6%95%b8%e5%ad%b8b%e8%80%83%e7%a7%91%e9%9d%9e%e9%81%b8%e6%93%87%e9%a1%8c%e5%8f%83%e8%80%83%e7%ad%94%e6%a1%88%e8%88%87%e8%a9%95%e5%88%86%e5%8e%9f%e5%89%87.pdf",
    "file": "資料/大考中心官方PDF/114學年度/數學B/114學測-數學B-非選擇題評分原則-05-114學測數學b考科非選擇題參考答案與評分原則.pdf"
  },
  {
    "id": "114-社會-試題內容-47",
    "year": "114",
    "subject": "社會",
    "type": "試題內容",
    "title": "05-114學測社會試題",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0p056429479567292230/05-114%e5%ad%b8%e6%b8%ac%e7%a4%be%e6%9c%83%e8%a9%a6%e9%a1%8c.pdf",
    "file": "資料/大考中心官方PDF/114學年度/社會/114學測-社會-試題內容-05-114學測社會試題.pdf"
  },
  {
    "id": "114-社會-答題卷-48",
    "year": "114",
    "subject": "社會",
    "type": "答題卷",
    "title": "05-114學測社會答題卷-定稿",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0p051540901690427198/05-114%e5%ad%b8%e6%b8%ac%e7%a4%be%e6%9c%83%e7%ad%94%e9%a1%8c%e5%8d%b7-%e5%ae%9a%e7%a8%bf.pdf",
    "file": "資料/大考中心官方PDF/114學年度/社會/114學測-社會-答題卷-05-114學測社會答題卷-定稿.pdf"
  },
  {
    "id": "114-社會-選擇題答案-49",
    "year": "114",
    "subject": "社會",
    "type": "選擇題答案",
    "title": "05-114學測社會答案",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0p051540219978700116/05-114%e5%ad%b8%e6%b8%ac%e7%a4%be%e6%9c%83%e7%ad%94%e6%a1%88.pdf",
    "file": "資料/大考中心官方PDF/114學年度/社會/114學測-社會-選擇題答案-05-114學測社會答案.pdf"
  },
  {
    "id": "114-社會-非選擇題評分原則-50",
    "year": "114",
    "subject": "社會",
    "type": "非選擇題評分原則",
    "title": "06-114學測社會考科非選擇題參考答案與評分原則",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0p055379523021477609/06-114%e5%ad%b8%e6%b8%ac%e7%a4%be%e6%9c%83%e8%80%83%e7%a7%91%e9%9d%9e%e9%81%b8%e6%93%87%e9%a1%8c%e5%8f%83%e8%80%83%e7%ad%94%e6%a1%88%e8%88%87%e8%a9%95%e5%88%86%e5%8e%9f%e5%89%87.pdf",
    "file": "資料/大考中心官方PDF/114學年度/社會/114學測-社會-非選擇題評分原則-06-114學測社會考科非選擇題參考答案與評分原則.pdf"
  },
  {
    "id": "114-自然-試題內容-51",
    "year": "114",
    "subject": "自然",
    "type": "試題內容",
    "title": "114學測自然試題定稿",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0p080497875174268441/114%e5%ad%b8%e6%b8%ac%e8%87%aa%e7%84%b6%e8%a9%a6%e9%a1%8c%e5%ae%9a%e7%a8%bf.pdf",
    "file": "資料/大考中心官方PDF/114學年度/自然/114學測-自然-試題內容-114學測自然試題定稿.pdf"
  },
  {
    "id": "114-自然-答題卷-52",
    "year": "114",
    "subject": "自然",
    "type": "答題卷",
    "title": "06-114學測自然答題卷-定稿",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0p051538390347145686/06-114%e5%ad%b8%e6%b8%ac%e8%87%aa%e7%84%b6%e7%ad%94%e9%a1%8c%e5%8d%b7-%e5%ae%9a%e7%a8%bf.pdf",
    "file": "資料/大考中心官方PDF/114學年度/自然/114學測-自然-答題卷-06-114學測自然答題卷-定稿.pdf"
  },
  {
    "id": "114-自然-選擇題答案-53",
    "year": "114",
    "subject": "自然",
    "type": "選擇題答案",
    "title": "06-114學測自然答案",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0p051538671981014603/06-114%e5%ad%b8%e6%b8%ac%e8%87%aa%e7%84%b6%e7%ad%94%e6%a1%88.pdf",
    "file": "資料/大考中心官方PDF/114學年度/自然/114學測-自然-選擇題答案-06-114學測自然答案.pdf"
  },
  {
    "id": "114-自然-非選擇題評分原則-54",
    "year": "114",
    "subject": "自然",
    "type": "非選擇題評分原則",
    "title": "07-114學測自然考科非選擇題參考答案與評分原則",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0p055380385668390981/07-114%e5%ad%b8%e6%b8%ac%e8%87%aa%e7%84%b6%e8%80%83%e7%a7%91%e9%9d%9e%e9%81%b8%e6%93%87%e9%a1%8c%e5%8f%83%e8%80%83%e7%ad%94%e6%a1%88%e8%88%87%e8%a9%95%e5%88%86%e5%8e%9f%e5%89%87.pdf",
    "file": "資料/大考中心官方PDF/114學年度/自然/114學測-自然-非選擇題評分原則-07-114學測自然考科非選擇題參考答案與評分原則.pdf"
  },
  {
    "id": "113-國綜-試題內容-55",
    "year": "113",
    "subject": "國綜",
    "type": "試題內容",
    "title": "01-113學測國綜試題定稿",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0o051429609806157906/01-113%e5%ad%b8%e6%b8%ac%e5%9c%8b%e7%b6%9c%e8%a9%a6%e9%a1%8c%e5%ae%9a%e7%a8%bf.pdf",
    "file": "資料/大考中心官方PDF/113學年度/國綜/113學測-國綜-試題內容-01-113學測國綜試題定稿.pdf"
  },
  {
    "id": "113-國綜-答題卷-56",
    "year": "113",
    "subject": "國綜",
    "type": "答題卷",
    "title": "01-113學測國綜答題卷-定稿",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0o051429870085905951/01-113%e5%ad%b8%e6%b8%ac%e5%9c%8b%e7%b6%9c%e7%ad%94%e9%a1%8c%e5%8d%b7-%e5%ae%9a%e7%a8%bf.pdf",
    "file": "資料/大考中心官方PDF/113學年度/國綜/113學測-國綜-答題卷-01-113學測國綜答題卷-定稿.pdf"
  },
  {
    "id": "113-國綜-選擇題答案-57",
    "year": "113",
    "subject": "國綜",
    "type": "選擇題答案",
    "title": "01-113學測國語文綜合能力測驗答案",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0o051429991629874988/01-113%e5%ad%b8%e6%b8%ac%e5%9c%8b%e8%aa%9e%e6%96%87%e7%b6%9c%e5%90%88%e8%83%bd%e5%8a%9b%e6%b8%ac%e9%a9%97%e7%ad%94%e6%a1%88.pdf",
    "file": "資料/大考中心官方PDF/113學年度/國綜/113學測-國綜-選擇題答案-01-113學測國語文綜合能力測驗答案.pdf"
  },
  {
    "id": "113-國綜-非選擇題評分原則-58",
    "year": "113",
    "subject": "國綜",
    "type": "非選擇題評分原則",
    "title": "01-113學測國文考科(國綜)非選擇題參考答案與評分原則",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0o051430121163753905/01-113%e5%ad%b8%e6%b8%ac%e5%9c%8b%e6%96%87%e8%80%83%e7%a7%91%28%e5%9c%8b%e7%b6%9c%29%e9%9d%9e%e9%81%b8%e6%93%87%e9%a1%8c%e5%8f%83%e8%80%83%e7%ad%94%e6%a1%88%e8%88%87%e8%a9%95%e5%88%86%e5%8e%9f%e5%89%87.pdf",
    "file": "資料/大考中心官方PDF/113學年度/國綜/113學測-國綜-非選擇題評分原則-01-113學測國文考科(國綜)非選擇題參考答案與評分原則.pdf"
  },
  {
    "id": "113-國寫-試題內容-59",
    "year": "113",
    "subject": "國寫",
    "type": "試題內容",
    "title": "07-113學測國寫定稿",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0o051428628384018349/07-113%e5%ad%b8%e6%b8%ac%e5%9c%8b%e5%af%ab%e5%ae%9a%e7%a8%bf.pdf",
    "file": "資料/大考中心官方PDF/113學年度/國寫/113學測-國寫-試題內容-07-113學測國寫定稿.pdf"
  },
  {
    "id": "113-國寫-答題卷-60",
    "year": "113",
    "subject": "國寫",
    "type": "答題卷",
    "title": "07-113學測國寫答題卷-定稿",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0o051428854379239835/07-113%e5%ad%b8%e6%b8%ac%e5%9c%8b%e5%af%ab%e7%ad%94%e9%a1%8c%e5%8d%b7-%e5%ae%9a%e7%a8%bf.pdf",
    "file": "資料/大考中心官方PDF/113學年度/國寫/113學測-國寫-答題卷-07-113學測國寫答題卷-定稿.pdf"
  },
  {
    "id": "113-國寫-非選擇題評分原則-61",
    "year": "113",
    "subject": "國寫",
    "type": "非選擇題評分原則",
    "title": "02-113學測國文考科(國寫)非選擇題評分原則",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0o051428995914108862/02-113%e5%ad%b8%e6%b8%ac%e5%9c%8b%e6%96%87%e8%80%83%e7%a7%91%28%e5%9c%8b%e5%af%ab%29%e9%9d%9e%e9%81%b8%e6%93%87%e9%a1%8c%e8%a9%95%e5%88%86%e5%8e%9f%e5%89%87.pdf",
    "file": "資料/大考中心官方PDF/113學年度/國寫/113學測-國寫-非選擇題評分原則-02-113學測國文考科(國寫)非選擇題評分原則.pdf"
  },
  {
    "id": "113-英文-試題內容-62",
    "year": "113",
    "subject": "英文",
    "type": "試題內容",
    "title": "02-113學測英文科定稿",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0o051427482769341323/02-113%e5%ad%b8%e6%b8%ac%e8%8b%b1%e6%96%87%e7%a7%91%e5%ae%9a%e7%a8%bf.pdf",
    "file": "資料/大考中心官方PDF/113學年度/英文/113學測-英文-試題內容-02-113學測英文科定稿.pdf"
  },
  {
    "id": "113-英文-答題卷-63",
    "year": "113",
    "subject": "英文",
    "type": "答題卷",
    "title": "02-113學測英文答題卷-定稿",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0o051427743847199378/02-113%e5%ad%b8%e6%b8%ac%e8%8b%b1%e6%96%87%e7%ad%94%e9%a1%8c%e5%8d%b7-%e5%ae%9a%e7%a8%bf.pdf",
    "file": "資料/大考中心官方PDF/113學年度/英文/113學測-英文-答題卷-02-113學測英文答題卷-定稿.pdf"
  },
  {
    "id": "113-英文-選擇題答案-64",
    "year": "113",
    "subject": "英文",
    "type": "選擇題答案",
    "title": "02-113學測英文答案",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0o051427843482078305/02-113%e5%ad%b8%e6%b8%ac%e8%8b%b1%e6%96%87%e7%ad%94%e6%a1%88.pdf",
    "file": "資料/大考中心官方PDF/113學年度/英文/113學測-英文-選擇題答案-02-113學測英文答案.pdf"
  },
  {
    "id": "113-英文-非選擇題評分原則-65",
    "year": "113",
    "subject": "英文",
    "type": "非選擇題評分原則",
    "title": "03-113學測英文考科非選擇題參考答案與評分原則",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0o051427944026947323/03-113%e5%ad%b8%e6%b8%ac%e8%8b%b1%e6%96%87%e8%80%83%e7%a7%91%e9%9d%9e%e9%81%b8%e6%93%87%e9%a1%8c%e5%8f%83%e8%80%83%e7%ad%94%e6%a1%88%e8%88%87%e8%a9%95%e5%88%86%e5%8e%9f%e5%89%87.pdf",
    "file": "資料/大考中心官方PDF/113學年度/英文/113學測-英文-非選擇題評分原則-03-113學測英文考科非選擇題參考答案與評分原則.pdf"
  },
  {
    "id": "113-數學A-試題內容-66",
    "year": "113",
    "subject": "數學A",
    "type": "試題內容",
    "title": "03-113學測數a試題定稿",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0o051426180137211766/03-113%e5%ad%b8%e6%b8%ac%e6%95%b8a%e8%a9%a6%e9%a1%8c%e5%ae%9a%e7%a8%bf.pdf",
    "file": "資料/大考中心官方PDF/113學年度/數學A/113學測-數學A-試題內容-03-113學測數a試題定稿.pdf"
  },
  {
    "id": "113-數學A-答題卷-67",
    "year": "113",
    "subject": "數學A",
    "type": "答題卷",
    "title": "03-113學測數學a答題卷-定稿",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0o051426511316069711/03-113%e5%ad%b8%e6%b8%ac%e6%95%b8%e5%ad%b8a%e7%ad%94%e9%a1%8c%e5%8d%b7-%e5%ae%9a%e7%a8%bf.pdf",
    "file": "資料/大考中心官方PDF/113學年度/數學A/113學測-數學A-答題卷-03-113學測數學a答題卷-定稿.pdf"
  },
  {
    "id": "113-數學A-選擇(填)題答案-68",
    "year": "113",
    "subject": "數學A",
    "type": "選擇(填)題答案",
    "title": "03-113學測數學a答案",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0o051426632950938748/03-113%e5%ad%b8%e6%b8%ac%e6%95%b8%e5%ad%b8a%e7%ad%94%e6%a1%88.pdf",
    "file": "資料/大考中心官方PDF/113學年度/數學A/113學測-數學A-選擇(填)題答案-03-113學測數學a答案.pdf"
  },
  {
    "id": "113-數學A-非選擇題評分原則-69",
    "year": "113",
    "subject": "數學A",
    "type": "非選擇題評分原則",
    "title": "04-113學測數學a考科非選擇題參考答案與評分原則",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0o051426762594817766/04-113%e5%ad%b8%e6%b8%ac%e6%95%b8%e5%ad%b8a%e8%80%83%e7%a7%91%e9%9d%9e%e9%81%b8%e6%93%87%e9%a1%8c%e5%8f%83%e8%80%83%e7%ad%94%e6%a1%88%e8%88%87%e8%a9%95%e5%88%86%e5%8e%9f%e5%89%87.pdf",
    "file": "資料/大考中心官方PDF/113學年度/數學A/113學測-數學A-非選擇題評分原則-04-113學測數學a考科非選擇題參考答案與評分原則.pdf"
  },
  {
    "id": "113-數學B-試題內容-70",
    "year": "113",
    "subject": "數學B",
    "type": "試題內容",
    "title": "04-113學測數學b試題定稿",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0o051423705511545740/04-113%e5%ad%b8%e6%b8%ac%e6%95%b8%e5%ad%b8b%e8%a9%a6%e9%a1%8c%e5%ae%9a%e7%a8%bf.pdf",
    "file": "資料/大考中心官方PDF/113學年度/數學B/113學測-數學B-試題內容-04-113學測數學b試題定稿.pdf"
  },
  {
    "id": "113-數學B-答題卷-71",
    "year": "113",
    "subject": "數學B",
    "type": "答題卷",
    "title": "04-113學測數學b答題卷-定稿",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0o051423895790393795/04-113%e5%ad%b8%e6%b8%ac%e6%95%b8%e5%ad%b8b%e7%ad%94%e9%a1%8c%e5%8d%b7-%e5%ae%9a%e7%a8%bf.pdf",
    "file": "資料/大考中心官方PDF/113學年度/數學B/113學測-數學B-答題卷-04-113學測數學b答題卷-定稿.pdf"
  },
  {
    "id": "113-數學B-選擇(填)題答案-72",
    "year": "113",
    "subject": "數學B",
    "type": "選擇(填)題答案",
    "title": "04-113學測數學b答案",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0o051424006334262722/04-113%e5%ad%b8%e6%b8%ac%e6%95%b8%e5%ad%b8b%e7%ad%94%e6%a1%88.pdf",
    "file": "資料/大考中心官方PDF/113學年度/數學B/113學測-數學B-選擇(填)題答案-04-113學測數學b答案.pdf"
  },
  {
    "id": "113-數學B-非選擇題評分原則-73",
    "year": "113",
    "subject": "數學B",
    "type": "非選擇題評分原則",
    "title": "05-113學測數學b考科非選擇題參考答案與評分原則",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0o051424166979130740/05-113%e5%ad%b8%e6%b8%ac%e6%95%b8%e5%ad%b8b%e8%80%83%e7%a7%91%e9%9d%9e%e9%81%b8%e6%93%87%e9%a1%8c%e5%8f%83%e8%80%83%e7%ad%94%e6%a1%88%e8%88%87%e8%a9%95%e5%88%86%e5%8e%9f%e5%89%87.pdf",
    "file": "資料/大考中心官方PDF/113學年度/數學B/113學測-數學B-非選擇題評分原則-05-113學測數學b考科非選擇題參考答案與評分原則.pdf"
  },
  {
    "id": "113-社會-試題內容-74",
    "year": "113",
    "subject": "社會",
    "type": "試題內容",
    "title": "05-113學測社會科試題定稿",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0o051421699906768624/05-113%e5%ad%b8%e6%b8%ac%e7%a4%be%e6%9c%83%e7%a7%91%e8%a9%a6%e9%a1%8c%e5%ae%9a%e7%a8%bf.pdf",
    "file": "資料/大考中心官方PDF/113學年度/社會/113學測-社會-試題內容-05-113學測社會科試題定稿.pdf"
  },
  {
    "id": "113-社會-答題卷-75",
    "year": "113",
    "subject": "社會",
    "type": "答題卷",
    "title": "05-113學測社會答題卷-定稿",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0o051421880185516679/05-113%e5%ad%b8%e6%b8%ac%e7%a4%be%e6%9c%83%e7%ad%94%e9%a1%8c%e5%8d%b7-%e5%ae%9a%e7%a8%bf.pdf",
    "file": "資料/大考中心官方PDF/113學年度/社會/113學測-社會-答題卷-05-113學測社會答題卷-定稿.pdf"
  },
  {
    "id": "113-社會-選擇題答案-76",
    "year": "113",
    "subject": "社會",
    "type": "選擇題答案",
    "title": "05-113學測社會答案",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0o051422000729495697/05-113%e5%ad%b8%e6%b8%ac%e7%a4%be%e6%9c%83%e7%ad%94%e6%a1%88.pdf",
    "file": "資料/大考中心官方PDF/113學年度/社會/113學測-社會-選擇題答案-05-113學測社會答案.pdf"
  },
  {
    "id": "113-社會-非選擇題評分原則-77",
    "year": "113",
    "subject": "社會",
    "type": "非選擇題評分原則",
    "title": "06-113學測社會考科非選擇題參考答案與評分原則",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0o051422130263364624/06-113%e5%ad%b8%e6%b8%ac%e7%a4%be%e6%9c%83%e8%80%83%e7%a7%91%e9%9d%9e%e9%81%b8%e6%93%87%e9%a1%8c%e5%8f%83%e8%80%83%e7%ad%94%e6%a1%88%e8%88%87%e8%a9%95%e5%88%86%e5%8e%9f%e5%89%87.pdf",
    "file": "資料/大考中心官方PDF/113學年度/社會/113學測-社會-非選擇題評分原則-06-113學測社會考科非選擇題參考答案與評分原則.pdf"
  },
  {
    "id": "113-自然-試題內容-78",
    "year": "113",
    "subject": "自然",
    "type": "試題內容",
    "title": "06-113學測自然試題定稿",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0o051419133380092609/06-113%e5%ad%b8%e6%b8%ac%e8%87%aa%e7%84%b6%e8%a9%a6%e9%a1%8c%e5%ae%9a%e7%a8%bf.pdf",
    "file": "資料/大考中心官方PDF/113學年度/自然/113學測-自然-試題內容-06-113學測自然試題定稿.pdf"
  },
  {
    "id": "113-自然-答題卷-79",
    "year": "113",
    "subject": "自然",
    "type": "答題卷",
    "title": "06-113學測自然答題卷-定稿",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0o051420214469840653/06-113%e5%ad%b8%e6%b8%ac%e8%87%aa%e7%84%b6%e7%ad%94%e9%a1%8c%e5%8d%b7-%e5%ae%9a%e7%a8%bf.pdf",
    "file": "資料/大考中心官方PDF/113學年度/自然/113學測-自然-答題卷-06-113學測自然答題卷-定稿.pdf"
  },
  {
    "id": "113-自然-選擇題答案-80",
    "year": "113",
    "subject": "自然",
    "type": "選擇題答案",
    "title": "06-113學測自然答案",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0o051420394003729671/06-113%e5%ad%b8%e6%b8%ac%e8%87%aa%e7%84%b6%e7%ad%94%e6%a1%88.pdf",
    "file": "資料/大考中心官方PDF/113學年度/自然/113學測-自然-選擇題答案-06-113學測自然答案.pdf"
  },
  {
    "id": "113-自然-非選擇題評分原則-81",
    "year": "113",
    "subject": "自然",
    "type": "非選擇題評分原則",
    "title": "07-113學測自然考科非選擇題參考答案與評分原則",
    "sourceUrl": "https://www.ceec.edu.tw/files/file_pool/1/0o051420615648697608/07-113%e5%ad%b8%e6%b8%ac%e8%87%aa%e7%84%b6%e8%80%83%e7%a7%91%e9%9d%9e%e9%81%b8%e6%93%87%e9%a1%8c%e5%8f%83%e8%80%83%e7%ad%94%e6%a1%88%e8%88%87%e8%a9%95%e5%88%86%e5%8e%9f%e5%89%87.pdf",
    "file": "資料/大考中心官方PDF/113學年度/自然/113學測-自然-非選擇題評分原則-07-113學測自然考科非選擇題參考答案與評分原則.pdf"
  }
];
