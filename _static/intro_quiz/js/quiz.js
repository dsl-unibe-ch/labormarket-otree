let questionIdx = 1;

const MAX_ID = Object.keys(js_vars.questions).length;
const NO_ANSWER = "Please answer the question";
//const HINT_TIMEOUT = 4000;

$(`#container-quiz${questionIdx}`).removeClass("hidden");
$("#next-button").on("click", checkAnswers);

function getCheckedRadioButton() {
  return $(`input[name="quiz${questionIdx}"]:checked`)[0] || null;
}

function clearRadioButtons() {
  const checkedRadioButton = getCheckedRadioButton();
  if (checkedRadioButton !== null) {
    checkedRadioButton.checked = false;
  }
}

function checkAnswers() {
  const checkedRadioButton = getCheckedRadioButton()
  const correct = check(js_vars.answers[questionIdx - 1], checkedRadioButton);

//  setTimeout(function () {
//    $("#hint-modal").modal("hide");
//    if (correct) {
//      nextQuestion();
//    }
//
//    if (checkedRadioButton !== null) {
//      checkedRadioButton.checked = false;
//    }
//  }, HINT_TIMEOUT);
}

function check(correctId, checkedRadioButton) {
  if (checkedRadioButton === null) {
    // No answer provided.
    showModal(NO_ANSWER);
    return false;
  } else if (checked(`quiz${questionIdx}-${correctId}`)) {
    // Correct answer provided.
    showModal(js_vars.hints[questionIdx - 1][1], true);
    return true;
  } else {
    // Incorrect answer provided.
    showModal(js_vars.hints[questionIdx - 1][0], false);
    return false;
  }
}

function checked(id) {
  return $(`#${id}`).prop("checked");
}

function showModal(message, correct) {
  $("#modal-title").html(correct ? "&#9989; Correct" : "&#10060; Incorrect");
  $("#modal-message").html(message);
  $("#close-button").html(correct ? "Next" : "Try again");

  const modal = $("#hint-modal");

  modal.off("hidden.bs.modal");
  modal.on("hidden.bs.modal", correct ? nextQuestion : clearRadioButtons);

  modal.modal({
    backdrop: "static",
    keyboard: false
  });
  modal.modal("show");
}

function nextQuestion() {
  // Hide current quiz
  $(`#container-quiz${questionIdx}`).addClass("hidden");

  // Increase quiz id
  questionIdx += 1;

  if (questionIdx > MAX_ID) {
    // If there are no more questions, we are done, submit form
    $("#form").submit();
  } else {
    // Show next quiz, skip over dropped
    let nextQuiz = $(`#container-quiz${questionIdx}`);
    while (nextQuiz === null && questionIdx < MAX_ID) {
      questionIdx += 1;
      nextQuiz = $(`#container-quiz${questionIdx}`);
    }
    nextQuiz.removeClass("hidden");
  }
}
