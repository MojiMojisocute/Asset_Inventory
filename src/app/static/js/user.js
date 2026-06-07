document.addEventListener('DOMContentLoaded', () => {
  const fSearch     = document.getElementById('f-search');
  const countEl     = document.getElementById('count');
  const noResults   = document.getElementById('no-results');
  const filterBadge = document.getElementById('filter-badge');
  const btnFilter   = document.getElementById('btn-filter');
  const filterPanel = document.getElementById('filter-panel');

  // Toggle panel
  btnFilter.addEventListener('click', e => {
    e.stopPropagation();
    filterPanel.classList.toggle('open');
  });

  // Close when clicking outside
  document.addEventListener('click', e => {
    if (!filterPanel.contains(e.target) && e.target !== btnFilter) {
      filterPanel.classList.remove('open');
    }
  });

  function getChecked(name) {
    return [...document.querySelectorAll(`input[name="${name}"]:checked`)].map(el => el.value);
  }

  function filter() {
    const search   = fSearch.value.trim().toLowerCase();
    const statuses = getChecked('status');
    const types    = getChecked('type');
    const depts    = getChecked('dept');

    let visible = 0;
    document.querySelectorAll('#tbody tr').forEach(row => {
      const match =
        (!search          || row.dataset.name.includes(search)) &&
        (!statuses.length || statuses.includes(row.dataset.status)) &&
        (!types.length    || types.includes(row.dataset.type)) &&
        (!depts.length    || depts.includes(row.dataset.dept));

      row.classList.toggle('hidden', !match);
      if (match) visible++;
    });

    countEl.textContent = visible;
    noResults.style.display = visible === 0 ? 'block' : 'none';

    const total = statuses.length + types.length + depts.length;
    filterBadge.textContent = total;
    filterBadge.style.display = total > 0 ? 'inline-flex' : 'none';
    btnFilter.classList.toggle('active', total > 0);
  }

  window.showTab = function(tab) {
    document.querySelectorAll('.filter-tab').forEach(el => {
      el.classList.toggle('active', el.dataset.tab === tab);
    });
    document.querySelectorAll('.filter-section').forEach(el => el.classList.remove('active'));
    document.getElementById('tab-' + tab).classList.add('active');
  };

  window.clearSection = function(name) {
    document.querySelectorAll(`input[name="${name}"]`).forEach(el => el.checked = false);
    filter();
  };

  window.clearAll = function() {
    document.querySelectorAll('.filter-panel input[type=checkbox]').forEach(el => el.checked = false);
    filter();
  };

  fSearch.addEventListener('input', filter);
  document.querySelectorAll('.filter-panel input[type=checkbox]').forEach(el => {
    el.addEventListener('change', filter);
  });
});