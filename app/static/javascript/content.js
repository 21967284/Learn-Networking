/**
 * Turns page into 'quiz mode' by showing only the quiz card and hiding the explanation and results card
 */
function goToQuiz() {
    const layer = document.title.replace(' Layer', '').toLowerCase();
    window.location.href = `${layer}-quiz`;
}
