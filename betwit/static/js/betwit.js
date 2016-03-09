$(document).ready(function(){
    $(".toggler").click(function(e){
        e.preventDefault();
        $('.round'+$(this).attr('data-betwit-round')).toggle();
    });
});

