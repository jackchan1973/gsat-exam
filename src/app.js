const STORAGE_KEY = "gsat-review-progress-v1";

const state = {
  view: "subjects",
  subject: null,
  year: null,
  category: null
};

const subjectGroups = [
  { id: "國文", label: "國文", short: "國", sourceSubjects: ["國綜", "國寫"], description: "字音字形、成語、文言文" },
  { id: "英文", label: "英文", short: "英", sourceSubjects: ["英文"], description: "單字、文意選填、閱讀理解" },
  { id: "數學", label: "數學", short: "數", sourceSubjects: ["數學A", "數學B"], description: "選擇題與詳解雛形" },
  { id: "社會", label: "社會", short: "社", sourceSubjects: ["社會"], description: "重點卡與題庫待建" },
  { id: "自然", label: "自然", short: "自", sourceSubjects: ["自然"], description: "觀念整理與練習待建" }
];

const typeOrder = ["試題內容", "答題卷", "選擇題答案", "選擇(填)題答案", "非選擇題評分原則"];
const optionLabels = ["A", "B", "C", "D", "E"];
const realQuestionSets = typeof QUESTION_BANKS === "undefined" ? [] : QUESTION_BANKS;
const mockQuestionSets = typeof MOCK_QUESTION_SETS === "undefined" ? [] : MOCK_QUESTION_SETS;

const screenHeader = document.getElementById("screenHeader");
const screenBody = document.getElementById("screenBody");
const homeButton = document.getElementById("homeButton");
const backButton = document.getElementById("backButton");
const teacherButton = document.getElementById("teacherButton");

function unique(values) {
  return [...new Set(values)].filter(Boolean);
}

function readProgress() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY)) || {};
  } catch {
    return {};
  }
}

function writeProgress(progress) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
}

function groupFor(subjectId) {
  return subjectGroups.find(group => group.id === subjectId);
}

function filesFor(subjectId, year) {
  const group = groupFor(subjectId);
  if (!group) return [];

  return EXAM_FILES
    .filter(file => group.sourceSubjects.includes(file.subject))
    .filter(file => !year || file.year === year)
    .sort((a, b) => {
      const yearCompare = b.year.localeCompare(a.year);
      if (yearCompare) return yearCompare;
      const subjectCompare = a.subject.localeCompare(b.subject, "zh-Hant");
      if (subjectCompare) return subjectCompare;
      return typeOrder.indexOf(a.type) - typeOrder.indexOf(b.type);
    });
}

function questionSetsFor(subjectId, year) {
  const realSets = realQuestionSets
    .filter(set => set.subject === subjectId)
    .filter(set => !year || set.year === year);
  if (realSets.length) return realSets;
  return mockQuestionSets
    .filter(set => set.subject === subjectId)
    .filter(set => !year || set.year === year);
}

function allQuestionSets() {
  return [...realQuestionSets, ...mockQuestionSets.filter(mockSet => {
    return !realQuestionSets.some(realSet => realSet.subject === mockSet.subject && realSet.year === mockSet.year);
  })];
}

function selectedSet() {
  return questionSetsFor(state.subject, state.year).find(set => set.category === state.category);
}

function goTo(view, nextState = {}) {
  Object.assign(state, nextState, { view });
  render();
}

function goHome() {
  goTo("subjects", { subject: null, year: null, category: null });
}

function goBack() {
  if (state.view === "teacher") {
    goTo(state.category ? "practice" : state.year ? "categories" : state.subject ? "years" : "subjects");
    return;
  }
  if (state.view === "practice") goTo("categories", { category: null });
  else if (state.view === "categories") goTo("years", { year: null, category: null });
  else if (state.view === "years") goHome();
  else goHome();
}

function renderHeader(title, subtitle) {
  screenHeader.innerHTML = `
    <h1>${title}</h1>
    <p>${subtitle}</p>
  `;
}

function renderSubjects() {
  renderHeader("學測複習入口", "先選科目，再進入對應的年度、題目分類與練習畫面。各科分開擴充，避免互相影響。");

  screenBody.innerHTML = `
    <div class="entry-grid subjects">
      ${subjectGroups.map(group => {
        const files = filesFor(group.id);
        const years = unique(files.map(file => file.year));
        return `
          <button class="entry-card subject-card" type="button" data-subject="${group.id}">
            <span class="card-icon">${group.short}</span>
            <strong>${group.label}</strong>
            <span>${group.description}</span>
            <small>收錄 ${years.length} 個年度官方試題</small>
          </button>
        `;
      }).join("")}
    </div>
  `;

  screenBody.querySelectorAll("[data-subject]").forEach(button => {
    button.addEventListener("click", () => {
      goTo("years", { subject: button.dataset.subject, year: null, category: null });
    });
  });
}

function renderYears() {
  const group = groupFor(state.subject);
  if (!group) return goHome();

  renderHeader(`${group.label}歷屆題目`, "選擇要練習的學年度。下一頁會進入題目分類。");

  const years = unique(filesFor(group.id).map(file => file.year)).sort((a, b) => b.localeCompare(a));
  screenBody.innerHTML = `
    <div class="breadcrumb">首頁 / ${group.label}</div>
    <div class="entry-grid years">
      ${years.map(year => {
        const sets = questionSetsFor(group.id, year);
        const done = sets.filter(set => readProgress()[set.id]).length;
        return `
          <button class="entry-card year-card" type="button" data-year="${year}">
            <strong>${year} 年題目</strong>
            <span>${group.label} ${year} 學年度</span>
            <small>${sets.length ? `${done}/${sets.length} 分類已完成` : "尚未建立測試題"}</small>
          </button>
        `;
      }).join("")}
    </div>
  `;

  screenBody.querySelectorAll("[data-year]").forEach(button => {
    button.addEventListener("click", () => {
      goTo("categories", { year: button.dataset.year, category: null });
    });
  });
}

function renderCategories() {
  const group = groupFor(state.subject);
  if (!group || !state.year) return goHome();

  renderHeader(`${group.label} ${state.year} 年題目分類`, "選擇分類後進入答題卡畫面。作文不納入；混合題非選擇題提供手寫作答區，交由師長檢查。");

  const sets = questionSetsFor(group.id, state.year);
  screenBody.innerHTML = `
    <div class="breadcrumb">首頁 / ${group.label} / ${state.year} 年</div>
    ${sets.length ? `
      <div class="entry-grid categories">
        ${sets.map(set => {
          const saved = readProgress()[set.id];
          return `
            <button class="entry-card category-card" type="button" data-category="${set.category}">
              <strong>${set.category}</strong>
              <span>${set.questions.length} 題</span>
              <small>${saved ? `已完成，錯 ${saved.wrongCount} 題${saved.manualCount ? `，人工檢查 ${saved.manualCount} 題` : ""}` : set.status}</small>
            </button>
          `;
        }).join("")}
      </div>
    ` : '<div class="empty">這個科目年份的互動題庫還在製作中。</div>'}
  `;

  screenBody.querySelectorAll("[data-category]").forEach(button => {
    button.addEventListener("click", () => {
      goTo("practice", { category: button.dataset.category });
    });
  });
}

function renderPractice() {
  const set = selectedSet();
  const group = groupFor(state.subject);
  if (!set || !group) return goTo("categories");

  const manualCount = set.questions.filter(question => question.type === "written").length;
  const guidance = manualCount
    ? `提交後會自動檢查選擇題，另有 ${manualCount} 題非選擇題交由師長檢查。`
    : "提交後會檢查錯題並顯示正確答案。";
  renderHeader(set.title, `${set.status}，共 ${set.questions.length} 題。${guidance}`);

  screenBody.innerHTML = `
    <div class="breadcrumb">首頁 / ${group.label} / ${state.year} 年 / ${set.category}</div>
    <form class="question-list" id="practiceForm">
      ${set.blocks
        ? set.blocks.map(renderExamBlock).join("")
        : set.displayGroups
          ? set.displayGroups.map(group => renderImageQuestionGroup(set, group)).join("")
          : set.questions.map(renderQuestion).join("")}
    </form>
    <div class="practice-actions">
      <button class="primary-btn" id="submitAnswers" type="button">提交並檢查錯題</button>
      <button class="secondary-btn" id="clearAnswers" type="button">清除作答</button>
    </div>
    <section class="result-panel" id="resultPanel" hidden></section>
  `;

  document.getElementById("submitAnswers").addEventListener("click", checkAnswers);
  document.getElementById("clearAnswers").addEventListener("click", () => {
    document.getElementById("practiceForm").reset();
    document.getElementById("resultPanel").hidden = true;
  });
}

function renderTeacherCheck() {
  const progress = readProgress();
  const allSets = allQuestionSets();
  const completedSets = allSets.filter(set => progress[set.id]);
  const totalQuestions = allSets.reduce((sum, set) => sum + set.questions.length, 0);
  const answeredQuestions = completedSets.reduce((sum, set) => sum + set.questions.length, 0);
  const wrongCount = completedSets.reduce((sum, set) => sum + (progress[set.id].wrongCount || 0), 0);
  const manualCount = completedSets.reduce((sum, set) => sum + (progress[set.id].manualCount || 0), 0);
  const completionRate = totalQuestions ? Math.round((answeredQuestions / totalQuestions) * 100) : 0;

  renderHeader("師長檢查", "查看目前題庫的完成率、錯題數與各分類狀態。");

  screenBody.innerHTML = `
    <div class="stats-grid">
      <article class="stat-card">
        <span>完成率</span>
        <strong>${completionRate}%</strong>
        <small>${answeredQuestions}/${totalQuestions} 題已完成</small>
      </article>
      <article class="stat-card">
        <span>完成分類</span>
        <strong>${completedSets.length}/${allSets.length}</strong>
        <small>依測試分類計算</small>
      </article>
      <article class="stat-card">
        <span>錯題數</span>
        <strong>${wrongCount}</strong>
        <small>選擇題自動判斷，人工檢查 ${manualCount} 題</small>
      </article>
    </div>
    <div class="report-list">
      ${allSets.map(set => {
        const saved = progress[set.id];
        return `
          <article class="report-row">
            <div>
              <strong>${set.subject} ${set.year} 年 ${set.category}</strong>
              <span>${set.questions.length} 題，${set.status}</span>
            </div>
            <div class="${saved ? "status-done" : "status-open"}">
              ${saved ? `完成，答對 ${saved.correctCount}/${saved.gradableTotal || saved.total}，錯 ${saved.wrongCount}${saved.manualCount ? `，人工檢查 ${saved.manualCount}` : ""}` : "未完成"}
            </div>
          </article>
        `;
      }).join("")}
    </div>
    <button class="secondary-btn danger" id="clearProgress" type="button">清除測試紀錄</button>
  `;

  document.getElementById("clearProgress").addEventListener("click", () => {
    localStorage.removeItem(STORAGE_KEY);
    renderTeacherCheck();
  });
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"]/g, char => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[char]));
}

// ===== 英文（含題組/共用文章/字庫/圖片選項）題型呈現 =====
function renderExamBlock(block) {
  const shared = block.shared;
  return `
    <section class="exam-block">
      <header class="exam-block-title">${escapeHtml(block.title)}</header>
      ${shared ? `<div class="exam-shared">${renderExamShared(shared, block)}</div>` : ""}
      <div class="exam-questions">
        ${block.questions.map(question => renderExamQuestion(question, shared)).join("")}
      </div>
    </section>
  `;
}

function renderExamShared(shared, block) {
  if (shared.kind === "image") {
    return `<div class="exam-shared-scroll"><img class="exam-passage-image" src="../${shared.src}" alt="${escapeHtml(block.title)} 官方文章"></div>`;
  }
  if (shared.kind === "passage") {
    return `<div class="exam-passage">${renderExamPassage(shared.text)}</div>`;
  }
  if (shared.kind === "passage-bank") {
    const bankRows = Object.entries(shared.bank)
      .map(([label, value]) => `<div><b>(${label})</b> ${escapeHtml(value)}</div>`)
      .join("");
    return `
      <div class="exam-passage">${renderExamPassage(shared.text)}</div>
      <div class="exam-bank" aria-label="${escapeHtml(shared.bankLabel)}">
        <span class="exam-bank-label">${escapeHtml(shared.bankLabel)}</span>
        ${bankRows}
      </div>
    `;
  }
  return "";
}

function renderExamPassage(text) {
  return escapeHtml(text).replace(/\{\{(\d+)\}\}/g, (match, no) => `<span class="exam-blank">${no}</span>`);
}

function renderExamQuestion(question, shared) {
  const inputType = question.type === "multiple" ? "checkbox" : "radio";
  let optionsHtml;
  if (question.optionImages) {
    optionsHtml = question.choices.map(label => `
      <label class="option-row option-image-row" for="${question.id}-${label}">
        <input id="${question.id}-${label}" name="${question.id}" type="${inputType}" value="${label}">
        <span class="opt-key">${label}</span>
        <img class="option-image" src="../${question.optionImages[label]}" alt="選項 ${label} 圖片">
      </label>
    `).join("");
  } else {
    const source = question.useBank ? shared.bank : question.options;
    optionsHtml = question.choices.map(label => {
      const optionText = source && source[label] != null ? source[label] : "";
      return `
        <label class="option-row" for="${question.id}-${label}">
          <input id="${question.id}-${label}" name="${question.id}" type="${inputType}" value="${label}">
          <span><strong>${label}</strong>${optionText ? `　${escapeHtml(optionText)}` : ""}</span>
        </label>
      `;
    }).join("");
  }
  const multiHint = question.type === "multiple" ? '<span class="exam-multi-hint">（多選）</span>' : "";
  return `
    <fieldset class="question-card exam-question">
      <legend>第 ${question.no} 題${multiHint}</legend>
      ${question.stem ? `<p class="exam-stem">${escapeHtml(question.stem)}</p>` : ""}
      <div class="option-list">${optionsHtml}</div>
    </fieldset>
  `;
}

function renderQuestion(question) {
  const choices = question.choices || optionLabels.slice(0, question.options.length);
  const inputType = question.type === "multiple" ? "checkbox" : "radio";
  return `
    <fieldset class="question-card">
      <legend>第 ${question.no} 題</legend>
      ${question.text ? `<pre class="official-question">${question.text}</pre>` : `<p>${question.prompt}</p>`}
      <div class="option-list">
        ${choices.map((label, index) => {
          const optionText = question.options ? `. ${question.options[index]}` : "";
          return `
            <label class="option-row" for="${question.id}-${label}">
              <input id="${question.id}-${label}" name="${question.id}" type="${inputType}" value="${label}">
              <span>${label}${optionText}</span>
            </label>
          `;
        }).join("")}
      </div>
    </fieldset>
  `;
}

function renderImageQuestionGroup(set, group) {
  const questions = group.questionNos.map(no => set.questions.find(question => question.no === no)).filter(Boolean);
  return `
    <section class="visual-question-group">
      <header class="visual-group-header">
        <h2>${group.label}</h2>
        <span>官方試卷裁切圖</span>
      </header>
      <div class="visual-answer-layout">
        <div class="official-image-list">
          ${group.images.map((image, index) => `
            <img class="official-page-image" src="../${image}" alt="${group.label} 官方試卷圖 ${index + 1}">
          `).join("")}
        </div>
        <div class="answer-card">
          <h3>答題卡</h3>
          ${questions.map(renderAnswerRow).join("")}
        </div>
      </div>
    </section>
  `;
}

function renderAnswerRow(question) {
  if (question.type === "written") {
    return `
      <div class="answer-row answer-row-written">
        <strong>${question.no}</strong>
        <label class="written-answer">
          <span>手寫作答區，需師長檢查</span>
          <textarea name="${question.id}" rows="4" placeholder="依官方題目限制作答"></textarea>
        </label>
      </div>
    `;
  }

  const choices = question.choices || optionLabels.slice(0, question.options.length);
  const inputType = question.type === "multiple" ? "checkbox" : "radio";
  return `
    <div class="answer-row">
      <strong>${question.no}</strong>
      <div class="answer-options">
        ${choices.map(label => `
          <label for="${question.id}-${label}">
            <input id="${question.id}-${label}" name="${question.id}" type="${inputType}" value="${label}">
            <span>${label}</span>
          </label>
        `).join("")}
      </div>
    </div>
  `;
}

function checkAnswers() {
  const set = selectedSet();
  if (!set) return;

  const form = document.getElementById("practiceForm");
  const resultPanel = document.getElementById("resultPanel");
  const wrong = [];
  const manual = [];
  let correctCount = 0;

  set.questions.forEach(question => {
    if (question.type === "written") {
      const value = form.querySelector(`[name="${question.id}"]`)?.value.trim() || "";
      manual.push({ question, userAnswer: value || "未作答" });
      return;
    }

    const picked = [...form.querySelectorAll(`input[name="${question.id}"]:checked`)].map(input => input.value);
    const userAnswer = question.type === "multiple" ? picked.sort() : (picked[0] || "未作答");
    const correctAnswer = Array.isArray(question.answer) ? [...question.answer].sort() : question.answer;
    const isCorrect = Array.isArray(correctAnswer)
      ? userAnswer.length === correctAnswer.length && userAnswer.every((value, index) => value === correctAnswer[index])
      : userAnswer === correctAnswer;
    if (isCorrect) {
      correctCount += 1;
    } else {
      wrong.push({ question, userAnswer });
    }
  });

  const gradableTotal = set.questions.length - manual.length;
  const progress = readProgress();
  progress[set.id] = {
    subject: set.subject,
    year: set.year,
    category: set.category,
    total: set.questions.length,
    gradableTotal,
    correctCount,
    wrongCount: wrong.length,
    manualCount: manual.length,
    updatedAt: new Date().toISOString()
  };
  writeProgress(progress);

  resultPanel.hidden = false;
  resultPanel.innerHTML = `
    <div class="result-score">
      <strong>${correctCount} / ${gradableTotal}</strong>
      <span>${wrong.length ? "以下是錯題與正確答案" : "選擇題全部答對"}${manual.length ? `，另有 ${manual.length} 題需師長檢查` : ""}</span>
    </div>
    ${wrong.length ? `
      <div class="wrong-list">
        ${wrong.map(item => `
          <div class="wrong-card">
            <strong>第 ${item.question.no} 題</strong>
            <span>你的答案：${formatAnswer(item.userAnswer)}</span>
            <span>正確答案：${formatAnswer(item.question.answer)}</span>
          </div>
        `).join("")}
      </div>
    ` : ""}
    ${manual.length ? `
      <div class="manual-list">
        ${manual.map(item => `
          <div class="manual-card">
            <strong>第 ${item.question.no} 題</strong>
            <span>作答狀態：${item.userAnswer === "未作答" ? "未作答" : "已填寫"}</span>
            <span>非選擇題不自動判分，請由師長依官方標準檢查。</span>
          </div>
        `).join("")}
      </div>
    ` : ""}
  `;
}

function formatAnswer(answer) {
  if (Array.isArray(answer)) return answer.length ? answer.join("") : "未作答";
  return answer;
}

function render() {
  homeButton.hidden = state.view === "subjects";
  backButton.hidden = state.view === "subjects";

  if (state.view === "subjects") renderSubjects();
  if (state.view === "years") renderYears();
  if (state.view === "categories") renderCategories();
  if (state.view === "practice") renderPractice();
  if (state.view === "teacher") renderTeacherCheck();
}

homeButton.addEventListener("click", goHome);
backButton.addEventListener("click", goBack);
teacherButton.addEventListener("click", () => goTo("teacher"));

render();
