/**
 * Created by joshua on 3/28/2015.
 */
var hipRow = document.getElementById("hipRow");

$('#sex2').click(function(e) {
   hipRow.hidden = false;
});

$('#sex1').click(function(e) {
    hipRow.hidden = true;
});