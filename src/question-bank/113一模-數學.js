// 全國 113 學年度一模 數學（翰林）答題卡。題目、答案與解析取自來源檔
// （測試用試題/113全國一模.pdf、113全國一模詳解.pdf），未經改寫。
// 公式看原圖讀成 LaTeX、以 KaTeX 渲染；圖形採官方裁圖。
(function () {
  const IMG = "public/images/113一模/數學/";
  const C5 = ["1", "2", "3", "4", "5"];

  const blocks = [
    {
      type: "group",
      title: "一、單選題（第 1–6 題，每題 5 分）",
      shared: null,
      questions: [
        {
          id: "matha-113mock-q1", no: 1, type: "single", choices: C5, answer: "5",
          stem: "試問有多少個整數 $x$ 滿足 $|x+5|+x\\le 5$？",
          options: { "1": "$0$", "2": "$4$", "3": "$5$", "4": "$6$", "5": "無限多個" },
          explanation: "①$x\\ge-5$：$(x+5)+x\\le5\\Rightarrow x\\le0$，得 $x=-5,-4,\\dots,0$。\n②$x<-5$：$-(x+5)+x\\le5\\Rightarrow-5\\le5$ 恆成立，所有負整數皆符合。\n故有無限多個整數。答案：(5)。"
        },
        {
          id: "matha-113mock-q2", no: 2, type: "single", choices: C5, answer: "2",
          stem: "已知實數 $a,b$ 滿足 $b=\\log a$ 且 $1<a<10$。設 $x=\\dfrac{2a+b}{3}$，$y=\\dfrac{a+3b}{4}$，$z=\\dfrac{a+5b}{6}$，則 $x,y,z$ 的大小關係為何？",
          options: { "1": "$z>y>x$", "2": "$x>y>z$", "3": "$x>z>y$", "4": "$y>z>x$", "5": "$y>x>z$" },
          explanation: "通分為分母 12：$x=\\dfrac{8a+4b}{12},\\ y=\\dfrac{3a+9b}{12},\\ z=\\dfrac{2a+10b}{12}$。\n因 $1<a<10\\Rightarrow 0<b<1<a$，$a$ 的係數越大值越大，故 $x>y>z$。答案：(2)。"
        },
        {
          id: "matha-113mock-q3", no: 3, type: "single", choices: C5, answer: "3",
          stem: "已知 $3^{0.4}\\approx 1.55$，$3^{0.01}\\approx 1.01$，則 $3^{\\sqrt{2}}$ 最接近下列哪個選項？",
          options: { "1": "$2.6$", "2": "$3.5$", "3": "$4.7$", "4": "$5.1$", "5": "$5.7$" },
          explanation: "$3^{\\sqrt2}\\approx 3^{1.41}=3^1\\cdot3^{0.4}\\cdot3^{0.01}\\approx3\\times1.55\\times1.01\\approx4.70$。答案：(3)。"
        },
        {
          id: "matha-113mock-q4", no: 4, type: "single", choices: C5, answer: "5",
          stem: "令多項式 $f(x)=(x^2-1)(x^2-2^2)^2(x^2-3^2)^3(x^2-4^2)^4$，則多項式方程式 $f(x)=0$ 的實數解將 $x$ 軸分割成的 9 個開區間中，有多少個開區間可使 $f(x)$ 的值恆正？（註：不含端點的區間，我們稱為開區間，例如 $(2,3)$ 代表 $2<x<3$，$(3,\\infty)$ 代表 $x>3$）",
          options: { "1": "$1$ 個", "2": "$2$ 個", "3": "$3$ 個", "4": "$4$ 個", "5": "$5$ 個" },
          explanation: "實數解 $x=\\pm1,\\pm2,\\pm3,\\pm4$ 分割成 9 個開區間。$f(x)>0$ 等價於 $(x-1)(x+1)(x-3)(x+3)>0$ 且 $x\\ne\\pm2,\\pm4$。\n恆正的區間為 $(-\\infty,-4),(-4,-3),(-1,1),(3,4),(4,\\infty)$ 共 5 個。答案：(5)。"
        },
        {
          id: "matha-113mock-q5", no: 5, type: "single", choices: C5, answer: "4",
          image: IMG + "113一模-數學-p3-1.png",
          stem: "室內配置圖上有兩個半徑為 $1$ 的圓形障礙物，其圓心分別為 $(2,4)$ 和 $(10,2)$。若室內設計師想以直線 $L:y=mx\\ (m>0)$ 為中心，規劃一條寬度為 $2$ 且不碰觸到圓形障礙物的通道（相切視為有碰觸），則 $m$ 可為下列哪個選項？",
          options: { "1": "$\\dfrac{4}{3}$", "2": "$1$", "3": "$\\dfrac{3}{4}$", "4": "$\\dfrac{2}{3}$", "5": "$\\dfrac{5}{2}$" },
          explanation: "設 $M_1(2,4),M_2(10,2)$，$L:mx-y=0$。通道不碰障礙物 $\\Rightarrow d(M_1,L)>2$ 且 $d(M_2,L)>2$。\n①$\\dfrac{|2m-4|}{\\sqrt{m^2+1}}>2\\Rightarrow m<\\dfrac34$；②$\\dfrac{|10m-2|}{\\sqrt{m^2+1}}>2\\Rightarrow m>\\dfrac{5}{12}$。\n故 $\\dfrac{5}{12}<m<\\dfrac34$，$m=\\dfrac23$ 符合。答案：(4)。"
        },
        {
          id: "matha-113mock-q6", no: 6, type: "single", choices: C5, answer: "1",
          image: IMG + "113一模-數學-q6.png",
          stem: "右圖為 $y=ax^2+bx+c$ 的圖形，虛線為 $x=\\dfrac{1}{2}$，則下列哪一個選項的圖形可以代表 $ax+by+c=0$？（選項中的虛線為直線 $y=x$）",
          explanation: "由拋物線：開口向上 $\\Rightarrow a>0$；與 $y$ 軸交於 $x$ 軸下方 $\\Rightarrow c<0$；頂點在 $x=\\dfrac12$ 左側 $\\Rightarrow 0<-\\dfrac{b}{2a}<\\dfrac12\\Rightarrow-\\dfrac{a}{b}>1$。\n直線 $ax+by+c=0$ 化為 $y=-\\dfrac{a}{b}x-\\dfrac{c}{b}$，斜率 $-\\dfrac ab>1$、$y$ 截距 $-\\dfrac cb<0$。答案：(1)。"
        }
      ]
    },
    {
      type: "group",
      title: "二、多選題（第 7–12 題，每題 5 分）",
      shared: null,
      questions: [
        {
          id: "matha-113mock-q7", no: 7, type: "multiple", choices: C5, answer: ["3", "4", "5"],
          stem: "若 $2^n$ 與 $3^{10}$ 有相同的位數，則 $n$ 可為下列哪些數？",
          options: { "1": "$12$", "2": "$13$", "3": "$14$", "4": "$15$", "5": "$16$" },
          explanation: "$3^{10}=10^{10\\log3}\\approx10^{4.771}$ 為 5 位數。$2^n=10^{n\\log2}\\approx10^{0.301n}$。\n同位數 $\\Rightarrow 4\\le0.301n<5\\Rightarrow13.28\\le n\\le16.61$，$n=14,15,16$。答案：(3)(4)(5)。"
        },
        {
          id: "matha-113mock-q8", no: 8, type: "multiple", choices: C5, answer: ["1", "5"],
          image: IMG + "113一模-數學-p4-4.png",
          stem: "如右圖，將一張面積為 $3$ 的正方形色紙放置於一張面積為 $5$ 的正方形色紙上，使得小正方形的頂點皆落在大正方形的邊上，此時大正方形被小正方形分割成 $4$ 個全等的直角三角形以及 $1$ 個正方形（小正方形），試選出正確的選項。",
          options: { "1": "三角形兩股的長度平方和為 $3$", "2": "三角形兩股的長度和為 $5$", "3": "三角形兩股的長度乘積為 $2$", "4": "三角形的面積為 $1$", "5": "三角形兩股長度相差 $1$" },
          explanation: "設兩股 $a\\ge b$，大正方形邊長 $\\sqrt5$、小正方形邊長 $\\sqrt3$。\n(1)$a^2+b^2=3$ ✓；(2)$a+b=\\sqrt5$（非 5）；(3)$2ab=(a+b)^2-(a^2+b^2)=5-3=2\\Rightarrow ab=1$（非 2）；(4)面積 $\\dfrac12ab=\\dfrac12$（非 1）；(5)$(a-b)^2=(a+b)^2-4ab=1\\Rightarrow a-b=1$ ✓。答案：(1)(5)。"
        },
        {
          id: "matha-113mock-q9", no: 9, type: "multiple", choices: C5, answer: ["1", "2", "3", "5"],
          image: IMG + "113一模-數學-p4-5.png",
          stem: "如右圖，兩直線 $L_1$、$L_2$ 的方程式分別為 $L_1:\\dfrac{x}{a}+\\dfrac{y}{b}=-1$、$L_2:\\dfrac{x}{c}-\\dfrac{y}{d}=1$。試選出數值為正的選項。",
          options: { "1": "$a$", "2": "$c$", "3": "$ab$", "4": "$cd$", "5": "$\\dfrac{b}{a}+\\dfrac{d}{c}$" },
          explanation: "改截距式 $L_1:\\dfrac{x}{-a}+\\dfrac{y}{-b}=1,\\ L_2:\\dfrac{x}{c}+\\dfrac{y}{-d}=1$。由圖 $-a<0,-b<0,c>0,-d>0\\Rightarrow a>0,b>0,c>0,d<0$。\n故 $a>0$✓、$c>0$✓、$ab>0$✓、$cd<0$✗；由斜率比較得 $\\dfrac ba+\\dfrac dc>0$✓。答案：(1)(2)(3)(5)。"
        },
        {
          id: "matha-113mock-q10", no: 10, type: "multiple", choices: C5, answer: ["2", "3"],
          stem: "已知三次不等式 $2x^3+2(k-6)x^2-(3k-16)x-2k>0$ 的解為 $x>2$，試選出可能是 $k$ 值的選項。",
          options: { "1": "$2$", "2": "$4$", "3": "$6$", "4": "$8$", "5": "$10$" },
          explanation: "$x=2$ 為根 $\\Rightarrow(x-2)$ 為因式：原式 $=(x-2)\\big(2x^2+2(k-4)x+k\\big)$。\n解為 $x>2\\Rightarrow2x^2+2(k-4)x+k$ 恆正 $\\Rightarrow$ 判別式 $<0$：$4k^2-40k+64<0\\Rightarrow(k-2)(k-8)<0\\Rightarrow2<k<8$。答案：(2)(3)。"
        },
        {
          id: "matha-113mock-q11", no: 11, type: "multiple", choices: C5, answer: ["1", "5"],
          stem: "關於滿足方程式 $x^2+y^2-4x-4y+6=0$ 的實數數對 $(x,y)$，試選出正確的選項。",
          options: {
            "1": "$x^2+y^2$ 有最大值為 $18$",
            "2": "$x^2+y^2$ 有最小值為 $\\sqrt{2}$",
            "3": "恰有 $34$ 組 $(x,y)$ 使得 $x^2+y^2$ 為整數",
            "4": "$\\dfrac{y}{x}$ 有最大值為 $1$",
            "5": "$\\dfrac{y}{x}$ 有最小值為 $2-\\sqrt{3}$"
          },
          explanation: "配方 $(x-2)^2+(y-2)^2=(\\sqrt2)^2$，圓心 $A(2,2)$、半徑 $\\sqrt2$，$\\overline{OA}=2\\sqrt2>r$，原點在圓外。\n(1)$x^2+y^2$ 最大 $=(\\overline{OA}+r)^2=18$ ✓；(2)最小 $=(\\overline{OA}-r)^2=2$（非 $\\sqrt2$）；(3)整數值共 32 組（非 34）；(4)(5)$\\dfrac yx\\in[2-\\sqrt3,\\,2+\\sqrt3]$，最小 $2-\\sqrt3$ ✓、最大非 1。答案：(1)(5)。"
        },
        {
          id: "matha-113mock-q12", no: 12, type: "multiple", choices: C5, answer: ["1", "4", "5"],
          stem: "令 $f(x)=(x+1)^3-3(x+1)^2+2(x+1)+1$，試選出正確的選項。",
          options: {
            "1": "$f(-0.999)$ 的近似值（四捨五入至整數位）為 $1$",
            "2": "$y=f(x)$ 圖形的對稱中心為 $(-1,1)$",
            "3": "不管 $y=f(x)$ 的圖形如何平移，圖形與 $x$ 軸僅有一個交點",
            "4": "$f(x)=(x-1)^3+3(x-1)^2+2(x-1)+1$",
            "5": "$y=f(x)$ 在 $x=1$ 附近的一次近似為 $y=2x-1$"
          },
          explanation: "化簡得 $f(x)=x^3-x+1$（由 $y=x^3-x$ 上移 1）。\n(1)$x=-1$ 附近一次近似 $y=2x+3\\Rightarrow f(-0.999)\\approx1$ ✓；(2)對稱中心 $(0,1)$（非 $(-1,1)$）；(3)$x^3-x$ 與 $x$ 軸有 3 個交點，平移後可超過 1 個；(4)綜合除法得 $(x-1)^3+3(x-1)^2+2(x-1)+1$ ✓；(5)$x=1$ 附近一次近似 $y=2x-1$ ✓。答案：(1)(4)(5)。"
        }
      ]
    },
    {
      type: "group",
      title: "三、選填題（第 13–17 題，每題 5 分）· 依格式填數字格",
      shared: null,
      questions: [
        {
          id: "matha-113mock-q13", no: 13, type: "fill", boxes: ["⑬-1", "⑬-2"], answer: ["1", "8"],
          stem: "已知面積為 $11+6\\sqrt{2}$ 的矩形，其周長的最小值為 $m$，將 $m$ 四捨五入至整數位後所得到的值為 $\\boxed{⑬\\text{-}1}\\ \\boxed{⑬\\text{-}2}$（兩位數）。",
          explanation: "$2(a+b)\\ge4\\sqrt{ab}=4\\sqrt{11+6\\sqrt2}=4\\sqrt{(3+\\sqrt2)^2}=4(3+\\sqrt2)=12+4\\sqrt2\\approx17.656$。\n四捨五入 $m=18$。"
        },
        {
          id: "matha-113mock-q14", no: 14, type: "fill", boxes: ["⑭-1", "⑭-2"], answer: ["-", "2"],
          stem: "若實係數三次多項式 $f(x)=x^3+ax^2+ax+a$ 除以 $x+1$ 與 $f(x)$ 除以 $x^2+x+1$ 有相同的餘式，則 $f(x)$ 除以 $x+2$ 的餘式為 $\\boxed{⑭\\text{-}1}\\ \\boxed{⑭\\text{-}2}$（⑭-1 填正負號，⑭-2 填數字）。",
          explanation: "除以 $x^2+x+1$ 餘 $1$；除以 $x+1$ 餘 $a-1$。兩者相等 $\\Rightarrow a-1=1\\Rightarrow a=2$。\n由餘式定理，除以 $x+2$ 的餘式 $=f(-2)=3a-8=-2$。"
        },
        {
          id: "matha-113mock-q15", no: 15, type: "fill", boxes: ["⑮-1", "⑮-2"], answer: ["5", "5"],
          stem: "將坐標平面上的直線 $ax+by=0$ 向右平移 $1$ 單位再向上平移 $2$ 單位後，與原本的直線恰好重合，則兩平行直線 $ax+by+a=0$ 與 $ax+by-b=0$ 間的距離為 $\\dfrac{\\sqrt{\\boxed{⑮\\text{-}1}}}{\\boxed{⑮\\text{-}2}}$（化為最簡分數；⑮-1 填根號內的數，⑮-2 填分母）。",
          explanation: "斜率 $-\\dfrac ab=2\\Rightarrow a=-2b$。兩平行線距離 $=\\dfrac{|a+b|}{\\sqrt{a^2+b^2}}=\\dfrac{|-b|}{\\sqrt{5b^2}}=\\dfrac{1}{\\sqrt5}=\\dfrac{\\sqrt5}{5}$。"
        },
        {
          id: "matha-113mock-q16", no: 16, type: "fill", boxes: ["⑯-1", "⑯-2"], answer: ["2", "4"],
          stem: "設 $f(x)$ 為首項係數為 $1$ 的實係數三次多項式，若對所有實數 $t$ 皆有關係式 $f(t-1)=-f(3-t)$，且 $f(2)=f(0)$，則 $f(4)=\\boxed{⑯\\text{-}1}\\ \\boxed{⑯\\text{-}2}$（兩位數）。",
          explanation: "由 $f(t-1)=-f(3-t)$ 知圖形對稱中心 $x=1$，且 $f(1)=0$；又 $f(0)=f(2)$ 且 $f(0)=-f(2)\\Rightarrow f(0)=f(2)=0$。\n故 $f(x)=x(x-1)(x-2)$，$f(4)=4\\cdot3\\cdot2=24$。"
        },
        {
          id: "matha-113mock-q17", no: 17, type: "fill", boxes: ["⑰"], answer: ["1"],
          stem: "坐標平面上有一圓 $C:(x-k)^2+(y+k)^2=k^2\\ (k\\ne 0)$，且圓 $C$ 上的點 $(x,y)$ 皆滿足 $3x-4y-12\\le 0$，則滿足條件的實數 $k$ 最大為 $\\boxed{⑰}$。",
          explanation: "圓心 $(k,-k)$、半徑 $|k|$。圓在直線 $3x-4y-12=0$ 左側 $\\Rightarrow$ ①$\\dfrac{|7k-12|}{5}\\ge|k|\\Rightarrow(k-1)(k-6)\\ge0$；②圓心 $7k-12<0\\Rightarrow k<\\dfrac{12}{7}$。\n故 $k\\le1$（$k\\ne0$），最大值 $k=1$。"
        }
      ]
    },
    {
      type: "group",
      title: "第貳部分、混合題或非選擇題（第 18–20 題為題組，占 15 分）",
      shared: {
        kind: "passage",
        text: "18–20 題為題組。給定坐標平面上點 A(4 , 8)、B(10 , 6)、C(0 , −4) 三點，及一動點 D，試回答下列問題。"
      },
      questions: [
        {
          id: "matha-113mock-q18", no: 18, type: "fill", boxes: ["⑱-1", "⑱-2", "⑱-3"], answer: ["3", "-", "8"],
          stem: "若平面上有一直線 $L$，直線 $L$ 上的動點 $P(x,y)$ 皆滿足 $\\overline{PA}=\\overline{PC}$，則直線 $L$ 的方程式為 $x+\\boxed{⑱\\text{-}1}\\,y+\\boxed{⑱\\text{-}2}\\,\\boxed{⑱\\text{-}3}=0$（⑱-1 填係數、⑱-2 填正負號、⑱-3 填常數；選填題，4 分）。",
          explanation: "$\\overline{PA}=\\overline{PC}\\Rightarrow L$ 為 $\\overline{AC}$ 的中垂線。$\\overline{AC}$ 中點 $(2,2)$、斜率 $3$，故 $L$ 過 $(2,2)$ 且斜率 $-\\dfrac13$：$x+3y-8=0$。"
        },
        {
          id: "matha-113mock-q19", no: 19, type: "single", choices: C5, answer: "1",
          stem: "若動點 $D$ 滿足 $\\overline{AD}\\le\\overline{CD}$，則下列何者可能為動點 $D$ 的坐標？（單選題，3 分）",
          options: { "1": "$(-1,3)$", "2": "$(-1,2)$", "3": "$(1,2)$", "4": "$(-10,5)$", "5": "$(-10,4)$" },
          explanation: "由第 18 題，$L:x+3y-8=0$ 上 $\\overline{AD}=\\overline{CD}$；$A(4,8)$ 代入 $x+3y-8=20>0$，故 $\\overline{AD}\\le\\overline{CD}$ 的 $D$ 滿足 $x+3y-8\\ge0$。\n只有 $(-1,3)$：$-1+9-8=0$ 符合。答案：(1)。"
        },
        {
          id: "matha-113mock-q20", no: 20, type: "handwritten",
          label: "第 20 題（非選擇題，8 分）",
          stem: "今欲以滿足 $\\overline{AD}\\le\\overline{BD}$ 之動點 $D$ 為圓心，分別以 $\\overline{BD}$ 和 $\\overline{AD}$ 為半徑作圓，使得點 $C$ 在兩圓之間（包含在圓上的情況）。試求在 $x\\ge 0$ 且 $y\\ge 0$ 時，動點 $D$ 所形成的區域面積。"
        }
      ]
    }
  ];

  QUESTION_BANKS.push({
    id: "matha-113mock-answer-card",
    subject: "數學",
    sourceSubject: "數學（翰林一模）",
    year: "113一模",
    category: "113 全國一模 數學 答題卡練習",
    title: "113 全國高中一模 數學 答題卡練習",
    status: "模擬考題庫（翰林）",
    source: {
      "題目": "測試用試題/113全國一模.pdf",
      "詳解": "測試用試題/113全國一模詳解.pdf"
    },
    note: "收錄 113 全國一模數學：可作答 19 題（單選 6＋多選 6＋選填 5＋題組單選 1、選填 1）＋手寫題 1 題（第 20 題，僅列出不判分）。公式以 LaTeX 呈現、KaTeX 渲染，圖形採官方裁圖；答案與解析取自官方詳解。錯題交卷後可展開解析。",
    questions: blocks.flatMap(b => b.questions),
    blocks
  });
})();
