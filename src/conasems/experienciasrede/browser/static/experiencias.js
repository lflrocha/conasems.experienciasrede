
    const searchInput = document.getElementById('experienciasSearchInput');
    const ufSelect = document.getElementById('experienciasUfSelect');
    const chips = document.querySelectorAll('.experiencias-chip');
    const cards = document.querySelectorAll('.experiencias-card');
    const resultCount = document.getElementById('experienciasResultCount');
    const emptyState = document.getElementById('experienciasEmptyState');

    let selectedAxis = '';

    function normalize(text) {
      return text
        .toLowerCase()
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '');
    }

    function filterCards() {
      const search = normalize(searchInput.value);
      const uf = ufSelect.value;
      let visibleCount = 0;

      cards.forEach(card => {
        const title = normalize(card.dataset.title);
        const author = normalize(card.dataset.author);
        const cardUf = card.dataset.uf;
        const axis = card.dataset.axis;

        const matchesSearch =
          title.includes(search) ||
          author.includes(search) ||
          normalize(cardUf).includes(search) ||
          normalize(axis).includes(search);

        const matchesUf = !uf || cardUf === uf;
        const matchesAxis = !selectedAxis || axis === selectedAxis;

        const shouldShow = matchesSearch && matchesUf && matchesAxis;

        card.style.display = shouldShow ? 'flex' : 'none';

        if (shouldShow) {
          visibleCount++;
        }
      });

      resultCount.textContent =
        visibleCount === 1
          ? '1 trabalho encontrado'
          : visibleCount + ' trabalhos encontrados';

      emptyState.style.display = visibleCount === 0 ? 'block' : 'none';
    }

    searchInput.addEventListener('input', filterCards);
    ufSelect.addEventListener('change', filterCards);

    chips.forEach(chip => {
      chip.addEventListener('click', () => {
        chips.forEach(item => item.classList.remove('active'));
        chip.classList.add('active');

        selectedAxis = chip.dataset.axis;
        filterCards();
      });
    });

    filterCards();
  