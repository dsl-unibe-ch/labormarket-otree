function offerConfirmationModalOnConfirm(event) {
    const modalEl = document.getElementById("offer-confirmation-modal")
    const modal = bootstrap.Modal.getInstance(modalEl)
    modal.hide()

    const nullChoice = document.querySelector("input[name='offer_employee'][value='0']");

    if (nullChoice.checked) {
        document.querySelector("input[name='offer_training'][value='False']").checked = true;
        // Required by InputSpinner
        document.querySelector("input[name='offer_wage']").setValue(1);
        document.getElementById("id_offer_wage:input_spinner").value = 1;
    }

    event.target.form.submit();
}

function showOfferConfirmationModal(worker, salary, training) {
    const workerEl = document.getElementById("offer-confirmation-modal-worker-name");
    const salaryEl = document.getElementById("offer-confirmation-modal-salary");
    const trainingEl = document.getElementById("offer-confirmation-modal-training");
    const modalEl = document.getElementById("offer-confirmation-modal");

    const offerModalBodyEl = document.getElementById("offer-modal-body");
    const noOfferModalBodyEl = document.getElementById("no-offer-modal-body");
    const confirmButtonEl = document.getElementById("offer-confirmation-modal-confirm-button");

    workerEl.innerHTML = worker;
    salaryEl.innerHTML = salary;
    trainingEl.innerHTML = training ? "Yes" : "No";

    if (worker === null && salary === null && training === null) {
        // No offer case
        offerModalBodyEl.style.display = "none";
        noOfferModalBodyEl.style.display = "block";
        confirmButtonEl.innerHTML = "Confirm No Offer";
    } else {
        // Offer selected case
        offerModalBodyEl.style.display = "block";
        noOfferModalBodyEl.style.display = "none";
        confirmButtonEl.innerHTML = "Confirm Offer";
    }

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

function onNoOffersClick(event) {
    event.preventDefault();
    showOfferConfirmationModal(null, null, null);
}

const sendOfferInput = document.getElementById("send_offer");
sendOfferInput.removeEventListener("click", onSendOfferClick);
sendOfferInput.addEventListener("click", onSendOfferClick);

const noOffersInput = document.getElementById("no_offers");
noOffersInput.removeEventListener("click", onNoOffersClick);
noOffersInput.addEventListener("click", onNoOffersClick);