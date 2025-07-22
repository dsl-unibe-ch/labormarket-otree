let questionIdx = 1;

const MAX_ID = Object.keys(js_vars.questions).length;
const NO_ANSWER = "Please answer the question";
const HINT_TIMEOUT = 4000;

document.getElementById(`container-quiz${questionIdx}`).classList.remove("hidden");
document.getElementById("next-button").addEventListener("click", checkAnswers);

function getCheckedRadioButton() {
  for (let checkBox of document.getElementsByName(`quiz${questionIdx}`)) {
    if (checkBox.checked) {
      return checkBox;
    }
  }
  return null;
}

function checkAnswers() {
  const checkedRadioButton = getCheckedRadioButton()
  const correct = check(js_vars.answers[questionIdx - 1], checkedRadioButton);

  setTimeout(function () {
    $("#hint-modal").modal("hide");
    if (correct) {
      nextQuestion();
    }

    if (checkedRadioButton !== null) {
      checkedRadioButton.checked = false;
    }
  }, HINT_TIMEOUT);
}

function check(correctId, checkedRadioButton) {
  if (checkedRadioButton === null) {
    // No answer provided.
    showModal(NO_ANSWER);
    return false;
  } else if (checked(`quiz${questionIdx}-${correctId}`)) {
    // Correct answer provided.
    showModal(js_vars.hints[questionIdx - 1][1]);
    return true;
  } else {
    // Incorrect answer provided.
    showModal(js_vars.hints[questionIdx - 1][0]);
    return false;
  }
}

function checked(id) {
  return document.getElementById(id).checked;
}

function showModal(message) {
  document.getElementById("modal-message").innerHTML = message;
  $('#hint-modal').modal({
    backdrop: 'static',
    keyboard: false
  });
  $('#hint-modal').modal('show');
}

function nextQuestion() {
  // Hide current quiz
  document.getElementById(`container-quiz${questionIdx}`).classList.add("hidden");

  // Increase quiz id
  questionIdx += 1;

  if (questionIdx > MAX_ID) {
    // If there are no more questions, we are done, submit form
    document.getElementById('form').submit();
  } else {
    // Show next quiz, skip over dropped
    let nextQuiz = document.getElementById(`container-quiz${questionIdx}`);
    while (nextQuiz === null && questionIdx < MAX_ID) {
      questionIdx += 1;
      nextQuiz = document.getElementById(`container-quiz${questionIdx}`);
    }
    nextQuiz.classList.remove("hidden");
  }
}
