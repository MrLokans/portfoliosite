$(document).ready(function(){
    login = $('input#inputEmail').val();
    password = $('input#inputPassword').val();
    submitBtn = $('#signinButton');

    submitBtn.on('click', function(e){
        // replace by django url
        e.preventDefault();
        $.post('/login', {'username': login, 'password': password})
            .done(function(){
                console.log("Successful login");
            })
            .error(function(e){
                console.log("Error!");
                // console.prompt(e);
                console.log(e);
            });
    });
});