var notify_message_badge_class;
var notify_menu_class;
var notify_api_url;
var notify_fetch_count;
var notify_unread_url;
var notify_mark_all_unread_url;
var notify_refresh_period = 15000;
var consecutive_misfires = 0;
var registered_functions = [];

function fill_notification_badge(data) {
    var notify_badges = document.getElementsByClassName('notis')
    // console.log(notify_badges);
    if (notify_badges) {
        for (var i = 0; i < notify_badges.length; i++) {
            notify_badges[i].innerHTML = data.unread_count;
        }
    }

    var notify_badges = document.getElementsByClassName('message')


    // console.log("message:" + JSON.stringify(data))

    messages = data.unread_list.filter(function (item) {
        return item.verb == "message"
    })

    // console.log("messages:" + JSON.stringify(messages))

    if (notify_badges) {
        for (var i = 0; i < notify_badges.length; i++) {
            notify_badges[i].innerHTML = messages.length;
        }
    }

}

function fill_notification_list(data) {
    var menus = document.getElementsByClassName(notify_menu_class);
    if (menus) {
        // console.log("data", data);



        var messages = data.unread_list.map(function (item) {
            var message = "";
            if (typeof item.actor !== 'undefined') {
                message = item.actor;
            }
            if (typeof item.verb !== 'undefined') {
                message = message + " " + item.verb;
            }
            if (typeof item.target !== 'undefined') {
                message = message + " " + item.target;
            }
            if (typeof item.timestamp !== 'undefined') {
                message = message + " " + item.timestamp;
            }


            if (typeof item.action_object !== 'undefined') {
                if (item.verb == "message") {
                    url = '/chat/thread/' + item.action_object;
                    // console.log(url);
                }
            }

            if (item.verb == "message") {
                return '<li><a class="dropdown-item" href="' + url + '">' + message + '</a></li>';
            } else {
                return '<li><a class="dropdown-item" href="#">' + message + '</a></li>';
            }
        }).join('')

        for (var i = 0; i < menus.length; i++) {
            menus[i].innerHTML = messages;
        }
    }
}

function register_notifier(func) {
    registered_functions.push(func);
}

function fetch_api_data() {
    if (registered_functions.length > 0) {
        //only fetch data if a function is setup
        var r = new XMLHttpRequest();
        r.addEventListener('readystatechange', function (event) {
            if (this.readyState === 4) {
                if (this.status === 200) {
                    consecutive_misfires = 0;
                    var data = JSON.parse(r.responseText);
                    for (var i = 0; i < registered_functions.length; i++) {
                        registered_functions[i](data);
                    }
                } else {
                    consecutive_misfires++;
                }
            }
        })
        r.open("GET", notify_api_url + '?max=' + notify_fetch_count, true);
        r.send();
    }
    if (consecutive_misfires < 10) {
        setTimeout(fetch_api_data, notify_refresh_period);
    } else {
        var badges = document.getElementsByClassName(notify_badge_class);
        if (badges) {
            for (var i = 0; i < badges.length; i++) {
                badges[i].innerHTML = "!";
                badges[i].title = "Connection lost!"
            }
        }
    }
}

setTimeout(fetch_api_data, 1000);
