const API = 'http://127.0.0.1:8000/api';

const demo = [
  {
    id: 1,
    source: 'youtube',
    title: 'The Art of the Cover Drive',
    description: 'A masterclass in timing, balance and beautiful batting.',
    creator_or_brand: 'Cricket Lab',
    tags: ['cricket', 'batting', 'sports'],
    thumbnail:
      'https://images.unsplash.com/photo-1531415074968-036ba1b575da?auto=format&fit=crop&w=900&q=80',
    score: 94
  },
  {
    id: 2,
    source: 'news',
    title: 'India’s next generation of fast bowlers',
    description: 'Why pace, data and fitness are reshaping the game.',
    creator_or_brand: 'The Sporting Post',
    tags: ['cricket', 'fitness', 'india'],
    thumbnail:
      'https://images.unsplash.com/photo-1624526267942-ab0ff8a3e972?auto=format&fit=crop&w=900&q=80',
    score: 89
  },
  {
    id: 3,
    source: 'shopping',
    title: 'Pro Grip Cricket Bat',
    description:
      'Engineered for a lighter pickup and powerful stroke play.',
    creator_or_brand: 'Willow & Co.',
    tags: ['cricket', 'batting', 'equipment'],
    thumbnail:
      'https://images.unsplash.com/photo-1589801258579-18e091f4ca26?auto=format&fit=crop&w=900&q=80',
    score: 84
  },
  {
    id: 4,
    source: 'instagram',
    title: 'Morning mobility for athletes',
    description:
      'Five moves to keep your shoulders and hips game-ready.',
    creator_or_brand: '@movebetter',
    tags: ['fitness', 'sports', 'training'],
    thumbnail:
      'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?auto=format&fit=crop&w=900&q=80',
    score: 78
  },
  {
    id: 5,
    source: 'youtube',
    title: 'Python in 60 minutes',
    description:
      'Build a data project from a clean notebook.',
    creator_or_brand: 'Code Atlas',
    tags: ['python', 'programming', 'technology'],
    thumbnail:
      'https://images.unsplash.com/photo-1515879218367-8466d910aaa4?auto=format&fit=crop&w=900&q=80',
    score: 76
  },
  {
    id: 6,
    source: 'news',
    title: 'AI is changing the way we watch sport',
    description:
      'The small models behind a more personal match day.',
    creator_or_brand: 'Signal Daily',
    tags: ['ai', 'technology', 'sports'],
    thumbnail:
      'https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=900&q=80',
    score: 72
  }
];

let s = {
  page: 'home',
  items: demo,
  recs: demo.slice(0, 4),
  filter: 'all',
  search: '',
  online: false,
  loggedIn: false,
  user: null,
  users: [],
  authMode: 'signin',
  profile: [
    ['cricket', 1],
    ['sports', 0.82],
    ['batting', 0.71],
    ['fitness', 0.42],
    ['india', 0.26]
  ]
};

const names = {
  youtube: 'YouTube',
  instagram: 'Instagram',
  shopping: 'Shopping',
  news: 'News'
};

const icons = {
  youtube: '▶',
  instagram: '◎',
  shopping: '◇',
  news: '✦'
};

const safe = v =>
  String(v || '').replace(
    /[&<>'"]/g,
    c => ({
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      "'": '&#39;',
      '"': '&quot;'
    }[c])
  );

function platform(x) {
  let url = (x.url || '').toLowerCase();
  let source = (x.source || '').toLowerCase();

  if (source !== 'demo' && names[source]) {
    return source;
  }

  if (url.includes('youtube.com') || url.includes('youtu.be')) {
    return 'youtube';
  }

  if (url.includes('instagram.com')) {
    return 'instagram';
  }

  if (
    source === 'shopping' ||
    url.includes('/products/') ||
    url.includes('shop.')
  ) {
    return 'shopping';
  }

  return 'news';
}

function card(x, n = '') {
  let source = platform(x);

  return `
    <article class="card">

      <div class="image">

        <img 
          src="${safe(x.thumbnail || x.image_url)}" 
          alt=""
        >

        <span class="platform ${source}">
          ${icons[source] || '✦'}
          ${names[source] || 'For you'}
        </span>

        ${
          n
            ? `<span class="rank">#${n}</span>`
            : ''
        }

      </div>

      <div class="cardBody">

        <div class="cardMeta">
          <span>
            ${safe(x.creator_or_brand || 'Recommended for you')}
          </span>

          <b>
            ${Math.round(x.score || 78)}% match
          </b>
        </div>

        <h3>
          ${safe(x.title)}
        </h3>

        <p>
          ${safe(x.description)}
        </p>

        <div class="tags">
          ${(x.tags || [])
            .slice(0, 3)
            .map(t => `<span>#${safe(t)}</span>`)
            .join('')}
        </div>

        <div class="actions">

          <button
            data-action="like"
            data-id="${x.id}"
          >
            ♡ Like
          </button>

          <button
            data-action="save"
            data-id="${x.id}"
          >
            ⌑ Save
          </button>

          <button
            data-action="dislike"
            data-id="${x.id}"
          >
            ×
          </button>

          <a
            href="${safe(x.url || '#')}"
            target="_blank"
          >
            Open ↗
          </a>

        </div>

      </div>

    </article>
  `;
}

function head(text) {
  let first = (s.user?.username || 'Alex').split('_')[0];

  return `
    <header>

      <div>

        <p class="eyebrow">
          ${
            s.page === 'home'
              ? 'GOOD MORNING, ' + first.toUpperCase()
              : 'PERSONALIZED DISCOVERY'
          }
        </p>

        <h1>
          ${text}
        </h1>

      </div>

      <div class="headerRight">

        <span class="status ${s.online ? 'live' : ''}">
          ● ${s.online ? 'Live connection' : 'Demo mode'}
        </span>

        <button
          class="headerLogout"
          data-logout
        >
          Log out ↗
        </button>

      </div>

    </header>
  `;
}

function home() {
  return `
    ${head('Find your next <em>favourite thing.</em>')}

    <section class="hero">

      <div>

        <span class="pill">
          ✦ Built around you
        </span>

        <h2>
          A feed that follows<br>
          your <em>curiosity.</em>
        </h2>

        <p>
          One intelligent stream, shaped by what you enjoy across every platform.
        </p>

        <button
          class="primary"
          data-page="explore"
        >
          Explore all content
          <span>→</span>
        </button>

      </div>

      <div class="orbit">

        <div class="orbitCore">
          FOR<br>
          YOU
        </div>

        <i class="o1">▶</i>
        <i class="o2">✦</i>
        <i class="o3">◎</i>
        <i class="o4">◇</i>

      </div>

    </section>

    <section class="sectionHead">

      <div>

        <p class="eyebrow">
          YOUR PERSONAL MIX
        </p>

        <h2>
          Picked for you <span>✦</span>
        </h2>

      </div>

      <button
        class="textButton"
        data-page="explore"
      >
        View all →
      </button>

    </section>

    <div class="cards">

      ${s.recs
        .slice(0, 8)
        .map((x, i) => card(x, i + 1))
        .join('')}

    </div>
  `;
}

function explore() {
  const list = s.items.filter(
    x =>
      (s.filter === 'all' || platform(x) === s.filter) &&
      `${x.title} ${(x.tags || []).join(' ')}`
        .toLowerCase()
        .includes(s.search.toLowerCase())
  );

  return `
    ${head('Explore everything.')}

    <div class="tools">

      <div class="search">

        ⌕

        <input
          id="search"
          value="${safe(s.search)}"
          placeholder="Search things to discover"
        >

      </div>

      <div class="filters">

        ${['all', 'youtube', 'instagram', 'shopping', 'news']
          .map(
            x => `
              <button
                data-filter="${x}"
                class="${s.filter === x ? 'selected' : ''}"
              >
                ${x === 'all' ? 'All sources' : names[x]}
              </button>
            `
          )
          .join('')}

      </div>

    </div>

    <p class="resultCount">
      ${list.length} things waiting to be discovered
    </p>

    <div class="cards exploreCards">

      ${list.map(x => card(x)).join('')}

    </div>
  `;
}

function interests() {
  let max = Math.max(
    ...s.profile.map(x => x[1]),
    1
  );

  return `
    ${head('What inspires you.')}

    <section class="insight">

      <div>

        <span class="pill">
          ◌ YOUR INTEREST PROFILE
        </span>

        <h2>
          Every interaction<br>
          tells a <em>story.</em>
        </h2>

        <p>
          These themes are learned from what you like, save and spend time with —
          then expanded through our tag graph.
        </p>

      </div>

      <div class="interestPulse">

        <b>89%</b>

        <span>
          PROFILE<br>
          CONFIDENCE
        </span>

      </div>

    </section>

    <section class="sectionHead">

      <div>

        <p class="eyebrow">
          DIRECT + GRAPH-EXPANDED
        </p>

        <h2>
          Your top signals
        </h2>

      </div>

      <span class="subtle">
        Updated just now
      </span>

    </section>

    <div class="interestList">

      ${s.profile
        .map(
          (x, i) => `
            <div class="interestRow">

              <span class="number">
                0${i + 1}
              </span>

              <b>
                #${safe(x[0])}
              </b>

              <div class="bar">
                <i
                  style="width:${(x[1] / max) * 100}%"
                ></i>
              </div>

              <strong>
                ${Math.round((x[1] / max) * 100)}%
              </strong>

              <span class="kind">
                ${i < 3 ? 'Direct signal' : 'Graph discovery'}
              </span>

            </div>
          `
        )
        .join('')}

    </div>
  `;
}

function graph() {
  let nodes = [
    ['cricket', 50, 51, 1],
    ['sports', 50, 16],
    ['batting', 20, 77],
    ['fitness', 82, 69],
    ['india', 78, 23],
    ['technology', 18, 25]
  ];

  let edges = [
    [50, 51, 50, 16],
    [50, 51, 20, 77],
    [50, 51, 82, 69],
    [50, 51, 78, 23],
    [50, 16, 78, 23],
    [18, 25, 50, 16]
  ];

  return `
    ${head('The map behind your feed.')}

    <div class="graphIntro">

      <span class="pill">
        ◌ WEIGHTED TAG GRAPH
      </span>

      <p>
        Nodes are interests. Lines are relationships.
        Thicker, warmer lines mean stronger connections.
      </p>

    </div>

    <section class="graphPanel">

      <div class="graphCanvas">

        <svg
          viewBox="0 0 100 100"
          preserveAspectRatio="none"
        >

          ${edges
            .map(
              (x, i) => `
                <line
                  x1="${x[0]}"
                  y1="${x[1]}"
                  x2="${x[2]}"
                  y2="${x[3]}"
                  stroke="${i < 3 ? '#ea754a' : '#bcc7c8'}"
                  stroke-width="${i < 3 ? '1.15' : '.55'}"
                />
              `
            )
            .join('')}

        </svg>

        ${nodes
          .map(
            x => `
              <div
                class="node ${x[3] ? 'focus' : ''}"
                style="left:${x[1]}%;top:${x[2]}%"
              >
                <span>
                  ${x[0]}
                </span>
              </div>
            `
          )
          .join('')}

      </div>

      <div class="legend">

        <p class="eyebrow">
          GRAPH INSIGHT
        </p>

        <h3>
          Cricket is your<br>
          <em>strongest hub.</em>
        </h3>

        <p>
          It connects your direct interest in batting
          with inferred interests like fitness and India.
        </p>

        <div class="stat">
          <b>${s.profile.length}</b>
          <span>active interests</span>
        </div>

        <div class="stat">
          <b>12</b>
          <span>weighted connections</span>
        </div>

      </div>

    </section>
  `;
}

function loginScreen() {
  let isRegister = s.authMode === 'register';

  document.querySelector('#app').innerHTML = `
    <main class="loginPage">

      <section class="loginArt">

        <div class="brand">

          <span class="brandMark">
            N
          </span>

          <span>
            NEXUS
          </span>

        </div>

        <div class="loginCopy">

          <span class="pill">
            ✦ SMART RECOMMENDATIONS
          </span>

          <h1>
            Discover what<br>
            moves <em>you.</em>
          </h1>

          <p>
            Sign in to generate a personal feed from your interests,
            interactions, and the weighted tag graph.
          </p>

        </div>

        <div class="loginOrbit">

          <b>YOU</b>

          <i>▶</i>
          <i>◎</i>
          <i>✦</i>

        </div>

      </section>

      <section class="loginFormWrap">

        <form
          id="loginForm"
          class="loginForm"
        >

          <p class="eyebrow">
            ${isRegister ? 'CREATE YOUR ACCOUNT' : 'WELCOME BACK'}
          </p>

          <h2>
            ${
              isRegister
                ? 'Start your <em>discovery.</em>'
                : 'Let’s make your feed<br><em>personal.</em>'
            }
          </h2>

          <p class="loginHint">
            ${
              isRegister
                ? 'Create an account to save your interests and receive personal recommendations.'
                : 'Sign in to continue with your saved recommendation profile.'
            }
          </p>

          <label for="username">
            Username
          </label>

          <input
            id="username"
            autocomplete="username"
            minlength="3"
            required
            placeholder="e.g. alex_kumar"
          >

          ${
            isRegister
              ? `
                <label for="email">
                  Email address
                </label>

                <input
                  id="email"
                  type="email"
                  autocomplete="email"
                  required
                  placeholder="you@example.com"
                >
              `
              : ''
          }

          <label for="password">
            Password
          </label>

          <input
            id="password"
            type="password"
            autocomplete="${isRegister ? 'new-password' : 'current-password'}"
            minlength="8"
            required
            placeholder="At least 8 characters"
          >

          <button
            class="primary"
            type="submit"
          >
            ${isRegister ? 'Create account' : 'Sign in'}
            <span>→</span>
          </button>

          <p
            id="authMessage"
            class="authMessage"
          ></p>

          <p class="loginStatus ${s.online ? 'live' : ''}">
            ● ${
              s.online
                ? 'Backend connected'
                : 'Backend not reachable — start the API first'
            }
          </p>

          <button
            class="authSwitch"
            type="button"
            data-auth-mode="${isRegister ? 'signin' : 'register'}"
          >
            ${
              isRegister
                ? 'Already have an account? Sign in'
                : 'New here? Create an account'
            }
          </button>

        </form>

      </section>

    </main>
  `;

  document.querySelector('#loginForm').onsubmit = submitAuth;

  document.querySelector('[data-auth-mode]').onclick = e => {
    s.authMode = e.currentTarget.dataset.authMode;
    render();
  };
}

async function submitAuth(event) {
  event.preventDefault();

  let username =
    document.querySelector('#username').value.trim();

  let password =
    document.querySelector('#password').value;

  let message =
    document.querySelector('#authMessage');

  let isRegister =
    s.authMode === 'register';

  let body = {
    username,
    password
  };

  if (isRegister) {
    body.email =
      document.querySelector('#email').value.trim();
  }

  message.textContent =
    isRegister
      ? 'Creating your account…'
      : 'Checking your account…';

  message.classList.remove('error');

  try {
    let response = await fetch(
      `${API}/auth/${isRegister ? 'register' : 'login'}`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
      }
    );

    let data = await response.json();

    if (!response.ok) {
      throw Error(
        data.detail || 'Unable to sign in.'
      );
    }

    s.user = data;
    s.loggedIn = true;

    localStorage.setItem(
      'nexusUser',
      JSON.stringify(data)
    );

    await load();

  } catch (error) {

    message.textContent =
      error.message ||
      'Unable to reach the backend. Please try again.';

    message.classList.add('error');
  }
}

function logout() {
  localStorage.removeItem('nexusUser');

  s.loggedIn = false;
  s.user = null;
  s.page = 'home';

  render();
}


/* =========================================================
   LIKE / SAVE / DISLIKE
   ========================================================= */

async function interaction(item_id, interactionType) {

  /*
    Correct message for each button
  */

  let messageText = '';

  if (interactionType === 'like') {
    messageText = 'Liked! Your preference has been recorded.';
  }

  else if (interactionType === 'save') {
    messageText = 'Saved! This item was added to your saved preferences.';
  }

  else if (interactionType === 'dislike') {
    messageText = 'Thanks! We’ll show you less like this.';
  }

  else {
    messageText = 'Your preference has been recorded.';
  }


  /*
    Show correct message immediately
  */

  alert(messageText);


  /*
    Send interaction to backend
  */

  try {

    const response = await fetch(
      `${API}/interactions`,
      {
        method: 'POST',

        headers: {
          'Content-Type': 'application/json'
        },

        body: JSON.stringify({
          user_id: s.user.id,
          item_id: item_id,
          interaction_type: interactionType
        })
      }
    );


    /*
      Check backend response
    */

    if (!response.ok) {

      let errorData;

      try {
        errorData = await response.json();
      } catch {
        errorData = {};
      }

      console.error(
        'Interaction failed:',
        errorData
      );

      alert(
        errorData.detail ||
        'Could not save your preference.'
      );

      return;
    }


    /*
      Reload recommendations and interests
      after successful interaction.
    */

    await load();

  }

  catch (error) {

    console.error(
      'Interaction error:',
      error
    );

    /*
      Backend may temporarily be unavailable.
      The UI still remains usable.
    */

  }
}


/* =========================================================
   LOAD DATA FROM BACKEND
   ========================================================= */

async function load() {

  try {

    let [
      itemsResponse,
      recommendationsResponse,
      interestsResponse
    ] = await Promise.all([

      fetch(
        `${API}/items?limit=50`
      ),

      fetch(
        `${API}/recommendations?user_id=${s.user.id}&limit=24`
      ),

      fetch(
        `${API}/users/${s.user.id}/expanded-interests`
      )

    ]);


    /*
      Items + recommendations are required
    */

    if (
      !itemsResponse.ok ||
      !recommendationsResponse.ok
    ) {
      throw new Error(
        'Failed to load recommendation data'
      );
    }


    /*
      Load items
    */

    s.items =
      await itemsResponse.json();


    /*
      Load recommendations
    */

    let rec =
      await recommendationsResponse.json();


    s.recs =
      rec.recommendations.map(
        x => ({
          ...x.item,
          score: x.score
        })
      );


    /*
      Load expanded interests
    */

    if (interestsResponse.ok) {

      let interests =
        await interestsResponse.json();

      /*
        If backend has interests,
        use them.
      */

      if (Array.isArray(interests) && interests.length > 0) {

        s.profile =
          interests.map(
            x => [
              x.tag,
              x.score
            ]
          );

      }

    }


    /*
      Backend is working
    */

    s.online = true;

  }

  catch (error) {

    console.error(
      'Load error:',
      error
    );

    /*
      Keep demo data if backend fails.
    */

    s.online = false;
  }


  render();
}


/* =========================================================
   PROFILE MODAL
   ========================================================= */

function openProfile() {

  let existing =
    document.querySelector('.profileOverlay');

  if (existing) {
    return;
  }

  let top =
    s.profile
      .slice(0, 3)
      .map(
        x =>
          `<span>#${safe(x[0])}</span>`
      )
      .join('');

  let initial =
    (s.user.username || 'A')
      .slice(0, 2)
      .toUpperCase();

  let modal =
    document.createElement('div');

  modal.className =
    'profileOverlay';

  modal.innerHTML = `

    <section
      class="profileModal"
      role="dialog"
      aria-modal="true"
      aria-label="Your profile"
    >

      <button
        class="closeProfile"
        aria-label="Close profile"
      >
        ×
      </button>

      <div class="largeProfileDot">
        ${initial}
      </div>

      <p class="eyebrow">
        YOUR NEXUS PROFILE
      </p>

      <h2>
        ${safe(s.user.username)}
      </h2>

      <p class="profileEmail">
        ${safe(
          s.user.email ||
          'Personalized discovery account'
        )}
      </p>

      <div class="profileStats">

        <div>
          <b>${s.profile.length}</b>
          <span>interests</span>
        </div>

        <div>
          <b>1</b>
          <span>active feed</span>
        </div>

        <div>
          <b>${s.online ? 'Live' : 'Demo'}</b>
          <span>connection</span>
        </div>

      </div>

      <p class="profileLabel">
        YOUR STRONGEST SIGNALS
      </p>

      <div class="profileTags">
        ${top}
      </div>

      <button
        class="primary profileGo"
      >
        View my interests
        <span>→</span>
      </button>

      <button
        class="logoutButton"
        type="button"
      >
        Log out
      </button>

    </section>
  `;

  document.body.append(modal);

  modal.querySelector(
    '.closeProfile'
  ).onclick = () => modal.remove();

  modal.onclick = e => {

    if (e.target === modal) {
      modal.remove();
    }

  };

  modal.querySelector(
    '.profileGo'
  ).onclick = () => {

    modal.remove();

    s.page = 'interests';

    render();
  };

  modal.querySelector(
    '.logoutButton'
  ).onclick = () => {

    localStorage.removeItem(
      'nexusUser'
    );

    s.loggedIn = false;
    s.user = null;

    modal.remove();

    render();
  };
}


/* =========================================================
   RENDER APPLICATION
   ========================================================= */

function render() {

  /*
    If user is not logged in,
    show login/register screen.
  */

  if (!s.loggedIn) {

    loginScreen();

    return;
  }


  /*
    Sidebar navigation
  */

  let nav = [
    ['home', '⌂', 'Home'],
    ['explore', '⌕', 'Explore'],
    ['interests', '◒', 'My interests'],
    ['graph', '◌', 'Tag graph']
  ];


  let initial =
    (s.user.username || 'A')
      .slice(0, 2)
      .toUpperCase();


  document.querySelector('#app').innerHTML = `

    <div class="app">

      <aside>

        <div class="brand">

          <span class="brandMark">
            N
          </span>

          <span>
            NEXUS
          </span>

        </div>

        <p class="eyebrow">
          SMART DISCOVERY
        </p>

        <nav>

          ${nav
            .map(
              x => `
                <button
                  data-page="${x[0]}"
                  class="${s.page === x[0] ? 'active' : ''}"
                >
                  <span>${x[1]}</span>
                  ${x[2]}
                </button>
              `
            )
            .join('')}

        </nav>

        <button
          class="sideBottom profileButton"
          data-profile
          aria-label="Open profile"
        >

          <div class="profileDot">
            ${initial}
          </div>

          <div>

            <b>
              ${safe(s.user.username)}
            </b>

            <small>
              Curious explorer
            </small>

          </div>

          <span class="dots">
            •••
          </span>

        </button>

      </aside>

      <main>

        ${
          {
            home,
            explore,
            interests,
            graph
          }[s.page]()
        }

      </main>

    </div>
  `;


  /*
    Page navigation
  */

  document
    .querySelectorAll('[data-page]')
    .forEach(x => {

      x.onclick = () => {

        s.page =
          x.dataset.page;

        render();

      };

    });


  /*
    Filter buttons
  */

  document
    .querySelectorAll('[data-filter]')
    .forEach(x => {

      x.onclick = () => {

        s.filter =
          x.dataset.filter;

        render();

      };

    });


  /*
    Search
  */

  let input =
    document.querySelector('#search');

  if (input) {

    input.oninput = e => {

      s.search =
        e.target.value;

      render();

      let newInput =
        document.querySelector('#search');

      if (newInput) {

        newInput.focus();

        newInput.selectionStart =
          newInput.value.length;

        newInput.selectionEnd =
          newInput.value.length;

      }

    };

  }


  /*
    LIKE / SAVE / DISLIKE buttons
  */

  document
    .querySelectorAll('[data-action]')
    .forEach(x => {

      x.onclick = () => {

        interaction(
          Number(x.dataset.id),
          x.dataset.action
        );

      };

    });


  /*
    Profile button
  */

  let profileButton =
    document.querySelector(
      '[data-profile]'
    );

  if (profileButton) {

    profileButton.onclick =
      openProfile;

  }


  /*
    Logout
  */

  let logoutButton =
    document.querySelector(
      '[data-logout]'
    );

  if (logoutButton) {

    logoutButton.onclick =
      logout;

  }
}


/* =========================================================
   APPLICATION START
   ========================================================= */

async function boot() {

  /*
    Check backend health
  */

  try {

    let r =
      await fetch(
        `${API}/health`
      );

    if (!r.ok) {
      throw new Error(
        'Backend unavailable'
      );
    }

    s.online = true;

  }

  catch {

    s.online = false;

  }


  /*
    Check whether a user is already logged in
  */

  let saved =
    localStorage.getItem(
      'nexusUser'
    );


  if (saved) {

    try {

      s.user =
        JSON.parse(saved);

      s.loggedIn = true;

      await load();

      return;

    }

    catch {

      localStorage.removeItem(
        'nexusUser'
      );

    }

  }


  /*
    Show login screen
  */

  render();
}


/*
  Start application
*/

boot();