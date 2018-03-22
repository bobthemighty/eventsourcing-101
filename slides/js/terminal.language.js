/*
  Language: terminal console
  Author: Josh Bode <joshbode@gmail.com>
*/

hljs.registerLanguage('terminal', function() {
  return {
    contains: [
      {
        className: 'string',
        begin: '^([\\w.]+)@([\\w.]+)'
      },
      {
        className: 'constant',
        begin: ' (.*) \\$ '
      },
      {
        className: 'ansi',
        begin: '<span style\\="([^"]+)">',
        end: '<\\/span>'
      }
    ]
  }
});
