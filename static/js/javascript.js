/* Toggle */
function myFunction() {
    var x = document.getElementById("myTopnav");
    if (x.className === "topnav") {
        x.className += " responsive";
    } else {
        x.className = "topnav";
    }
}

$( "#toggleVnosi" ).click(function() {
    $( "#tabelaVnosov" ).toggle();
    $(this).text(function(i, text){
        return text === "Prikaži vse vnose kategorije" ? "Skij vse vnose kategorije" : "Prikaži vse vnose kategorije";
    })
});