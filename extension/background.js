// Background worker - handles page navigation
const API_URL = 'http://localhost:8000';

let settings = { enabled: false, profileId: 1 };

// Load settings
chrome.storage.local.get(['settings'], (result) => {
  if (result.settings) {
    settings = result.settings;
  }
});

// Listen for page loads
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url && !tab.url.startsWith('chrome://')) {
    if (settings.enabled && settings.profileId) {
      chrome.tabs.sendMessage(tabId, { action: 'extract', profileId: settings.profileId });
    }
  }
});

// Handle messages
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.action === 'ingest') {
    fetch(`${API_URL}/ingest`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(msg.data)
    })
    .then(r => r.json())
    .then(data => sendResponse({ success: true, data }))
    .catch(err => sendResponse({ success: false, error: err.message }));
    return true;
  }
  
  if (msg.action === 'search') {
    fetch(`${API_URL}/search`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: msg.query, profile_id: msg.profileId })
    })
    .then(r => r.json())
    .then(data => sendResponse({ success: true, results: data }))
    .catch(err => sendResponse({ success: false, error: err.message }));
    return true;
  }
  
  if (msg.action === 'getProfiles') {
    fetch(`${API_URL}/profiles`)
    .then(r => r.json())
    .then(data => sendResponse({ success: true, profiles: data }))
    .catch(err => sendResponse({ success: false, error: err.message }));
    return true;
  }
  
  if (msg.action === 'updateSettings') {
    settings = msg.settings;
    chrome.storage.local.set({ settings });
    sendResponse({ success: true });
  }
});