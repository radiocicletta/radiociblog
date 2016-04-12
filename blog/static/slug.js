if (typeof jQuery === 'undefined' && django && django.jQuery) {
    jQuery = django.jQuery;
}

if (typeof redactor_custom_options === 'undefined') {
    redactor_custom_options = {}
}

(function($) {
    $(document).ready(function() {
        $('input.autoslug').each(function(){
            var el = $(this).data('source'),
                $input = $(this),
                $source = $('input[name=' + el + "]");
            $source.on('keyup', function(){
                $input.val($source.val().replace(/[^\w]*/g, ''));
            });
        });
    });
})(jQuery);
