(function () {
    const modal = document.getElementById('modal');
    if (!modal) return;
    
    const dialog = modal.querySelector('.modal_dialog');
    const closeBtn = modal.querySelector('.modal_close');
    const backdrop = modal.querySelector('.modal_backdrop');
    const titleEl = document.getElementById('modal-title');
    const bodyEl  = document.getElementById('modal-body');
    const startQuizBtn = document.getElementById('modal-start');
    const lastAttemptBtn = document.getElementById('modal-last-attempt');
    
    //store current quiz and user info for Last Attempt button
    let currentQuizId = null;
    let currentUserId = null;
  
    const open = ({ title, description, grade, url, quizId, userId }) => {
      titleEl.textContent = title || '';
      bodyEl.innerHTML = `
        <div class="quiz-details">
          ${description ? `<p class="quiz-description">${description}</p>` : ''}
          ${grade ? `<p class="quiz-grade"><strong>Last attempt:</strong> ${grade}</p>` : ''}
        </div>
      `;
      
      //store quiz and user IDs for Last Attempt button
      currentQuizId = quizId || null;
      currentUserId = userId || window.DASHBOARD_USER_ID || null;
      
      modal.classList.add('show');
      modal.setAttribute('aria-hidden', 'false');
      closeBtn.focus();
      
      const startBtn = document.getElementById('modal-start');
      if (startBtn) {
        if (url) {
          startBtn.removeAttribute('disabled');
          startBtn.onclick = () => { window.location.href = url; };
        } else {
          startBtn.setAttribute('disabled', 'disabled');
          startBtn.onclick = null;
        }
      }
      
      //handle last attempt button - check if user has taken the quiz
      if (lastAttemptBtn && currentQuizId && currentUserId) {
        // Initially disable the button
        lastAttemptBtn.disabled = true;
        lastAttemptBtn.style.display = 'inline-block';
        
        // Check if user has taken this quiz
        fetch(`/check_quiz_attempt/${currentQuizId}/${currentUserId}`)
          .then(response => response.json())
          .then(data => {
            if (data.has_attempt) {
              lastAttemptBtn.disabled = false;
              lastAttemptBtn.onclick = () => {
                window.location.href = `/last_attempt/${currentQuizId}/${currentUserId}`;
              };
            } else {
              lastAttemptBtn.disabled = true;
              lastAttemptBtn.onclick = null;
            }
          })
          .catch(error => {
            console.error('Error checking quiz attempt:', error);
            lastAttemptBtn.disabled = true;
            lastAttemptBtn.onclick = null;
          });
      } else {
        if (lastAttemptBtn) {
          lastAttemptBtn.style.display = 'none';
          lastAttemptBtn.disabled = true;
          lastAttemptBtn.onclick = null;
        }
      }
      
      document.addEventListener('keydown', onKeyDown);
    };
  
    const close = () => {
      modal.classList.remove('show');
      modal.setAttribute('aria-hidden', 'true');
      document.removeEventListener('keydown', onKeyDown);
      currentQuizId = null;
      currentUserId = null;
    };
  
    const onKeyDown = (e) => { if (e.key === 'Escape') close(); };
  
    //handle student dashboard items (.item)
    document.querySelectorAll('.item').forEach(el => {
      const isLocked = el.dataset.locked === 'true';
      
      //add locked class and prevent interaction if locked
      if (isLocked) {
        el.classList.add('locked');
        el.setAttribute('aria-disabled', 'true');
        el.style.cursor = 'not-allowed';
        
        //prevent navigation on locked anchor links
        if (el.tagName === 'A') {
          el.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
          });
        }
        return;
      }

      const isAnchorLink = el.tagName === 'A' && el.getAttribute('href');
      const shouldShowModal = el.dataset.modal === 'true' || (!isAnchorLink && el.dataset.modal !== 'false');

      if (!shouldShowModal) {
        return;
      }

      el.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        const title = el.dataset.quizName || el.textContent.trim();
        const description = el.dataset.quizDescription || el.dataset.body || '';
        const grade = '';
        const url = el.dataset.quizUrl || '';
        const quizId = el.dataset.quizId || '';
        const userId = window.DASHBOARD_USER_ID || '';
        open({ title, description, grade, url, quizId, userId });
      });
    });
  
    closeBtn.addEventListener('click', close);
    backdrop.addEventListener('click', close);
  })();

