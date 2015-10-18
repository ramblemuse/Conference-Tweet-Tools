// *****************************************************************************
//  Creates large images when thumbnail images are present. The original size
//  depends on the viewport size (small or medium). Sets a event handler so
//  that the larger image is displayed when the mouse hovers over the thumbnail
//  image. When a dummy image has been used for the user icon, grabs the URL
//  for the actual image from the data-src attribute and loads the image.
//
//  Pops-up the larger image when the thumbnail image is hovered over,
//  scaling the image to fit in the viewport.
//
//  Loads the user icons, replacing a temporary icons used to speed loading.
//
//  Keith Eric Grant (keg@ramblemuse.com) -- 25 Mar 2015
//  08 May 2015 - Added link to larger image to pictures
//
// *****************************************************************************


function addEvent(obj, evType, fn) {

    // Function to stack multiple window.onload events

    if (obj.addEventListener){
        obj.addEventListener(evType, fn, false);
        return true;

    } else if (obj.attachEvent){

        var r = obj.attachEvent("on"+evType, fn);
        return r;
    }
}


function loadPosterIcons () {

    // Load the real user (aka poster) icons if a dummy icon
    // has been used to speed loading. The real URL for the
    // icon will be in the data-src attribute for the image.

    // Don't do anything if the Document Object Model (DOM)
    // isn't supported by the browser
    if ( !document.getElementsByClassName ) return;

    // Get a list of the thumbnail elements (divs)
    var posterIcons = document.getElementsByClassName("posterimg");

    // Grab the real image src from the dataset src, replacing
    // the temporary icon used to speed page loading.
    var img;
    var tmp;
    for (var ix=0; ix < posterIcons.length; ix++) {
        img = posterIcons[ix].getElementsByTagName('img')[0];
        if ( img.dataset.src ) {
            addEvent (img, 'error', recantImage);
            tmp = img.src;
            img.src = img.dataset.src;
            img.dataset.src = tmp;
        }
    }
}


function recantImage (event) {

    // This function is used on image loading error events to replace
    // the failed actual image with the default loading image.

    // Handle older IE or W3C event models. W3C event pass the event
    // as an argument. IE (<=8) stores it under window.event. The
    // names of the "target" element creating the event are
    // also different.

    if (!event) {
        var event = window.event;
        var img = event.srcElement;
    } else {
        var img = event.target;
    }

    var tmp = img.src;
    img.src = img.dataset.src;
    img.dataset.src = tmp;

    // If the direct parent of the image is a link, move the
    // image element before the link, then remove the link.
    if ( img.parentNode.nodeName.toLowerCase() == 'a' ) {
        var lnk = img.parentNode;
        var par = lnk.parentNode;
        par.insertBefore(img, lnk);
        par.removeChild(lnk);
    }
}


function addPictures () {

    // Load the actual thumbnail pictures if a dummy image was
    // used to speed loading and create the larger images
    // displayed when the mouse hovers over the thumbnail. The
    // size of the larger image fetched from Twitter (small or
    // medium) depends on the viewport size.

    // Don't do anything if the Document Object Model (DOM)
    // isn't supported by the browser

    if ( !document.getElementsByClassName ) {
        return;
    }

    // Calculate the viewport width and height
    var space  = tweets.getBoundingClientRect();
    var vpwidth = space.right - space.left;
    var vpheight = document.documentElement.clientHeight;

    // Get a list of the thumbnail elements
    var thumbnails = document.getElementsByClassName("thumbnail");
    var thumbSrc;
    var pictSrc;
    var linkSrc;
    var tmp;

    for (var ix=0; ix < thumbnails.length; ix++) {

        // Get the source URL for the thumbnail and remove the
        // ':thumb' off of the end. Allow for the thumbnail
        // itself being post-loaded from the data-src attribute.

        if ( thumbnails[ix].dataset.src ) {

            // Dummy image used for the thumbnail. Get the real
            // sources from the data-src attribute.

            addEvent(thumbnails[ix], 'error', recantImage);
            tmp = thumbnails[ix].src;
            thumbSrc = thumbnails[ix].dataset.src;
            thumbnails[ix].src = thumbSrc;
            thumbnails[ix].dataset.src = tmp;

        } else {

            // The actual thumbnail is already loaded.
            thumbSrc = thumbnails[ix].src;
        }

        // Set the base URLs for the hover picture and the link to a larger
        // picture, then choose image sizes (small and medium or medium and
        // large) from Twitter based on the viewport width.
        pictSrc = thumbSrc.split(/:thumb/)[0];
        linkSrc = pictSrc;
        if ( vpwidth < 600 ) {
            pictSrc += ':small';
            linkSrc += ':medium';
        } else {
            pictSrc += ':medium';
            linkSrc += ':large';
        }

        // Insert the hover image into the DOM after the thumbnail
        var img = document.createElement("img");
        img.style.display = 'none';

        // Create a fallback if the wanted image has an error
        if ( thumbnails[ix].dataset.src ) {
            img.dataset.src = thumbnails[ix].dataset.src;
            addEvent(thumbnails[ix], 'error', recantImage);
        }

        img.src = pictSrc;
        img.className = 'picture';
        img.alt = 'larger picture';
        thumbnails[ix].parentNode.insertBefore(img, thumbnails[ix].nextSibling);

        // Wrap the thumbnail image in a link to a larger image.
        var lnk = document.createElement('a');
        lnk.setAttribute('href', linkSrc);
        thumbnails[ix].parentNode.insertBefore(lnk, thumbnails[ix]);
        lnk.appendChild(thumbnails[ix]);
    }
}

function mouseImageEvent (event) {

    // Handle older IE or W3C event models. W3C event pass the event
    // as an argument. IE (<=8) stores it under window.event. The
    // names of the "target" element creating the event are
    // also different.

    if (!event) {
        var event = window.event;
        var thumbnail = event.srcElement;
    } else {
        var thumbnail = event.target;
    }

    var link   = thumbnail.parentNode;
    var tweet  = link.parentNode;
    var tweets = tweet.parentNode;
    var image  = tweet.getElementsByClassName("picture")[0];
    var rmarg  = 0.85;

    if (image) {

        switch ( event.type.toLowerCase() ) {

        case 'mouseover' :

            // Calculate the viewport width and height
            var space  = tweets.getBoundingClientRect();
            var vpwidth = space.right - space.left;
            var vpheight = document.documentElement.clientHeight;

            // Bring the larger image into the display so that
            // its width and height can be determined.
            image.style.display = 'block';

            // Get the image width and height
            var width  = image.offsetWidth;
            var height = image.offsetHeight;

            // Scale the larger image as necessary to ensure that it fits in the
            // viewport and doesn't overlap the thumbnail image.
            if (width > rmarg*vpwidth) {
                height = (rmarg * vpwidth/width) * height;
                width  = rmarg * vpwidth;
            }
            if (height > 0.95*vpheight) {
                width  = (0.95 * vpheight/height) * width;
                height = 0.95 * vpheight;
            }

            // Now the position can be calculated allowing for the desired
            // margins. The image vertical location is relative to the
            // beginning of all tweets, not just the tweet containing it.

            var left = Math.min(Math.max(0,rmarg*vpwidth-width), 0.5*(vpwidth-width));
            var top  = (vpheight - height)/2 - space.top;

            // Finally, set the image position and size.
            image.style.left   = left.toString()   + 'px';
            image.style.top    = top.toString()    + 'px';
            image.style.width  = width.toString()  + 'px';
            image.style.height = height.toString() + 'px';

            break;

        case 'mouseout' :
            image.style.display = 'none';
            break;

        case 'mousedown' :
            image.style.display = 'none';
            break;
        }
    }
    return false;
}


function setMouseHandler () {

    // Don't do anything if the Document Object Model (DOM)
    // isn't supported by the browser
    if ( !document.getElementsByClassName ) return;

    // Get a list of the thumbnail elements
    var thumbnails = document.getElementsByClassName("thumbnail");

    for (var ix=0; ix < thumbnails.length; ix++) {

        var img = thumbnails[ix];

        // Set event listeners for the thumbnail
        img.onmouseover = mouseImageEvent;
        img.onmouseout  = mouseImageEvent;
        img.onmousedown = mouseImageEvent;

    }
    return false;
}

addEvent (window, 'load', function () {addPictures ();  setMouseHandler ();} );
addEvent (window, 'load', loadPosterIcons);