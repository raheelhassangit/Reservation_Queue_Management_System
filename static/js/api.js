const API_BASE = "http://127.0.0.1:8000/api";

function saveTokens(data) {
  localStorage.setItem("access", data.access);
  if (data.refresh) localStorage.setItem("refresh", data.refresh);
}

function getAccessToken() {
  return localStorage.getItem("access");
}

function logout() {
  localStorage.removeItem("access");
  localStorage.removeItem("refresh");
  window.location.href = "/login/";
}

async function refreshAccessToken() {
  const refresh = localStorage.getItem("refresh");
  if (!refresh) return null;

  const res = await fetch(API_BASE + "/token/refresh/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh }),
  });
  if (!res.ok) return null;

  const data = await res.json();
  localStorage.setItem("access", data.access);
  return data.access;
}

async function apiFetch(path, options = {}) {
    let token = getAccessToken();
    const doFetch = (tok) => {
        const headers = { "Content-Type": "application/json", ...options.headers };
        if (tok) headers["Authorization"] = "Bearer " + tok;
        return fetch(API_BASE + path, { ...options, headers });
    };

    let res = await doFetch(token);

    if (res.status === 401) {
        const newToken = await refreshAccessToken();
        if (!newToken) {
            logout();
            throw new Error("Session expired");
        }
        res = await doFetch(newToken);
    }

    if (res.status === 429) {
        const retryAfter = res.headers.get("Retry-After");
        alert(`Too many requests — please wait ${retryAfter || "a moment"} and try again.`);
    }

    return res;
}