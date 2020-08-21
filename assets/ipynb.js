function toggleAllInput( link ) {
    if ( $(link).data("show-input") ) {
        $('div.input').show();
        $(link).data( "show-input", false );
    } else {
        $('div.input').hide();
        $(link).data("show-input", true)
    }
}

function toggleNextInput( element ) {
    $(element).parents(".cell").next(".cell").children("div.input").slideToggle();
}

function toggleNextOutput( element ) {
    $(element).parents(".cell").next(".cell").children("div.output_wrapper").slideToggle();
}

$( document ).ready(function() {
    toggleAllInput( $("#toggle_all_input") );
});
