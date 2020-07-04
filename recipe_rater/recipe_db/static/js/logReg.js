// Ajax for email registration and see if email exists or doesn't have proper email format
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function isEmail(email){
    var regex = /^([a-zA-Z0-9_\.\-\+])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    if(!regex.test(email)){
        return false;
    } else {
        return true;
    }
}

$(document).ready(function () {
    $('#email').keyup(function () {
        var data = $(this).serialize();
        var email = $(this).val();
        if(isEmail(email) == true){
            $.ajax({
                method: "POST",
                url: "/email",
                data: data
            })
            .done(function (res) {
                $('#errors').html(res)
            })
        } else {
            $('#errors').html('<p class="text-danger eVal">Must be a valid email</p>')
            return false;
        }
    });
    $('#signInEmail').keyup(function () {
        var data = $(this).serialize();
        var email = $(this).val();
        if(isEmail(email) == true){
            $.ajax({
                method: "POST",
                url: "/email_login",
                data: data
            })
            .done(function (res) {
                $('#errors').html(res)
            })
        } else {
            $('#errors').html('<p class="text-danger eVal">Must be a valid email</p>')
            return false;
        }
    });
    $('#confpw').keyup(function(){
        var pw = $('#pw').val();
        var confpw = $(this).val();
        var data = $(this).serialize();
        if(pw == confpw){
            $.ajax({
                method: "POST",
                url: "/confpw",
                data: data
            })
            .done(function(res){
                $('#errors').html(res)
            })
        } else {
            $('#errors').html('<p class="text-danger eVal">Passwords must match</p>')
            return false;
        }
    })
});