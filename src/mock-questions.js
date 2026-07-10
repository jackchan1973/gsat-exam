const MOCK_QUESTION_SETS = [
  {
    id: "chinese-115-reading",
    subject: "國文",
    sourceSubject: "國綜",
    year: "115",
    category: "閱讀測驗",
    title: "115 年國文閱讀測驗",
    status: "測試模擬題",
    questions: [
      {
        id: "chinese-115-reading-1",
        no: 1,
        prompt: "下列哪一項最適合作為這段文字的主旨？",
        options: ["說明閱讀速度的重要", "強調判讀文本脈絡", "介紹古今字義差異", "比較不同文體特色"],
        answer: "B"
      },
      {
        id: "chinese-115-reading-2",
        no: 2,
        prompt: "若要判斷作者態度，最應優先注意哪一項？",
        options: ["標點符號數量", "關鍵詞與轉折語", "文章總字數", "段落排列位置"],
        answer: "B"
      }
    ]
  },
  {
    id: "english-115-vocab",
    subject: "英文",
    year: "115",
    category: "詞彙題",
    title: "115 年英文詞彙題",
    status: "測試模擬題",
    questions: [
      {
        id: "english-115-vocab-1",
        no: 1,
        prompt: "The teacher asked students to read the passage carefully before choosing the most suitable answer.",
        options: ["quickly", "carefully", "rarely", "silently"],
        answer: "B"
      },
      {
        id: "english-115-vocab-2",
        no: 2,
        prompt: "The word 'annual' is closest in meaning to ____.",
        options: ["daily", "weekly", "yearly", "random"],
        answer: "C"
      }
    ]
  },
  {
    id: "math-a-114-choice",
    subject: "數學",
    sourceSubject: "數學A",
    year: "114",
    category: "選擇題",
    title: "114 年數學選擇題",
    status: "測試模擬題",
    questions: [
      {
        id: "math-a-114-choice-1",
        no: 1,
        prompt: "若 f(x)=2x+3，則 f(4)=？",
        options: ["7", "9", "11", "13"],
        answer: "C"
      },
      {
        id: "math-a-114-choice-2",
        no: 2,
        prompt: "一等差數列首項為 3，公差為 2，則第 5 項為？",
        options: ["9", "10", "11", "12"],
        answer: "C"
      }
    ]
  },
  {
    id: "social-113-concept",
    subject: "社會",
    year: "113",
    category: "概念題",
    title: "113 年社會概念題",
    status: "測試模擬題",
    questions: [
      {
        id: "social-113-concept-1",
        no: 1,
        prompt: "判斷一項政策影響時，最需要同時考慮哪兩個面向？",
        options: ["名稱與口號", "成本與效益", "顏色與標誌", "地點與天氣"],
        answer: "B"
      }
    ]
  },
  {
    id: "science-115-analysis",
    subject: "自然",
    year: "115",
    category: "資料判讀",
    title: "115 年自然資料判讀",
    status: "測試模擬題",
    questions: [
      {
        id: "science-115-analysis-1",
        no: 1,
        prompt: "閱讀實驗數據時，最能支持結論的是哪一項？",
        options: ["單一次最高值", "可重複的趨勢", "圖表顏色", "題目字數"],
        answer: "B"
      }
    ]
  }
];
