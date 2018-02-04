$(document).ready(function(){
    $(".toggler").click(function(e){
        e.preventDefault();
        $('.round'+$(this).attr('data-betwit-matchid')).toggle(1000);
        $('html, body').animate({ scrollTop: $("#"+$(this).attr('data-betwit-matchid')).offset().top-51}, 1000);
    });
});

