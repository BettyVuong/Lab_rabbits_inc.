(function () {
  const questions = Array.from(document.querySelectorAll('.quiz-question'));
  const trackerButtons = Array.from(document.querySelectorAll('.tracker-btn'));
  const prevBtn = document.getElementById('prev-btn');
  const nextBtn = document.getElementById('next-btn');
  const currentQuestionEl = document.getElementById('current-question');
  const form = document.getElementById('quiz-form');

  if (!form || questions.length === 0) {
    return;
  }

  let currentIndex = 0;

  const totalQuestions = questions.length;

  const showQuestion = (index) => {
    questions.forEach((section, idx) => {
      const isActive = idx === index;
      section.classList.toggle('active', isActive);
      section.toggleAttribute('hidden', !isActive);
      section.setAttribute('aria-hidden', (!isActive).toString());
    });

    trackerButtons.forEach((btn, idx) => {
      btn.classList.toggle('current', idx === index);
    });

    prevBtn.disabled = index === 0;
    nextBtn.textContent = index === totalQuestions - 1 ? 'Submit' : 'Next';
    currentQuestionEl.textContent = index + 1;
    currentIndex = index;
  };

  const markCompleted = (index) => {
    const answered = form.querySelectorAll(`input[name="question_${questions[index].dataset.questionId}"]:checked`).length > 0;
    trackerButtons[index].classList.toggle('completed', answered);
  };

  questions.forEach((section, index) => {
    const questionId = section.dataset.questionId;
    if (questionId) {
      section.addEventListener('change', () => {
        const hasAnswer = form.querySelectorAll(`input[name="question_${questionId}"]:checked`).length > 0;
        trackerButtons[index].classList.toggle('completed', hasAnswer);
      });
    } else {
      section.addEventListener('change', () => markCompleted(index));
    }
  });

  trackerButtons.forEach((btn) => {
    btn.addEventListener('click', () => {
      const index = Number(btn.dataset.target);
      if (!Number.isNaN(index)) {
        showQuestion(index);
      }
    });
  });

  prevBtn.addEventListener('click', () => {
    if (currentIndex > 0) {
      showQuestion(currentIndex - 1);
    }
  });

  nextBtn.addEventListener('click', () => {
    if (currentIndex === totalQuestions - 1) {
      form.submit();
    } else {
      showQuestion(currentIndex + 1);
    }
  });

  showQuestion(0);

  // Exit quiz confirmation modal
  const exitQuizBtn = document.getElementById('exit-quiz-btn');
  const logoHomeBtn = document.getElementById('logo-home-btn');
  const exitForm = document.getElementById('exit-quiz-form');
  const exitModal = document.getElementById('exit-confirm-modal');
  const exitModalClose = exitModal?.querySelector('.quiz-exit-modal-close');
  const exitModalBackdrop = exitModal?.querySelector('.quiz-exit-modal-backdrop');
  const exitCancelBtn = document.getElementById('exit-cancel-btn');
  const exitConfirmBtn = document.getElementById('exit-confirm-btn');

  // Get user_id from window variable or default to 1
  const dashboardUserId = window.QUIZ_USER_ID || 1;

  if (exitModal) {
    const openExitModal = (shouldSubmitForm = false) => {
      exitModal.classList.add('show');
      exitModal.setAttribute('aria-hidden', 'false');
      exitModalClose?.focus();
      document.addEventListener('keydown', onExitKeyDown);
      
      // Store whether to submit form or redirect
      exitModal.dataset.shouldSubmit = shouldSubmitForm ? 'true' : 'false';
    };

    const closeExitModal = () => {
      exitModal.classList.remove('show');
      exitModal.setAttribute('aria-hidden', 'true');
      document.removeEventListener('keydown', onExitKeyDown);
    };

    const onExitKeyDown = (e) => {
      if (e.key === 'Escape') closeExitModal();
    };

    // Exit quiz button handler
    if (exitQuizBtn) {
      exitQuizBtn.addEventListener('click', (e) => {
        e.preventDefault();
        openExitModal(true); // true = submit form
      });
    }

    // Logo home button handler
    if (logoHomeBtn) {
      logoHomeBtn.addEventListener('click', (e) => {
        e.preventDefault();
        openExitModal(false); // false = redirect to dashboard
      });
    }

    exitModalClose?.addEventListener('click', closeExitModal);
    exitModalBackdrop?.addEventListener('click', closeExitModal);
    exitCancelBtn?.addEventListener('click', closeExitModal);

    exitConfirmBtn?.addEventListener('click', () => {
      const shouldSubmit = exitModal.dataset.shouldSubmit === 'true';
      if (shouldSubmit && exitForm) {
        exitForm.submit();
      } else {
        // Redirect to dashboard
        window.location.href = `/dashboard/${dashboardUserId}`;
      }
    });
  }
})();