import { useEffect, useMemo, useState } from 'react';
import {
  BookOpen,
  Bot,
  ExternalLink,
  FilePenLine,
  Gamepad2,
  Github,
  Heart,
  LogIn,
  LogOut,
  MessageCircle,
  PencilLine,
  PlusCircle,
  RefreshCw,
  Save,
  Search,
  ShieldCheck,
  Star,
  ThumbsDown,
  Trash2,
  UserRound,
  X,
  Zap
} from 'lucide-react';
import { aiNews as fallbackNews, articles as fallbackArticles, gameModule, profile as fallbackProfile } from './data.js';

const createEmptyArticleForm = () => ({
  title: '',
  summary: '',
  content: '',
  tags: '',
  date: new Date().toISOString().slice(0, 10),
  readTime: '3 min'
});

const navItems = [
  { id: 'overview', label: '首页', icon: UserRound },
  { id: 'articles', label: '文章', icon: BookOpen },
  { id: 'ai', label: 'AI', icon: Bot },
  { id: 'game', label: '游戏', icon: Gamepad2 },
  { id: 'login', label: '登录', icon: LogIn },
  { id: 'admin', label: '管理', icon: FilePenLine }
];

function App() {
  const [activeView, setActiveView] = useState('overview');
  const [query, setQuery] = useState('');
  const [selectedTag, setSelectedTag] = useState('全部');
  const [profile, setProfile] = useState(fallbackProfile);
  const [articles, setArticles] = useState(fallbackArticles);
  const [aiNews, setAiNews] = useState(fallbackNews);
  const [reactions, setReactions] = useState({});
  const [reactionCounts, setReactionCounts] = useState({});
  const [commentDrafts, setCommentDrafts] = useState({});
  const [comments, setComments] = useState({
    'react-fastapi-mvp': [{ id: 'local-1', authorName: '访客', content: '第一版先把前后端结构跑起来，后续再接数据库。' }]
  });
  const [articleForm, setArticleForm] = useState(createEmptyArticleForm);
  const [editingArticleId, setEditingArticleId] = useState(null);
  const [adminMessage, setAdminMessage] = useState('');
  const [isSavingArticle, setIsSavingArticle] = useState(false);
  const [authToken, setAuthToken] = useState(() => localStorage.getItem('felix_blog_token') || '');
  const [currentUser, setCurrentUser] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem('felix_blog_user') || 'null');
    } catch {
      return null;
    }
  });
  const [authMode, setAuthMode] = useState('login');
  const [authForm, setAuthForm] = useState({
    email: '',
    password: '',
    displayName: 'Felix Fu'
  });
  const [authMessage, setAuthMessage] = useState('');
  const [isAuthLoading, setIsAuthLoading] = useState(false);

  useEffect(() => {
    async function loadInitialData() {
      try {
        const [profileRes, newsRes] = await Promise.all([
          fetch('/api/profile'),
          fetch('/api/ai/news')
        ]);

        if (profileRes.ok) {
          setProfile(await profileRes.json());
        }
        if (newsRes.ok) {
          setAiNews(await newsRes.json());
        }
        await refreshArticles();
      } catch {
        // The MVP can run as a standalone frontend before the API is started.
      }
    }

    loadInitialData();
  }, []);

  useEffect(() => {
    const params = new URLSearchParams(window.location.hash.replace(/^#/, ''));
    if (params.get('auth') !== 'github') return;

    const token = params.get('token');
    const error = params.get('error');
    window.history.replaceState(null, '', window.location.pathname + window.location.search);

    if (token) {
      localStorage.setItem('felix_blog_token', token);
      localStorage.removeItem('felix_blog_user');
      setCurrentUser(null);
      setAuthToken(token);
      setAuthMessage('GitHub 登录成功');
      setActiveView('admin');
      return;
    }

    setAuthMessage(error ? `GitHub 登录失败：${error}` : 'GitHub 登录失败');
    setActiveView('login');
  }, []);

  useEffect(() => {
    if (!authToken) {
      localStorage.removeItem('felix_blog_token');
      localStorage.removeItem('felix_blog_user');
      setCurrentUser(null);
      return;
    }

    async function loadCurrentUser() {
      try {
        const response = await fetch('/api/auth/me', {
          headers: { Authorization: `Bearer ${authToken}` }
        });
        if (!response.ok) {
          logout(false);
          return;
        }
        const result = await response.json();
        setCurrentUser(result.user);
        localStorage.setItem('felix_blog_user', JSON.stringify(result.user));
      } catch {
        setAuthMessage('后端服务不可用，无法校验登录状态');
      }
    }

    loadCurrentUser();
  }, [authToken]);

  async function refreshArticles() {
    const articlesRes = await fetch('/api/articles');
    if (!articlesRes.ok) return [];
    const articleData = await articlesRes.json();
    setArticles(articleData);
    hydrateArticleState(articleData);
    return articleData;
  }

  function hydrateArticleState(nextArticles) {
    const nextComments = {};
    const nextReactionCounts = {};

    nextArticles.forEach((article) => {
      nextComments[article.id] = (article.comments || []).map((comment, index) =>
        typeof comment === 'string'
          ? { id: `${article.id}-${index}`, authorName: '访客', content: comment }
          : comment
      );
      nextReactionCounts[article.id] = {
        like: article.reactions?.like || 0,
        favorite: article.reactions?.favorite || 0,
        downvote: article.reactions?.downvote || 0
      };
    });

    setComments(nextComments);
    setReactionCounts(nextReactionCounts);
  }

  function getAuthHeaders() {
    return authToken ? { Authorization: `Bearer ${authToken}` } : {};
  }

  function updateAuthForm(field, value) {
    setAuthForm((current) => ({ ...current, [field]: value }));
  }

  async function submitAuthForm(event) {
    event.preventDefault();
    setIsAuthLoading(true);
    setAuthMessage('');

    const endpoint = authMode === 'register' ? '/api/auth/register' : '/api/auth/login';
    const payload = {
      email: authForm.email,
      password: authForm.password,
      ...(authMode === 'register' ? { displayName: authForm.displayName } : {})
    };

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const result = await response.json().catch(() => ({}));
      if (!response.ok) {
        setAuthMessage(result.detail || '登录失败');
        return;
      }

      localStorage.setItem('felix_blog_token', result.token);
      localStorage.setItem('felix_blog_user', JSON.stringify(result.user));
      setAuthToken(result.token);
      setCurrentUser(result.user);
      setAuthMessage(authMode === 'register' ? '管理员已初始化' : '已登录');
      setActiveView('admin');
    } catch {
      setAuthMessage('后端服务不可用，登录失败');
    } finally {
      setIsAuthLoading(false);
    }
  }

  function logout(redirect = true) {
    localStorage.removeItem('felix_blog_token');
    localStorage.removeItem('felix_blog_user');
    setAuthToken('');
    setCurrentUser(null);
    setAuthMessage('');
    if (redirect) {
      setActiveView('overview');
    }
  }

  const tags = useMemo(() => {
    const uniqueTags = new Set(articles.flatMap((article) => article.tags));
    return ['全部', ...uniqueTags];
  }, [articles]);

  const filteredArticles = useMemo(() => {
    const normalizedQuery = query.trim().toLowerCase();

    return articles.filter((article) => {
      const tagMatched = selectedTag === '全部' || article.tags.includes(selectedTag);
      const text = `${article.title} ${article.summary} ${article.content} ${article.tags.join(' ')}`.toLowerCase();
      return tagMatched && (!normalizedQuery || text.includes(normalizedQuery));
    });
  }, [articles, query, selectedTag]);

  async function toggleReaction(articleId, type) {
    const nextActive = !reactions[articleId]?.[type];

    setReactions((current) => ({
      ...current,
      [articleId]: {
        ...current[articleId],
        [type]: nextActive
      }
    }));

    setReactionCounts((current) => ({
      ...current,
      [articleId]: {
        like: current[articleId]?.like || 0,
        favorite: current[articleId]?.favorite || 0,
        downvote: current[articleId]?.downvote || 0,
        [type]: Math.max(0, (current[articleId]?.[type] || 0) + (nextActive ? 1 : -1))
      }
    }));

    try {
      const response = await fetch(`/api/articles/${articleId}/reaction`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type, active: nextActive })
      });

      if (response.ok) {
        const result = await response.json();
        setReactionCounts((current) => ({
          ...current,
          [articleId]: result.reactions
        }));
      }
    } catch {
      // Keep the optimistic local state when the API is unavailable.
    }
  }

  async function submitComment(articleId) {
    const value = commentDrafts[articleId]?.trim();
    if (!value) return;

    setCommentDrafts((current) => ({ ...current, [articleId]: '' }));

    try {
      const response = await fetch(`/api/articles/${articleId}/comments`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: value, authorName: '访客' })
      });

      if (response.ok) {
        const result = await response.json();
        setComments((current) => ({
          ...current,
          [articleId]: result.comments
        }));
        return;
      }
    } catch {
      // Fall through to local-only behavior for standalone frontend previews.
    }

    setComments((current) => ({
      ...current,
      [articleId]: [
        ...(current[articleId] || []),
        { id: `${articleId}-${Date.now()}`, authorName: '访客', content: value }
      ]
    }));
  }

  function updateArticleForm(field, value) {
    setArticleForm((current) => ({ ...current, [field]: value }));
  }

  function resetArticleForm() {
    setArticleForm(createEmptyArticleForm());
    setEditingArticleId(null);
    setAdminMessage('');
  }

  function startEditingArticle(article) {
    setActiveView('admin');
    setEditingArticleId(article.id);
    setAdminMessage(`正在编辑：${article.title}`);
    setArticleForm({
      title: article.title,
      summary: article.summary,
      content: article.content,
      tags: article.tags.join(', '),
      date: article.date,
      readTime: article.readTime
    });
  }

  async function submitArticleForm(event) {
    event.preventDefault();
    if (!authToken) {
      setAdminMessage('请先登录管理员账号');
      setActiveView('login');
      return;
    }

    setIsSavingArticle(true);
    setAdminMessage('');

    const payload = {
      title: articleForm.title,
      summary: articleForm.summary,
      content: articleForm.content,
      tags: articleForm.tags
        .split(/[,，]/)
        .map((tag) => tag.trim())
        .filter(Boolean),
      date: articleForm.date,
      readTime: articleForm.readTime
    };

    try {
      const response = await fetch(editingArticleId ? `/api/admin/articles/${editingArticleId}` : '/api/admin/articles', {
        method: editingArticleId ? 'PUT' : 'POST',
        headers: { 'Content-Type': 'application/json', ...getAuthHeaders() },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        setAdminMessage(error.detail || '保存失败');
        if (response.status === 401 || response.status === 403) {
          setActiveView('login');
        }
        return;
      }

      await refreshArticles();
      setAdminMessage(editingArticleId ? '文章已更新' : '文章已发布');
      setArticleForm(createEmptyArticleForm());
      setEditingArticleId(null);
    } catch {
      setAdminMessage('后端服务不可用，保存失败');
    } finally {
      setIsSavingArticle(false);
    }
  }

  async function deleteArticle(article) {
    if (!window.confirm(`确定删除《${article.title}》吗？`)) return;
    if (!authToken) {
      setAdminMessage('请先登录管理员账号');
      setActiveView('login');
      return;
    }

    try {
      const response = await fetch(`/api/admin/articles/${article.id}`, {
        method: 'DELETE',
        headers: getAuthHeaders()
      });
      if (!response.ok) {
        setAdminMessage('删除失败');
        if (response.status === 401 || response.status === 403) {
          setActiveView('login');
        }
        return;
      }

      if (editingArticleId === article.id) {
        resetArticleForm();
      }
      await refreshArticles();
      setAdminMessage(`已删除：${article.title}`);
    } catch {
      setAdminMessage('后端服务不可用，删除失败');
    }
  }

  return (
    <div className="app-shell">
      <aside className="sidebar" aria-label="博客导航">
        <div className="brand">
          <span className="brand-mark">FJ</span>
          <div>
            <strong>{profile.name}</strong>
            <span>{profile.englishName}</span>
          </div>
        </div>

        <nav className="nav-list">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <button
                key={item.id}
                className={activeView === item.id ? 'nav-button active' : 'nav-button'}
                type="button"
                onClick={() => setActiveView(item.id)}
              >
                <Icon size={18} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>

        <div className="login-panel">
          {currentUser ? (
            <>
              <span>管理员</span>
              <strong>{currentUser.displayName}</strong>
              <button className="icon-text-button" type="button" onClick={() => logout()}>
                <LogOut size={17} />
                <span>退出</span>
              </button>
            </>
          ) : (
            <>
              <span>后台账号</span>
              <button className="icon-text-button" type="button" onClick={() => setActiveView('login')}>
                <LogIn size={17} />
                <span>登录</span>
              </button>
            </>
          )}
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div className="search-box">
            <Search size={18} />
            <input
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="搜索标题、正文或标签"
              aria-label="搜索标题、正文或标签"
            />
          </div>
          <div className="status-pill">
            <Zap size={16} />
            <span>本地 MVP</span>
          </div>
        </header>

        {activeView === 'overview' && <Overview profile={profile} articles={articles} />}

        {activeView === 'articles' && (
          <ArticleWorkspace
            articles={filteredArticles}
            tags={tags}
            selectedTag={selectedTag}
            setSelectedTag={setSelectedTag}
            reactions={reactions}
            reactionCounts={reactionCounts}
            toggleReaction={toggleReaction}
            comments={comments}
            commentDrafts={commentDrafts}
            setCommentDrafts={setCommentDrafts}
            submitComment={submitComment}
          />
        )}

        {activeView === 'ai' && <AiWorkspace news={aiNews} articles={articles} />}

        {activeView === 'game' && <GameWorkspace />}

        {activeView === 'login' && (
          <LoginWorkspace
            authMode={authMode}
            setAuthMode={setAuthMode}
            authForm={authForm}
            updateAuthForm={updateAuthForm}
            submitAuthForm={submitAuthForm}
            authMessage={authMessage}
            isAuthLoading={isAuthLoading}
            currentUser={currentUser}
            logout={logout}
            goToAdmin={() => setActiveView('admin')}
          />
        )}

        {activeView === 'admin' && currentUser?.role !== 'admin' && (
          <LoginWorkspace
            authMode={authMode}
            setAuthMode={setAuthMode}
            authForm={authForm}
            updateAuthForm={updateAuthForm}
            submitAuthForm={submitAuthForm}
            authMessage={authMessage || '请先登录管理员账号'}
            isAuthLoading={isAuthLoading}
            currentUser={currentUser}
            logout={logout}
            goToAdmin={() => setActiveView('admin')}
          />
        )}

        {activeView === 'admin' && currentUser?.role === 'admin' && (
          <AdminWorkspace
            articles={articles}
            articleForm={articleForm}
            updateArticleForm={updateArticleForm}
            editingArticleId={editingArticleId}
            isSavingArticle={isSavingArticle}
            adminMessage={adminMessage}
            submitArticleForm={submitArticleForm}
            resetArticleForm={resetArticleForm}
            startEditingArticle={startEditingArticle}
            deleteArticle={deleteArticle}
            currentUser={currentUser}
            logout={logout}
          />
        )}
      </main>
    </div>
  );
}

function Overview({ profile, articles }) {
  return (
    <section className="workspace">
      <div className="profile-grid">
        <div className="profile-copy">
          <p className="eyebrow">{profile.school}</p>
          <h1>{profile.name}的个人博客</h1>
          <p className="summary">{profile.summary}</p>
          <div className="interest-row">
            {profile.interests.map((interest) => (
              <span key={interest}>{interest}</span>
            ))}
          </div>
        </div>
        <img className="profile-image" src="/profile-cover.png" alt="付江樊个人博客封面" />
      </div>

      <div className="metric-grid">
        {profile.metrics.map((metric) => (
          <div className="metric" key={metric.label}>
            <span>{metric.label}</span>
            <strong>{metric.value}</strong>
          </div>
        ))}
      </div>

      <section className="content-band">
        <div className="section-heading">
          <p className="eyebrow">最近文章</p>
          <h2>学习笔记和项目记录</h2>
        </div>
        <div className="article-list compact">
          {articles.slice(0, 3).map((article) => (
            <article className="article-card" key={article.id}>
              <span className="date">{article.date}</span>
              <h3>{article.title}</h3>
              <p>{article.summary}</p>
              <div className="tag-row">
                {article.tags.map((tag) => (
                  <span key={tag}>{tag}</span>
                ))}
              </div>
            </article>
          ))}
        </div>
      </section>
    </section>
  );
}

function ArticleWorkspace({
  articles,
  tags,
  selectedTag,
  setSelectedTag,
  reactions,
  reactionCounts,
  toggleReaction,
  comments,
  commentDrafts,
  setCommentDrafts,
  submitComment
}) {
  return (
    <section className="workspace">
      <div className="section-heading">
        <p className="eyebrow">文章中心</p>
        <h1>学习笔记、项目记录和标签搜索</h1>
      </div>

      <div className="tag-filter" aria-label="文章标签筛选">
        {tags.map((tag) => (
          <button
            key={tag}
            className={selectedTag === tag ? 'tag-button active' : 'tag-button'}
            type="button"
            onClick={() => setSelectedTag(tag)}
          >
            {tag}
          </button>
        ))}
      </div>

      <div className="article-list">
        {articles.map((article) => (
          <article className="article-card" key={article.id}>
            <div className="article-meta">
              <span>{article.date}</span>
              <span>{article.readTime}</span>
            </div>
            <h2>{article.title}</h2>
            <p>{article.summary}</p>
            <div className="tag-row">
              {article.tags.map((tag) => (
                <span key={tag}>{tag}</span>
              ))}
            </div>

            <div className="reaction-row">
              <IconToggle
                active={reactions[article.id]?.like}
                label="点赞"
                count={reactionCounts[article.id]?.like || 0}
                icon={Heart}
                onClick={() => toggleReaction(article.id, 'like')}
              />
              <IconToggle
                active={reactions[article.id]?.favorite}
                label="收藏"
                count={reactionCounts[article.id]?.favorite || 0}
                icon={Star}
                onClick={() => toggleReaction(article.id, 'favorite')}
              />
              <IconToggle
                active={reactions[article.id]?.downvote}
                label="点踩"
                count={reactionCounts[article.id]?.downvote || 0}
                icon={ThumbsDown}
                onClick={() => toggleReaction(article.id, 'downvote')}
              />
            </div>

            <div className="comment-box">
              <div className="comment-title">
                <MessageCircle size={17} />
                <span>评论</span>
              </div>
              {(comments[article.id] || []).map((comment, index) => (
                <p className="comment" key={comment.id || `${article.id}-${index}`}>
                  <strong>{comment.authorName || '访客'}：</strong>
                  <span>{comment.content}</span>
                </p>
              ))}
              <div className="comment-form">
                <input
                  value={commentDrafts[article.id] || ''}
                  onChange={(event) =>
                    setCommentDrafts((current) => ({
                      ...current,
                      [article.id]: event.target.value
                    }))
                  }
                  placeholder="写一条评论"
                  aria-label={`评论 ${article.title}`}
                />
                <button type="button" onClick={() => submitComment(article.id)}>
                  发布
                </button>
              </div>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}

function AiWorkspace({ news, articles }) {
  return (
    <section className="workspace">
      <div className="section-heading">
        <p className="eyebrow">AI 自动化</p>
        <h1>每日技术新闻和文章总结</h1>
      </div>

      <div className="split-grid">
        <section className="tool-panel">
          <h2>每日技术新闻</h2>
          {news.map((item) => (
            <article className="news-item" key={item.title}>
              <span>{item.source}</span>
              <h3>{item.title}</h3>
              <p>{item.summary}</p>
            </article>
          ))}
        </section>

        <section className="tool-panel">
          <h2>文章 AI 总结</h2>
          {articles.map((article) => (
            <article className="digest-item" key={article.id}>
              <strong>{article.title}</strong>
              <p>{article.summary}</p>
            </article>
          ))}
        </section>
      </div>
    </section>
  );
}

function GameWorkspace() {
  const [frameKey, setFrameKey] = useState(0);

  return (
    <section className="workspace">
      <div className="section-heading">
        <p className="eyebrow">小游戏</p>
        <h1>{gameModule.title}</h1>
      </div>

      <div className="game-layout">
        <div className="game-details">
          <span className="status-pill inline">{gameModule.status}</span>
          <div className="game-copy">
            <h2>Card War 在线试玩</h2>
            <p>{gameModule.plan}</p>
          </div>
          <div className="game-actions">
            <button type="button" onClick={() => setFrameKey((current) => current + 1)}>
              <RefreshCw size={17} />
              <span>刷新游戏</span>
            </button>
            <a href={gameModule.playUrl} target="_blank" rel="noreferrer">
              <ExternalLink size={17} />
              <span>新窗口打开</span>
            </a>
            <a className="secondary-link" href={gameModule.repository} target="_blank" rel="noreferrer">
              <Github size={17} />
              <span>查看仓库</span>
            </a>
          </div>
        </div>
        <div className="game-stage">
          <iframe
            key={frameKey}
            title="决斗小游戏"
            src={gameModule.playUrl}
            loading="lazy"
            allow="fullscreen; gamepad; autoplay"
          />
        </div>
      </div>
    </section>
  );
}

function LoginWorkspace({
  authMode,
  setAuthMode,
  authForm,
  updateAuthForm,
  submitAuthForm,
  authMessage,
  isAuthLoading,
  currentUser,
  logout,
  goToAdmin
}) {
  if (currentUser?.role === 'admin') {
    return (
      <section className="workspace">
        <div className="section-heading">
          <p className="eyebrow">账号</p>
          <h1>已登录管理员账号</h1>
        </div>
        <div className="admin-panel auth-panel">
          <div className="auth-user">
            <ShieldCheck size={22} />
            <div>
              <strong>{currentUser.displayName}</strong>
              <span>{currentUser.email}</span>
            </div>
          </div>
          <div className="admin-actions">
            <button className="primary-action" type="button" onClick={goToAdmin}>
              <FilePenLine size={17} />
              <span>进入后台</span>
            </button>
            <button className="ghost-button" type="button" onClick={() => logout()}>
              <LogOut size={17} />
              <span>退出登录</span>
            </button>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section className="workspace">
      <div className="section-heading">
        <p className="eyebrow">账号</p>
        <h1>管理员登录</h1>
      </div>

      <form className="admin-panel admin-form auth-panel" onSubmit={submitAuthForm}>
        <a className="github-auth-button" href="/api/auth/github/start">
          <Github size={18} />
          <span>使用 GitHub 登录</span>
        </a>

        <div className="auth-divider">
          <span>或使用邮箱账号</span>
        </div>

        <div className="auth-mode-switch" aria-label="账号模式">
          <button
            type="button"
            className={authMode === 'login' ? 'active' : ''}
            onClick={() => setAuthMode('login')}
          >
            登录
          </button>
          <button
            type="button"
            className={authMode === 'register' ? 'active' : ''}
            onClick={() => setAuthMode('register')}
          >
            初始化管理员
          </button>
        </div>

        {authMode === 'register' && (
          <label>
            <span>显示名称</span>
            <input
              value={authForm.displayName}
              onChange={(event) => updateAuthForm('displayName', event.target.value)}
              placeholder="Felix Fu"
              required
            />
          </label>
        )}

        <label>
          <span>邮箱</span>
          <input
            type="email"
            value={authForm.email}
            onChange={(event) => updateAuthForm('email', event.target.value)}
            placeholder="you@example.com"
            required
          />
        </label>

        <label>
          <span>密码</span>
          <input
            type="password"
            value={authForm.password}
            onChange={(event) => updateAuthForm('password', event.target.value)}
            placeholder="至少 8 位"
            minLength={8}
            required
          />
        </label>

        <div className="admin-actions">
          <button className="primary-action" type="submit" disabled={isAuthLoading}>
            <LogIn size={17} />
            <span>{isAuthLoading ? '处理中' : authMode === 'register' ? '初始化' : '登录'}</span>
          </button>
        </div>

        {authMessage && <p className="admin-message">{authMessage}</p>}
      </form>
    </section>
  );
}

function AdminWorkspace({
  articles,
  articleForm,
  updateArticleForm,
  editingArticleId,
  isSavingArticle,
  adminMessage,
  submitArticleForm,
  resetArticleForm,
  startEditingArticle,
  deleteArticle,
  currentUser,
  logout
}) {
  return (
    <section className="workspace">
      <div className="section-heading">
        <p className="eyebrow">管理后台</p>
        <h1>文章发布、编辑和删除</h1>
      </div>

      <div className="admin-session">
        <div>
          <ShieldCheck size={18} />
          <span>{currentUser.displayName}</span>
        </div>
        <button className="ghost-button" type="button" onClick={() => logout()}>
          <LogOut size={17} />
          <span>退出</span>
        </button>
      </div>

      <div className="admin-layout">
        <form className="admin-panel admin-form" onSubmit={submitArticleForm}>
          <div className="admin-panel-heading">
            <h2>{editingArticleId ? '编辑文章' : '发布文章'}</h2>
            {editingArticleId && (
              <button className="ghost-button" type="button" onClick={resetArticleForm}>
                <X size={17} />
                <span>取消编辑</span>
              </button>
            )}
          </div>

          <label>
            <span>标题</span>
            <input
              value={articleForm.title}
              onChange={(event) => updateArticleForm('title', event.target.value)}
              placeholder="输入文章标题"
              required
            />
          </label>

          <label>
            <span>摘要</span>
            <textarea
              value={articleForm.summary}
              onChange={(event) => updateArticleForm('summary', event.target.value)}
              placeholder="用于文章列表展示的短摘要"
              rows={3}
              required
            />
          </label>

          <label>
            <span>正文</span>
            <textarea
              value={articleForm.content}
              onChange={(event) => updateArticleForm('content', event.target.value)}
              placeholder="先支持纯文本/Markdown 内容，后续再加预览"
              rows={10}
              required
            />
          </label>

          <div className="admin-form-grid">
            <label>
              <span>标签</span>
              <input
                value={articleForm.tags}
                onChange={(event) => updateArticleForm('tags', event.target.value)}
                placeholder="React, FastAPI, 学习"
              />
            </label>
            <label>
              <span>日期</span>
              <input
                type="date"
                value={articleForm.date}
                onChange={(event) => updateArticleForm('date', event.target.value)}
              />
            </label>
            <label>
              <span>阅读时长</span>
              <input
                value={articleForm.readTime}
                onChange={(event) => updateArticleForm('readTime', event.target.value)}
                placeholder="3 min"
              />
            </label>
          </div>

          <div className="admin-actions">
            <button className="primary-action" type="submit" disabled={isSavingArticle}>
              {editingArticleId ? <Save size={17} /> : <PlusCircle size={17} />}
              <span>{isSavingArticle ? '保存中' : editingArticleId ? '保存修改' : '发布文章'}</span>
            </button>
            <button className="ghost-button" type="button" onClick={resetArticleForm}>
              <X size={17} />
              <span>清空</span>
            </button>
          </div>

          {adminMessage && <p className="admin-message">{adminMessage}</p>}
        </form>

        <section className="admin-panel article-manager">
          <div className="admin-panel-heading">
            <h2>已有文章</h2>
            <span>{articles.length} 篇</span>
          </div>

          <div className="manager-list">
            {articles.map((article) => (
              <article className="manager-row" key={article.id}>
                <div>
                  <h3>{article.title}</h3>
                  <p>{article.summary}</p>
                  <div className="tag-row">
                    {article.tags.map((tag) => (
                      <span key={tag}>{tag}</span>
                    ))}
                  </div>
                </div>
                <div className="manager-actions">
                  <button type="button" onClick={() => startEditingArticle(article)}>
                    <PencilLine size={17} />
                    <span>编辑</span>
                  </button>
                  <button className="danger-button" type="button" onClick={() => deleteArticle(article)}>
                    <Trash2 size={17} />
                    <span>删除</span>
                  </button>
                </div>
              </article>
            ))}
          </div>
        </section>
      </div>
    </section>
  );
}

function IconToggle({ active, label, count, icon: Icon, onClick }) {
  return (
    <button className={active ? 'icon-toggle active' : 'icon-toggle'} type="button" onClick={onClick} title={label}>
      <Icon size={17} />
      <span>{label} {count}</span>
    </button>
  );
}

export default App;
