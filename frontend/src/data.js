export const profile = {
  name: '付江樊',
  englishName: 'Felix Fu',
  school: '浙江大学',
  role: '个人博客 · 学习笔记 · AI 工作台 · 技术项目',
  interests: ['技术写作', 'AI 自动化', '长跑', '游戏'],
  summary:
    '这里沉淀学习笔记、项目复盘和个人实验。当前博客已经具备文章发布、Markdown/LaTeX、图片上传、评论审核、GitHub 登录、云端部署和 AI 工作台骨架。',
  metrics: [
    { label: '当前阶段', value: 'v1.7.1' },
    { label: '写作后台', value: '已可用' },
    { label: 'AI 模块', value: '工作台骨架' }
  ]
};

export const articles = [
  {
    id: 'react-fastapi-mvp',
    title: 'React + FastAPI 个人博客 MVP 搭建记录',
    summary:
      '记录个人博客第一版的页面结构、接口规划和前后端分离方式，作为后续 PostgreSQL、登录和部署的基础。',
    content:
      '本篇文章聚焦 MVP 阶段：先搭建 React 页面，使用 FastAPI 提供个人信息、文章列表和搜索接口，再逐步接入 PostgreSQL、GitHub Actions 和云服务器部署。',
    tags: ['React', 'FastAPI', 'MVP'],
    date: '2026-06-14',
    readTime: '5 min'
  },
  {
    id: 'running-and-study',
    title: '长跑、学习和项目节奏',
    summary:
      '把长跑训练里的节奏感迁移到项目推进中，按周拆解任务，稳定积累可展示成果。',
    content:
      '个人博客的建设也可以像训练计划一样推进：先有可运行版本，再逐步增加数据库、鉴权、自动化、AI 和小游戏模块。',
    tags: ['长跑', '学习方法', '计划'],
    date: '2026-06-14',
    readTime: '3 min'
  },
  {
    id: 'ai-digest-plan',
    title: '每日技术新闻和文章 AI 总结计划',
    summary:
      '规划 AI 自动化模块：每天抓取技术新闻，自动提炼摘要，并为站内文章生成结构化总结。',
    content:
      'AI 自动化模块会分两步实现。第一步展示占位数据和页面入口，第二步接入真实模型和定时任务，第三步缓存摘要结果并形成可检索知识库。',
    tags: ['AI', '自动化', '技术新闻'],
    date: '2026-06-14',
    readTime: '4 min'
  }
];

export const aiNews = [
  {
    title: '前后端分离项目优先打通接口契约',
    source: 'Daily Tech Digest',
    summary: '先固定页面、数据结构和 API 路由，可以降低后续接入数据库和鉴权时的改动成本。'
  },
  {
    title: 'AI 总结模块适合从文章摘要开始',
    source: 'AI Workflow',
    summary: 'MVP 阶段可先保留摘要入口，后续把文章正文发送到模型服务并缓存总结结果。'
  }
];

export const gameModule = {
  title: '决斗小游戏',
  repository: 'https://github.com/firefelixfu026/card-war-made-by-class-3',
  playUrl: 'https://firefelixfu026.github.io/card-war-made-by-class-3/',
  status: '已嵌入',
  plan: '当前通过 GitHub Pages 页面直接嵌入博客。后续可以继续补充游戏介绍、排行榜和统一登录后的分数记录。'
};
