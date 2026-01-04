$(document).ready(function() {
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

        });