//constants
const PAGE_ITEMS = [
    {
        label: 'home',
        icon: 'house',
        link: '../otherPages/home.html',
        pageTitle: 'A journey through the tcp/ip model'
    },
    {
        label: 'Login',
        icon: 'door-open',
        link: '../otherPages/login.html',
        pageTitle: 'Login'
    },
    {
        label: 'App',
        icon: 'window',
        link: '../contentPages/application-forward.html',
        pageTitle: 'Application Layer'
    },
    {
        label: 'Transport',
        icon: 'truck',
        link: 'www.google.com',
        pageTitle: 'Transport Layer'
    },
    {
        label: 'Network',
        icon: 'hdd-network',
        link: 'www.google.com',
        pageTitle: 'Network Layer'

    },
    {
        label: 'Link',
        icon: 'link',
        link: 'www.google.com',
        pageTitle: 'Link Layer'
    },
    {
        label: 'Network',
        icon: 'hdd-network',
        link: 'www.google.com',
        pageTitle: 'Network Layer'
    },
    {
        label: 'Transport',
        icon: 'truck',
        link: 'www.google.com',
        pageTitle: 'Transport Layer'
    },
    {
        label: 'App',
        icon: 'window',
        link: 'www.google.com',
        pageTitle: 'Application Layer'
    },
    {
        label: 'Result',
        icon: 'check2-square',
        link: '../otherPages/results.html',
        pageTitle: 'Results'
    }
]


const NAVIGATION_ITEM_TEMPLATE = ({label, icon, link}) => `
    <li class="nav-item"> 
      <a class="nav-link active jetbrains-mono-font" href="${link}">
        <i class="bi bi-${icon} mr-15"></i>
        ${label}      
      </a>
    </li>`;

const HEADER_BAR_TEMPLATE = ({pageTitle}) => `
   <div class="transparent-glass-card p-3 m-3">
      <h1 class="major-mono-font white-text d-flex justify-content-center">Networking</h1>

      <h2 class="major-mono-font white-text d-flex justify-content-center mb-30">${pageTitle}</h2>
    </div>`;

const HEAD_IMPORTS = [
    {
        id: "bootstrapcss",
        type: 'link',
        url: "https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css",
        rel: "stylesheet",
        integrity: "sha384-eOJMYsd53ii+scO/bJGFsiCZc+5NDVN2yr8+0RDqr0Ql0h+rP48ckxlpbzKgwra6", 
        crossorigin: "anonymous"
    },
    {
        id: "bootstrapcdn",
        type: 'link',
        url: "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css",
        rel: "stylesheet"
    },
    {
        id: "bootstrapicons",
        type: 'link',
        url: "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.4.1/font/bootstrap-icons.css",
        rel: "stylesheet"
    },
    {
        id: "gfpreconnect",
        type: 'link',
        url: "https://fonts.gstatic.com",
        rel: "preconnect"
    },
    {
        id: "gffonts",
        type: 'link',
        url: "https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@200;400&family=Major+Mono+Display&family=Press+Start+2P&display=swap",
        rel: "stylesheet"
    },
    {
        id: "globalcss",
        type: 'link',
        url: "../../global.css", 
        rel: "stylesheet"
    }
]

window.onload = onInit;

/**
 * Triggered once the window has finished loading/rendering
 * Calls functions that requires the html template to finish loading first
 */
function onInit() {
    HEAD_IMPORTS.forEach(importElement);
    constructNavigation();
    constructHeaderBar();

    //non content pages will not have explanation/results/quiz cards, so we do not need to turn on explanation mode
    if(isContentPage()) {
        explanationMode();
    }
}

/**
 * Imports a given link into the head
 * Appends an element to the document head using its details found in the constants section
 * uses element.type instead of 'link' in case we want to add other types to import
 */
 function importElement(element){
    if (!document.getElementById(element.id))
    {
        var head  = document.getElementsByTagName('head')[0];
        var newElement = document.createElement(element.type);
        newElement.id = element.id;
        newElement.rel = element.rel;
        newElement.href = element.url;
        head.appendChild(newElement);
    }
}

/**
 * Constructs the navigation bar
 * Uses html template specified in NAVIGATION_ITEM_TEMPLATE and
 * navigation items specified in PAGE_ITEMS
 */
function constructNavigation() {
    $('#navigationBar').html(PAGE_ITEMS.map(NAVIGATION_ITEM_TEMPLATE).join(''));
}

/**
 * Constructs header bar
 * Uses html template specified in HEADER_BAR_TEMPLATE
 * Determine current page using path name
 * Note this is dependent on the current directory naming convention - if directory is changed, this will need to be updated
 */
function constructHeaderBar() {
    const pathName = window.location.pathname;
    const indexOfCurrentPage = pathName.match('Pages/').index;
    const identifier = pathName.slice( indexOfCurrentPage );

    const currentPage = PAGE_ITEMS.filter((item) => item.link.search(identifier) !== -1);

    $('#headerBar').html(currentPage.map(HEADER_BAR_TEMPLATE).join(''));
}

/**
 * Turns page into 'explanation mode' by showing only the explanation card and hiding the quiz and results card
 */
function explanationMode() {
    hideElementById('quiz-card');
    hideElementById('results-card');
    showElementById('explanation-card');
}

/**
 * Turns page into 'quiz mode' by showing only the quiz card and hiding the explanation and results card
 */
function quizMode() {
    hideElementById('explanation-card');
    hideElementById('results-card');
    showElementById('quiz-card');
}

/**
 * Turns page into 'quiz mode' by showing only the results card and hiding the explanation and quiz card
 */
function resultsMode() {
    hideElementById('quiz-card');
    hideElementById('explanation-card');
    showElementById('results-card');
}


/**
 * Evaluates the quiz submission
 */
function evaluateSubmission() {
    //something to send data to server and retrieve results
    resultsMode();
}

/**
 * Determines if current page is content page or not
 * @returns {boolean}
 */
function isContentPage() {
    const pathName = window.location.pathname;
    return Boolean(pathName.match('content'));
}


//'Utility' functions

/**
 * Shows elements by Id
 * Retrieves element by Id, removes bootstrap's d-none class if present and adds bootstrap's d-block class to make it visible
 * @ param - string of elementId
 */
function showElementById(id) {
    let element = document.getElementById(id);

    element.classList.forEach( className => {
        if (className === 'd-none') {
            element.classList.remove("d-none");
        }
    });
    element.classList.add("d-block");
}

/**
 * Hide elements by Id
 * Retrieve elements by Id, resmoves bootstrap's d-block class if present and add bootstraps' d-none class to hide it
 * @ param - string of elementId
 */
function hideElementById(id) {
    let element = document.getElementById(id);
    element.classList.forEach( className => {
        if (className === 'd-block') {
            element.classList.remove("d-block");
        }
    });
    element.classList.add("d-none");
}
