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
    nextBtn.textContent = 'Next';
    nextBtn.disabled = index === totalQuestions - 1;
    currentQuestionEl.textContent = index + 1;
    currentIndex = index;
  };

  const markCompleted = (index) => {
    const questionId = questions[index].dataset.questionId;
    const answered = form.querySelectorAll(`input[name="question_${questionId}"]:checked`).length > 0;
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
    if (currentIndex < totalQuestions - 1) {
      showQuestion(currentIndex + 1);
    }
  });

  showQuestion(0);

  const exitQuizBtn = document.getElementById('exit-quiz-btn');
  const logoHomeBtn = document.getElementById('logo-home-btn');
  const exitForm = document.getElementById('exit-quiz-form');
  const exitModal = document.getElementById('exit-confirm-modal');
  const exitModalClose = exitModal?.querySelector('.quiz-exit-modal-close');
  const exitModalBackdrop = exitModal?.querySelector('.quiz-exit-modal-backdrop');
  const exitCancelBtn = document.getElementById('exit-cancel-btn');
  const exitConfirmBtn = document.getElementById('exit-confirm-btn');

  //teacher_id from window variable
  const teacherId = window.QUIZ_TEACHER_ID || 1;

  if (exitModal) {
    const openExitModal = () => {
      exitModal.classList.add('show');
      exitModal.setAttribute('aria-hidden', 'false');
      exitModalClose?.focus();
      document.addEventListener('keydown', onExitKeyDown);
    };

    const closeExitModal = () => {
      exitModal.classList.remove('show');
      exitModal.setAttribute('aria-hidden', 'true');
      document.removeEventListener('keydown', onExitKeyDown);
    };

    const onExitKeyDown = (e) => {
      if (e.key === 'Escape') closeExitModal();
    };

    //exit demo button handler
    if (exitQuizBtn) {
      exitQuizBtn.addEventListener('click', (e) => {
        e.preventDefault();
        openExitModal();
      });
    }

    //logo home button handler
    if (logoHomeBtn) {
      logoHomeBtn.addEventListener('click', (e) => {
        e.preventDefault();
        openExitModal();
      });
    }

    exitModalClose?.addEventListener('click', closeExitModal);
    exitModalBackdrop?.addEventListener('click', closeExitModal);
    exitCancelBtn?.addEventListener('click', closeExitModal);

    exitConfirmBtn?.addEventListener('click', () => {
      if (exitForm) {
        exitForm.submit();
      } else {
        window.location.href = `/teacher_dashboard/${teacherId}`;
      }
    });
  }
})();

