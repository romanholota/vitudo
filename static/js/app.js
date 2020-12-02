var full_url = location.href;
var url = location.protocol + '//' + location.host + location.pathname;
var sideMenuLinks = document.getElementById("sidebarMenu").getElementsByTagName("a");

for(var i=0; i<sideMenuLinks.length; i++) {
  var lb = sideMenuLinks[i].href;
  if(lb == url || lb == full_url) {
    sideMenuLinks[i].className += " active";
  }
}    

$(function() {

    $("#search_location").keyup(function () {
        var search = $(this).val();

        $.ajax({
            type: 'GET',
            url: '/transfers/locations',
            data: {
                'search': search,
            },
            dataType: 'html',
            success: function (data) {
                $('#location_table').html(data)
            }
        });
    });

    $("#id_end").change(function() {
        var date = Date.parse($(this).val());
        if (date < Date.now()) {
            $("#error").html('Neplatný dátum výpožičky.');
            $("#submit_button").prop('disabled', true);
        }
        else {
            $("#error").html('');
            $("#submit_button").prop('disabled', false);                
        }
    });
});