(()=>{
const root=document.documentElement,system=window.matchMedia('(prefers-color-scheme: dark)');
let saved=null;try{saved=localStorage.getItem('pydantic-knowledge-theme')}catch{}
function apply(theme){root.dataset.theme=theme;const button=document.getElementById('theme-toggle');if(button){const label=theme==='dark'?'Switch to light mode':'Switch to dark mode';button.setAttribute('aria-label',label);button.title=label}}
apply(saved==='light'||saved==='dark'?saved:system.matches?'dark':'light');
document.addEventListener('DOMContentLoaded',()=>{apply(root.dataset.theme);document.getElementById('theme-toggle')?.addEventListener('click',()=>{saved=root.dataset.theme==='dark'?'light':'dark';apply(saved);try{localStorage.setItem('pydantic-knowledge-theme',saved)}catch{}})});
system.addEventListener('change',event=>{if(!saved)apply(event.matches?'dark':'light')});
})();
