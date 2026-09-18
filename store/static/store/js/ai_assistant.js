document.addEventListener('DOMContentLoaded', function () {
  const chatBody = document.getElementById('aiChatBody');
  const chatForm = document.getElementById('aiChatForm');
  const searchInput = document.getElementById('aiSearchInput');
  const sendBtn = document.getElementById('aiSendBtn');
  const chips = document.querySelectorAll('.ai-chip');

  if (!chatForm || !searchInput || !chatBody) return;

  function scrollToBottom() {
    chatBody.scrollTop = chatBody.scrollHeight;
  }

  function getCsrfToken() {
    const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
    if (csrfInput) return csrfInput.value;
    return '';
  }

  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function formatText(text) {
    if (!text) return '';
    let escaped = escapeHtml(text);
    return escaped
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\n/g, '<br>');
  }

  function appendUserMessage(text) {
    const msgDiv = document.createElement('div');
    msgDiv.className = 'ai-msg ai-msg-user';
    msgDiv.innerHTML = '<div class="ai-avatar ai-avatar-user"><i class="fa fa-user"></i></div><div class="ai-bubble">' + escapeHtml(text) + '</div>';
    chatBody.appendChild(msgDiv);
    scrollToBottom();
  }

  function showLoading() {
    const indicator = document.createElement('div');
    indicator.id = 'aiLoadingIndicator';
    indicator.className = 'ai-msg ai-msg-assistant';
    indicator.innerHTML = '<div class="ai-avatar ai-avatar-bot"><i class="fa fa-robot"></i></div><div class="ai-bubble"><span class="ai-loading-text">Searching store products...</span></div>';
    chatBody.appendChild(indicator);
    scrollToBottom();
  }

  function removeLoading() {
    const indicator = document.getElementById('aiLoadingIndicator');
    if (indicator) indicator.remove();
  }

  function appendAssistantMessage(data) {
    const msgDiv = document.createElement('div');
    msgDiv.className = 'ai-msg ai-msg-assistant';

    let productsHtml = '';
    if (data.products && data.products.length > 0) {
      productsHtml = '<div class="ai-product-grid">';
      data.products.forEach(function (p) {
        const imgHtml = p.image_url
          ? '<img src="' + p.image_url + '" class="ai-product-img" alt="' + escapeHtml(p.name) + '">'
          : '<div class="ai-product-img d-flex align-items-center justify-content-center bg-secondary text-white"><i class="fa fa-image fa-2x"></i></div>';

        productsHtml +=
          '<div class="ai-product-card">' +
          imgHtml +
          '<div class="ai-product-info">' +
          '<div class="ai-product-title">' + escapeHtml(p.name) + '</div>' +
          '<div class="ai-product-price">$' + Number(p.price).toFixed(2) + '</div>' +
          '<div class="mt-auto d-flex gap-1">' +
          '<a href="/product/' + p.id + '/" class="btn btn-outline-light btn-sm w-50 py-1" style="font-size:0.75rem;">View</a>' +
          '<a href="/add-to-cart/' + p.id + '/" class="btn btn-warning btn-sm w-50 py-1 fw-bold" style="font-size:0.75rem;"><i class="fa fa-cart-plus me-1"></i>Add</a>' +
          '</div></div></div>';
      });
      productsHtml += '</div>';
    }

    msgDiv.innerHTML = '<div class="ai-avatar ai-avatar-bot"><i class="fa fa-robot"></i></div><div class="ai-bubble" style="max-width:100%;"><div>' + formatText(data.reply) + '</div>' + productsHtml + '</div>';
    chatBody.appendChild(msgDiv);
    scrollToBottom();
  }

  function sendQuery(query) {
    if (!query) return;

    appendUserMessage(query);
    searchInput.value = '';
    searchInput.disabled = true;
    sendBtn.disabled = true;

    showLoading();

    fetch('/api/ai-search/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken()
      },
      body: JSON.stringify({ query: query })
    })
      .then(function (res) {
        return res.json();
      })
      .then(function (data) {
        removeLoading();
        appendAssistantMessage(data);
      })
      .catch(function () {
        removeLoading();
        appendAssistantMessage({
          reply: 'Unable to connect right now. Please try again.',
          products: []
        });
      })
      .finally(function () {
        searchInput.disabled = false;
        sendBtn.disabled = false;
        searchInput.focus();
      });
  }

  chatForm.addEventListener('submit', function (e) {
    e.preventDefault();
    const query = searchInput.value.trim();
    if (query) {
      sendQuery(query);
    }
  });

  chips.forEach(function (chip) {
    chip.addEventListener('click', function () {
      const text = this.getAttribute('data-prompt') || this.innerText;
      sendQuery(text.trim());
    });
  });
});
