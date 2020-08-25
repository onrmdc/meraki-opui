// own js codes

$('#signInButton').click(function() {
  $('#signInButton').html('<span class="spinner-border spinner-border-sm mr-2" role="status" aria-hidden="true">' +
      '</span>Loading...').addClass('disabled');
});

$(document).ready(function() {
    $("#selectNewExistingForm").change(function () {
        $(this).find("option:selected").each(function () {
            var optionValue = $(this).attr("value");
            if (optionValue == 'new') {
                $("#newNetForm").slideDown();
                $("#existingNetForm").slideUp();
            } else {
                $("#newNetForm").slideUp();
                $("#existingNetForm").slideDown();
            }
        });
    }).change();
});

$(document).ready(function(){
    $("#netTypeSelect").change(function(){
        $(this).find("option:selected").each(function(){
            var optionValue = $(this).attr("value");
            if(optionValue=='firewall'){
                $("#templateFormArea").slideDown();
            } else{
                $("#templateFormArea").slideUp();
                }
            });
        }).change();
});


var $table = $('#networksTable');
var $deviceTable = $('#deviceTable');

// post form
var formErrorDiv = document.getElementById("formErrorDiv")
$(document).on("submit", "#networkDeviceForm", function(event){
    event.preventDefault();
    $.ajax({
        url: "/",
        type: "POST",
        data: new FormData(this),
        dataType: "json",
        contentType: false,
        cache: false,
        processData: false,
        success: function(data) {
            if(data != null) {
                formErrorDiv.innerHTML = JSON.stringify(data);
            }else{
                $table.bootstrapTable('refresh');
            }
        }

    });
});

//vf lines for fade effect for devices table on select,unselect event on network table
// device table creation

//vf $('.dev-table-selector').hide()
var JSON_Selected = $table.bootstrapTable('getSelections');
$(function() {
    $table.on('check.bs.table', function (e, row, $element) {
        //e.preventDefault();
        console.log('CHECKED');
        checkUnCheckResult();
    });
});
$(function() {
    $table.on('uncheck.bs.table', function (e, row, $element) {
        //e.preventDefault();
        console.log('UNCHECKED');
        checkUnCheckResult();
    });
});

function checkUnCheckResult() {
    //$deviceTable = $('#deviceTable');
    JSON_Selected = $table.bootstrapTable('getSelections');
    if (JSON_Selected.length==0) {
        // $deviceTable.fadeOut();
        //vf $('.dev-table-selector').fadeOut()
        $deviceTable.bootstrapTable("destroy");
        return
    }
    // console.log(JSON_Selected);
    $.ajax({
        url: "device.json",
        data: JSON.stringify(JSON_Selected),
        type: 'POST',
        contentType: "application/json",
        success: function(data) {
            console.log(data);
            $deviceTable.bootstrapTable("destroy");
            $deviceTable.bootstrapTable({data: data}); // device table source
            // $deviceTable.bootstrapTable('refresh');
            // $deviceTable.hide();
            // $deviceTable.fadeIn();
            //vf $('.dev-table-selector').hide();
            //vf $('.dev-table-selector').fadeIn();
        },
        error: function(error) {
            console.log(error);
        }
    });

}

// reset device table on page change event for network table;
$(function() {
    $table.on('page-change.bs.table', function (e, row, $element) {
        $deviceTable.bootstrapTable("destroy");
    });
});

// network delete modal
var deleteResult = document.getElementById("deleteResult")
$(document).on("click", "#deleteSelectedNetsButton", function(event){
    JSON_Selected = $table.bootstrapTable('getSelections');
    $.ajax({
        url: "/delete_networks",
        type: "POST",
        data: JSON.stringify(JSON_Selected),
        dataType: "json",
        contentType: "application/json",
        success: function(data) {
            console.log(data);
            $table.bootstrapTable('refresh');
            //vf $deviceTable.bootstrapTable("destroy");
            $('.dev-table-selector').hide()
            var output = '';
            for (var i = 0; i < data.length; i++){
                output += "<li>" + data[i] + "</li>";
            }
            deleteResult.innerHTML = output;
        }
    });
});