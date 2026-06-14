import { useEffect, useMemo, useState } from 'react';
import {
  BookOpen,
  Bot,
  ExternalLink,
  Gamepad2,
  Github,
  Heart,
  MessageCircle,
  RefreshCw,
  Search,
  Star,
  ThumbsDown,
  UserRound,
  Zap
} from 'lucide-react';
import { aiNews as fallbackNews, articles as fallbackArticles, gameModule, profile as fallbackProfile } from './data.js';

const navItems = [
  { id: 'overview', label: '首页', icon: UserRound },
  { id: 'articles', label: '文章', icon: BookOpen },
  { id: 'ai', label: 'AI', icon: Bot },
  { id: 'game', label: '游戏', icon: Gamepad2 }
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

  useEffect(() => {
    async function loadInitialData() {
      try {
        const [profileRes, articlesRes, newsRes] = await Promise.all([
          fetch('/api/profile'),
          fetch('/api/articles'),
          fetch('/api/ai/news')
        ]);

        if (profileRes.ok) {
          setProfile(await profileRes.json());
        }
        if (articlesRes.ok) {
          const articleData = await articlesRes.json();
          setArticles(articleData);
          hydrateArticleState(articleData);
        }
        if (newsRes.ok) {
          setAiNews(await newsRes.json());
        }
      } catch {
        // The MVP can run as a standalone frontend before the API is started.
      }
    }

    loadInitialData();
  }, []);

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
          <span>登录入口</span>
          <button className="icon-text-button" type="button" title="GitHub 登录后续接入">
            <Github size={17} />
            <span>GitHub</span>
          </button>
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

function IconToggle({ active, label, count, icon: Icon, onClick }) {
  return (
    <button className={active ? 'icon-toggle active' : 'icon-toggle'} type="button" onClick={onClick} title={label}>
      <Icon size={17} />
      <span>{label} {count}</span>
    </button>
  );
}

export default App;
