<script>
function supported(){
    if(window.webkitNotifications){
        return true;
    } else{
        return false;
    }
}
function requestPermission(){
    if(supported){
        window.webkitNotifications.requestPermission();
        statue = window.webkitNotifications.checkPermission();
    }
}
function checkStatue(){
    switch (statue){
        case 0:   // granted
            message();
            break;
        case 1:  // default
            requestPermission();
            break;
        case 2:  // denied
            return;
    }
}
function message(){
    var icon = "../IMAGE/mediaICON/pause.png"; //如果直接拷贝，这个地方URL路径可能会报错！
    var title = "hupeng";
    var body = "Hello World";
    var msgObj = window.webkitNotifications.createNotification(icon, title, body);
    msgObj.show();
} 
window.webkitNotifications.requestPermission();
        statue = window.webkitNotifications.checkPermission();
    var icon = "../IMAGE/mediaICON/pause.png"; //如果直接拷贝，这个地方URL路径可能会报错！
    var title = "hupeng";
    var body = "Hello World";
    var msgObj = window.webkitNotifications.createNotification(icon, title, body);
    msgObj.show();


    </script>
