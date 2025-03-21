function initModal() {
  const btnOpen   = document.getElementById('btnNieuwOnderzoek');
  const modal     = document.getElementById('modalNieuwOnderzoek');
  const btnClose  = document.getElementById('closeModal');
  const form      = document.getElementById('formNieuwOnderzoek');


  if (!btnOpen || !modal || !btnClose || !form) return;


  btnOpen.onclick = () => {
    modal.style.display = 'block';
    const naamInput = form.querySelector('#naamOnderzoek');
    if (naamInput) naamInput.focus();
  };


  btnClose.onclick = () => {
    modal.style.display = 'none';
  };


  window.onclick = (event) => {
    if (event.target === modal) {
      modal.style.display = 'none';
    }
  };


  form.onsubmit = (event) => {

    const naam = form.querySelector('#naamOnderzoek').value.trim();
    const beschrijving = form.querySelector('#beschrijvingOnderzoek').value.trim();

    if (!naam || !beschrijving) {
      event.preventDefault();
      alert("Vul alstublieft alle verplichte velden in (Naam en Beschrijving).");
      return;
    }

  };
}

document.addEventListener('DOMContentLoaded', initModal);
