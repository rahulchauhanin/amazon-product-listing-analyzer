const alertBox = document.getElementById('alert-box')

$(document).ready(function() {
    console.log( "ready!" );

    // Ajax submisson for the Form
    $("#form-link-analyze").submit(function(e){
        e.preventDefault();
        var serializedData = $(this).serialize();
        $("#main-content").empty();
        alertBox.innerHTML = ""
        $("#btn-submit-form").prop('disabled', true); // Disable the Submit Button on form submisson
        $("#btn-submit-form").html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Analyzing...`);
        $.ajax({
            type: "POST",
            url: "",
            data: serializedData,
            success: function(response){
                console.log("Hello: ", response.msg)
                alertBox.innerHTML=`<div class="alert alert-success alert-dismissible fade show" role="alert">
                    ${response.msg}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>`

                $("#main-content").append(response.html);
                $("#form-link-analyze")[0].reset()
                $("#btn-submit-form").prop('disabled', false);
                $("#btn-submit-form").html("Analyze");
                
            },
            error: function(response){
                console.log("Error: ", response.responseJSON.msg)
                alertBox.innerHTML=`<div class="alert alert-danger alert-dismissible fade show" role="alert">
                    ${response.responseJSON.msg}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>`

                $("#btn-submit-form").prop('disabled', false);
                $("#btn-submit-form").html("Analyze");
            },
            dataType: 'json'
          });
      });
});