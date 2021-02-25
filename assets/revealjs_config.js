function loadScript(url)
{
  var head = document.getElementsByTagName('head')[0];
  var script = document.createElement('script');
  script.type = 'text/javascript';
  script.src = url;
  head.appendChild(script);
}

loadScript('/pub-docs/assets/reveal.js/js/reveal.js');

window.onload = function() {
  Reveal.initialize({
    // XGA (1024 x 768, AR = 1.334), WXGA (1280 x 800, AR = 1.6), HD (1920 x 1080, AR = 1.778)
    // AR = 1.6
    width: 1120, height: 700,
    math: {
       mathjax: 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.0/MathJax.js',
       config: 'TeX-AMS_SVG-full'
    },
    dependencies: [
       { src: '../assets/reveal.js/plugin/markdown/marked.js' },
       { src: '../assets/reveal.js/plugin/markdown/markdown.js' },
       { src: '../assets/reveal.js/plugin/notes/notes.js', async: true },
       { src: '../assets/reveal.js/plugin/highlight/highlight.js', async: true, callback: function() { hljs.initHighlightingOnLoad(); } },
       { src: '../assets/reveal.js/plugin/math/math.js', async: true }
    ],
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
