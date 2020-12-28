$(function(){
    const videoDiv = $('#video-div');
    $('.exchange-image-div').click(function(){
        const videoLink = $(this).attr('data-href');
        videoDiv.empty();
        newIframe = $('<iframe></iframe>');
        newIframe.attr({
            class: 'embed-responsive-item',
            src: videoLink,
            allowfullscreen: true,
        });
        videoDiv.append(newIframe)
    })

    $('.collapse').on('show.bs.collapse', function(){
        const arrowSelector = $(this).attr('data-target') 
        const arrow = $(arrowSelector);
        arrow.removeClass('fa-caret-down').addClass('fa-caret-up')
    })
    $('.collapse').on('hide.bs.collapse', function(){
        const arrowSelector = $(this).attr('data-target') 
        const arrow = $(arrowSelector);
        arrow.removeClass('fa-caret-up').addClass('fa-caret-down')
    })
})