
// Ajax for email registration and see if email exists or doesn't have proper email format
$(document).ready(function(){
    $('#email').keyup(function(){
        var data = $('.registerForm').serialize()
        $.ajax({
            method: "POST",
            url: "/email",
            data: data,
        })
        .done(function(res){
            $('#usernameMsg').html(res)
        })
    })
})