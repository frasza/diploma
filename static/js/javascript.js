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

$(document).ready(function() {
    $('#entriesTable').DataTable( {
        "language": {
            "url": "https://cdn.datatables.net/plug-ins/1.10.15/i18n/Slovenian.json"
        }
    } );
} );