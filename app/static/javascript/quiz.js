const QUESTIONS_TEMPLATE = ({questionContent, questionId}) => `
    <label for="${questionId}" id="${questionId}">${questionContent}</label>
    <div class="m-2" id="${questionId}-container"></div>
    <hr>
`;

const ANSWERS_OPTIONS_TEMPLATE = ({name, id, value, text}) => `
    <div class="form-check">
        <input class="form-check-input" type="radio" name="${name}" id="${id}" value="${value}">
            <label class="form-check-label" for="${id}">
                ${text}
            </label>
            <br>
    </div>

`
const STARS_TEMPLATE = '<i class="bi bi-star-fill"></i>'

const LAYER_ORDER = ['Link', 'Network', 'Transport', 'Application'];


window.onload = onInit;

function onInit() {
    $("#no-questions-alert").hide();
    $("#quiz-previously-attempted-alert").hide();
    quizMode();
    loadQuizQuestions();
}

/**
 * Turns page into 'quiz mode' by showing only the quiz card and hiding the explanation and results card
 */
function quizMode() {
    $('#quiz-card').show();
    $('#results-card').hide();
}

/**
 * Turns page into 'results mode' by showing only the results card and hiding the explanation and quiz card
 */
function resultsMode() {
    $('#quiz-card').hide();
    $('#results-card').show();
}

/**
 * Retrieve quiz questions from server
 * Shows alert if there are no quiz questions
 * Otherwise, Calls on another function to dynamically build quiz form from result
 * Expected result format from server -
 * [{
 *     'questionContent': 'What is 1 + 1?',
 *     'questionId': 'question1',
 *     'answerOptions': [1, 2, 3, 4]
 * },{
 *     'questionContent': 'What is 1 + 1?',
 *     'questionId': 'question1',
 *     'answerOptions': [1, 2, 3, 4]
 * }]
 */
function loadQuizQuestions() {
    const topic = document.title.replace(' Layer Quiz', '');
    $.ajax({
        url: '/retrieve-questions',
        type: "GET",
        data: {
            topic: topic
        },
    }).done(result => {
        if (!result.data.length) {
            setAlertAndHideInnerQuizCard();
        }
        buildQuiz(result);
        $('#questions-spinner').hide();
    });
}

/**
 * Dynamically builds the quiz form based
 * @param result
 */
function buildQuiz(result) {
    result.data.forEach(questionSet => {
        const questionConfig = [{
            'questionContent': questionSet.questionContent,
            'questionId': questionSet.questionId
        }];

        $("#questions-form").append(questionConfig.map(QUESTIONS_TEMPLATE))

        questionSet.answerOptions.forEach(option => {
            console.log('')
            const answerOptionsConfig = [{
                'name': `${questionSet.questionId}`,
                'id': `${option.id}`,
                'value': `${option.answer}`,
                'text': `${option.answer}`
            }];
            $(`#${questionSet.questionId}-container`).append(answerOptionsConfig.map(ANSWERS_OPTIONS_TEMPLATE))
        });
    });
}

/**
 * Shows an alert indicating that there are no questions available for that particular topic
 * Only used if server does not return any questions
 * Hides the submit button as there is no quiz form to submit
 */
function setAlertAndHideInnerQuizCard() {
    $("#no-questions-alert").show();
    $("#inner-quiz-card").hide();
}

/**
 * Sends form response to be evaluated by server
 * Process the result and switch to results mode
 */
function evaluateSubmission() {
    //gives name based on question-id and returns value based on selected choice
    const form = $("form").serializeArray();
    const mappedFormData = form.map(item => {
        const question_id = item.name.replace("question-id-", "");
        console.log('item', item);
        return {
            'question_id': question_id,
            'answer': item.value
        }
    });
    const currentTopic = document.title.replace(' Layer Quiz', '');

    const bodyData = {
        topic: currentTopic,
        quizData: mappedFormData
    }
    console.log('mapepdformdata', mappedFormData);
    $.ajax({
        url: '/submit-quiz',
        type: "POST",
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify(bodyData),
    }).done(result => {
        if (result.error) {
            processError();
        } else {
            processResults(result.data);
            resultsMode();
        }
    })
}

function processError() {
    $("#quiz-previously-attempted-alert").show();
}

/**
 * process results by showing percentage result on screen and
 * calculating and showing the number of stars to be awarded
 * @param result
 */
function processResults(result) {
    setPercentage(result);
    calculateAndSetStars(result);
}

/**
 * Displays the result on screen
 * @param result
 */
function setPercentage(result) {
    const resultPercentage = result + '%';
    document.getElementById('results-percentage').innerHTML = resultPercentage;
    $("#results-percentage-spinner").hide();
}

/**
 * Calculates how many stars should bae rewarded for the accuracy mark
 * Each 20% is awareded one star
 * 20%: 1 star, 40%: 2 star, 60%: 3 star, 80%: 4 star, 100%: 5star
 * Calls on setStars to generate correct number of stars to show
 * @param result
 */
function calculateAndSetStars(result) {
    const noOfStars = result / 20;
    setStars(noOfStars);
}

/**
 * Function to alter the number of stars shown on screen for progress and accuracy tiles
 * @param noOfStars - how many stars it should show
 */
function setStars(noOfStars) {
    for (i = 0; i < noOfStars; i++) {
        $("#results-star-container").append(STARS_TEMPLATE);
    }

    $("#results-star-spinner").hide();
    $("#results-star-container").show();
}

/**
 * Proceeds to explanation section of next layer
 */
function proceedToNextLayer() {
    const currentLayer = document.title.replace(' Layer Quiz', '');
    const nextLayer = LAYER_ORDER[LAYER_ORDER.indexOf(currentLayer) + 1].toLowerCase();
    window.location.href = `${nextLayer}`;
}