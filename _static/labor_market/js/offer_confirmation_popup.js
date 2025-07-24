function offerConfirmationModalOnConfirm(event) {
    const modalEl = document.getElementById("offer-confirmation-modal")
    const modal = bootstrap.Modal.getInstance(modalEl)
    modal.hide()

    event.target.form.submit();
}

function showOfferConfirmationModal(worker, salary, training) {
    const workerEl = document.getElementById("offer-confirmation-modal-worker-name");
    const salaryEl = document.getElementById("offer-confirmation-modal-salary");
    const trainingEl = document.getElementById("offer-confirmation-modal-training");
    const modalEl = document.getElementById("offer-confirmation-modal");

    workerEl.innerHTML = worker;
    salaryEl.innerHTML = salary;
    trainingEl.innerHTML = training ? "Yes" : "No";

    const confirmButtonEl = document.getElementById("offer-confirmation-modal-confirm-button");
    confirmButtonEl.removeEventListener("click", offerConfirmationModalOnConfirm);
    confirmButtonEl.addEventListener("click", offerConfirmationModalOnConfirm);

    let modal = bootstrap.Modal.getInstance(modalEl);
    if (!modal) {
      modal = new bootstrap.Modal(modalEl, {
        backdrop: "static",
        keyboard: true
      });
    }

    modal.show();
}

function onSendOfferClick(event) {
    event.preventDefault();

    const form = event.target.form;

    if (!form.checkValidity()) {
      if (form.reportValidity) {
        form.reportValidity();
      } else {
        alert(msg.ieErrorForm);
      }
    } else {
      const employeeInput = document.querySelector("input[name='offer_employee']:checked");
      const salaryInput = document.getElementById("id_offer_wage");
      const trainingInput = document.querySelector("input[name='offer_training']:checked");

      const worker = employeeInput ? employeeInput.dataset.label : "";
      const salary = salaryInput ? salaryInput.value : "";
      const training = trainingInput ? trainingInput.value === "True" : false;

      showOfferConfirmationModal(worker, salary, training);
    }
}

const sendOfferInput = document.getElementById("send_offer");
sendOfferInput.removeEventListener("click", onSendOfferClick);
sendOfferInput.addEventListener("click", onSendOfferClick);