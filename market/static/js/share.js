$(document).ready(function() {

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
 });






