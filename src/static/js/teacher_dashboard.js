(function () {
    const modal = document.getElementById('modal');
    if (!modal) return;
    
    const dialog = modal.querySelector('.modal_dialog');
    const closeBtn = modal.querySelector('.modal_close');
    const backdrop = modal.querySelector('.modal_backdrop');
    const titleEl = document.getElementById('modal-title');
    const bodyEl  = document.getElementById('modal-body');
    const startQuizBtn = document.getElementById('modal-start');
    const deleteQuizForm = document.getElementById('delete-quiz-form');
    const difficultySelect = document.getElementById('difficulty-select');
    const difficultyContainer = document.getElementById('modal-difficulty');
    
    //store current quiz info for the modal
    let currentQuizId = null;
    let currentTeacherId = null;
  
    const open = ({ title, description, quizId, teacherId }) => {
      titleEl.textContent = title || '';
      bodyEl.innerHTML = `
        <div class="quiz-details">
          ${description ? `<p class="quiz-description">${description}</p>` : ''}
        </div>
      `;
      
      //ensure they're strings
      currentQuizId = String(quizId || '').trim();
      currentTeacherId = String(teacherId || '').trim();
      
      if (deleteQuizForm && currentQuizId && currentTeacherId) {
        deleteQuizForm.action = `/delete_quiz/${currentTeacherId}/${currentQuizId}`;
        deleteQuizForm.onsubmit = function(e) {
          return confirm('Are you sure you want to delete this quiz? This action cannot be undone.');
        };
      }
      
      //difficulty dropdown for teacher dashboard
      if (difficultyContainer) {
        difficultyContainer.style.display = 'block';
      }
      
      modal.classList.add('show');
      modal.setAttribute('aria-hidden', 'false');
      closeBtn.focus();
      
      const startBtn = document.getElementById('modal-start');
      if (startBtn && currentQuizId && currentTeacherId) {
        startBtn.removeAttribute('disabled');
        startBtn.onclick = (e) => {
          e.preventDefault();
          e.stopPropagation();
          const elo = difficultySelect ? difficultySelect.value : '1000';
          const quizId = currentQuizId;
          const teacherId = currentTeacherId;
          const url = `/test_quiz/${teacherId}/${quizId}/${elo}`;
          if (quizId && teacherId && quizId !== 'null' && teacherId !== 'null') {
            window.location.href = url;
          } else {
            alert('Error: Invalid quiz information. Please try again.');
          }
        };
      } else {
        startBtn.setAttribute('disabled', 'disabled');
        startBtn.onclick = null;
      }
      document.addEventListener('keydown', onKeyDown);
    };
  
    const close = () => {
      modal.classList.remove('show');
      modal.setAttribute('aria-hidden', 'true');
      document.removeEventListener('keydown', onKeyDown);
      currentQuizId = null;
      currentTeacherId = null;
    };
  
    const onKeyDown = (e) => { if (e.key === 'Escape') close(); };

    document.querySelectorAll('.t-item').forEach(el => {
      const shouldShowModal = el.dataset.modal === 'true';
      
      if (!shouldShowModal) {
        return;
      }
      
      el.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        const title = el.dataset.quizName || el.textContent.trim();
        const description = el.dataset.quizDescription || '';
        let quizId = el.dataset.quizId;
        if (!quizId) {
          quizId = el.getAttribute('data-quiz-id');
        }
        
        let teacherId = el.dataset.teacherId;
        if (!teacherId) {
          teacherId = el.getAttribute('data-teacher-id');
        }
        if (!teacherId) {
          teacherId = window.DASHBOARD_USER_ID || '';
        }
        
        //to strings and ensure they're valid numbers
        quizId = String(quizId || '').trim();
        teacherId = String(teacherId || '').trim();
        
        //make sure they're numbers
        if (!quizId || !teacherId || isNaN(quizId) || isNaN(teacherId)) {
          alert('Error: Invalid quiz information. Please refresh the page.');
          return;
        }
        
        open({ title, description, quizId, teacherId });
      });
    });
  
    closeBtn.addEventListener('click', close);
    backdrop.addEventListener('click', close);
  })();

