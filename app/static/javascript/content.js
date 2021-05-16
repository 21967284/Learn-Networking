/**
 * Redirects user to quiz section of correct topic/layer
 */
function goToQuiz() {
    const layer = document.title.replace(' Layer', '').toLowerCase();
    window.location.href = `${layer}-quiz`;
}
