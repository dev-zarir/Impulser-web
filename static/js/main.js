var theme = window.localStorage.getItem('theme');
var host = window.location.protocol + "//" + window.location.host;
if (theme == null) {
    window.localStorage.setItem('theme', 'dark')
} else {
    if (theme == 'light') {
        document.body.classList.remove('dark-mode')
    }
    if (theme == 'dark') {
        document.body.classList.add('dark-mode')
    }
}
var theme_toggle_buttons = document.getElementsByClassName('theme-toggle');
for (var i = 0; i < theme_toggle_buttons.length; i++) {
    var elem = theme_toggle_buttons[i].addEventListener('click', change_mode)
}
var sidebar_toggle_buttons = document.getElementsByClassName('sidebar-toggle');
for (var i = 0; i < sidebar_toggle_buttons.length; i++) {
    var elem = sidebar_toggle_buttons[i].addEventListener('click', () => {
        impulser.toggleSidebar()
    })
}

function change_mode() {
    theme = window.localStorage.getItem('theme');
    if (theme == null) {
        window.localStorage.setItem('theme', 'light')
    }
    if (theme == 'light') {
        document.body.classList.add('dark-mode');
        window.localStorage.setItem('theme', 'dark');
        document.getElementById('tglico').classList.add('fa-sun');
        document.getElementById('tglico').classList.remove('fa-moon');
    }
    if (theme == 'dark') {
        document.body.classList.remove('dark-mode');
        window.localStorage.setItem('theme', 'light');
        document.getElementById('tglico').classList.remove('fa-sun');
        document.getElementById('tglico').classList.add('fa-moon');
    }
}

function showalert(content, title = '', type = '', allowdismis = true, timeout = 5000) {
    // Types are: "alert-primary" || "alert-success" || "alert-secondary" || "alert-danger"
    impulser.initStickyAlert({
        content: content,
        title: title,
        alertType: type,
        hasDismissButton: allowdismis,
        timeShown: timeout
    })
}

function submitform() {
    var number = document.getElementById('number')
    var amount = document.getElementById('amount')
    var mode = document.getElementById('mode')
    if (number.value.length != 11) {
        return showalert('Please enter original number. Eg: 01947284737', 'Invalid Number', 'alert-secondary')
    }
    if (amount.value < 1) {
        return showalert('Please enter sms amount between 1-5000.', 'Unsupported Amount', 'alert-secondary')
    }
    if (amount.value > 5001) {
        return showalert('Please enter sms amount between 1-5000.', 'Unsupported Amount', 'alert-secondary')
    }
    if (mode.value == 'none') {
        return showalert('Please Choose any mode. Click \'Learn More\' for details', 'Wrong Mode', 'alert-secondary')
    }
    var submitbtn = document.getElementById('submitwork')
    submitbtn.setAttribute('disabled', 'true')
    var xhr = new XMLHttpRequest();
    xhr.open("POST", window.location.href);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            var status = xhr.status
            if (status == 200) {
                var text = JSON.parse(xhr.responseText)
                if (text['success'] == true) {
                    submitbtn.removeAttribute('disabled')
                    showalert(text['message'], '', text['category'])
                    setTimeout(() => {
                        window.location.href = host + `/progress/${text['id']}`
                    }, 2000)
                } else {
                    submitbtn.removeAttribute('disabled')
                    showalert(text['message'], text['category'])
                }
            } else {
                submitbtn.removeAttribute('disabled')
                showalert('Something went wrong! Please try again later', '', 'alert-secondary')
            }
        }
    };
    var data = `number=${number.value}&amount=${amount.value}&mode=${mode.value}`;
    xhr.send(data);
}

function update_info() {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", window.location.href);
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            var status = xhr.status
            if (status == 200) {
                var text = JSON.parse(xhr.responseText)
                $('#id').text(text['id'])
                $('#number').text(text['number'])
                $('#amount').text(text['amount'])
                $('#mode').text(text['mode'])
                $('#running').text(text['running'])
                $('#completed').text(text['completed'])
                $('#total').text(text['total'])
                $('#sent').text(text['sent'])
                $('#failed').text(text['failed'])
                $('#progress').text(text['progress'])
                $('#progressbar').width(text['progress'])
                $('#progressbar').text(text['progress'])
                if (text['running'] == 'no') {
                    clearInterval(2);
                    $('#progressbar').removeClass('progress-bar-animated');
                    $('#close-modal').click();
                    $('#stopbtn').hide();
                    $('#back-to-home').show();
                }
                if (text['completed']=='yes'){
                    $('#progressbar').addClass('bg-success');
                }
                if ((text['completed']=='no' & text['running']=='no')==1){
                    $('#progressbar').addClass('bg-danger');
                }
            }
        }
    };
    xhr.send();
}

function stop_bomb() {
    id = $('#id').text()
    if (id == '') {
        return
    }
    var xhr = new XMLHttpRequest();
    xhr.open("POST", host + '/stop/' + id);
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            var status = xhr.status
            if (status == 200) {
                var text = JSON.parse(xhr.responseText)
                showalert(text['message'], '', text['category'])
                if (text['stopped'] == true) {
                    setTimeout(() => {
                        $('#close-modal').click();
                        $('#stopbtn').hide();
                        $('#back-to-home').show();
                    }, 2000)
                }
            }
        }
    };
    xhr.send();
}