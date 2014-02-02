
jQuery(function ($) {

    var countdown = $('.countdown');
    setInterval(function () {
        var cur = countdown.text(),
            parts = cur.split(':'),
            i, zero = true;

        for (i = 0; i < parts.length; i++) {
            parts[i] = parseInt(parts[i], 10);
            zero = zero && parts[i] == 0;
        }

        if (!zero) {
            var at = parts.length - 1, carry = 1;
            while (at >= 0) {
                parts[at] -= carry;
                carry = 0;

                if (parts[at] < 0) {
                    parts[at] += 60;
                    carry = 1;
                }

                at--;
            }
        }

        var res = '';
        for (i = 0; i < parts.length; i++) {
            if (i != 0) res += ':';
            if (parts[i] < 10) res += '0';
            res += parts[i].toString();
        }

        countdown.text(res);

    }, 1000);

});

