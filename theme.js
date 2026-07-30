// Theme handling. The initial theme is applied by an inline snippet in <head> (no flash): it uses a
// stored preference if the user picked one, otherwise the OS setting (prefers-color-scheme).
//
// By default the site follows the OS theme automatically — including live changes while the page is
// open (e.g. the OS flipping to dark at sunset). Clicking the toggle sets an explicit preference that
// overrides the OS; from then on that choice sticks.

// Follow the OS theme live, but only while the user hasn't chosen an explicit preference.
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function (e) {
  if (!localStorage.getItem('theme')) {
    document.documentElement.classList.toggle('dark', e.matches);
  }
});

function toggleTheme() {
  var isDark = document.documentElement.classList.toggle('dark');
  localStorage.setItem('theme', isDark ? 'dark' : 'light');
}
