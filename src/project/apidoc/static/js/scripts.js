function getRapiDoc() {
    return document.getElementById('thedoc');
  }

  function changeSchemaStyle() {
    let docEl = getRapiDoc();
    if (docEl.getAttribute('schema-style') === 'table') {
      docEl.setAttribute('schema-style', "tree");
    }
    else {
      docEl.setAttribute('schema-style', "table");
    }
  }

  function changeTheme(themeName) {

    let docEl = getRapiDoc();

    docEl.setAttribute('show-header', '');
    docEl.setAttribute('bg-color', '');
    docEl.setAttribute('text-color', '');
    docEl.setAttribute('nav-bg-color', '');
    docEl.setAttribute('nav-text-color', '');
    docEl.setAttribute('nav-hover-bg-color', '');
    docEl.setAttribute('nav-hover-text-color', '');
    docEl.setAttribute('nav-accent-color', '');
    docEl.setAttribute('primary-color', '');

    if (themeName === 'dark') {
      docEl.setAttribute('theme', 'dark');
      docEl.setAttribute('primary-color', '#1ca72c');
      // docEl.setAttribute('bg-color', '#333');
      // docEl.setAttribute('text-color', '#BBB');

    } else if (themeName === 'light') {
      docEl.setAttribute('theme', 'light');
      docEl.setAttribute('primary-color', '#1ca72c');
      // docEl.setAttribute('bg-color', '#F1F3F4');
      // docEl.setAttribute('text-color', '#2D3748');
      // docEl.setAttribute('header-colo', '#0367BD');
      // docEl.setAttribute('nav-bg-color', '#0367BD');
      // docEl.setAttribute('nav-hover-bg-color', '#F1F3F4');


    } else if (themeName === 'night') {
      docEl.setAttribute('theme', 'dark');
      docEl.setAttribute('bg-color', '#14191f');
      docEl.setAttribute('text-color', '#aec2e0');
    } else if (themeName === 'mud') {
      docEl.setAttribute('theme', 'dark');
      docEl.setAttribute('bg-color', '#403635');
      docEl.setAttribute('text-color', '#c3b8b7');
    } else if (themeName === 'cofee') {
      docEl.setAttribute('theme', 'dark');
      docEl.setAttribute('bg-color', '#36312C');
      docEl.setAttribute('text-color', '#ceb8a0');
    } else if (themeName === 'forest') {
      docEl.setAttribute('theme', 'dark');
      docEl.setAttribute('bg-color', '#384244');
      docEl.setAttribute('text-color', '#BDD6DB');
    } else if (themeName === 'olive') {
      docEl.setAttribute('theme', 'dark');
      docEl.setAttribute('bg-color', '#2a2f31');
      docEl.setAttribute('text-color', '#acc7c8');
    } else if (themeName === 'outerspace') {
      docEl.setAttribute('theme', 'dark');
      docEl.setAttribute('bg-color', '#2D3133');
      docEl.setAttribute('text-color', '#CAD9E3');
    } else if (themeName === 'ebony') {
      docEl.setAttribute('theme', 'dark');
      docEl.setAttribute('bg-color', '#2B303B');
      docEl.setAttribute('text-color', '#dee3ec');
    } else if (themeName === 'snow') {
      docEl.setAttribute('theme', 'light');
      docEl.setAttribute('bg-color', '#FAFAFA');
      docEl.setAttribute('text-color', '#555');
    } else if (themeName === 'green') {
      docEl.setAttribute('theme', 'light');
      docEl.setAttribute('bg-color', '#f9fdf7');
      docEl.setAttribute('text-color', '#375F1B');
    } else if (themeName === 'blue') {
      docEl.setAttribute('theme', 'light');
      docEl.setAttribute('bg-color', '#ecf1f7');
      docEl.setAttribute('text-color', '#133863');
    } else if (themeName === 'beige') {
      docEl.setAttribute('show-header', 'true');
      docEl.setAttribute('theme', 'light');
      docEl.setAttribute('bg-color', '#fdf8ed');
      docEl.setAttribute('text-color', '#342809');
    } else if (themeName === 'graynav') {
      getRapiDoc().setAttribute('render-style', 'read');
      docEl.setAttribute('show-header', 'false');
      docEl.setAttribute('theme', 'light');
      docEl.setAttribute('nav-bg-color', '#3e4b54');
      docEl.setAttribute('nav-accent-color', '#fd6964');
      docEl.setAttribute('primary-color', '#1ca72c');
    } else if (themeName === 'purplenav') {
      getRapiDoc().setAttribute('render-style', 'read');
      docEl.setAttribute('show-header', 'false');
      docEl.setAttribute('theme', 'light');
      docEl.setAttribute('nav-accent-color', '#ffd8e7');
      docEl.setAttribute('nav-bg-color', '#666699');
      docEl.setAttribute('primary-color', '#ea526f');
      docEl.setAttribute('bg-color', '#fff9fb');
    } else if (themeName === 'lightgraynav') {
      getRapiDoc().setAttribute('render-style', 'read');
      docEl.setAttribute('show-header', 'false');
      docEl.setAttribute('theme', 'light');
      docEl.setAttribute('nav-bg-color', '#fafafa');
      docEl.setAttribute('nav-hover-text-color', '#9b0700');
      docEl.setAttribute('nav-hover-bg-color', '#ffebea');
      docEl.setAttribute('primary-color', '#F63C41');
      docEl.setAttribute('bg-color', '#ffffff');
    } else if (themeName === 'darkbluenav') {
      getRapiDoc().setAttribute('render-style', 'read');
      docEl.setAttribute('show-header', 'false');
      docEl.setAttribute('theme', 'light');
      docEl.setAttribute('bg-color', '#f9f9fa');
      docEl.setAttribute('nav-bg-color', '#3f4d67');
      docEl.setAttribute('nav-text-color', '#a9b7d0');
      docEl.setAttribute('nav-hover-bg-color', '#333f54');
      docEl.setAttribute('nav-hover-text-color', '#fff');
      docEl.setAttribute('nav-accent-color', '#f87070');
      docEl.setAttribute('primary-color', '#5c7096');
    }

  }

  let renderStyles = ['read', 'view', 'focused'];
  let counter = 0;

  function changeRenderStyle() {

    let current = renderStyles[counter];

    counter++;

    if (counter == renderStyles.length) {
      counter = 0;
    }

    getRapiDoc().setAttribute('render-style', current);
  }
