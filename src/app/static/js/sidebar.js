(function () {
  "use strict";

  const STORAGE_KEY = "sidebar_open_groups";

  function loadOpenGroups() {
    try {
      return new Set(JSON.parse(localStorage.getItem(STORAGE_KEY)) || []);
    } catch {
      return new Set();
    }
  }

  function saveOpenGroups(set) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify([...set]));
  }

  const openGroups = loadOpenGroups();

  document.querySelectorAll(".nav-group").forEach((group) => {
    const groupName = group.dataset.group;
    const btn       = group.querySelector(".nav-group-btn");
    const children  = group.querySelector(".nav-group-children");
    const hasActive = group.querySelector(".nav-child.active");

    const shouldOpen = hasActive || openGroups.has(groupName);

    if (shouldOpen) {
      group.classList.add("open");
      openGroups.add(groupName);
      saveOpenGroups(openGroups);
    }

    children.style.transition = "none";
    children.style.height = group.classList.contains("open")
      ? children.scrollHeight + "px"
      : "0";

    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        children.style.transition = "height 0.2s ease";
      });
    });

    btn.addEventListener("click", () => {
      const isOpen = group.classList.contains("open");

      if (isOpen) {
        children.style.height = children.scrollHeight + "px";
        requestAnimationFrame(() => {
          children.style.height = "0";
        });
        group.classList.remove("open");
        openGroups.delete(groupName);
      } else {
        children.style.height = children.scrollHeight + "px";
        group.classList.add("open");
        openGroups.add(groupName);

        children.addEventListener("transitionend", function handler() {
          if (group.classList.contains("open")) {
            children.style.height = "auto";
          }
          children.removeEventListener("transitionend", handler);
        });
      }

      saveOpenGroups(openGroups);
    });
  });

})();