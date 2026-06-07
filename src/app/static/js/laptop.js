document.addEventListener('DOMContentLoaded', () => {
  const fSearch   = document.getElementById('f-search');
  const fBrand    = document.getElementById('f-brand');
  const fModel    = document.getElementById('f-model');
  const fState    = document.getElementById('f-state');
  const fVendor   = document.getElementById('f-vendor');
  const countEl   = document.getElementById('count');
  const noResults = document.getElementById('no-results');

  function filter() {
    const search = (fSearch?.value || '').trim().toLowerCase();
    const brand  = fBrand?.value || '';
    const model  = fModel?.value || '';
    const state  = fState?.value || '';
    const vendor = fVendor?.value || '';

    let visible = 0;

    document.querySelectorAll('#tbody tr').forEach(row => {
      const serial   = (row.dataset.serial || '').toLowerCase();
      const hostname = (row.dataset.hostname || '').toLowerCase();
      const rowBrand = row.dataset.brand || '';
      const rowModel = row.dataset.model || '';
      const rowState = row.dataset.state || '';
      const rowVendor = row.dataset.vendor || '';

      const match =
        (!search || serial.includes(search) || hostname.includes(search)) &&
        (!brand  || rowBrand === brand) &&
        (!model  || rowModel === model) &&
        (!state  || rowState === state) &&
        (!vendor || rowVendor === vendor);

      row.classList.toggle('hidden', !match);

      if (match) {
        visible++;
      }
    });

    if (countEl) {
      countEl.textContent = visible;
    }

    if (noResults) {
      noResults.style.display = visible === 0 ? 'block' : 'none';
    }
  }

  window.resetFilters = function () {
    if (fSearch) fSearch.value = '';

    [fBrand, fModel, fState, fVendor].forEach(el => {
      if (el) el.selectedIndex = 0;
    });

    filter();
  };

  if (fSearch) {
    fSearch.addEventListener('input', filter);
  }

  [fBrand, fModel, fState, fVendor].forEach(el => {
    if (el) {
      el.addEventListener('change', filter);
    }
  });

  filter();
});