
function open_img(imgs) {
    // Get the expanded image
    window.open(imgs.alt, '_blank').focus();
} 


// Next/previous controls
function plusSlides(n) {
    let slides = document.getElementsByClassName("mySlides");
    if (n > slides.length) {showSlides(slideIndex = n);}
    else{showSlides(slideIndex += n);}
    
}

// Thumbnail image controls
function currentSlide(n) {
    showSlides(slideIndex = n);
}

function showSlides(n) {
    let slideIndex = n;
    let i;
    let slides = document.getElementsByClassName("mySlides");
    let dots = document.getElementsByClassName("demo");
    let captionText = document.getElementById("caption");
    if (n > slides.length) {return none}
    if (n < 1) {slideIndex = slides.length}
    for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
    }
    for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
    }
    slides[slideIndex - 1].style.display = "block";
    dots[slideIndex - 1].className += " active";
    captionText.innerHTML = dots[slideIndex-1].alt;
} 

function getCurrentSlide(){
    let slides = document.getElementsByClassName("mySlides");
    for (i = 0; i < slides.length; i++){
    if (slides[i].className.includes('mySlides active')){
        let slideIndex = i
    }
    }
    document.getElementsByClassName("numberSlide")[0].value = slideIndex 
    return slideIndex


}
