/**
 * Created by alex on 29/06/16.
 */
;(function () {
    var $btn = $('#send');

    var $red = $('#red');
    var $red_val = $('#red_val');

    var $green = $('#green');
    var $green_val = $('#green_val');

    var $blue = $('#blue');
    var $blue_val = $('#blue_val');

    loadState();


    $red.on('change', function () {
        $red_val.text($red.val());
    });

    $green.on('change', function () {
        $green_val.text($green.val());
    });

    $blue.on('change', function () {
        $blue_val.text($blue.val());
    });

    $btn.on('click', function () {
        var changeUrl = '/set?' + $.param(grabRgb());
        $.ajax({
            'url': changeUrl,
            'success': function (data) {
                saveState(data);
            }
        })
    });

    function grabRgb() {
        return {
            'r': $red.val(),
            'g': $green.val(),
            'b': $blue.val()
        }
    }

    function saveState(s) {
        var c = s['colors'];

        $red.val(c['red']).change();
        $green.val(c['green']).change();
        $blue.val(c['blue']).change();
    }

    function loadState() {
        $.ajax({
            'url': '/get',
            'success': function (data) {
                saveState(data);
            }
        })
    }

})();