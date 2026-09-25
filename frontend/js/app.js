/**
 * app.js - Full-Stack Client Application Logic
 * Powers navigation, CRUD operations, live NLP predictions, and data bindings.
 */

// Application State
const AppState = {
    currentTab: 'overview',
    theme: localStorage.getItem('capstron_theme') || 'dark',
    overviewData: null,
    aspectsData: null,
    driftData: null,
    feedbackFilters: {
        page: 1,
        page_size: 10,
        course: 'All',
        semester: 'All',
        language: 'All',
        sentiment: 'All',
        aspect: 'All',
        search: ''
    },
    newFeedbackRating: 5
};

// ==========================================================================
// Initialization & Navigation
// ==========================================================================
document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    setupEventListeners();
    setupNavigation();
    setupRatingPicker();
    setupLiveSandbox();

    // Initial Data Load
    loadOverview();
});

function initTheme() {
    document.documentElement.setAttribute('data-theme', AppState.theme);
    updateThemeIcon();
}

function toggleTheme() {
    AppState.theme = AppState.theme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', AppState.theme);
    localStorage.setItem('capstron_theme', AppState.theme);
    updateThemeIcon();
    ChartManager.refreshAllOnThemeChange();
}

function updateThemeIcon() {
    const icon = document.getElementById('theme-toggle-icon');
    if (icon) {
        icon.className = AppState.theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    }
}

function setupNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const tabTarget = item.getAttribute('data-tab');
            switchTab(tabTarget);
        });
    });
}

function switchTab(tabId) {
    AppState.currentTab = tabId;

    // Update Sidebar Navigation state
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.toggle('active', item.getAttribute('data-tab') === tabId);
    });

    // Update View Containers
    document.querySelectorAll('.tab-pane').forEach(pane => {
        pane.classList.remove('active');
    });
    const targetPane = document.getElementById(`tab-${tabId}`);
    if (targetPane) {
        targetPane.classList.add('active');
    }

    // Update Top Header Titles
    const titleMap = {
        'overview': { title: 'Executive Intelligence Overview', subtitle: 'Institutional metrics, sentiment distributions & automated AI insights' },
        'aspects': { title: '12-Aspect Sentiment Breakdown', subtitle: 'Granular pedagogical & infrastructure sentiment analytics' },
        'drift': { title: 'Temporal Topic Drift & Trends', subtitle: 'Tracking evolving curriculum concerns across 6 academic semesters' },
        'feedback': { title: 'Student Feedback Management', subtitle: 'Interactive CRUD database explorer with real-time NLP classification' },
        'sandbox': { title: 'Interactive AI Sandbox Playground', subtitle: 'Test live multilingual NLP inference on any Hindi, Hinglish, or English sentence' },
        'viva': { title: 'Viva Documentation & Architecture', subtitle: 'Complete capstone project documentation, viva questions & technical specs' }
    };

    if (titleMap[tabId]) {
        document.getElementById('header-title').textContent = titleMap[tabId].title;
        document.getElementById('header-subtitle').textContent = titleMap[tabId].subtitle;
    }

    // Load data for specific tab if needed
    if (tabId === 'overview' && !AppState.overviewData) loadOverview();
    if (tabId === 'aspects') loadAspects();
    if (tabId === 'drift') loadDrift();
    if (tabId === 'feedback') loadFeedback();
}

// ==========================================================================
// API Handlers & Data Loaders
// ==========================================================================

// 1. Load Overview Dashboard
async function loadOverview() {
    try {
        const res = await fetch('/api/overview');
        if (!res.ok) throw new Error('Failed to load overview data');
        const data = await res.json();
        AppState.overviewData = data;

        // Render KPI Cards
        document.getElementById('kpi-total-feedback').textContent = data.kpis.total_feedback.toLocaleString();
        document.getElementById('kpi-avg-rating').textContent = `${data.kpis.avg_rating} / 5.0`;
        document.getElementById('kpi-positive-pct').textContent = `${data.kpis.positive_pct}%`;
        document.getElementById('kpi-negative-pct').textContent = `${data.kpis.negative_pct}%`;
        document.getElementById('kpi-active-courses').textContent = data.kpis.active_courses;

        // Render AI Insights
        renderAIInsights(data.insights);

        // Render Charts
        ChartManager.renderSentimentDonut('chart-sentiment', data.sentiment_distribution);
        ChartManager.renderLanguageDonut('chart-language', data.language_distribution);
        ChartManager.renderRatingBar('chart-ratings', data.rating_distribution);
        ChartManager.renderCourseLeaderboard('chart-leaderboard', data.courses_leaderboard);

        // Render Leaderboard Table
        renderLeaderboardTable(data.courses_leaderboard);

    } catch (err) {
        console.error(err);
        showToast('Error loading overview data: ' + err.message, 'error');
    }
}

function renderAIInsights(insights) {
    const container = document.getElementById('insights-container');
    if (!container) return;

    container.innerHTML = '';

    if (Array.isArray(insights) && insights.length > 0) {
        insights.forEach(item => {
            let icon = 'fas fa-info-circle';
            let color = 'var(--primary)';

            const cat = (item.category || '').toLowerCase();
            if (item.type === 'positive' || cat.includes('strength') || cat.includes('asset') || cat.includes('driver')) {
                icon = 'fas fa-thumbs-up';
                color = 'var(--color-positive)';
            } else if (item.type === 'warning' || cat.includes('pain') || cat.includes('dissatisfaction')) {
                icon = 'fas fa-exclamation-triangle';
                color = 'var(--color-negative)';
            } else if (item.type === 'trend' || cat.includes('drift')) {
                icon = 'fas fa-arrow-trend-up';
                color = 'var(--color-neutral)';
            } else if (cat.includes('course')) {
                icon = 'fas fa-trophy';
                color = 'var(--secondary)';
            } else if (cat.includes('multilingual')) {
                icon = 'fas fa-language';
                color = 'var(--accent-purple)';
            }

            const div = document.createElement('div');
            div.className = 'insight-item';
            div.innerHTML = `
                <div class="insight-icon" style="color: ${color}"><i class="${icon}"></i></div>
                <div class="insight-content">
                    <h4>${escapeHtml(item.category || 'Institutional Insight')}</h4>
                    <p>${escapeHtml(item.text || '')}</p>
                </div>
            `;
            container.appendChild(div);
        });
        return;
    }

    const items = [
        {
            icon: 'fas fa-trophy',
            color: 'var(--color-positive)',
            title: 'Top Pedagogical Strength',
            desc: 'Practical Sessions and Exams lead institutional positive sentiment.'
        },
        {
            icon: 'fas fa-exclamation-triangle',
            color: 'var(--color-negative)',
            title: 'Priority Pain Point',
            desc: 'Study Material and evaluation pace require departmental review.'
        }
    ];

    items.forEach(item => {
        const div = document.createElement('div');
        div.className = 'insight-item';
        div.innerHTML = `
            <div class="insight-icon" style="color: ${item.color}"><i class="${item.icon}"></i></div>
            <div class="insight-content">
                <h4>${item.title}</h4>
                <p>${item.desc}</p>
            </div>
        `;
        container.appendChild(div);
    });
}

function renderLeaderboardTable(courses) {
    const tbody = document.getElementById('leaderboard-tbody');
    if (!tbody) return;

    tbody.innerHTML = courses.slice(0, 5).map(c => `
        <tr>
            <td><strong>${c.course_id}</strong></td>
            <td>${c.course_name}</td>
            <td><span class="badge badge-lang">${c.total} reviews</span></td>
            <td><span class="rating-stars">★</span> <strong>${c.avg_rating}</strong></td>
            <td>
                <span class="badge badge-positive">${c.pos_rate}% Pos</span>
                <span class="badge badge-negative">${c.neg_rate}% Neg</span>
            </td>
        </tr>
    `).join('');
}

// 2. Load 12-Aspect Analysis
async function loadAspects() {
    try {
        const res = await fetch('/api/aspects');
        if (!res.ok) throw new Error('Failed to load aspect data');
        const data = await res.json();
        AppState.aspectsData = data;

        ChartManager.renderAspectsBar('chart-aspects-bar', data.aspects_summary);

        // Render Strengths & Pain Points
        const strengthsList = document.getElementById('aspects-strengths-list');
        if (strengthsList) {
            strengthsList.innerHTML = data.strengths.map(s => `
                <div class="insight-item" style="border-left: 4px solid var(--color-positive);">
                    <div class="insight-content" style="width: 100%;">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <strong>${s.aspect}</strong>
                            <span class="badge badge-positive">+${s.net_score}% Net</span>
                        </div>
                        <p style="margin-top: 4px; font-size: 0.8rem;">
                            ${s.positive} Positive (${s.pos_rate}%) • ${s.negative} Negative (${s.neg_rate}%)
                        </p>
                    </div>
                </div>
            `).join('');
        }

        const painList = document.getElementById('aspects-pain-list');
        if (painList) {
            painList.innerHTML = data.pain_points.map(p => `
                <div class="insight-item" style="border-left: 4px solid var(--color-negative);">
                    <div class="insight-content" style="width: 100%;">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <strong>${p.aspect}</strong>
                            <span class="badge badge-negative">${p.neg_rate}% Neg</span>
                        </div>
                        <p style="margin-top: 4px; font-size: 0.8rem;">
                            ${p.negative} Complaints • Total mentions: ${p.total}
                        </p>
                    </div>
                </div>
            `).join('');
        }

        // Render Aspect Heatmap Table
        renderAspectHeatmapTable(data.heatmap);

    } catch (err) {
        console.error(err);
        showToast('Error loading aspect data: ' + err.message, 'error');
    }
}

function renderAspectHeatmapTable(heatmap) {
    const tableHead = document.getElementById('heatmap-thead');
    const tableBody = document.getElementById('heatmap-tbody');
    if (!tableHead || !tableBody || !heatmap.courses) return;

    tableHead.innerHTML = `
        <tr>
            <th>Course Name</th>
            ${heatmap.aspects.map(a => `<th>${a}</th>`).join('')}
        </tr>
    `;

    tableBody.innerHTML = heatmap.courses.map((course, rowIdx) => {
        const scores = heatmap.matrix[rowIdx];
        return `
            <tr>
                <td><strong>${course}</strong></td>
                ${scores.map(val => {
                    let bg = 'rgba(245, 158, 11, 0.15)'; // Neutral
                    let color = '#f59e0b';
                    if (val > 20) {
                        bg = 'rgba(16, 185, 129, 0.2)';
                        color = '#10b981';
                    } else if (val < -10) {
                        bg = 'rgba(239, 68, 68, 0.2)';
                        color = '#ef4444';
                    }
                    return `<td style="background-color: ${bg}; color: ${color}; font-weight: 700; text-align: center;">${val > 0 ? '+' : ''}${val}%</td>`;
                }).join('')}
            </tr>
        `;
    }).join('');
}

// 3. Load Topic Drift Analytics
async function loadDrift() {
    try {
        const res = await fetch('/api/drift');
        if (!res.ok) throw new Error('Failed to load drift data');
        const data = await res.json();
        AppState.driftData = data;

        ChartManager.renderTopicDriftChart('chart-drift-timeline', data.semesters, data.chart_series);

        // Render Classifications Table
        const tbody = document.getElementById('drift-tbody');
        if (tbody) {
            tbody.innerHTML = data.classifications.map(t => {
                let badgeClass = 'badge-neutral';
                let icon = 'fas fa-minus';
                if (t.status === 'Emerging') { badgeClass = 'badge-negative'; icon = 'fas fa-arrow-trend-up'; }
                if (t.status === 'Declining') { badgeClass = 'badge-positive'; icon = 'fas fa-arrow-trend-down'; }
                if (t.status === 'New') { badgeClass = 'badge-aspect'; icon = 'fas fa-star'; }

                return `
                    <tr>
                        <td><strong>${t.topic_name}</strong></td>
                        <td><span class="badge ${badgeClass}"><i class="${icon}"></i> ${t.status}</span></td>
                        <td>${(t.slope * 100).toFixed(2)}% / sem</td>
                        <td>${(t.first_sem_pct * 100).toFixed(1)}%</td>
                        <td>${(t.last_sem_pct * 100).toFixed(1)}%</td>
                        <td><strong>${(t.net_change_pct * 100).toFixed(1)}%</strong></td>
                    </tr>
                `;
            }).join('');
        }

    } catch (err) {
        console.error(err);
        showToast('Error loading topic drift data: ' + err.message, 'error');
    }
}

// 4. Load Feedback Records (Filterable & Paginated)
async function loadFeedback() {
    try {
        const f = AppState.feedbackFilters;
        const queryParams = new URLSearchParams({
            page: f.page,
            page_size: f.page_size,
            course: f.course,
            semester: f.semester,
            language: f.language,
            sentiment: f.sentiment,
            aspect: f.aspect,
            search: f.search
        });

        const res = await fetch(`/api/feedback?${queryParams.toString()}`);
        if (!res.ok) throw new Error('Failed to fetch feedback records');
        const data = await res.json();

        // Update count
        document.getElementById('feedback-total-count').textContent = `${data.total_count} records found`;
        document.getElementById('feedback-page-info').textContent = `Page ${data.page} of ${data.total_pages}`;

        // Disable/enable pagination buttons
        document.getElementById('btn-prev-page').disabled = (data.page <= 1);
        document.getElementById('btn-next-page').disabled = (data.page >= data.total_pages);

        // Render Table Rows
        const tbody = document.getElementById('feedback-tbody');
        if (!tbody) return;

        if (data.records.length === 0) {
            tbody.innerHTML = `<tr><td colspan="7" style="text-align: center; padding: 40px; color: var(--text-muted);">No feedback records found matching your filters.</td></tr>`;
            return;
        }

        tbody.innerHTML = data.records.map(r => {
            const sentClass = r.overall_sentiment === 'Positive' ? 'badge-positive' : (r.overall_sentiment === 'Negative' ? 'badge-negative' : 'badge-neutral');
            const aspectsHtml = (r.aspects || []).map(a => `<span class="badge badge-aspect" title="${a.evidence_snippet || ''}">${a.aspect} (${a.sentiment[0]})</span>`).join(' ') || '<span style="color:var(--text-muted); font-size:0.75rem;">None</span>';
            const stars = '★'.repeat(r.rating) + '☆'.repeat(5 - r.rating);

            return `
                <tr>
                    <td><strong>${r.feedback_id}</strong><br><small style="color:var(--text-muted);">${r.student_id}</small></td>
                    <td>
                        <strong>${r.course_name}</strong><br>
                        <small style="color:var(--text-muted);">${r.semester} • ${r.date}</small>
                    </td>
                    <td>
                        <span class="badge ${sentClass}">${r.overall_sentiment}</span>
                        <div style="font-size:0.72rem; color:var(--text-muted); margin-top:2px;">${(r.sentiment_confidence * 100).toFixed(0)}% conf</div>
                    </td>
                    <td><span class="badge badge-lang">${r.language}</span></td>
                    <td><span class="rating-stars" style="letter-spacing:1px;">${stars}</span></td>
                    <td style="max-width: 320px;">
                        <div style="margin-bottom:6px; font-size:0.86rem; color:var(--text-primary);">${escapeHtml(r.feedback_text)}</div>
                        <div>${aspectsHtml}</div>
                    </td>
                    <td>
                        <button class="btn-icon" style="color:var(--color-negative); width:32px; height:32px;" onclick="deleteFeedbackRecord('${r.feedback_id}')" title="Delete Feedback">
                            <i class="fas fa-trash-alt"></i>
                        </button>
                    </td>
                </tr>
            `;
        }).join('');

    } catch (err) {
        console.error(err);
        showToast('Error loading feedback: ' + err.message, 'error');
    }
}

// Delete feedback record
async function deleteFeedbackRecord(feedbackId) {
    if (!confirm(`Are you sure you want to delete feedback ${feedbackId}? This will remove it from the database.`)) {
        return;
    }

    try {
        const res = await fetch(`/api/feedback/${feedbackId}`, { method: 'DELETE' });
        if (!res.ok) throw new Error('Delete request failed');
        const data = await res.json();

        showToast(data.message, 'success');
        loadFeedback();
        // Also refresh overview numbers
        loadOverview();
    } catch (err) {
        showToast('Error deleting record: ' + err.message, 'error');
    }
}

// ==========================================================================
// Add Feedback Modal & CRUD Submission
// ==========================================================================
function setupRatingPicker() {
    const stars = document.querySelectorAll('#star-picker i');
    stars.forEach(star => {
        star.addEventListener('click', () => {
            const val = parseInt(star.getAttribute('data-value'));
            AppState.newFeedbackRating = val;
            stars.forEach(s => {
                const sVal = parseInt(s.getAttribute('data-value'));
                s.classList.toggle('active', sVal <= val);
            });
        });
    });
}

function openAddModal() {
    document.getElementById('add-feedback-modal').classList.add('active');
}

function closeAddModal() {
    document.getElementById('add-feedback-modal').classList.remove('active');
    document.getElementById('add-feedback-form').reset();
    AppState.newFeedbackRating = 5;
    document.querySelectorAll('#star-picker i').forEach(s => s.classList.add('active'));
}

async function handleAddFeedbackSubmit(e) {
    e.preventDefault();
    const courseSelect = document.getElementById('new-course-select');
    const courseId = courseSelect.value;
    const courseName = courseSelect.options[courseSelect.selectedIndex].text;
    const semester = document.getElementById('new-semester-select').value;
    const feedbackText = document.getElementById('new-feedback-text').value.trim();

    if (!feedbackText) {
        showToast('Please provide feedback comments.', 'error');
        return;
    }

    const submitBtn = document.getElementById('btn-submit-feedback');
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Running Real-Time NLP...';

    try {
        const payload = {
            course_id: courseId,
            course_name: courseName,
            semester: semester,
            rating: AppState.newFeedbackRating,
            feedback_text: feedbackText
        };

        const res = await fetch('/api/feedback', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail || 'Failed to submit feedback');
        }

        const data = await res.json();
        showToast(`Feedback saved! Detected ${data.record.language} with ${data.record.overall_sentiment} sentiment.`, 'success');

        closeAddModal();
        // Refresh both feedback list and dashboard metrics
        loadFeedback();
        loadOverview();

    } catch (err) {
        showToast(err.message, 'error');
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="fas fa-check"></i> Analyze & Save Feedback';
    }
}

// ==========================================================================
// Interactive Live AI Sandbox Playground
// ==========================================================================
function setupLiveSandbox() {
    // Preset buttons
    const presets = [
        "Ye course bohot bekaar tha, professor kabhi time pe nahi aate aur assignments bohot tough the.",
        "The lectures were exceptional and assignments were highly practical. Loved this course!",
        "Teacher ne topics acche se explain kiye lekin grading system bahut strict aur unfair tha.",
        "Syllabus is modern and curriculum is comprehensive, but the lab equipment needs urgent upgrade."
    ];

    const presetChips = document.querySelectorAll('.preset-chip');
    presetChips.forEach((chip, idx) => {
        chip.addEventListener('click', () => {
            document.getElementById('sandbox-input-text').value = presets[idx] || '';
            runLiveSandbox();
        });
    });
}

async function runLiveSandbox() {
    const text = document.getElementById('sandbox-input-text').value.trim();
    if (!text) {
        showToast('Please enter text to analyze in the sandbox.', 'info');
        return;
    }

    const btn = document.getElementById('btn-run-sandbox');
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Running Full NLP Pipeline...';

    try {
        const res = await fetch('/api/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: text })
        });

        if (!res.ok) throw new Error('Live prediction failed');
        const data = await res.json();

        // 1. Language Step
        document.getElementById('sandbox-lang-badge').textContent = `${data.language.language} (${data.language.script})`;
        document.getElementById('sandbox-lang-conf').textContent = `${(data.language.confidence * 100).toFixed(0)}%`;
        document.getElementById('sandbox-lang-fill').style.width = `${data.language.confidence * 100}%`;

        // 2. Translation Step
        document.getElementById('sandbox-translation-text').textContent = data.pipeline_a_translation || data.input_text;

        // 3. Sentiment Step
        const sentBadge = document.getElementById('sandbox-sent-badge');
        sentBadge.textContent = data.sentiment.sentiment;
        sentBadge.className = `badge ${data.sentiment.sentiment === 'Positive' ? 'badge-positive' : (data.sentiment.sentiment === 'Negative' ? 'badge-negative' : 'badge-neutral')}`;
        document.getElementById('sandbox-sent-conf').textContent = `${(data.sentiment.confidence * 100).toFixed(0)}%`;
        document.getElementById('sandbox-sent-fill').style.width = `${data.sentiment.confidence * 100}%`;

        // 4. Aspects Step
        const aspectsContainer = document.getElementById('sandbox-aspects-list');
        if (data.aspects.length === 0) {
            aspectsContainer.innerHTML = '<div style="color:var(--text-muted); font-size:0.85rem;">No explicit pedagogical aspects detected in this sentence.</div>';
        } else {
            aspectsContainer.innerHTML = data.aspects.map(asp => `
                <div style="background:var(--bg-card); border:1px solid var(--border-color); border-radius:var(--radius-sm); padding:10px 14px; margin-bottom:8px;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <strong>${asp.aspect}</strong>
                        <span class="badge ${asp.sentiment === 'Positive' ? 'badge-positive' : (asp.sentiment === 'Negative' ? 'badge-negative' : 'badge-neutral')}">${asp.sentiment}</span>
                    </div>
                    <div style="font-size:0.78rem; color:var(--text-muted); margin-top:4px;">
                        <em>"${asp.evidence_snippet}"</em> (${(asp.confidence * 100).toFixed(0)}% conf)
                    </div>
                </div>
            `).join('');
        }

        document.getElementById('sandbox-result-card').style.display = 'block';

    } catch (err) {
        showToast('Inference error: ' + err.message, 'error');
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-bolt"></i> Analyze Multilingual Feedback';
    }
}

// ==========================================================================
// UI Helpers & Event Listeners
// ==========================================================
function setupEventListeners() {
    // Theme Switch
    const themeBtn = document.getElementById('btn-toggle-theme');
    if (themeBtn) themeBtn.addEventListener('click', toggleTheme);

    // Modal Trigger
    const openModalBtn = document.getElementById('btn-open-add-modal');
    if (openModalBtn) openModalBtn.addEventListener('click', openAddModal);

    const closeModalBtn = document.getElementById('btn-close-modal');
    if (closeModalBtn) closeModalBtn.addEventListener('click', closeAddModal);

    const cancelModalBtn = document.getElementById('btn-cancel-modal');
    if (cancelModalBtn) cancelModalBtn.addEventListener('click', closeAddModal);

    // Add Form Submit
    const addForm = document.getElementById('add-feedback-form');
    if (addForm) addForm.addEventListener('submit', handleAddFeedbackSubmit);

    // Live Sandbox Button
    const sandboxBtn = document.getElementById('btn-run-sandbox');
    if (sandboxBtn) sandboxBtn.addEventListener('click', runLiveSandbox);

    // Feedback Search & Filters
    const searchInput = document.getElementById('filter-search');
    let debounceTimer;
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                AppState.feedbackFilters.search = e.target.value;
                AppState.feedbackFilters.page = 1;
                loadFeedback();
            }, 300);
        });
    }

    const filterCourse = document.getElementById('filter-course');
    if (filterCourse) {
        filterCourse.addEventListener('change', (e) => {
            AppState.feedbackFilters.course = e.target.value;
            AppState.feedbackFilters.page = 1;
            loadFeedback();
        });
    }

    const filterSem = document.getElementById('filter-semester');
    if (filterSem) {
        filterSem.addEventListener('change', (e) => {
            AppState.feedbackFilters.semester = e.target.value;
            AppState.feedbackFilters.page = 1;
            loadFeedback();
        });
    }

    const filterLang = document.getElementById('filter-language');
    if (filterLang) {
        filterLang.addEventListener('change', (e) => {
            AppState.feedbackFilters.language = e.target.value;
            AppState.feedbackFilters.page = 1;
            loadFeedback();
        });
    }

    const filterSent = document.getElementById('filter-sentiment');
    if (filterSent) {
        filterSent.addEventListener('change', (e) => {
            AppState.feedbackFilters.sentiment = e.target.value;
            AppState.feedbackFilters.page = 1;
            loadFeedback();
        });
    }

    // Pagination buttons
    const prevBtn = document.getElementById('btn-prev-page');
    if (prevBtn) {
        prevBtn.addEventListener('click', () => {
            if (AppState.feedbackFilters.page > 1) {
                AppState.feedbackFilters.page--;
                loadFeedback();
            }
        });
    }

    const nextBtn = document.getElementById('btn-next-page');
    if (nextBtn) {
        nextBtn.addEventListener('click', () => {
            AppState.feedbackFilters.page++;
            loadFeedback();
        });
    }
}

// Toast System
function showToast(message, type = 'info') {
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    const icon = type === 'success' ? 'fa-check-circle' : (type === 'error' ? 'fa-exclamation-circle' : 'fa-info-circle');
    toast.innerHTML = `<i class="fas ${icon}"></i> <span>${escapeHtml(message)}</span>`;

    container.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(50px)';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

function escapeHtml(str) {
    if (!str) return '';
    return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}
