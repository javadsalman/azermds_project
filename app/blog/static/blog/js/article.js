const controllers = [];

// share button scripts
const shareController = (function () {
    const url = encodeURIComponent(window.location.href);
    const copyButton = $('#copy-url');
    function popShareButton(id, link, name) {
        $(`#${id}`).click(function () {
            window.open(link + url, `${name}-share-dialog`, 'width=800,height=600');
            return false;
        });
    }

    function init() {
        popShareButton('fb-share-button', 'https://www.facebook.com/sharer/sharer.php?u=', 'facebook');
        popShareButton('twitter-share-button', 'https://twitter.com/intent/tweet?url=', 'twitter');
        popShareButton('whatsapp-share-button', 'https://api.whatsapp.com/send?text=', 'whatsapp');
        popShareButton('linkedin-share-button', 'https://www.linkedin.com/sharing/share-offsite/?url=', 'linkedin');
    
        $('#mail-share').attr('href', `mailto:?body=${url}`);
    
        copyButton.tooltip();
        copyButton.click(function () {
            const newInput = $('<input>')
            newInput.attr({
                id: 'input-for-url',
                type: 'text',
                style: 'width:5px; border:none;',
                value: location.href,
            });
            $('#share-section').append(newInput);
            rawInput = newInput[0];
            rawInput.select();
            rawInput.setSelectionRange(0, rawInput.value.length);
            document.execCommand('copy');
            newInput.remove();
            setTimeout(() => {
                $(this).tooltip('hide');
            }, 800)
        });
    }

    return {
        init: init
    };
})()

// Editing Article with scripts




const modalController = (function() {
    const modal = $('#imageModal');
    const modalImage = $('.modal-image');
    const closeIcon = $('.close-icon');
    const imageContent = $('.image-content');

    function openModal() {
        modal.modal('show');
        imageContent.css('display', 'none');
    }

    function changeImage(newSrc) {
        modalImage.attr('src', newSrc);
    }

    function addText(newText) {
        imageContent.css('display', 'block');
        imageContent.text(newText)
    }

    function init() {
        closeIcon.click(() => {
            modal.modal('hide')
        })

    }

    return {
        init,
        openModal,
        changeImage,
        addText
    };
})()




const imageController = (function (modalController) {
    
    class Image {
        constructor(image) {
            // it covers all of the jquery element, image element, selector. All of them return jquery element
            this.$image = $(image) ;
            // only emogies have referrerpolicy attribute
            this.isEmogy = this.$image.width() < 30;
            this.hasCaption = Boolean(this.$image.attr('alt'));
        }

        attr(name) {
            return this.$image.attr(name);
        }

        addClass(name) {
            this.$image.addClass(name)
        }

        click(callback) {
            this.$image.click(callback);
        }

        removeAttrs(attrNames) {
            attrNames.forEach(name => this.$image.attr(name, ''));
        }

        removeStyle(name) {
            this.$image.css(name, '');
        }
        
        addStyle(name, value) {
            this.$image.css(name, value);
        }
        
        getStyleValue(name) {
            return this.$image.css(name);
        }

        getCopy() {
            return this.$image.clone();
        }

        replace(el) {
            this.$image.replaceWith(el);
        }

    }

    function getAllImages() {
        return $('.main-post img');
    }


    function addCaption(image) {
        // height crash the flexibility of caption. So we remove it
        image.removeStyle('height')
        // we get the style and classes of image to set caption
        const imageStyle = image.attr('style');
        const imageClasses = image.attr('class');
        // we remove all style of and class of image
        image.removeAttrs(['class', 'style'])
        // get the clone of image. Because it will replaced. So you ensure set image to caption
        const imageClone = image.getCopy();
        // get alt to set caption
        const altText = image.attr('alt')

        const figure = $(`<figure class="image-figure ${imageClasses}" style="${imageStyle}";></figure>`);
        const figcaption = $(`<figcaption class="image-caption"><p class="m-0 py-2 py-lg-1">${altText}</p></figcaption>`);

        figure.append(imageClone).append(figcaption);
        image.replace(figure);
        return {
            figure: figure,
            newImage: imageClone,
            text: altText
        }
    }

    function addModalProperty(image, text) {
        image.click(() => {
            modalController.openModal();
            modalController.changeImage(image.attr('src'))
            if (text) {
                modalController.addText(text);
            }
        })
    }
    

    function init() {
        for (let img of getAllImages()) {

            image = new Image(img);

            if (image.hasCaption && !image.isEmogy) {
                const {newImage, text} = addCaption(image);
                addModalProperty(newImage, text);
            } 
            
            else if(!image.hasCaption && !image.isEmogy) {
                image.addClass('img-without-caption')
                addModalProperty(image);
            }
        }
    }


    return {
        init: init,
        Image: Image
    };

 
})(modalController);







// Running Controllers
$(function() {
    shareController.init();
    modalController.init();
    imageController.init();
})