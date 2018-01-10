$(function() {
    $('#gallery ~ p img').click(function() {
        $('.imagepreview').attr('src', $(this).attr('src'));
        //$('#modal-caption').text($(this).attr('alt')); //TODO: Style these up nicely and then enable them
        $('#imagemodal').modal('show');
    });
});