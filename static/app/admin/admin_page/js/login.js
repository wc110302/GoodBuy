function get_verify_code() {
        var timestamp = Date.parse(new Date());
        timestamp = timestamp / 1000;
        $('#verify_code').attr('src',"/verify_code?t="+timestamp);
    }
