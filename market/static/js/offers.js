$(document).ready(function() {
$('#btn-open-negotiation').on('click', function() {
        $('#negotiationModal').css('display', 'flex');
    });

    $('.close-modal').on('click', function() {
        $('#negotiationModal').hide();
        $('#offer-status').text('');
    });

    $(window).on('click', function(event) {
        if (event.target.id === 'negotiationModal') {
            $('#negotiationModal').hide();
        }
    });

    $('#btn-send-offer').on('click', function() {
        const listingId = $('#offer-listing-id').val();
        const price = $('#offer-price').val();
        const message = $('#offer-message').val();
        const $status = $('#offer-status');
        const csrftoken = getCookie('csrftoken');

        $(this).prop('disabled', true).text('Wysyłanie...');

        fetch('/api/offers/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                listing: listingId,
                price: price,
                message: message
            })
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(errData => { throw errData; });
            }
            return response.json();
        })
        .then(data => {
            $status.css('color', 'green').text('✅ Oferta wysłana pomyślnie!');

            $('#offer-price').val('');
            $('#offer-message').val('');

            setTimeout(() => {
                $('#negotiationModal').hide();
                $('#btn-send-offer').prop('disabled', false).text('Wyślij ofertę');
                $status.text('');
            }, 2000);
        })
        .catch(error => {
            console.error('Błąd:', error);
            $('#btn-send-offer').prop('disabled', false).text('Wyślij ofertę');

            let errorMsg = "Wystąpił błąd.";

            if (error.detail) { errorMsg = error.detail; }
            else if (error.non_field_errors) { errorMsg = error.non_field_errors[0]; }
            else if (error.price) { errorMsg = "Cena: " + error.price[0]; }

            $status.css('color', 'red').text('❌ ' + errorMsg);
        });
    });

    function handleOfferDecision(offerId, status) {

        const csrftoken = getCookie('csrftoken');

        fetch(`/api/offers/${offerId}/manage/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({ status: status })
        })
        .then(response => {
            if (!response.ok) throw new Error("Błąd sieci");
            return response.json();
        })
        .then(data => {
            alert(data.message);
            location.reload();
        })
        .catch(error => {
            console.error('Błąd:', error);
            alert("Wystąpił błąd podczas przetwarzania decyzji.");
        });
    }

    $('.btn-accept').on('click', function() {
        const id = $(this).data('id');
        if(confirm("Czy na pewno chcesz zaakceptować tę ofertę? Cena gry zostanie zmieniona na nową.")) {
            handleOfferDecision(id, 'accepted');
        }
    });

    $('.btn-reject').on('click', function() {
        const id = $(this).data('id');
        if(confirm("Czy na pewno chcesz odrzucić tę ofertę?")) {
            handleOfferDecision(id, 'rejected');
        }
    });
    });