$(function () {
    $('[data-toggle="popover"]').popover()
    $('.popover-dismiss').popover({
        trigger: 'focus'
    })


    $('#language-selection').change(function(){
        $('#language-form').submit();
    })
})