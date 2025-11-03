// Popup UI logic
const enableToggle = document.getElementById('enableToggle');
const profileSelect = document.getElementById('profileSelect');
const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');
const resultsDiv = document.getElementById('results');

let settings = { enabled: false, profileId: 1 };

// Load settings and profiles
chrome.storage.local.get(['settings'], (result) => {
  if (result.settings) {
    settings = result.settings;
    enableToggle.checked = settings.enabled;
  }
  loadProfiles();
});

function loadProfiles() {
  chrome.runtime.sendMessage({ action: 'getProfiles' }, (response) => {
    if (response.success) {
      profileSelect.innerHTML = '';
      response.profiles.forEach(p => {
        const opt = document.createElement('option');
        opt.value = p.id;
        opt.textContent = p.name;
        profileSelect.appendChild(opt);
      });
      if (settings.profileId) {
        profileSelect.value = settings.profileId;
      }
    } else {
      alert('Failed to load profiles. Is backend running?');
    }
  });
}

// Toggle tracking
enableToggle.addEventListener('change', () => {
  settings.enabled = enableToggle.checked;
  chrome.runtime.sendMessage({ action: 'updateSettings', settings });
});

// Profile selection
profileSelect.addEventListener('change', () => {
  settings.profileId = parseInt(profileSelect.value);
  chrome.runtime.sendMessage({ action: 'updateSettings', settings });
});

// Search
searchBtn.addEventListener('click', () => {
  const query = searchInput.value.trim();
  if (!query) {
    alert('Enter a search query');
    return;
  }
  
  chrome.runtime.sendMessage({
    action: 'search',
    query: query,
    profileId: settings.profileId
  }, (response) => {
    if (response.success) {
      displayResults(response.results);
    } else {
      alert('Search failed: ' + response.error);
    }
  });
});

function displayResults(results) {
  resultsDiv.innerHTML = '';
  
  if (results.length === 0) {
    resultsDiv.innerHTML = '<p>No results found</p>';
    return;
  }
  
  results.forEach(r => {
    const div = document.createElement('div');
    div.className = 'result';
    div.innerHTML = `
      <div class="result-title">${r.title || 'Untitled'}</div>
      <div class="result-url">${r.url}</div>
      <div>${r.snippet}...</div>
      <div style="font-size: 12px; color: green;">
        Similarity: ${(r.similarity * 100).toFixed(1)}%
      </div>
    `;
    div.onclick = () => chrome.tabs.create({ url: r.url });
    resultsDiv.appendChild(div);
  });
}