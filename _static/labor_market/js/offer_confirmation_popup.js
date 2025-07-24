function offerConfirmationModalOnConfirm(event) {
    console.log(event);
}

function showOfferConfirmationModal(worker, salary, training) {
    const workerEl = document.getElementById("offer-confirmation-modal-worker-name");
    const salaryEl = document.getElementById("offer-confirmation-modal-salary");
    const trainingEl = document.getElementById("offer-confirmation-modal-training");
    const modalEl = document.getElementById("offer-confirmation-modal");

    workerEl.innerHTML = worker;
    salaryEl.innerHTML = salary;
    trainingEl.innerHTML = training ? "Yes" : "No";

    // Remove any existing listener
    modalEl.removeEventListener("hidden.bs.modal", offerConfirmationModalOnConfirm);
    modalEl.addEventListener("hidden.bs.modal", offerConfirmationModalOnConfirm);

    const modal = new bootstrap.Modal(modalEl, {
        backdrop: "static",
        keyboard: true
    });

    modal.show();
}

function onSendOfferClick(event) {
    event.preventDefault();

    const employeeInput = document.querySelector("input[name='offer_employee']:checked");
    const salaryInput = document.getElementById("id_offer_wage");
    const trainingInput = document.querySelector("input[name='offer_training']:checked");

    const worker = employeeInput ? employeeInput.dataset.label : "";
    const salary = salaryInput ? salaryInput.value : "";
    const training = trainingInput ? trainingInput.value === "True" : false;

    showOfferConfirmationModal(worker, salary, training);
}

const sendOfferInput = document.getElementById("send_offer");
sendOfferInput.removeEventListener("click", onSendOfferClick);
sendOfferInput.addEventListener("click", onSendOfferClick);