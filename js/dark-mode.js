const STORAGE_KEY = 'darkModeEnabled';
const darkModeToggle = document.querySelector('#dark-mode-toggle');

function applyTheme(isDark) {
    document.body.classList.toggle('dark-mode', isDark);
    if (darkModeToggle) {
        darkModeToggle.checked = isDark;
    }
}

function saveThemePreference(isDark) {
    localStorage.setItem(STORAGE_KEY, isDark);
}

let preferredTheme = localStorage.getItem(STORAGE_KEY);
let isDarkMode;

if (preferredTheme !== null) {
    isDarkMode = preferredTheme === 'true';
} else {
    isDarkMode = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
}

applyTheme(isDarkMode);

if (darkModeToggle) {
    darkModeToggle.addEventListener('change', function (ev) {
        const isChecked = darkModeToggle.checked;
        applyTheme(isChecked);
        saveThemePreference(isChecked);
    });

    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', event => {
        if (localStorage.getItem(STORAGE_KEY) === null) {
            const newColorScheme = event.matches;
            applyTheme(newColorScheme);
        }
    });
}

document.documentElement.addEventListener('click', function(ev) {
  const target = ev.target;

  if (document.documentElement.classList.contains('show-modal')) {
    if (!target.closest('.toggle-switch')) {
      document.documentElement.classList.remove("show-modal");
      if (window.location.hash.length > 1 && history.replaceState) {
        try {
          history.replaceState(null, "", window.location.pathname + window.location.search);
        } catch (e) {
        }
      }
    }
  }

  if (!target.closest('.nav-menucontainer') && !target.closest('.toggle-switch')) {
    document.querySelectorAll('.nav-dropdown').forEach(link => link.setAttribute('aria-expanded', 'false'));
  }

  if (!target.closest("nav") && !target.closest('.toggle-switch')) {
    const navInput = document.querySelector("nav input[type=checkbox]");
    if (navInput) navInput.checked = false;
  }
});