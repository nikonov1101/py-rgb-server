/**
 * Created by alex on 29/06/16.
 */
;(function () {
    var $updateBtn = $('#send');
    var $resetBtn = $('#reset');

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

    $updateBtn.on('click', function () {
        setDeviceState(grabValues());
    });

    $resetBtn.on('click', function(){
        resetDeviceState();
    })

    function grabValues() {
        return {
            'r': $red.val(),
            'g': $green.val(),
            'b': $blue.val()
        }
    }

    function setViewState(s) {
        var c = s['colors'];

        $red.val(c['red']).change();
        $green.val(c['green']).change();
        $blue.val(c['blue']).change();
    }

    function loadState() {
        $.ajax({
            'url': '/get',
            'success': function (data) {
                setViewState(data);
            }
        })
    }

    function setDeviceState(s) {
        var url = '/set?' + $.param(s);
        callAjax(url);
    }

    function resetDeviceState() {
        var url = '/set?' + $.param({'r': '0', 'g': '0', 'b': 0})
        callAjax(url);
    }

    function callAjax(url) {
        $.ajax({
            'url': url,
            'success': function (data) {
                setViewState(data);
            }
        })
    }

})();
