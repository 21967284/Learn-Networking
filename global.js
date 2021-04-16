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

window.onload = onInit;

/**
 * Triggered once the window has finished loading/rendering
 * Calls functions that requires the html template to finish loading first
 */
function onInit() {
    constructNavigation();
    constructHeaderBar();

    //non content pages will not have explanation/results/quiz cards, so we do not need to turn on explanation mode
    if(isContentPage()) {
        explanationMode();
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
