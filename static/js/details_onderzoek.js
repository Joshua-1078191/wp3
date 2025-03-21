function initDetailButtons() {
    const detailButtons = document.querySelectorAll('.details-btn');
    const modal = document.getElementById('modalDetailOnderzoek');
    const closeModal = document.getElementById('closeDetailModal');

    if (!detailButtons || !modal || !closeModal) return;

    function hideModal() {
        modal.style.display = 'none';
    }

    closeModal.onclick = hideModal;

    window.onclick = (event) => {
        if (event.target === modal) {
            hideModal();
        }
    };

    detailButtons.forEach((btn) => {
        btn.addEventListener('click', () => {
            const onderzoekId = btn.dataset.onderzoekId;
            if (!onderzoekId) return;

            fetch(`/api/onderzoek/${onderzoekId}`)
                .then((res) => res.json())
                .then((data) => {
                    if (!data.success) {
                        alert('Onderzoek niet gevonden of fout.');
                        return;
                    }
                    const ond = data.onderzoek;
                    document.getElementById('detail_titel').innerText = ond.titel;
                    document.getElementById('detail_status').innerText = ond.status;
                    document.getElementById('detail_beschrijving').innerText = ond.beschrijving;
                    document.getElementById('detail_datum_vanaf').innerText = ond.datum_vanaf;
                    document.getElementById('detail_datum_tot').innerText = ond.datum_tot;
                    document.getElementById('detail_type_onderzoek').innerText = ond.type_onderzoek;
                    document.getElementById('detail_locatie').innerText = ond.locatie;
                    document.getElementById('detail_beheerder').innerText = ond.beheerder;
                    document.getElementById('detail_organisatie').innerText = ond.organisatie;
                    document.getElementById('detail_ervaringsdeskundige').innerText = ond.ervaringsdeskundige;

                    modal.style.display = 'block';
                })
                .catch((err) => {
                    console.error(err);
                    alert('Fout bij ophalen van details.');
                });
        });
    });
}

document.addEventListener('DOMContentLoaded', initDetailButtons);