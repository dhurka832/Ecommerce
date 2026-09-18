document.addEventListener('DOMContentLoaded', function () {
  const toggleBtn = document.getElementById('chatbotToggleBtn');
  const chatWindow = document.getElementById('chatbotWindow');
  const closeBtn = document.getElementById('chatbotCloseBtn');
  const chatBody = document.getElementById('chatbotBody');
  const chatForm = document.getElementById('chatbotForm');
  const chatInput = document.getElementById('chatbotInput');
  const sendBtn = document.getElementById('chatbotSendBtn');
  const chips = document.querySelectorAll('.chatbot-chip');

  if (!toggleBtn || !chatWindow || !chatBody) return;

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

  function formatMarkdown(text) {
    if (!text) return '';
    let formatted = escapeHtml(text);
    formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    formatted = formatted.replace(/\n/g, '<br>');
    return formatted;
  }

  function appendUserMessage(text) {
    const msgDiv = document.createElement('div');
    msgDiv.className = 'chatbot-msg chatbot-msg-user';
    msgDiv.innerHTML = '<div class="chatbot-bubble">' + escapeHtml(text) + '</div>';
    chatBody.appendChild(msgDiv);
    scrollToBottom();
  }

  function showLoading() {
    const loadingDiv = document.createElement('div');
    loadingDiv.id = 'chatbotLoading';
    loadingDiv.className = 'chatbot-msg chatbot-msg-bot';
    loadingDiv.innerHTML = '<div class="chatbot-bubble opacity-75"><em>Thinking...</em></div>';
    chatBody.appendChild(loadingDiv);
    scrollToBottom();
  }

  function removeLoading() {
    const loadingDiv = document.getElementById('chatbotLoading');
    if (loadingDiv) loadingDiv.remove();
  }

  function appendBotMessage(text) {
    const msgDiv = document.createElement('div');
    msgDiv.className = 'chatbot-msg chatbot-msg-bot';
    msgDiv.innerHTML = '<div class="chatbot-bubble">' + formatMarkdown(text) + '</div>';
    chatBody.appendChild(msgDiv);
    scrollToBottom();
  }

  function sendQuery(message) {
    if (!message) return;

    appendUserMessage(message);
    if (chatInput) chatInput.value = '';
    if (chatInput) chatInput.disabled = true;
    if (sendBtn) sendBtn.disabled = true;

    showLoading();

    fetch('/api/chatbot/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken()
      },
      body: JSON.stringify({ message: message })
    })
      .then(function (res) {
        return res.json();
      })
      .then(function (data) {
        removeLoading();
        appendBotMessage(data.reply || 'Hello! How can I assist you today?');
      })
      .catch(function () {
        removeLoading();
        appendBotMessage("Sorry, I'm having trouble connecting right now. Please try again.");
      })
      .finally(function () {
        if (chatInput) chatInput.disabled = false;
        if (sendBtn) sendBtn.disabled = false;
        if (chatInput) chatInput.focus();
      });
  }

  toggleBtn.addEventListener('click', function () {
    chatWindow.classList.toggle('d-none');
    if (!chatWindow.classList.contains('d-none') && chatInput) {
      chatInput.focus();
    }
  });

  if (closeBtn) {
    closeBtn.addEventListener('click', function () {
      chatWindow.classList.add('d-none');
    });
  }

  if (chatForm) {
    chatForm.addEventListener('submit', function (e) {
      e.preventDefault();
      const val = chatInput ? chatInput.value.trim() : '';
      if (val) sendQuery(val);
    });
  }

  chips.forEach(function (chip) {
    chip.addEventListener('click', function () {
      const msg = this.getAttribute('data-msg') || this.innerText;
      sendQuery(msg.trim());
    });
  });
});
