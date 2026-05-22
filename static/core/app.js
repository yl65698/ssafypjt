const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

const state = {
  user: null,
  selectedGameId: null,
  selectedGameTitle: "",
};

async function api(path, options = {}) {
  const response = await fetch(path, {
    credentials: "same-origin",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
      ...(options.headers || {}),
    },
    ...options,
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "요청에 실패했습니다." }));
    throw new Error(error.detail || "요청에 실패했습니다.");
  }
  return response.json();
}

function showView(name) {
  document.querySelectorAll(".view").forEach((view) => view.classList.add("hidden"));
  document.querySelector(`#${name}-view`).classList.remove("hidden");
  document.querySelector("#app-nav").classList.toggle("hidden", name === "welcome" || name === "auth");
  window.scrollTo({ top: 0, behavior: "smooth" });
  if (name === "profile") loadProfile();
  if (name === "gear") loadProducts();
}

function formatPrice(value) {
  return `₩${Number(value).toLocaleString("ko-KR")}`;
}

function historyFromPrice(bestPrice, points = 8) {
  const current = bestPrice?.current_price || 30000;
  const original = bestPrice?.original_price || current * 1.6;
  const low = bestPrice?.historical_low || current * 0.8;
  return Array.from({ length: points }, (_, index) => {
    const wave = Math.sin(index * 1.35) * 0.13;
    const trend = original - ((original - current) / Math.max(points - 1, 1)) * index;
    const value = Math.max(low, Math.round(trend * (1 + wave)));
    return value;
  });
}

function drawLineChart(canvas, values, color = "#57b7ff") {
  const ctx = canvas.getContext("2d");
  const width = canvas.width = canvas.clientWidth * devicePixelRatio;
  const height = canvas.height = canvas.clientHeight * devicePixelRatio;
  ctx.scale(devicePixelRatio, devicePixelRatio);
  const w = canvas.clientWidth;
  const h = canvas.clientHeight;
  ctx.clearRect(0, 0, w, h);
  const min = Math.min(...values);
  const max = Math.max(...values);
  const pad = 22;
  const range = Math.max(max - min, 1);

  ctx.strokeStyle = "rgba(255,255,255,0.08)";
  ctx.lineWidth = 1;
  for (let i = 0; i < 4; i += 1) {
    const y = pad + ((h - pad * 2) / 3) * i;
    ctx.beginPath();
    ctx.moveTo(pad, y);
    ctx.lineTo(w - pad, y);
    ctx.stroke();
  }

  ctx.strokeStyle = color;
  ctx.lineWidth = 3;
  ctx.beginPath();
  values.forEach((value, index) => {
    const x = pad + ((w - pad * 2) / (values.length - 1)) * index;
    const y = h - pad - ((value - min) / range) * (h - pad * 2);
    if (index === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  });
  ctx.stroke();

  ctx.fillStyle = "#f4f1e8";
  ctx.font = "12px Arial";
  ctx.fillText(formatPrice(max), pad, 16);
  ctx.fillText(formatPrice(min), pad, h - 6);
}

function gameCard(game) {
  const price = game.best_price;
  const status = game.buy_status;
  const tags = game.tags.map((tag) => `<span class="pill">${tag.name}</span>`).join("");
  return `
    <article class="card game-card" data-game-id="${game.id}">
      <img src="${game.image_url}" alt="${game.title}">
      <div class="card-body">
        <span class="status ${status.status}">${status.status}</span>
        <h4>${game.title}</h4>
        <p>${game.genre} · ${game.platforms}</p>
        <p>${price ? `${formatPrice(price.current_price)} / ${price.discount_rate}% 할인` : "가격 정보 없음"}</p>
        <div class="pill-row">${tags}</div>
      </div>
    </article>
  `;
}

function productCard(product, extra = "") {
  return `
    <article class="card product-card" data-product-id="${product.id}">
      <img src="${product.image_url}" alt="${product.name}">
      <div class="card-body">
        <span class="pill">${product.category}</span>
        <h4>${product.name}</h4>
        <p>${product.brand} · ${product.mall_name}</p>
        <p>${formatPrice(product.price)}</p>
        ${extra}
      </div>
    </article>
  `;
}

function bindCards() {
  document.querySelectorAll("[data-game-id]").forEach((element) => {
    element.addEventListener("click", () => loadGameDetail(element.dataset.gameId));
  });
  document.querySelectorAll("[data-product-id]").forEach((element) => {
    element.addEventListener("click", () => loadProductDetail(element.dataset.productId));
  });
}

async function loadDashboard() {
  const data = await api("/api/dashboard/");
  document.querySelector("#dashboard-grid").innerHTML = data.buy_now.map(gameCard).join("");
  document.querySelector("#game-grid").innerHTML = data.recommended.map(gameCard).join("");
  bindCards();
}

async function loadGames(query = "") {
  const data = await api(`/api/games/${query ? `?q=${encodeURIComponent(query)}` : ""}`);
  document.querySelector("#game-grid").innerHTML = data.map(gameCard).join("");
  bindCards();
}

async function loadProducts(query = "") {
  const data = await api(`/api/products/${query ? `?q=${encodeURIComponent(query)}` : ""}`);
  document.querySelector("#product-grid").innerHTML = data.map((product) => productCard(product)).join("");
  bindCards();
}

async function loadGameDetail(id) {
  state.selectedGameId = id;
  const game = await api(`/api/games/${id}/`);
  state.selectedGameTitle = game.title;
  showView("game-detail");

  const history = historyFromPrice(game.best_price, 10);
  const prices = game.prices.map((price) => `
    <div class="price-row">
      <strong>${price.store.name}</strong>
      <span>${formatPrice(price.current_price)} · ${price.discount_rate}% 할인</span>
      <a class="small-button" href="${price.purchase_url}" target="_blank" rel="noreferrer">게임 구매</a>
    </div>
  `).join("");
  const requirements = game.requirements.map((req) => `
    <div class="spec-row">
      <strong>${req.type === "recommended" ? "권장" : "최소"} 사양</strong>
      <span>CPU ${req.cpu}, GPU ${req.gpu}, RAM ${req.ram_gb}GB, 저장공간 ${req.storage_gb}GB</span>
    </div>
  `).join("");

  document.querySelector("#game-detail").innerHTML = `
    <img class="detail-cover" src="${game.image_url}" alt="${game.title}">
    <div class="detail-title">
      <div>
        <p class="eyebrow">${game.genre}</p>
        <h2>${game.title}</h2>
      </div>
      <button id="own-game-button" type="button">내 게임에 추가</button>
    </div>
    <p class="muted">${game.description}</p>
    <div class="pill-row">${game.tags.map((tag) => `<span class="pill">${tag.name}</span>`).join("")}</div>

    <section class="report-block">
      <h3>가격 변동 추이</h3>
      <canvas id="game-price-chart" class="line-chart"></canvas>
    </section>

    <section class="report-grid">
      <article>
        <h3>가격 비교</h3>
        <div class="price-list">${prices}</div>
      </article>
      <article>
        <h3>구매 타이밍</h3>
        <p><span class="status ${game.buy_status.status}">${game.buy_status.status}</span> ${game.buy_status.score}점</p>
        <p class="muted">${game.buy_status.reason}</p>
      </article>
      <article>
        <h3>가격 예측</h3>
        <p>${game.price_prediction.summary}</p>
      </article>
      <article>
        <h3>장비 요구사항</h3>
        ${requirements}
      </article>
    </section>
  `;
  drawLineChart(document.querySelector("#game-price-chart"), history);
  document.querySelector("#own-game-button").addEventListener("click", addSelectedGame);
  await loadPlayability(id);
}

async function loadPlayability(id) {
  const data = await api(`/api/games/${id}/playability/`);
  const recommendations = await api(`/api/games/${id}/gear-recommendations/`);
  const targets = data.targets.map((target) => `<p><strong>${target.name}</strong> ${target.status}</p>`).join("");
  const gears = recommendations.map((item) => productCard(item, `<p class="muted">${item.reason}</p>`)).join("");
  document.querySelector("#gear-check").innerHTML = `
    <h3>내 장비로 가능할까?</h3>
    <p><span class="status WATCH">${data.label}</span> ${data.score}점</p>
    <p class="muted">${data.summary}</p>
    <div class="target-list">${targets}</div>
    <div class="button-row">
      <button data-view="gear" type="button">필요한 장비 구매하기</button>
      <button class="secondary-button" data-view="device" type="button">내 장비 정보 업데이트</button>
    </div>
    <h3>추천 업그레이드</h3>
    <div class="side-card-list">${gears}</div>
  `;
  bindViewButtons();
  bindCards();
}

async function loadProductDetail(id) {
  const product = await api(`/api/products/${id}/`);
  showView("product-detail");
  const history = historyFromPrice({
    current_price: product.price,
    original_price: Math.round(product.price * 1.22),
    historical_low: Math.round(product.price * 0.84),
  }, 9);
  document.querySelector("#product-detail").innerHTML = `
    <div class="product-layout">
      <img class="detail-cover" src="${product.image_url}" alt="${product.name}">
      <div>
        <p class="eyebrow">${product.category}</p>
        <h2>${product.name}</h2>
        <p class="muted">${product.brand} · ${product.mall_name}</p>
        <p class="big-price">${formatPrice(product.price)}</p>
        <a class="primary-button" href="${product.product_url}" target="_blank" rel="noreferrer">구매 페이지로 이동</a>
      </div>
    </div>
    <section class="report-block">
      <h3>장비 가격 추이</h3>
      <canvas id="product-price-chart" class="line-chart"></canvas>
    </section>
    <section class="report-grid">
      <article>
        <h3>가격 비교</h3>
        <div class="price-row"><strong>Naver Shopping</strong><span>${formatPrice(product.price)}</span><a class="small-button" href="${product.product_url}" target="_blank" rel="noreferrer">구매</a></div>
        <div class="price-row"><strong>Partner Mall</strong><span>${formatPrice(Math.round(product.price * 1.04))}</span><span class="pill">비교</span></div>
      </article>
      <article>
        <h3>구매 타이밍</h3>
        <p><span class="status BUY">BUY</span> 현재 시세 기준 합리적인 가격입니다.</p>
      </article>
      <article>
        <h3>추천 이유</h3>
        <p>현재 선택한 게임의 목표 환경을 맞추기 위한 업그레이드 후보입니다.</p>
      </article>
      <article>
        <h3>적합한 환경</h3>
        <p>FHD 고주사율 또는 QHD 게이밍 환경에 적합합니다.</p>
      </article>
    </section>
  `;
  drawLineChart(document.querySelector("#product-price-chart"), history, "#8ed35f");
}

async function addSelectedGame() {
  if (!state.user) {
    showView("auth");
    return;
  }
  try {
    await api("/api/me/games/", {
      method: "POST",
      body: JSON.stringify({ game_id: Number(state.selectedGameId), status: "playing", is_favorite: true }),
    });
    alert(`${state.selectedGameTitle}을(를) 내 게임에 추가했습니다.`);
  } catch (error) {
    alert("이미 추가된 게임이거나 저장할 수 없습니다.");
  }
}

async function refreshAuth() {
  const data = await api("/api/accounts/me/");
  state.user = data.is_authenticated ? data.user : null;
  if (state.user) {
    document.querySelector("#auth-message").textContent = `${state.user.email} 계정으로 로그인 중입니다.`;
    showView("dashboard");
  }
}

async function loadProfile() {
  if (!state.user) {
    showView("auth");
    return;
  }
  const [games, devices, dna] = await Promise.all([
    api("/api/me/games/"),
    api("/api/me/devices/"),
    api("/api/me/play-dna/"),
  ]);
  document.querySelector("#owned-games").innerHTML = games.length
    ? games.map((item) => `<div class="list-row"><strong>${item.game.title}</strong><span>${item.status}</span></div>`).join("")
    : `<p class="muted">아직 저장한 게임이 없습니다.</p>`;
  document.querySelector("#owned-devices").innerHTML = devices.length
    ? devices.map((device) => `
      <div class="list-row">
        <strong>${device.gpu}</strong>
        <span>${device.cpu} · RAM ${device.ram_gb}GB · ${device.monitor_resolution} ${device.refresh_rate}Hz</span>
      </div>
    `).join("")
    : `<p class="muted">아직 등록한 장비가 없습니다.</p>`;
  renderDna(dna.scores);
}

function renderDna(scores) {
  document.querySelector("#dna-chart").innerHTML = Object.entries(scores).map(([name, value]) => `
    <div class="dna-row">
      <strong>${name}</strong>
      <div class="bar"><span style="width:${value}%"></span></div>
      <span>${value}%</span>
    </div>
  `).join("");
}

function bindViewButtons() {
  document.querySelectorAll("[data-view]").forEach((button) => {
    button.addEventListener("click", () => {
      const target = button.dataset.view;
      if (button.dataset.demo === undefined && target === "dashboard" && !state.user) {
        showView("auth");
        return;
      }
      if ((target === "profile" || target === "device") && !state.user) {
        showView("auth");
        return;
      }
      showView(target);
    });
  });
}

document.querySelector("#game-search-form").addEventListener("submit", (event) => {
  event.preventDefault();
  loadGames(document.querySelector("#game-query").value);
});

document.querySelector("#product-search-form").addEventListener("submit", (event) => {
  event.preventDefault();
  loadProducts(document.querySelector("#product-query").value);
});

document.querySelector("#ai-search-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const query = document.querySelector("#ai-query").value;
  const data = await api("/api/games/natural-search/", {
    method: "POST",
    body: JSON.stringify({ query }),
  });
  document.querySelector("#game-grid").innerHTML = data.map(gameCard).join("");
  bindCards();
});

document.querySelector("#auth-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = new FormData(event.target);
  try {
    const user = await api("/api/accounts/signup/", {
      method: "POST",
      body: JSON.stringify(Object.fromEntries(form.entries())),
    });
    state.user = user;
    await loadDashboard();
    showView("dashboard");
  } catch (error) {
    document.querySelector("#auth-message").textContent = error.message;
  }
});

document.querySelector("#login-button").addEventListener("click", async () => {
  const form = new FormData(document.querySelector("#auth-form"));
  try {
    const user = await api("/api/accounts/login/", {
      method: "POST",
      body: JSON.stringify(Object.fromEntries(form.entries())),
    });
    state.user = user;
    await loadDashboard();
    showView("dashboard");
  } catch (error) {
    document.querySelector("#auth-message").textContent = error.message;
  }
});

document.querySelector("#logout-button").addEventListener("click", async () => {
  await api("/api/accounts/logout/", { method: "POST", body: "{}" });
  state.user = null;
  showView("welcome");
});

document.querySelector("#device-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!state.user) {
    showView("auth");
    return;
  }
  const values = Object.fromEntries(new FormData(event.target).entries());
  values.ram_gb = Number(values.ram_gb);
  values.storage_gb = Number(values.storage_gb);
  values.refresh_rate = Number(values.refresh_rate);
  await api("/api/me/devices/", { method: "POST", body: JSON.stringify(values) });
  document.querySelector("#device-message").textContent = "장비 정보가 저장되었습니다.";
  if (state.selectedGameId) await loadPlayability(state.selectedGameId);
});

document.querySelector("#dna-button").addEventListener("click", async () => {
  if (!state.user) {
    showView("auth");
    return;
  }
  const data = await api("/api/me/play-dna/");
  renderDna(data.scores);
});

bindViewButtons();
loadDashboard();
loadGames();
loadProducts();
refreshAuth();
