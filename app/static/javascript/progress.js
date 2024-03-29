const STARS_TEMPLATE = '<i class="bi bi-star-fill"></i>'

const LIGHT_ORANGE = 'rgba(255, 131, 0, 0.2)';
const LIGHT_BLUE = 'rgba(54, 162, 235, 0.2)';
const LIGHT_YELLOW = 'rgba(255, 206, 86, 0.2)';
const LIGHT_GREEN = 'rgba(75, 192, 192, 0.2)';
const LIGHT_GREY = 'rgba(46, 49, 49, 0.2)';

const DARK_ORANGE = 'rgba(255, 131, 0, 1)';
const DARK_BLUE = 'rgba(54, 162, 235, 1)';
const DARK_YELLOW = 'rgba(255, 206, 86, 1)';
const DARK_GREEN = 'rgba(75, 192, 192, 1)';
const DARK_GREY = 'rgba(46, 49, 49, 1)';

const CHART_BACKGROUND_COLOURS = [LIGHT_ORANGE, LIGHT_BLUE, LIGHT_GREEN, LIGHT_YELLOW];
const CHART_BORDER_COLOURS = [DARK_ORANGE, DARK_BLUE, DARK_GREEN, DARK_YELLOW];

const CHART_OPTIONS = {
    responsive: true,
    aspectRatio: 1,
}

window.onload = onInit;

/**
 * Triggered once the window has finished loading/rendering
 */
function onInit() {
    loadAndProcessAccuracyData();
    loadAndProcessProgressData();
}

/**
 * Makes a HTTP call to fetch the accuracy data
 * Calls on other functions to process data once received
 */
function loadAndProcessAccuracyData() {
    $.ajax({
        url: '/retrieve-accuracy-data',
        type: "GET",
    }).done(result => {
        processAccuracyData(result);
    });
}

/**
 * Makes a HTTP call to fetch the progress data
 * Calls on other functions to process data once received
 */
function loadAndProcessProgressData() {
    $.ajax({
        url: '/retrieve-progress-data'
    }).done(result => {
        processProgressData(result);
    })
}

/**
 * Processes accuracy data, by converting the object into an array
 * uses array information to call other functions to calculate overall accuracy and no of stars to be rewarded
 * uses calculated info to show stars and build accuracy chart
 * @param accuracyData
 */
function processAccuracyData(accuracyData) {
    //create an array with the accuracy percentage only
    //essentially converts { 'Link': 40, 'Network': 10, 'Transport': 50, 'Application': 90} to [40, 10, 50, 90]

    const accuracyResultsArray = []
    accuracyResultsArray.push(accuracyData.Link, accuracyData.Network, accuracyData.Transport, accuracyData.Application);

    const overallAccuracy = calculateAndSetOverallAccuracy(accuracyResultsArray);
    const noOfStars = calculateAccuracyStars(overallAccuracy);
    setStars(noOfStars, 'accuracy');
    buildAccuracyChart(accuracyResultsArray);
}

/**
 * Calculates overall accuracy and displays it on the tile
 * @param accuracyResults - array of accuracy results by topic
 * @returns {number} - overall/average accuracy
 */
function calculateAndSetOverallAccuracy(accuracyResults) {
    let total = 0;

    accuracyResults.forEach(progress => {
        total += progress;
    });

    const overallAccuracy = total / accuracyResults.length;
    const overallAccuracyPercentage = overallAccuracy + '%';

    document.getElementById('overall-accuracy-percentage').innerHTML = overallAccuracyPercentage;
    $("#overall-accuracy-percentage-spinner").hide();

    return overallAccuracy;
}

/**
 * Calculates how many stars should be rewarded for the overall  accuracy mark
 * Each 20% is awareded one star
 * 20%: 1 star, 40%: 2 star, 60%: 3 star, 80%: 4 star, 100%: 5star
 * @param overallAccuracy
 * @returns {number} - no of stars to be rewarded
 */
function calculateAccuracyStars(overallAccuracy) {
    return overallAccuracy / 20;
}

/**
 * Processes accuracy data, by converting the object into an array
 * uses array information to calculate no of stars to be rewarded and
 * call other functions to calculate overall progress
 * uses calculated info to show stars and build accuracy chart
 * @param accuracyData
 */
function processProgressData(progressData) {
    const progressDataArray = []
    progressDataArray.push(progressData.Link, progressData.Network, progressData.Transport, progressData.Application);

    const noOfStars = progressDataArray.filter(Boolean).length;

    calculateAndSetOverallProgress(progressDataArray);
    setStars(noOfStars, 'progress');
    buildProgressChart(progressDataArray);
}

/**
 * Calculates overall progress and displays it on the tile
 * @param accuracyResults - array of progress results by topic
 */
function calculateAndSetOverallProgress(progressResults) {
    const overallProgress = progressResults.filter(Boolean).length / progressResults.length;
    const overallProgressPercentage = (overallProgress * 100) + '%';

    document.getElementById('overall-progress-percentage').innerHTML = overallProgressPercentage;
    $("#overall-progress-percentage-spinner").hide()
}

/**
 * Builds accuracy chart using chart.js library
 * @param accuracyData - array of accuracy results by topic
 */
function buildAccuracyChart(accuracyData) {
    const progressChartElement = document.getElementById('accuracy-chart').getContext('2d');
    new Chart(progressChartElement, {
        type: 'bar',
        data: {
            labels: ['Link', 'Network', 'Transport', 'Application'],
            datasets: [{
                label: 'Percentage completion by topic',
                data: accuracyData,
                backgroundColor: CHART_BACKGROUND_COLOURS,
                borderColor: CHART_BORDER_COLOURS,
                borderWidth: 2
            }]
        },
        options: CHART_OPTIONS
    });

    $("#overall-accuracy-chart-spinner").hide();
}

/**
 * Builds progress chart using chart.js library
 * @param progressData - array of progrss results by topic
 */
function buildProgressChart(progressData) {
    //uses progressData array to determine which colour to shade in the doughnut chart
    //if the user has completed the topic (ie progressData[topicNo] == true), the chart section will display in colour, else it will be in grey
    const backgroundColours = CHART_BACKGROUND_COLOURS.map((colour, index) => {
        if (progressData[index] == false) {
            return LIGHT_GREY
        } else return colour;
    });

    const backgroundBorderColours = CHART_BORDER_COLOURS.map((colour, index) => {
        if (progressData[index] == false) {
            return DARK_GREY
        } else return colour;
    });

    const progressChartElement = document.getElementById('progress-chart').getContext('2d');
    new Chart(progressChartElement, {
        type: 'doughnut',
        data: {
            labels: ['Link', 'Network', 'Transport', 'Application'],
            datasets: [{
                label: 'Percentage completion by topic',
                data: [1, 1, 1, 1],
                backgroundColor: backgroundColours,
                borderColor: backgroundBorderColours,
                borderWidth: 2
            }]
        },
        options: CHART_OPTIONS
    });

    $("#overall-progress-chart-spinner").hide();

}


/**
 * Function to alter the number of stars shown on screen for progress and accuracy tiles
 * @param noOfStars - how many stars it should show
 * @param tile - which tile (accuracy or progress) it is for
 */
function setStars(noOfStars, tile) {
    for (i = 0; i < noOfStars; i++) {
        $(`#${tile}-star-container`).append(STARS_TEMPLATE);
    }

    $(`#${tile}-star-spinner`).hide();
    $(`#${tile}-star-container`).show();
}
