// Theme toggle. The initial theme is applied by an inline snippet in <head> (no flash);
// this only handles the switch button. Persists to localStorage under "theme" (light|dark).
function toggleTheme() {
  var isDark = document.documentElement.classList.toggle('dark');
  localStorage.setItem('theme', isDark ? 'dark' : 'light');
}
