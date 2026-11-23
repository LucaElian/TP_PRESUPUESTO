(() => {
    const form = document.querySelector('#tasas-form');
    if (!form) return;
    const fields = [...form.querySelectorAll('input[type="number"]')];
    const status = document.querySelector('#completion-status');
    const exampleButton = document.querySelector('#example-button');
    const clearButton = document.querySelector('#clear-button');
    const exampleNotice = document.querySelector('#example-notice');
    const staleNotice = document.querySelector('#stale-notice');
    const calculateButton = document.querySelector('#calculate-button');
    const hasResults = document.body.dataset.hasResults === 'true';
    const examples = {
        'Banco Provincia': [36, 38, 40],
        'Banco Nacion': [39, 41, 43],
        'Banco Hipotecario': [34, 37, 38.5]
    };
    exampleButton.hidden = false;
    clearButton.hidden = false;

    function updateStatus() {
        const completed = fields.filter(field => field.value !== '' && field.validity.valid).length;
        status.textContent = `${completed} de ${fields.length} tasas cargadas`;
        status.classList.toggle('is-complete', completed === fields.length);
        staleNotice.hidden = !hasResults || !fields.some(field => field.value !== field.dataset.initialValue);
    }

    fields.forEach(field => {
        field.addEventListener('input', () => {
            field.setAttribute('aria-invalid', String(!field.validity.valid));
            exampleNotice.hidden = true;
            updateStatus();
        });
        field.addEventListener('invalid', () => field.setAttribute('aria-invalid', 'true'));
    });

    exampleButton.addEventListener('click', () => {
        fields.forEach(field => {
            field.value = examples[field.dataset.bank][Number(field.dataset.year) - 1].toFixed(2);
            field.setAttribute('aria-invalid', 'false');
        });
        exampleNotice.hidden = false;
        updateStatus();
    });
    clearButton.addEventListener('click', () => {
        fields.forEach(field => {
            field.value = '';
            field.removeAttribute('aria-invalid');
        });
        exampleNotice.hidden = true;
        updateStatus();
        fields[0].focus();
    });
    form.addEventListener('submit', () => {
        calculateButton.disabled = true;
        calculateButton.querySelector('span').textContent = 'Calculando…';
        form.setAttribute('aria-busy', 'true');
    });
    window.addEventListener('pageshow', () => {
        calculateButton.disabled = false;
        calculateButton.querySelector('span').textContent = 'Calcular inversiones';
        form.removeAttribute('aria-busy');
        updateStatus();
    });

    const links = [...document.querySelectorAll('nav a')];
    function setCurrent(id) {
        links.forEach(link => {
            if (link.hash === `#${id}`) link.setAttribute('aria-current', 'location');
            else link.removeAttribute('aria-current');
        });
    }
    links.forEach(link => link.addEventListener('click', () => setCurrent(link.hash.slice(1))));
    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver(entries => {
            entries.forEach(entry => { if (entry.isIntersecting) setCurrent(entry.target.id); });
        }, {rootMargin: '-20% 0px -50% 0px'});
        links.forEach(link => observer.observe(document.querySelector(link.hash)));
    }
    updateStatus();
    if (document.body.dataset.hasError === 'true') {
        form.querySelector('[aria-invalid="true"]')?.focus({preventScroll: true});
        document.querySelector('#cargar').scrollIntoView();
    } else if (hasResults && !location.hash) {
        document.querySelector('#historicos-titulo').focus({preventScroll: true});
        document.querySelector('#resultados').scrollIntoView();
        history.replaceState(null, '', '#resultados');
    }
})();
