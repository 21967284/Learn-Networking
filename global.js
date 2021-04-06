const NAVIGATION_ITEMS = [
    {
        label: 'home',
        icon: 'house',
        link: 'www.google.com'
    },
    {
        label: 'Login',
        icon: 'door-open',
        link: 'www.google.com'
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
        link: 'www.google.com'
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
 * Shows elements by Id
 * Retrieves element by Id and adds bootstrap's d-block class to make it visible
 * @ param - string of elementId
 */
function showElementById(id) {
    let element = document.getElementById(id);
    element.classList.add("d-block");
}

/**
 * Hide elements by Id
 * Retrieve elements by Id and add bootstraps' d-none class to hide it
 * @ param - string of elementId
 */
function hideElementById(id) {
    let element = document.getElementById(id);
    element.classList.add("d-none");
}
