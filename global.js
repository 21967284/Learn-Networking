//constants
const NAVIGATION_ITEMS = [
    {
        label: 'home',
        icon: 'house',
        link: '../otherPages/home.html'
    },
    {
        label: 'Login',
        icon: 'door-open',
        link: '../otherPages/login.html'
    },
    {
        label: 'App',
        icon: 'window',
        link: 'www.google.com'
    },
    {
        label: 'Transport',
        icon: 'truck',
        link: 'www.google.com'
    },
    {
        label: 'Network',
        icon: 'hdd-network',
        link: 'www.google.com'
    },
    {
        label: 'Link',
        icon: 'link',
        link: 'www.google.com'
    },
    {
        label: 'Network',
        icon: 'hdd-network',
        link: 'www.google.com'
    },
    {
        label: 'Transport',
        icon: 'truck',
        link: 'www.google.com'
    },
    {
        label: 'App',
        icon: 'window',
        link: 'www.google.com'
    },
    {
        label: 'Result',
        icon: 'check2-square',
        link: '../otherPages/results.html'
    }
]

const NAVIGATION_ITEM_TEMPLATE = ({label, icon, link}) => `
    <li class="nav-item"> 
      <a class="nav-link active jetbrains-mono-font" href="${link}">
        <i class="bi bi-${icon} mr-15"></i>
        ${label}      
      </a>
    </li>`;

window.onload = onInit;

/**
 * Triggered once the window has finished loading/rendering
 * Calls functions that requires the html template to finish loading first
 */
function onInit() {
    constructNavigation();
    explanationMode();
}

/**
 * Constructs the navigation bar
 * Uses html template specified in NAVIGATION_ITEM_TEMPLATE and
 * navigation items specified in NAVGIATION_ITEMS
 */
function constructNavigation() {
    $('#navigationBar').html(NAVIGATION_ITEMS.map(NAVIGATION_ITEM_TEMPLATE).join(''));
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
