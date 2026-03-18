const state = {
  subjects: [],
  dashboard: null,
  resources: [],
  settings: null,
  history: [],
  currentExam: null,
  currentAnswers: {},
  currentResult: null,
  currentHistoryId: null,
};

const viewMeta = {
  dashboard: ["概览", "查看题库规模、薄弱专题、错题本和自动复习建议。"],
  exam: ["模拟考试", "支持综合模拟、专题冲刺、弱项补刷和错题重练。"],
  history: ["成绩记录", "查看每次考试的得分、答题快照和错因分析。"],
  resources: ["补充资源", "浏览官方考试大纲、样题和 AI 接入资料。"],
  settings: ["系统设置", "配置 OpenAI Compatible 与 Sub2API 最新兼容接入。"],
};

const LOCAL_EXAM_KEY = "ncre-current-exam";

const dom = {
  banner: document.getElementById("banner"),
  statsGrid: document.getElementById("stats-grid"),
  subjectGrid: document.getElementById("subject-grid"),
  latestAttempts: document.getElementById("latest-attempts"),
  weakTopicList: document.getElementById("weak-topic-list"),
  wrongBookList: document.getElementById("wrong-book-list"),
  topicMasteryList: document.getElementById("topic-mastery-list"),
  studyRecommendationList: document.getElementById("study-recommendation-list"),
  subjectSelect: document.getElementById("subject-select"),
  topicSelect: document.getElementById("topic-select"),
  historyFilter: document.getElementById("history-filter"),
  examMeta: document.getElementById("exam-meta"),
  examContainer: document.getElementById("exam-container"),
  resultContainer: document.getElementById("result-container"),
  historyList: document.getElementById("history-list"),
  historyDetail: document.getElementById("history-detail"),
  resourceList: document.getElementById("resource-list"),
  pageTitle: document.getElementById("page-title"),
  pageSubtitle: document.getElementById("page-subtitle"),
  examTimer: document.getElementById("exam-timer"),
  submitExamBtn: document.getElementById("submit-exam-btn"),
  seedInput: document.getElementById("seed-input"),
  weaknessBoostInput: document.getElementById("weakness-boost-input"),
  presetOpenAIButton: document.getElementById("preset-openai-btn"),
  presetSub2APIButton: document.getElementById("preset-sub2api-btn"),
  testConnectionButton: document.getElementById("test-connection-btn"),
};

let timerHandle = null;

async function request(url, options = {}) {
  const response = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.error || "请求失败");
  }
  return payload;
}

function showBanner(message, tone = "info") {
  dom.banner.textContent = message;
  dom.banner.className = `banner visible ${tone}`;
}

function clearBanner() {
  dom.banner.className = "banner";
  dom.banner.textContent = "";
}

function setView(view) {
  document.querySelectorAll(".view").forEach((element) => {
    element.classList.toggle("active", element.id === `view-${view}`);
  });
  document.querySelectorAll(".nav-link").forEach((element) => {
    element.classList.toggle("active", element.dataset.view === view);
  });
  const [title, subtitle] = viewMeta[view];
  dom.pageTitle.textContent = title;
  dom.pageSubtitle.textContent = subtitle;
}

function formatRate(rate) {
  return `${(Number(rate || 0) * 100).toFixed(1)}%`;
}

function formatDate(dateText) {
  if (!dateText) return "-";
  return new Date(dateText).toLocaleString("zh-CN", { hour12: false });
}

function persistExam() {
  if (!state.currentExam) {
    localStorage.removeItem(LOCAL_EXAM_KEY);
    return;
  }
  localStorage.setItem(LOCAL_EXAM_KEY, JSON.stringify({
    exam: state.currentExam,
    answers: state.currentAnswers,
    result: state.currentResult,
  }));
}

function restoreExam() {
  const raw = localStorage.getItem(LOCAL_EXAM_KEY);
  if (!raw) return;
  try {
    const saved = JSON.parse(raw);
    state.currentExam = saved.exam || null;
    state.currentAnswers = saved.answers || {};
    state.currentResult = saved.result || null;
  } catch {
    localStorage.removeItem(LOCAL_EXAM_KEY);
  }
}

function renderStats() {
  if (!state.dashboard) return;
  const items = [
    ["内置科目", state.dashboard.subject_count],
    ["题目总量", state.dashboard.question_count],
    ["考试次数", state.dashboard.attempt_count],
    ["平均分", state.dashboard.average_score],
    ["平均正确率", formatRate(state.dashboard.average_correct_rate)],
  ];
  dom.statsGrid.innerHTML = items.map(([label, value]) => `
    <article class="stats-card">
      <span class="muted">${label}</span>
      <strong>${value}</strong>
    </article>
  `).join("");
}

function renderLatestAttempts() {
  const attempts = state.dashboard?.latest_attempts || [];
  if (!attempts.length) {
    dom.latestAttempts.innerHTML = `<div class="empty-state">还没有交卷记录，先去生成一套试卷。</div>`;
    return;
  }
  dom.latestAttempts.innerHTML = attempts.map((item) => `
    <article class="attempt-card">
      <strong>${item.subject_name}</strong>
      <p>${item.exam_mode === "ai" ? "AI 生成" : item.exam_mode === "wrong_book" ? "错题重练" : "系统组卷"} · ${formatDate(item.submitted_at)}</p>
      <p class="score-badge">${item.obtained_score} / ${item.total_score} · 正确率 ${formatRate(item.correct_rate)}</p>
    </article>
  `).join("");
}

function renderWeakTopics() {
  const weakTopics = state.dashboard?.weak_topics || [];
  if (!weakTopics.length) {
    dom.weakTopicList.innerHTML = `<div class="empty-state">还没有足够的错题数据，提交几次试卷后这里会显示你的薄弱专题。</div>`;
    return;
  }
  dom.weakTopicList.innerHTML = weakTopics.map((item) => `
    <article class="attempt-card">
      <strong>${item.topic}</strong>
      <p>错题权重 ${item.mistake_weight}，建议优先专题冲刺或按弱项补刷。</p>
    </article>
  `).join("");
}

function renderWrongBookPreview() {
  const wrongBook = state.dashboard?.wrong_book_preview || [];
  if (!wrongBook.length) {
    dom.wrongBookList.innerHTML = `<div class="empty-state">还没有形成错题本，提交试卷后这里会沉淀高价值错题。</div>`;
    return;
  }
  dom.wrongBookList.innerHTML = wrongBook.map((item) => `
    <article class="attempt-card">
      <strong>${item.question_id}</strong>
      <p>${item.topic || item.type} · 错误 ${item.wrong_count} 次 ${item.frequency === "high" ? "· 高频考点" : ""}</p>
      <p>${item.stem}</p>
    </article>
  `).join("");
}

function renderTopicMastery() {
  const topicMastery = state.dashboard?.topic_mastery || [];
  if (!topicMastery.length) {
    dom.topicMasteryList.innerHTML = `<div class="empty-state">还没有足够的答题数据，提交试卷后这里会显示专题掌握度。</div>`;
    return;
  }
  dom.topicMasteryList.innerHTML = topicMastery.slice(0, 10).map((item) => {
    const progress = Math.max(4, Math.round((item.weighted_accuracy || 0) * 100));
    return `
      <article class="attempt-card mastery-card">
        <strong>${item.topic}</strong>
        <div class="mastery-bar">
          <span style="width:${progress}%"></span>
        </div>
        <p>加权正确率 ${formatRate(item.weighted_accuracy)} · 原始正确率 ${formatRate(item.accuracy)}</p>
        <p>作答 ${item.total_count} 次，答对 ${item.correct_count} 次</p>
      </article>
    `;
  }).join("");
}

function renderStudyRecommendations() {
  const recommendations = state.dashboard?.study_recommendations || [];
  if (!recommendations.length) {
    dom.studyRecommendationList.innerHTML = `<div class="empty-state">还没有足够的数据生成复习建议，继续刷题后这里会自动整理下一步重点。</div>`;
    return;
  }
  dom.studyRecommendationList.innerHTML = recommendations.map((item) => `
    <article class="attempt-card recommendation-${item.priority}">
      <strong>${item.topic}</strong>
      <p>优先级 ${item.priority} · 加权正确率 ${formatRate(item.weighted_accuracy)} · 错题权重 ${item.mistake_weight}</p>
      <p>${item.action}</p>
    </article>
  `).join("");
}

function renderResources() {
  dom.resourceList.innerHTML = state.resources.map((resource) => `
    <article class="resource-card">
      <header>
        <div>
          <h4>${resource.title}</h4>
          <p>${resource.note}</p>
        </div>
        <span class="pill">${resource.type}</span>
      </header>
      <footer>
        <span class="muted">${new URL(resource.url).hostname}</span>
        <a class="primary-btn" href="${resource.url}" target="_blank" rel="noreferrer">打开链接</a>
      </footer>
    </article>
  `).join("");
}

function populateSettings() {
  const settings = state.settings || {};
  document.getElementById("setting-enabled").checked = Boolean(settings.enabled);
  document.getElementById("setting-provider-name").value = settings.provider_name || "";
  document.getElementById("setting-protocol").value = settings.protocol || "auto";
  document.getElementById("setting-base-url").value = settings.base_url || "";
  document.getElementById("setting-api-key").value = settings.api_key || "";
  document.getElementById("setting-model").value = settings.model || "";
  document.getElementById("setting-temperature").value = settings.temperature ?? 0.2;
  document.getElementById("setting-timeout-seconds").value = settings.timeout_seconds ?? 60;
  document.getElementById("setting-organization").value = settings.organization || "";
  document.getElementById("setting-project").value = settings.project || "";
  document.getElementById("setting-extra-headers").value = settings.extra_headers || "";
  document.getElementById("setting-grading-mode").value = settings.grading_mode || "hybrid";
  document.getElementById("setting-enable-ai-review").checked = Boolean(settings.enable_ai_review);
}

function applyProviderPreset(preset) {
  if (preset === "sub2api") {
    document.getElementById("setting-enabled").checked = true;
    document.getElementById("setting-provider-name").value = "Sub2API";
    document.getElementById("setting-protocol").value = "auto";
    document.getElementById("setting-base-url").value = "https://sub2api.example.com";
    document.getElementById("setting-model").value = "gpt-4.1-mini";
    document.getElementById("setting-temperature").value = 0.2;
    document.getElementById("setting-timeout-seconds").value = 60;
    showBanner("已应用 Sub2API 最新兼容预设，请把 Base URL 和 API Key 改成你的实际配置。");
    return;
  }

  document.getElementById("setting-enabled").checked = true;
  document.getElementById("setting-provider-name").value = "OpenAI Compatible";
  document.getElementById("setting-protocol").value = "auto";
  document.getElementById("setting-base-url").value = "https://api.openai.com/v1";
  document.getElementById("setting-model").value = "gpt-4.1-mini";
  document.getElementById("setting-temperature").value = 0.2;
  document.getElementById("setting-timeout-seconds").value = 60;
  showBanner("已恢复 OpenAI 默认预设。");
}

function renderSubjects() {
  const template = document.getElementById("subject-card-template");
  dom.subjectGrid.innerHTML = "";
  dom.subjectSelect.innerHTML = "";
  dom.historyFilter.innerHTML = `<option value="">全部科目</option>`;

  state.subjects.forEach((subject) => {
    const fragment = template.content.cloneNode(true);
    fragment.querySelector("h4").textContent = subject.name;
    fragment.querySelector(".muted").textContent = `${subject.level} · ${subject.completeness}`;
    fragment.querySelector(".pill").textContent = subject.completeness === "broad" ? "重点题库" : "starter bank";
    fragment.querySelector(".subject-desc").textContent = subject.description;
    fragment.querySelector(".subject-count").textContent = `${subject.question_count} 题 · 高频 ${subject.high_frequency_question_count || 0} 题`;
    fragment.querySelector(".subject-action").addEventListener("click", async () => {
      dom.subjectSelect.value = subject.code;
      await loadTopicsForSubject(subject.code);
      setView("exam");
      showBanner(`已切换到 ${subject.name}，可以开始综合模拟、专题冲刺或错题重练。`);
    });
    dom.subjectGrid.appendChild(fragment);

    const option = document.createElement("option");
    option.value = subject.code;
    option.textContent = subject.name;
    dom.subjectSelect.appendChild(option);

    const historyOption = document.createElement("option");
    historyOption.value = subject.code;
    historyOption.textContent = subject.name;
    dom.historyFilter.appendChild(historyOption);
  });

  if (!dom.subjectSelect.value && state.subjects.length) {
    dom.subjectSelect.value = state.subjects[0].code;
  }
}

async function loadTopicsForSubject(subjectCode) {
  if (!subjectCode) {
    dom.topicSelect.innerHTML = `<option value="">综合模拟</option>`;
    return;
  }
  const topics = await request(`/api/topics/${encodeURIComponent(subjectCode)}`);
  dom.topicSelect.innerHTML = `<option value="">综合模拟</option>`;
  topics.forEach((topic) => {
    const option = document.createElement("option");
    option.value = topic;
    option.textContent = topic;
    dom.topicSelect.appendChild(option);
  });
}

function renderHistory() {
  if (!state.history.length) {
    dom.historyList.innerHTML = `<div class="empty-state">暂无历史记录，提交试卷后这里会保留所有考试快照。</div>`;
    return;
  }

  dom.historyList.innerHTML = state.history.map((item) => `
    <article class="history-item ${state.currentHistoryId === item.id ? "active" : ""}" data-id="${item.id}">
      <header>
        <div>
          <h4>${item.subject_name}</h4>
          <p>${item.exam_mode === "ai" ? "AI 生成" : item.exam_mode === "wrong_book" ? "错题重练" : "系统组卷"} · ${formatDate(item.submitted_at)}</p>
        </div>
        <span class="pill">${item.ai_used ? "含 AI 批改" : "题库判卷"}</span>
      </header>
      <p>得分 ${item.obtained_score} / ${item.total_score}，正确率 ${formatRate(item.correct_rate)}</p>
    </article>
  `).join("");

  document.querySelectorAll(".history-item").forEach((node) => {
    node.addEventListener("click", async () => {
      state.currentHistoryId = node.dataset.id;
      renderHistory();
      await loadHistoryDetail(node.dataset.id);
    });
  });
}

async function loadHistoryDetail(attemptId) {
  try {
    const detail = await request(`/api/history/${attemptId}`);
    const modeText = detail.exam_mode === "ai" ? "AI 试卷" : detail.exam_mode === "wrong_book" ? "错题重练卷" : "系统试卷";
    dom.historyDetail.innerHTML = `
      <div class="result-card">
        <h4>${detail.subject_name} · ${detail.title}</h4>
        <p>${formatDate(detail.submitted_at)} · ${modeText}</p>
        <p class="score-badge">${detail.obtained_score} / ${detail.total_score} · 正确率 ${formatRate(detail.correct_rate)}</p>
      </div>
      ${detail.result.question_results.map((item) => `
        <article class="result-card">
          <h4>${item.question_id} · ${item.question_type}</h4>
          <div class="meta-row">
            <span class="pill">${item.obtained_score} / ${item.max_score}</span>
            ${item.topic ? `<span class="pill">${item.topic}</span>` : ""}
            ${item.frequency === "high" ? `<span class="pill">高频考点</span>` : ""}
            <span class="${item.is_correct ? "ok" : "danger"}">${item.is_correct ? "通过" : "待加强"}</span>
          </div>
          <p><strong>作答：</strong>${Array.isArray(item.user_answer) ? item.user_answer.join(", ") : (item.user_answer || "未作答")}</p>
          <p><strong>参考答案：</strong>${Array.isArray(item.expected_answer) ? item.expected_answer.join(", ") : (item.expected_answer ?? "见评分点")}</p>
          <p><strong>题库解析：</strong>${item.analysis}</p>
          ${item.ai_feedback ? `<p><strong>AI 讲评：</strong>${item.ai_feedback.reason}</p>` : ""}
        </article>
      `).join("")}
    `;
  } catch (error) {
    showBanner(error.message, "error");
  }
}

function renderQuestionInput(question) {
  if (question.type === "single_choice") {
    return `
      <div class="option-list">
        ${question.options.map((option) => `
          <label class="option-item">
            <input type="radio" name="${question.id}" value="${option.charAt(0)}" ${state.currentAnswers[question.id] === option.charAt(0) ? "checked" : ""}>
            <span>${option}</span>
          </label>
        `).join("")}
      </div>
    `;
  }

  return `
    <textarea data-answer-input="${question.id}" rows="${question.type === "programming" ? 8 : 5}" placeholder="请输入答案或解题思路">${state.currentAnswers[question.id] || ""}</textarea>
  `;
}

function bindQuestionInputs() {
  document.querySelectorAll("input[type='radio']").forEach((input) => {
    input.addEventListener("change", () => {
      state.currentAnswers[input.name] = input.value;
      persistExam();
    });
  });

  document.querySelectorAll("textarea[data-answer-input]").forEach((textarea) => {
    textarea.addEventListener("input", () => {
      state.currentAnswers[textarea.dataset.answerInput] = textarea.value;
      persistExam();
    });
  });
}

function renderExam() {
  if (!state.currentExam) {
    dom.examContainer.className = "exam-container empty-state";
    dom.examContainer.textContent = "请选择科目并生成试卷。";
    dom.examMeta.textContent = "";
    dom.submitExamBtn.disabled = true;
    updateTimer();
    return;
  }

  const blueprint = state.currentExam.blueprint;
  const sourceText = state.currentExam.source === "ai"
    ? "AI 生成"
    : state.currentExam.source === "wrong_book"
      ? "错题重练"
      : "系统组卷";
  const focusText = state.currentExam.focus_topic
    ? ` · 专题 ${state.currentExam.focus_topic}`
    : (state.currentExam.prioritized_topics?.length ? ` · 弱项 ${state.currentExam.prioritized_topics.join(" / ")}` : "");
  dom.examMeta.textContent = `${state.currentExam.subject_name} · ${sourceText}${focusText} · ${blueprint.duration_minutes} 分钟 · 总分 ${state.currentExam.total_score} · 高频题 ${state.currentExam.high_frequency_count || 0}`;
  dom.submitExamBtn.disabled = false;
  dom.examContainer.className = "exam-container";
  dom.examContainer.innerHTML = state.currentExam.questions.map((question, index) => `
    <article class="question-card" data-question-id="${question.id}">
      <h4>${index + 1}. ${question.stem}</h4>
      <div class="meta-row">
        <span class="pill">${question.type}</span>
        <span class="pill">${question.score} 分</span>
        ${question.topic ? `<span class="pill">${question.topic}</span>` : ""}
        ${question.frequency === "high" ? `<span class="pill">高频考点</span>` : ""}
      </div>
      ${renderQuestionInput(question)}
    </article>
  `).join("");
  bindQuestionInputs();
  updateTimer();
}

function renderResult() {
  if (!state.currentResult) {
    dom.resultContainer.className = "result-container empty-state";
    dom.resultContainer.textContent = "交卷后这里会展示总分、分题得分和错因分析。";
    return;
  }
  const summary = state.currentResult.summary;
  dom.resultContainer.className = "result-container";
  dom.resultContainer.innerHTML = `
    <article class="result-card">
      <h4>总评</h4>
      <div class="meta-row">
        <span class="pill">得分 ${summary.obtained_score} / ${summary.total_score}</span>
        <span class="pill">正确率 ${formatRate(summary.correct_rate)}</span>
        <span class="pill">答对 ${summary.correct_count} / ${summary.question_count}</span>
      </div>
      <p>本次考试已经存档，可以在“成绩记录”中复盘，也可以继续错题重练。</p>
    </article>
    ${state.currentResult.question_results.map((item) => `
      <article class="result-card">
        <h4>${item.question_id}</h4>
        <div class="meta-row">
          <span class="pill">${item.question_type}</span>
          <span class="pill">${item.obtained_score} / ${item.max_score}</span>
          ${item.topic ? `<span class="pill">${item.topic}</span>` : ""}
          ${item.frequency === "high" ? `<span class="pill">高频考点</span>` : ""}
          <span class="${item.is_correct ? "ok" : "danger"}">${item.is_correct ? "正确或基本正确" : "需要加强"}</span>
        </div>
        <p><strong>作答：</strong>${Array.isArray(item.user_answer) ? item.user_answer.join(", ") : (item.user_answer || "未作答")}</p>
        <p><strong>参考答案：</strong>${Array.isArray(item.expected_answer) ? item.expected_answer.join(", ") : (item.expected_answer ?? "见评分点")}</p>
        <p><strong>题库解析：</strong>${item.analysis}</p>
        ${item.ai_feedback ? `
          <p><strong>AI 评分：</strong>${item.ai_feedback.score} 分</p>
          <p><strong>AI 原因：</strong>${item.ai_feedback.reason}</p>
          <p><strong>AI 建议：</strong>${(item.ai_feedback.improvement_suggestions || []).join("；") || "无"}</p>
        ` : ""}
      </article>
    `).join("")}
  `;
}

function updateTimer() {
  if (timerHandle) {
    window.clearInterval(timerHandle);
  }
  if (!state.currentExam) {
    dom.examTimer.textContent = "未开始";
    return;
  }
  const endTime = new Date(state.currentExam.started_at).getTime() + state.currentExam.blueprint.duration_minutes * 60 * 1000;
  const tick = () => {
    const remaining = endTime - Date.now();
    if (remaining <= 0) {
      dom.examTimer.textContent = "建议时间已到";
      return;
    }
    const totalSeconds = Math.floor(remaining / 1000);
    const hours = String(Math.floor(totalSeconds / 3600)).padStart(2, "0");
    const minutes = String(Math.floor((totalSeconds % 3600) / 60)).padStart(2, "0");
    const seconds = String(totalSeconds % 60).padStart(2, "0");
    dom.examTimer.textContent = `剩余建议时间 ${hours}:${minutes}:${seconds}`;
  };
  tick();
  timerHandle = window.setInterval(tick, 1000);
}

async function loadDashboard() {
  state.dashboard = await request("/api/dashboard");
  renderStats();
  renderLatestAttempts();
  renderWeakTopics();
  renderWrongBookPreview();
  renderTopicMastery();
  renderStudyRecommendations();
}

async function loadResources() {
  state.resources = await request("/api/resources");
  renderResources();
}

async function loadSettings() {
  state.settings = await request("/api/settings");
  populateSettings();
}

async function loadHistory() {
  const subjectCode = dom.historyFilter.value || "";
  const query = subjectCode ? `?subject_code=${encodeURIComponent(subjectCode)}` : "";
  state.history = await request(`/api/history${query}`);
  renderHistory();
}

async function bootstrap() {
  clearBanner();
  restoreExam();
  try {
    state.subjects = await request("/api/subjects");
    renderSubjects();
    await loadTopicsForSubject(dom.subjectSelect.value);
    await Promise.all([loadDashboard(), loadResources(), loadSettings(), loadHistory()]);
    renderExam();
    renderResult();
  } catch (error) {
    showBanner(error.message, "error");
  }
}

async function generateExam(mode) {
  try {
    clearBanner();
    const subjectCode = dom.subjectSelect.value;
    if (!subjectCode) {
      showBanner("请先选择科目。", "error");
      return;
    }
    const payload = { subject_code: subjectCode };
    if (dom.seedInput.value) {
      payload.seed = Number(dom.seedInput.value);
    }
    if (mode === "system") {
      if (dom.topicSelect.value) {
        payload.focus_topic = dom.topicSelect.value;
      }
      payload.weakness_boost = dom.weaknessBoostInput.checked;
    }
    const endpoint = mode === "system"
      ? "/api/exams/system"
      : mode === "wrong_book"
        ? "/api/exams/wrong-book"
        : "/api/exams/ai";
    const exam = await request(endpoint, {
      method: "POST",
      body: JSON.stringify(payload),
    });
    state.currentExam = exam;
    state.currentAnswers = {};
    state.currentResult = null;
    persistExam();
    renderExam();
    renderResult();
    setView("exam");
    showBanner(`${exam.title} 已生成，可以开始作答。`);
  } catch (error) {
    showBanner(error.message, "error");
  }
}

async function submitExam() {
  if (!state.currentExam) return;
  const unanswered = state.currentExam.questions.filter((question) => !state.currentAnswers[question.id]);
  if (unanswered.length && !window.confirm(`仍有 ${unanswered.length} 题未作答，确认提交吗？`)) {
    return;
  }
  try {
    const payload = await request("/api/exams/submit", {
      method: "POST",
      body: JSON.stringify({
        exam: state.currentExam,
        answers: state.currentAnswers,
        started_at: state.currentExam.started_at,
      }),
    });
    state.currentResult = payload.result;
    persistExam();
    renderResult();
    await loadDashboard();
    await loadHistory();
    showBanner(`交卷完成，成绩记录 ${payload.attempt_id} 已保存。`);
  } catch (error) {
    showBanner(error.message, "error");
  }
}

function readSettingsForm() {
  return {
    enabled: document.getElementById("setting-enabled").checked,
    provider_name: document.getElementById("setting-provider-name").value.trim(),
    protocol: document.getElementById("setting-protocol").value,
    base_url: document.getElementById("setting-base-url").value.trim(),
    api_key: document.getElementById("setting-api-key").value.trim(),
    model: document.getElementById("setting-model").value.trim(),
    temperature: Number(document.getElementById("setting-temperature").value || 0.2),
    timeout_seconds: Number(document.getElementById("setting-timeout-seconds").value || 60),
    organization: document.getElementById("setting-organization").value.trim(),
    project: document.getElementById("setting-project").value.trim(),
    extra_headers: document.getElementById("setting-extra-headers").value,
    grading_mode: document.getElementById("setting-grading-mode").value,
    enable_ai_review: document.getElementById("setting-enable-ai-review").checked,
  };
}

document.querySelectorAll(".nav-link").forEach((button) => {
  button.addEventListener("click", () => setView(button.dataset.view));
});

document.getElementById("reload-btn").addEventListener("click", bootstrap);
document.getElementById("history-refresh-btn").addEventListener("click", loadHistory);
document.getElementById("generate-system-btn").addEventListener("click", () => generateExam("system"));
document.getElementById("generate-wrong-book-btn").addEventListener("click", () => generateExam("wrong_book"));
document.getElementById("generate-ai-btn").addEventListener("click", () => generateExam("ai"));
document.getElementById("quick-generate-btn").addEventListener("click", async () => {
  dom.subjectSelect.value = "level2_c";
  dom.weaknessBoostInput.checked = false;
  await loadTopicsForSubject("level2_c");
  await generateExam("system");
});
dom.subjectSelect.addEventListener("change", async () => {
  await loadTopicsForSubject(dom.subjectSelect.value);
});
dom.submitExamBtn.addEventListener("click", submitExam);
dom.historyFilter.addEventListener("change", loadHistory);
dom.presetOpenAIButton.addEventListener("click", () => applyProviderPreset("openai"));
dom.presetSub2APIButton.addEventListener("click", () => applyProviderPreset("sub2api"));

document.getElementById("settings-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  try {
    state.settings = await request("/api/settings", {
      method: "PUT",
      body: JSON.stringify(readSettingsForm()),
    });
    populateSettings();
    showBanner("AI 设置已保存。");
  } catch (error) {
    showBanner(error.message, "error");
  }
});

dom.testConnectionButton.addEventListener("click", async () => {
  try {
    const result = await request("/api/settings/test", {
      method: "POST",
      body: JSON.stringify(readSettingsForm()),
    });
    showBanner(`连接测试成功：${result.provider_name} / ${result.model} / ${result.protocol}`);
  } catch (error) {
    showBanner(error.message, "error");
  }
});

document.getElementById("open-openai-console-btn").addEventListener("click", () => {
  const url = state.settings?.openai_console_url || "https://platform.openai.com/settings/organization/api-keys";
  window.open(url, "_blank", "noopener,noreferrer");
});

bootstrap();
