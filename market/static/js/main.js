$(document).ready(function() {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    $('.select2-game').select2({
        placeholder: "Kliknij i zacznij pisać nazwę gry...",
        allowClear: true,
        language: {
            noResults: function() {
                return "Nie znaleziono takiej gry - wpisz ją poniżej w polu 'Własny tytuł'";
            }
        }
    });

    const $gameSelect = $('#id_game');
    const $customInput = $('#id_custom_title');

    $gameSelect.on('change', function() {
        if ($(this).val()) {
            $customInput.val('').prop('disabled', true);
            $customInput.attr('placeholder', 'Wybrano grę z listy (odznacz X, aby wpisać własną)');
        } else {
            $customInput.prop('disabled', false);
            $customInput.attr('placeholder', 'LUB wpisz własną nazwę (jeśli nie ma na liście)');
        }
    });

    $customInput.on('input', function() {
        if ($(this).val().length > 0) {
            $gameSelect.val(null).trigger('change');
        }
    });

    $gameSelect.trigger('change');

    $('#share-btn').on('click', function() {
    const url = window.location.href;

    navigator.clipboard.writeText(url).then(function() {
        const originalText = $('#share-btn').text();
        $('#share-btn').text('✅ Skopiowano!').css('background', '#27ae60');

        setTimeout(function() {
            $('#share-btn').text(originalText).css('background', 'dodgerblue');
        }, 2000);
    }, function(err) {
        alert('Nie udało się skopiować linku.');
    });
});

    $('#btn-api-search').on('click', function() {
        fetchListings();
    });

    $('#api-search-query').on('keypress', function(e) {
        if(e.which == 13) fetchListings();
    });

    function fetchListings() {
        const query = $('#api-search-query').val();
        const price = $('#api-max-price').val();
        const condition = $('#api-condition').val();

        const params = new URLSearchParams({
            query: query,
            max_price: price,
            condition: condition
        });

        fetch(`/api/search/?${params.toString()}`)
            .then(response => response.json())
            .then(data => {
                const listings = data;
                const $grid = $('#listings-grid');
                $grid.empty();

                if (listings.length === 0) {
                    $grid.append('<p>Brak wyników spełniających kryteria.</p>');
                    return;
                }

                listings.forEach(item => {

                    let imgHtml = item.image_url
                        ? `<img src="${item.image_url}" alt="${item.title}">`
                        : `<div class="no_photo">Brak zdjęcia</div>`;

                    const cardHtml = `
                        <div class="card">
                            <a href="/listing/${item.id}/" class="card-link-wrapper">
                                ${imgHtml}
                                <h3>${item.title}</h3>
                                <p>${item.category}</p>
                                <p class="price">${item.price} PLN</p>
                                <p>Stan: <strong>${item.condition_display}</strong></p>
                                <small>Sprzedawca: ${item.seller}</small>
                            </a>
                        </div>
                    `;
                    $grid.append(cardHtml);
                });
            })
            .catch(error => console.error('Błąd:', error));
    }
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

