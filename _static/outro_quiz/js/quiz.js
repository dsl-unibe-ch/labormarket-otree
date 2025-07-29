let questionIdx = 1;

const MAX_ID = Object.keys(js_vars.questions).length;
const NO_ANSWER = "Please answer the question";

// Show the first question
document.getElementById(`container-quiz${questionIdx}`).classList.remove("hidden");

// Attach click handler to Next button
document.getElementById("next-button").addEventListener("click", checkAnswers);

function getCheckedRadioButton() {
  return document.querySelector(`input[name="quiz${questionIdx}"]:checked`);
}

function clearRadioButtons() {
  const checkedRadioButton = getCheckedRadioButton();
  if (checkedRadioButton !== null) {
    checkedRadioButton.checked = false;
  }
}

function checkAnswers() {
  const checkedRadioButton = getCheckedRadioButton()
  const correct = check(checkedRadioButton);
  if (correct) {
    nextQuestion();
  }
}

function check(checkedRadioButton) {
  if (checkedRadioButton === null) {
    // No answer provided.
    showModal(NO_ANSWER, false);
    return false;
  } else {
    // Answer provided.
    return true;
  }
}

function checked(id) {
  const el = document.getElementById(id);
  return el ? el.checked : false;
}

function showModal(message, correct) {
  const titleEl = document.getElementById("hint-modal-title");
  const msgEl = document.getElementById("hint-modal-message");
  const btnEl = document.getElementById("hint-modal-close-button");
  const modalEl = document.getElementById("hint-modal");

  titleEl.innerHTML = correct ? "&#9989; Correct" : "&#10060; Incorrect";
  msgEl.innerHTML = message;
  btnEl.textContent = correct ? "Next" : "Try again";

  // Remove old listeners
  modalEl.removeEventListener("hidden.bs.modal", nextQuestion);
  modalEl.removeEventListener("hidden.bs.modal", clearRadioButtons);

  modalEl.addEventListener("hidden.bs.modal", correct ? nextQuestion : clearRadioButtons);

  let modal = bootstrap.Modal.getInstance(modalEl);
  if (!modal) {
    modal = new bootstrap.Modal(modalEl, {
      backdrop: "static",
      keyboard: true
    });
  }

  modal.show();
}

function nextQuestion() {
  // Hide current quiz
  const currentContainer = document.getElementById(`container-quiz${questionIdx}`);
  if (currentContainer) {
    currentContainer.classList.add("hidden");
  }

  // Increase quiz index
  questionIdx += 1;

  if (questionIdx > MAX_ID) {
    // Submit form if no more questions
    document.getElementById("form").submit();
  } else {
    // Show next available quiz
    let nextContainer = document.getElementById(`container-quiz${questionIdx}`);
    while (!nextContainer && questionIdx < MAX_ID) {
      questionIdx += 1;
      nextContainer = document.getElementById(`container-quiz${questionIdx}`);
    }

    if (nextContainer) {
      nextContainer.classList.remove("hidden");
    }
  }
}
