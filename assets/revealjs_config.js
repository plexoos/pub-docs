function loadScript(url)
{
  var head = document.getElementsByTagName('head')[0];
  var script = document.createElement('script');
  script.type = 'text/javascript';
  script.src = url;
  head.appendChild(script);
}

loadScript('/pub-docs/assets/reveal.js/dist/reveal.js');
loadScript('/pub-docs/assets/reveal.js/plugin/notes/notes.js');
loadScript('/pub-docs/assets/reveal.js/plugin/markdown/markdown.js');
loadScript('/pub-docs/assets/reveal.js/plugin/highlight/highlight.js');
loadScript('/pub-docs/assets/reveal.js/plugin/math/math.js');

window.onload = function() {
  // More info about initialization & config:
  // - https://revealjs.com/initialization/
  // - https://revealjs.com/config/
  Reveal.initialize({
    hash: true,
    // XGA (1024 x 768, AR = 1.334), WXGA (1280 x 800, AR = 1.6), HD (1920 x 1080, AR = 1.778)
    // AR = 1.6
    width: 1120, height: 700,

    // Learn about plugins: https://revealjs.com/plugins/
    plugins: [ RevealMarkdown, RevealHighlight, RevealNotes ],
    plugins: [ RevealMarkdown, RevealHighlight, RevealNotes, RevealMath ],

    controls: false,
    history: true,
    center: false,
    progress: false,
    transition: 'none',
    transitionSpeed: 'fast',
    viewDistance: 100
  });

  Reveal.configure( { slideNumber: 'c', hashOneBasedIndex: true, showSlideNumber: 'all' } );
};
