// nav.js — shared navigation for all dashboard pages
function renderNav(activePage) {
  const pages = [
    { id: 'dashboard',  label: 'Dashboard',         icon: `<svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>`, href: 'dashboard.html' },
    { id: 'record',     label: 'Record Usage',      icon: `<svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4 12.5-12.5z"/></svg>`, href: 'record-usage.html' },
    { id: 'predictions',label: 'Predictions',       icon: `<svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>`, href: 'predictions.html' },
    { id: 'supply',     label: 'Supply Management', icon: `<svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg>`, href: 'supply-management.html' },
    { id: 'alerts',     label: 'Alerts',            icon: `<svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>`, href: 'alerts.html' },
  ];

  return `
  <nav class="navbar">
    <a href="dashboard.html" class="nav-brand">
      <div class="nav-logo">
        <svg width="20" height="20" viewBox="0 0 36 36" fill="none">
          <polyline points="2,22 9,12 15,20 22,8 29,16 34,10" stroke="white" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>
      <div class="nav-brand-text">
        <span class="nav-title">MedSupply AI</span>
        <span class="nav-sub">Prediction System</span>
      </div>
    </a>

    <div class="nav-links">
      ${pages.map(p => `
        <a href="${p.href}" class="nav-link ${activePage === p.id ? 'active' : ''}">
          ${p.icon}
          ${p.label}
        </a>
      `).join('')}
    </div>

    <div class="nav-right">
      <div class="nav-user">
        <div class="nav-avatar">
          <svg width="18" height="18" fill="none" stroke="#2952e3" stroke-width="2" stroke-linecap="round" viewBox="0 0 24 24">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>
          </svg>
        </div>
        <div class="nav-user-info">
          <span class="nav-user-name">Dr Karabo Sello</span>
          <span class="nav-user-role">Administrator</span>
        </div>
      </div>
      <button class="btn-logout" onclick="window.location.href='login.html'">
        <svg width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" viewBox="0 0 24 24">
          <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/>
        </svg>
        Logout
      </button>
    </div>
  </nav>`;
}

const navCSS = `
  .navbar {
    display: flex;
    align-items: center;
    gap: 0;
    padding: 0 28px;
    height: 64px;
    background: white;
    border-bottom: 1px solid #e8eeff;
    box-shadow: 0 2px 12px rgba(41,82,227,0.07);
    position: sticky;
    top: 0;
    z-index: 100;
  }

  .nav-brand {
    display: flex;
    align-items: center;
    gap: 10px;
    text-decoration: none;
    margin-right: 28px;
    flex-shrink: 0;
  }

  .nav-logo {
    width: 38px; height: 38px;
    background: linear-gradient(135deg, #1a3fcb, #4b72f5);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .nav-brand-text { display: flex; flex-direction: column; line-height: 1.2; }
  .nav-title { font-family: 'Syne', sans-serif; font-size: 0.95rem; font-weight: 800; color: #1a1f36; }
  .nav-sub { font-size: 0.7rem; color: #6b7280; font-weight: 400; }

  .nav-links {
    display: flex;
    align-items: center;
    gap: 4px;
    flex: 1;
  }

  .nav-link {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 8px 14px;
    border-radius: 10px;
    font-size: 0.875rem;
    font-weight: 500;
    color: #6b7280;
    text-decoration: none;
    transition: background 0.15s, color 0.15s;
    white-space: nowrap;
  }

  .nav-link:hover { background: #f0f4ff; color: #2952e3; }

  .nav-link.active {
    background: #2952e3;
    color: white;
    font-weight: 600;
  }

  .nav-right { display: flex; align-items: center; gap: 14px; margin-left: auto; }

  .nav-user {
    display: flex;
    align-items: center;
    gap: 10px;
    background: #f3f6ff;
    border-radius: 12px;
    padding: 6px 14px 6px 8px;
  }

  .nav-avatar {
    width: 34px; height: 34px;
    background: #e8eeff;
    border-radius: 9px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .nav-user-info { display: flex; flex-direction: column; line-height: 1.3; }
  .nav-user-name { font-size: 0.82rem; font-weight: 600; color: #1a1f36; }
  .nav-user-role { font-size: 0.7rem; color: #6b7280; }

  .btn-logout {
    display: flex;
    align-items: center;
    gap: 6px;
    background: #2952e3;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 9px 16px;
    font-size: 0.875rem;
    font-weight: 600;
    font-family: 'DM Sans', sans-serif;
    cursor: pointer;
    transition: background 0.15s, transform 0.1s;
  }

  .btn-logout:hover { background: #1a3fcb; transform: translateY(-1px); }
`;

function injectNav(activePage) {
  // Inject CSS
  const style = document.createElement('style');
  style.textContent = navCSS;
  document.head.appendChild(style);

  // Inject HTML
  const navEl = document.createElement('div');
  navEl.innerHTML = renderNav(activePage);
  document.body.insertBefore(navEl.firstElementChild, document.body.firstChild);
}
