function initModal() {
    const btnOpen = document.getElementById('btnNieuwOnderzoek');
    const modal = document.getElementById('modalNieuwOnderzoek');
    const btnClose = document.getElementById('closeModal');
    const form = document.getElementById('formNieuwOnderzoek');
    const popup = document.getElementById('succesPopup');
    if (!btnOpen || !modal || !btnClose || !form || !popup) return;
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
      event.preventDefault();
      const naam = form.querySelector('#naamOnderzoek').value.trim();
      const beschrijving = form.querySelector('#beschrijvingOnderzoek').value.trim();
      if (!naam || !beschrijving) {
        alert("Vul alstublieft alle verplichte velden in (Naam en Beschrijving).");
        return;
      }
      modal.style.display = 'none';
      form.reset();
      popup.innerText = "Uw onderzoek is verzonden!";
      popup.classList.add('show');
      setTimeout(() => {
        popup.classList.remove('show');
      }, 3000);
    };
  }
  document.addEventListener('DOMContentLoaded', initModal);
  