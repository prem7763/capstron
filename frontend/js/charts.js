/**
 * charts.js - Chart.js Visualizations Manager
 * Handles responsive, theme-adaptive charts with custom gradients & tooltips.
 */

const ChartManager = {
    instances: {},

    // Returns theme-aware styling colors
    getThemeColors() {
        const isLight = document.documentElement.getAttribute('data-theme') === 'light';
        return {
            textColor: isLight ? '#475569' : '#94a3b8',
            gridColor: isLight ? 'rgba(0, 0, 0, 0.06)' : 'rgba(255, 255, 255, 0.06)',
            tooltipBg: isLight ? 'rgba(255, 255, 255, 0.95)' : 'rgba(17, 24, 39, 0.95)',
            tooltipText: isLight ? '#0f172a' : '#f8fafc',
            borderColor: isLight ? '#cbd5e1' : '#334155'
        };
    },

    // Destroy existing chart instance to prevent canvas reuse errors
    destroyChart(canvasId) {
        if (this.instances[canvasId]) {
            this.instances[canvasId].destroy();
            delete this.instances[canvasId];
        }
    },

    // 1. Sentiment Donut Chart
    renderSentimentDonut(canvasId, sentimentData) {
        this.destroyChart(canvasId);
        const ctx = document.getElementById(canvasId);
        if (!ctx) return;

        const theme = this.getThemeColors();
        const labels = ['Positive', 'Negative', 'Neutral'];
        const dataValues = [
            sentimentData.Positive || 0,
            sentimentData.Negative || 0,
            sentimentData.Neutral || 0
        ];

        this.instances[canvasId] = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: dataValues,
                    backgroundColor: [
                        '#10b981', // Positive Emerald
                        '#ef4444', // Negative Crimson
                        '#f59e0b'  // Neutral Amber
                    ],
                    borderWidth: 2,
                    borderColor: theme.borderColor,
                    hoverOffset: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '72%',
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: theme.textColor,
                            font: { family: 'Plus Jakarta Sans', weight: '600', size: 12 },
                            padding: 16,
                            usePointStyle: true,
                            pointStyle: 'circle'
                        }
                    },
                    tooltip: {
                        backgroundColor: theme.tooltipBg,
                        titleColor: theme.tooltipText,
                        bodyColor: theme.tooltipText,
                        borderColor: theme.borderColor,
                        borderWidth: 1,
                        padding: 12,
                        cornerRadius: 8
                    }
                }
            }
        });
    },

    // 2. Language Distribution Donut Chart
    renderLanguageDonut(canvasId, langData) {
        this.destroyChart(canvasId);
        const ctx = document.getElementById(canvasId);
        if (!ctx) return;

        const theme = this.getThemeColors();
        const labels = Object.keys(langData);
        const values = Object.values(langData);

        const colors = ['#6366f1', '#06b6d4', '#a855f7', '#ec4899'];

        this.instances[canvasId] = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: values,
                    backgroundColor: colors.slice(0, labels.length),
                    borderWidth: 2,
                    borderColor: theme.borderColor,
                    hoverOffset: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '72%',
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: theme.textColor,
                            font: { family: 'Plus Jakarta Sans', weight: '600', size: 12 },
                            padding: 16,
                            usePointStyle: true,
                            pointStyle: 'circle'
                        }
                    },
                    tooltip: {
                        backgroundColor: theme.tooltipBg,
                        titleColor: theme.tooltipText,
                        bodyColor: theme.tooltipText,
                        borderColor: theme.borderColor,
                        borderWidth: 1,
                        padding: 12,
                        cornerRadius: 8
                    }
                }
            }
        });
    },

    // 3. Rating Distribution Bar Chart
    renderRatingBar(canvasId, ratingData) {
        this.destroyChart(canvasId);
        const ctx = document.getElementById(canvasId);
        if (!ctx) return;

        const theme = this.getThemeColors();
        const labels = Object.keys(ratingData);
        const values = Object.values(ratingData);

        this.instances[canvasId] = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Feedback Count',
                    data: values,
                    backgroundColor: '#f59e0b',
                    borderRadius: 6,
                    borderSkipped: false
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: theme.tooltipBg,
                        titleColor: theme.tooltipText,
                        bodyColor: theme.tooltipText,
                        borderColor: theme.borderColor,
                        borderWidth: 1,
                        padding: 12,
                        cornerRadius: 8
                    }
                },
                scales: {
                    x: {
                        grid: { display: false },
                        ticks: { color: theme.textColor, font: { family: 'Plus Jakarta Sans', weight: '600' } }
                    },
                    y: {
                        grid: { color: theme.gridColor },
                        ticks: { color: theme.textColor, font: { family: 'Plus Jakarta Sans' } }
                    }
                }
            }
        });
    },

    // 4. Course Leaderboard Horizontal Bar Chart
    renderCourseLeaderboard(canvasId, courses) {
        this.destroyChart(canvasId);
        const ctx = document.getElementById(canvasId);
        if (!ctx) return;

        const theme = this.getThemeColors();
        const topCourses = courses.slice(0, 7);
        const labels = topCourses.map(c => c.course_name.length > 20 ? c.course_name.substring(0, 18) + '...' : c.course_name);
        const values = topCourses.map(c => c.pos_rate);

        this.instances[canvasId] = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: '% Positive Satisfaction',
                    data: values,
                    backgroundColor: '#6366f1',
                    borderRadius: 6
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: theme.tooltipBg,
                        titleColor: theme.tooltipText,
                        bodyColor: theme.tooltipText,
                        callbacks: {
                            label: function(ctx) { return `${ctx.raw}% Positive Feedback`; }
                        }
                    }
                },
                scales: {
                    x: {
                        max: 100,
                        grid: { color: theme.gridColor },
                        ticks: {
                            color: theme.textColor,
                            callback: function(v) { return v + '%'; }
                        }
                    },
                    y: {
                        grid: { display: false },
                        ticks: { color: theme.textColor, font: { family: 'Plus Jakarta Sans', weight: '600' } }
                    }
                }
            }
        });
    },

    // 5. 12-Aspect Net Score Bar Chart
    renderAspectsBar(canvasId, aspects) {
        this.destroyChart(canvasId);
        const ctx = document.getElementById(canvasId);
        if (!ctx) return;

        const theme = this.getThemeColors();
        const labels = aspects.map(a => a.aspect);
        const netScores = aspects.map(a => a.net_score);

        const barColors = netScores.map(score => score >= 0 ? '#10b981' : '#ef4444');

        this.instances[canvasId] = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Net Sentiment Score (%)',
                    data: netScores,
                    backgroundColor: barColors,
                    borderRadius: 6
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: theme.tooltipBg,
                        titleColor: theme.tooltipText,
                        bodyColor: theme.tooltipText,
                        callbacks: {
                            label: function(ctx) { return `Net Score: ${ctx.raw > 0 ? '+' : ''}${ctx.raw}%`; }
                        }
                    }
                },
                scales: {
                    x: {
                        grid: { color: theme.gridColor },
                        ticks: {
                            color: theme.textColor,
                            callback: function(v) { return v + '%'; }
                        }
                    },
                    y: {
                        grid: { display: false },
                        ticks: { color: theme.textColor, font: { family: 'Plus Jakarta Sans', weight: '600' } }
                    }
                }
            }
        });
    },

    // 6. Topic Drift Timeline Line Chart
    renderTopicDriftChart(canvasId, semesters, seriesList) {
        this.destroyChart(canvasId);
        const ctx = document.getElementById(canvasId);
        if (!ctx) return;

        const theme = this.getThemeColors();
        const palette = ['#6366f1', '#06b6d4', '#10b981', '#f59e0b', '#ec4899', '#8b5cf6', '#3b82f6'];

        const datasets = seriesList.map((item, idx) => ({
            label: item.topic_name,
            data: item.data.map(v => (v * 100).toFixed(1)),
            borderColor: palette[idx % palette.length],
            backgroundColor: 'transparent',
            borderWidth: 2.5,
            tension: 0.35,
            pointRadius: 4,
            pointHoverRadius: 7
        }));

        this.instances[canvasId] = new Chart(ctx, {
            type: 'line',
            data: {
                labels: semesters,
                datasets: datasets
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    mode: 'index',
                    intersect: false
                },
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: theme.textColor,
                            font: { family: 'Plus Jakarta Sans', weight: '600', size: 11 },
                            padding: 14,
                            usePointStyle: true
                        }
                    },
                    tooltip: {
                        backgroundColor: theme.tooltipBg,
                        titleColor: theme.tooltipText,
                        bodyColor: theme.tooltipText,
                        padding: 12,
                        cornerRadius: 8,
                        callbacks: {
                            label: function(ctx) {
                                return ` ${ctx.dataset.label}: ${ctx.raw}% of feedback`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        grid: { color: theme.gridColor },
                        ticks: { color: theme.textColor, font: { family: 'Plus Jakarta Sans', weight: '600' } }
                    },
                    y: {
                        grid: { color: theme.gridColor },
                        ticks: {
                            color: theme.textColor,
                            callback: function(v) { return v + '%'; }
                        }
                    }
                }
            }
        });
    },

    // Refresh all charts when theme changes
    refreshAllOnThemeChange() {
        const theme = this.getThemeColors();
        Object.values(this.instances).forEach(chart => {
            if (chart.options.scales) {
                if (chart.options.scales.x && chart.options.scales.x.ticks) {
                    chart.options.scales.x.ticks.color = theme.textColor;
                }
                if (chart.options.scales.y && chart.options.scales.y.ticks) {
                    chart.options.scales.y.ticks.color = theme.textColor;
                }
            }
            if (chart.options.plugins && chart.options.plugins.legend && chart.options.plugins.legend.labels) {
                chart.options.plugins.legend.labels.color = theme.textColor;
            }
            chart.update();
        });
    }
};
