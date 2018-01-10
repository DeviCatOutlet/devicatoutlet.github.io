$(function() {
    $('#gallery ~ p img').click(function() {
        $('.imagepreview').attr('src', $(this).attr('src'));
        $('#modal-caption').text($(this).attr('alt'));
        $('#imagemodal').modal('show');
    });
});