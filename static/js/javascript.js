// Enables popover
$(document).ready(function(){
    $('[data-toggle="popover"]').popover();
    });

// Animated title
$('h1').addClass('animated rubberBand');


//Makes whole table row linkable
/*
$('tr').click( function() {
    window.location = $(this).find('a').attr('href');
}).hover( function() {
    $(this).toggleClass('hover');
});
*/

$('table').stacktable();

/* Toggle between adding and removing the "responsive" class to topnav when the user clicks on the icon */
function myFunction() {
    var x = document.getElementById("myTopnav");
    if (x.className === "topnav") {
        x.className += " responsive";
    } else {
        x.className = "topnav";
    }
}