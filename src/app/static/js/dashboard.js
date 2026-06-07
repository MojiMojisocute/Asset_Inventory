const fName = document.getElementById('f-name');
const fDept = document.getElementById('f-dept');
const fType = document.getElementById('f-type');
const fBrand = document.getElementById('f-brand');
const fModel = document.getElementById('f-model');

const countEl = document.getElementById('count');
const headerCount = document.getElementById('header-count');
const noResults = document.getElementById('no-results');

function filter() {
    const name = fName.value.trim().toLowerCase();
    const dept = fDept.value;
    const type = fType.value;
    const brand = fBrand.value;
    const model = fModel.value;

    let visible = 0;

    document.querySelectorAll('#tbody tr').forEach(row => {
        const match =
            (!name || row.dataset.name.includes(name) || row.dataset.hostname.includes(name)) &&
            (!dept || row.dataset.dept === dept) &&
            (!type || row.dataset.type === type) &&
            (!brand || row.dataset.brand === brand) &&
            (!model || row.dataset.model === model);

        row.classList.toggle('hidden', !match);

        if (match) visible++;
    });

    countEl.textContent = visible;
    headerCount.textContent = `${visible} assignments`;
    noResults.style.display = visible === 0 ? 'block' : 'none';
}

function resetFilters() {
    fName.value = '';

    [fDept, fType, fBrand, fModel].forEach(el => {
        el.selectedIndex = 0;
    });

    filter();
}

[fName, fDept, fType, fBrand, fModel].forEach(el => {
    el.addEventListener('input', filter);
    el.addEventListener('change', filter);
});

window.resetFilters = resetFilters;