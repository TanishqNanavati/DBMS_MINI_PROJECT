// Content script - extracts page content

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.action === 'extract') {
    const title = document.title;
    const url = window.location.href;
    
    // Get main content
    let content = '';
    const main = document.querySelector('main') || 
                 document.querySelector('article') || 
                 document.body;
    
    content = getTextFromElement(main);
    
    if (content.length < 100) {
      return; // Skip short pages
    }
    
    // Send to background
    chrome.runtime.sendMessage({
      action: 'ingest',
      data: {
        profile_id: msg.profileId,
        url: url,
        title: title,
        content: content
      }
    });
  }
});

function getTextFromElement(element) {
  const skip = ['SCRIPT', 'STYLE', 'NOSCRIPT', 'IFRAME'];
  if (skip.includes(element.tagName)) return '';
  
  let text = '';
  for (const node of element.childNodes) {
    if (node.nodeType === Node.TEXT_NODE) {
      text += node.textContent + ' ';
    } else if (node.nodeType === Node.ELEMENT_NODE) {
      text += getTextFromElement(node) + ' ';
    }
  }
  return text.replace(/\s+/g, ' ').trim();
}