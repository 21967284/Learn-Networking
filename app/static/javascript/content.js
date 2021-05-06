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

window.onload = onInit;

function onInit() {
    explanationMode();
}

/**
 * Turns page into 'explanation mode' by showing only the explanation card and hiding the quiz and results card
 */
function explanationMode() {
    $('#results-card').hide();
    $('#quiz-card').hide();
    $('#explanation-card').show();
}

/**
 * Turns page into 'quiz mode' by showing only the quiz card and hiding the explanation and results card
 */
function quizMode() {
    loadQuizQuestions();
    $('#results-card').hide();
    $('#explanation-card').hide();
    $('#quiz-card').show();
}

/**
 * Turns page into 'quiz mode' by showing only the results card and hiding the explanation and quiz card
 */
function resultsMode() {
    $('#explanation-card').hide();
    $('#quiz-card').hide();
    $('#results-card').show();
}

/**
 * Retrieve quiz questions from server
 * Use results to dynamically generate the quiz question form
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
    $.ajax({
        url: '/retrieve-questions',
        type: "GET",
        data: {
            topic: document.title
        },
    }).done(result => {

        result.data.forEach(questionSet => {
            const questionConfig = [{
                'questionContent': questionSet.questionContent,
                'questionId': questionSet.questionId
            }];

            $("#questions-form").append(questionConfig.map(QUESTIONS_TEMPLATE))

            questionSet.answerOptions.forEach(option => {
                const answerOptionsConfig = [{
                    'name': `${questionSet.questionId}`,
                    'id': `${option}`,
                    'value': `${option}`,
                    'text': `${option}`
                }];

                $(`#${questionSet.questionId}-container`).append(answerOptionsConfig.map(ANSWERS_OPTIONS_TEMPLATE))
            });
        });

        $('#questions-spinner').hide();
    });
}
