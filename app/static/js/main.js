$("#add_user_form").submit(function(e) {

    e.preventDefault();

    var form = $(this);
    var url = '/add_user'

    $.ajax({
           type: "POST",
           url: url,
           data: form.serialize(),
           success: function(data){ location.reload(); }
         });
});
