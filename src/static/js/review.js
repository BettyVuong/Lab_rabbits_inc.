(() => {
    const cards = Array.from(document.querySelectorAll('.review-card'));
    const trackerButtons = Array.from(document.querySelectorAll('.review-tracker-btn'));
    const prevBtn = document.getElementById('review-prev');
    const nextBtn = document.getElementById('review-next');
    const currentEl = document.getElementById('review-current');
    const revealButtons = Array.from(document.querySelectorAll('.reveal-btn'));

    if (!cards.length) {
        return;
    }

    const totalCards = cards.length;
    let currentIndex = 0;

    const showCard = (index) => {
        // Update currentIndex
        currentIndex = index;

        // Show/hide cards
        cards.forEach((card, idx) => {
            const isActive = idx === index;
            card.classList.toggle('active', isActive);
            card.toggleAttribute('hidden', !isActive);
            card.setAttribute('aria-hidden', (!isActive).toString());
        });

        // Update tracker button highlighting
        trackerButtons.forEach((btn, idx) => {
            if (idx === index) {
                btn.classList.add('current');
            } else {
                btn.classList.remove('current');
            }
        });

        // Update counter display
        if (currentEl) {
            currentEl.textContent = index + 1;
        }

        // Update prev/next button states
        if (prevBtn) {
            prevBtn.disabled = index === 0;
        }
        if (nextBtn) {
            nextBtn.disabled = index === totalCards - 1;
        }
    };

    trackerButtons.forEach((btn) => {
        btn.addEventListener('click', () => {
            const target = Number(btn.dataset.target);
            if (!Number.isNaN(target) && target >= 0 && target < totalCards) {
                showCard(target);
            }
        });
    });

    if (prevBtn) {
        prevBtn.addEventListener('click', () => {
            if (currentIndex > 0) {
                showCard(currentIndex - 1);
            }
        });
    }

    if (nextBtn) {
        nextBtn.addEventListener('click', () => {
            if (currentIndex < totalCards - 1) {
                showCard(currentIndex + 1);
            }
        });
    }

    revealButtons.forEach((btn) => {
        btn.addEventListener('click', () => {
            const answer = btn.nextElementSibling;
            if (!answer) {
                return;
            }
            const isVisible = answer.dataset.visible === 'true';
            answer.dataset.visible = (!isVisible).toString();
        });
    });

    // Initialize with first card
    showCard(0);
})();
