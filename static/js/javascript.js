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

$('#entriesTable th').each(function(index, th) {
    $(th).unbind('click');
    $(th).append('<button class="sort-btn btn-asc">&#9650;</button>');
    $(th).append('<button class="sort-btn btn-desc">&#9660;</button>');
  
    $(th).find('.btn-asc').click(function() {
       table.column(index).order('asc').draw();
    }); 
    $(th).find('.btn-desc').click(function() {
       table.column(index).order('desc').draw();      
    }); 
  }); 