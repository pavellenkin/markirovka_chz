function getCookie(name) {
    var matches = document.cookie.match(new RegExp("(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"));
    return matches ? decodeURIComponent(matches[1]) : undefined;}

function PostButtonCode(qwery){
    document.getElementById("message-bar").style.display = "none";
    document.getElementById("item_search").style.display = "none";
    $('#preloader').toggle();
    document.querySelector('#predmet').style.display = "block";
    document.querySelector('#predmet_text').style.display = "block";
    document.querySelector('#search_item').style.display = 'none';
    document.querySelector('#message-bar').style.display = 'none';
    code = qwery;
    type = localStorage.setupType;
    $.ajax({
                url: '/ps_in_code/',
                method: 'post',
                dataType: 'json',
                headers: {
    "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
  },
                data: {
                type: type,
                code: code
                },
                success: async function(data){
                    if (data.status === 'href_none'){
                    $('#preloader').toggle();
                        document.querySelector('#search_item').style.display = 'block';
                        document.querySelector('#avatar').src = data.data.img;
                        document.querySelector('#shk_item').innerHTML = data.data.code;
                        document.querySelector('#text').innerHTML = "<b>" +data.data.text+"</b>" ;
                        document.querySelector('#identification').innerHTML = "&ensp;&ensp;" +data.data.identification;
                        document.querySelector('#org').innerHTML = data.data.org;
                        document.querySelector('#org_title').innerHTML = data.data.org_title;
                        document.querySelector('#inn_priority_title').innerHTML = data.data.inn_priority_title;
                        document.querySelector('#inn_priority').innerHTML = data.data.inn_priority;
                        document.querySelector('#inn_second_important').innerHTML = data.data.inn_second_important;
                        document.querySelector('#searchInput').value="";
                        document.querySelector('#predmet').style.display = "none";
                        document.querySelector('#predmet_text').style.display = "none";

                    }
                    else if (data.status === 'success'){
                        $('#preloader').toggle();
                        document.querySelector('#search_item').style.display = 'block';
                        document.querySelector('#avatar').src = data.data.img;
                        document.querySelector('#shk_item').innerHTML = data.data.code;
                        document.querySelector('#text').innerHTML = "<b>" +data.data.text+"</b>" ;
                        document.querySelector('#identification').innerHTML = "&ensp;&ensp;" +data.data.identification;
                        document.querySelector('#org').innerHTML = data.data.org;
                        document.querySelector('#org_title').innerHTML = data.data.org_title;
                        document.querySelector('#inn_priority_title').innerHTML = data.data.inn_priority_title;
                        document.querySelector('#inn_priority').innerHTML = data.data.inn_priority;
                        document.querySelector('#inn_second_important').innerHTML = data.data.inn_second_important;
                        document.querySelector('#searchInput').value="";
                    }
                    else {
                        $('#preloader').toggle();
                        document.querySelector('#message-bar').style.display = 'block';
                        document.querySelector('#message-bar-text').innerHTML = data.status;
                        document.querySelector('#searchInput').value="";
                        }
                }
            });
}



function PostInputCode(){
    document.getElementById("message-bar").style.display = "none";
    document.getElementById("item_search").style.display = "none";
    $('#preloader').toggle();
    document.querySelector('#predmet').style.display = "block";
    document.querySelector('#predmet_text').style.display = "block";
    document.querySelector('#search_item').style.display = 'none';
    document.querySelector('#message-bar').style.display = 'none';
    document.querySelector('#message-bar-tm').style.display = 'none';
    document.querySelector('#message-bar-text-tm').innerHTML = '';
     code = $('input[name="code"]').val();
     type = localStorage.setupType;

        $.ajax({
                url: '/ps_in_code/',
                method: 'post',
                dataType: 'json',
                headers: {
    "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
  },
                data: {
                code: code,
                type: type
                },
                success: async function(data){
                    if (data.status === 'href_none'){
                    $('#preloader').toggle();
                        document.querySelector('#search_item').style.display = 'block';
                        document.querySelector('#avatar').src = data.data.img;
                        document.querySelector('#shk_item').innerHTML = data.data.code;
                        document.querySelector('#text').innerHTML = "<b>" +data.data.text+"</b>" ;
                        document.querySelector('#identification').innerHTML = "&ensp;&ensp;" +data.data.identification;
                        document.querySelector('#org').innerHTML = data.data.org;
                        document.querySelector('#org_title').innerHTML = data.data.org_title;
                        document.querySelector('#inn_priority_title').innerHTML = data.data.inn_priority_title;
                        document.querySelector('#inn_priority').innerHTML = data.data.inn_priority;
                        document.querySelector('#inn_second_important').innerHTML = data.data.inn_second_important;
                        document.querySelector('#searchInput').value="";
                        document.querySelector('#predmet').style.display = "none";
                        document.querySelector('#predmet_text').style.display = "none";

                    }
                    else if (data.status === 'tm'){
                             document.querySelector('#search_tm').style.display = 'none';
                             document.querySelector('#search_tm').innerHTML = '';
                             $('#preloader').toggle();
                             document.querySelector('#message-bar-tm').style.display = 'block';


                             document.querySelector('#search_tm').style.display = 'block';
                             const re_list = data.list;
                             var item_search = document.getElementById("search_tm");
                             if (re_list.length === 0){
                                document.querySelector('#message-bar-text-tm').innerHTML = 'По вашему запросу ничего не найдено';
                             }
                             else {
                             for (ind = 0; re_list.length; ++ind) {

                                let button_item = document.createElement('button');
                                button_item.setAttribute('class', 'list-group-item list-group-item-action');
                                link = 'https://xn----7sbabas4ajkhfocclk9d3cvfsa.xn--p1ai/search/?q='+re_list[ind].Brand+'&type=tm'
                                button_item.setAttribute('onclick', "window.open('"+link+"');" );
                                button_item.innerHTML = re_list[ind].Value;
                                item_search.appendChild(button_item);
                             }
                             }
                    }


                    else if (data.status === 'success'){
                        $('#preloader').toggle();
                        document.querySelector('#search_item').style.display = 'block';
                        document.querySelector('#avatar').src = data.data.img;
                        document.querySelector('#shk_item').innerHTML = data.data.code;
                        document.querySelector('#text').innerHTML = "<b>" +data.data.text+"</b>" ;
                        document.querySelector('#identification').innerHTML = "&ensp;&ensp;" +data.data.identification;
                        document.querySelector('#org').innerHTML = data.data.org;
                        document.querySelector('#org_title').innerHTML = data.data.org_title;
                        document.querySelector('#inn_priority_title').innerHTML = data.data.inn_priority_title;
                        document.querySelector('#inn_priority').innerHTML = data.data.inn_priority;
                        document.querySelector('#inn_second_important').innerHTML = data.data.inn_second_important;
                        document.querySelector('#searchInput').value="";
                    }
                    else {
                        $('#preloader').toggle();
                        document.querySelector('#message-bar').style.display = 'block';
                        document.querySelector('#message-bar-text').innerHTML = data.status;
                        document.querySelector('#searchInput').value="";
                        }
                }
            });
}

window.addEventListener('load', function () {
  var preloader = document.getElementById('preloader');

  setTimeout(function(){

    preloader.style.display = 'none';

  }, 400);


});


function CopyToClipboard(containerid) {
    var copyText = document.getElementById(containerid);
    var textArea = document.createElement("textarea");
    textArea.value = copyText.innerHTML;
    document.body.appendChild(textArea);
    textArea.select();
    document.execCommand("Copy");
    textArea.remove();
    document.execCommand("copy");
}

function KeepTrack() {

    setupType = localStorage.setupType;
    if (setupType === 'tm'){

    }
    if (setupType === 'goods'){
        document.querySelector('#message-bar-tm').style.display = 'none';
        document.querySelector('#search_tm').style.display = 'none';
        document.querySelector('#search_tm').innerHTML = '';

        document.querySelector('#searchInput').addEventListener('input', function(event) {
        if (setupType === 'tm'){
            return;
        }
        if (event.inputType == "deleteContentBackward" || event.target.value.length < 2) {
            document.getElementById("item_search").style.display = "none";
            return;
        }
        else {
            document.getElementById("search_item").style.display = "none";
            document.getElementById("message-bar").style.display = "none";
            if (event.target.value===''){
                    document.getElementById("item_search").style.display = "none";
            }
            else{
                    document.getElementById("item_search").style.display = "block";
            };

            $.ajax({
                        url: '/nc_find/',
                        method: 'post',
                        dataType: 'json',
                        headers: {
                            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
                        },
                        data: {
                                query: event.target.value
                                },
                        success: async function(data){
                        document.getElementById("item_search").innerHTML = '';
                         const re_list = data.list;
                         var item_search = document.getElementById("item_search");
                         for (ind = 0; re_list.length; ++ind) {

                            let button_item = document.createElement('button');
                            button_item.setAttribute('class', 'list-group-item list-group-item-action');
                            button_item.setAttribute('onclick', "PostButtonCode('"+re_list[ind].Value+"');" );
                            button_item.innerHTML = re_list[ind].Value;
                            item_search.appendChild(button_item);
                         }

                         }
                    });

}
    });
}

}


function ChangeSearch(evt) {
   localStorage.clear();
  if (evt.target.value === "Товары") {
    document.getElementById("item_search").style.display = "none";
    document.getElementById("item_search").innerHTML = "";
    document.querySelector('#searchInput').value="";
    document.querySelector('#searchInput').placeholder="Поиск товаров";

    localStorage.setupType = 'goods';

  }
  if (evt.target.value === "Торговые марки") {
    document.getElementById("item_search").style.display = "none";
    document.getElementById("item_search").innerHTML = "";
    document.querySelector('#searchInput').value="";
    document.querySelector('#searchInput').placeholder="Поиск по торговым маркам";

    localStorage.setupType = 'tm';

  }
}

function InVisibleAbout(){
     document.getElementById("main_check").style.display = "none";
    document.getElementById("response_check").style.display = "block";
        setTimeout(function () {
            document.getElementById("main_check").style.display = "block";
            document.getElementById("response_check").style.display = "none";
            location.reload(true);
        }, 3200);
}

function VisibleAbout(){

    document.getElementById("main_check").style.display = "none";

    document.getElementById("response_check").style.display = "block";

    document.getElementById("button_close").style.display = "block";


}

function SendCode() {
    $('#preloader').toggle();

//    document.getElementById("response_check").style.display = "none";
//    document.getElementById("button_close").style.display = "none";
    let timeout = null;

    document.querySelector('#searchInput').addEventListener('keyup', function(event) {
    code = $('input[name="check_code"]').val();
    clearTimeout(timeout);
    timeout = setTimeout(function () {
          $.ajax({
                        url: '/check_code/',
                        method: 'post',
                        dataType: 'json',
                        cache: false,
                        timeout: 5000,
                        headers: {
                            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
                        },
                        data: {
                                check_code: code
                                },
                        success: async function(data){
                                document.querySelector('input#searchInput').value = '';
                                if (data.status === 'success'){
//                                    if (data.body.audio == 'success'){
////                                            var audio = new Audio('/static/audio/cock.wav');
////                                            audio.play();
//                                    }else{
////                                            var audio = new Audio('/static/audio/error.wav');
////                                            audio.play();
//                                        }

                                    document.getElementById("message-bar-text").innerHTML = data.body.product_name+"<br>Код ТНВЭД: "+data.body.product_tnved+"<br>GTIN: "+data.body.product_gtin+"<br>"+"Производитель: "+data.body.producer_name_comp+"<br>Собственник: "+data.body.owner+"<br>"+data.body.status_check+"<br>Дата производства: "+data.body.produced_date+"<br>Годен до: "+data.body.expire_date+"";

                                        if (data.body.button_close === 'invisible'){
                                               InVisibleAbout();
                                                }
                                        if (data.body.button_close === 'visible'){
                                            VisibleAbout();
                                                }
                                        }
                                else{
//                                    var audio = new Audio('/static/audio/error.wav');
//                                    audio.play();

                                    document.getElementById("main_check").style.display = "none";
                                    document.getElementById("response_check").style.display = "block";
                                    svg = '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" class="bi bi-exclamation-triangle text-danger" viewBox="0 0 16 16"><path d="M7.938 2.016A.13.13 0 0 1 8.002 2a.13.13 0 0 1 .063.016.15.15 0 0 1 .054.057l6.857 11.667c.036.06.035.124.002.183a.2.2 0 0 1-.054.06.1.1 0 0 1-.066.017H1.146a.1.1 0 0 1-.066-.017.2.2 0 0 1-.054-.06.18.18 0 0 1 .002-.183L7.884 2.073a.15.15 0 0 1 .054-.057m1.044-.45a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767z"/><path d="M7.002 12a1 1 0 1 1 2 0 1 1 0 0 1-2 0M7.1 5.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0z"/></svg>'
                                    document.getElementById("message-bar-text").innerHTML = svg + "<br><h3>КИ не найден</h3>"
                                    setTimeout(function () {
                                        document.getElementById("main_check").style.display = "block";
                                        document.getElementById("response_check").style.display = "none";
                                        location.reload(true);

                                    }, 3200);
                                }
                         },
                        error: function(jqxhr, status, errorMsg) {
                              if (status === 'timeout'){
                                               document.getElementById("main_check").style.display = "none";
                                    document.getElementById("response_check").style.display = "block";
                                    svg = '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" class="bi bi-exclamation-triangle text-danger" viewBox="0 0 16 16"><path d="M7.938 2.016A.13.13 0 0 1 8.002 2a.13.13 0 0 1 .063.016.15.15 0 0 1 .054.057l6.857 11.667c.036.06.035.124.002.183a.2.2 0 0 1-.054.06.1.1 0 0 1-.066.017H1.146a.1.1 0 0 1-.066-.017.2.2 0 0 1-.054-.06.18.18 0 0 1 .002-.183L7.884 2.073a.15.15 0 0 1 .054-.057m1.044-.45a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767z"/><path d="M7.002 12a1 1 0 1 1 2 0 1 1 0 0 1-2 0M7.1 5.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0z"/></svg>'
                                    document.getElementById("message-bar-text").innerHTML = svg + "<br><h3>Timeout</h3>"
                                    setTimeout(function () {
                                        document.getElementById("main_check").style.display = "block";
                                        document.getElementById("response_check").style.display = "none";
                                        location.reload(true);

                                    }, 1500);
                                                }
                            }
                    });
    }, 500);
                    });
}





function SendCodeButon() {

    document.getElementById("message-bar").style.display = "none";
    code = $('input[name="check_code"]').val();

        $.ajax({
                        url: '/check_code/',
                        method: 'post',
                        dataType: 'json',
                        headers: {
                            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
                        },
                        data: {
                                check_code: code
                                },
                                success: async function(data){
                                    document.querySelector('input#searchInput').value = '';
                                    if (data.status === 'success'){
                                            document.getElementById("message-bar").style.display = "block";
                                            document.getElementById("message-bar-header").innerHTML = "<h1><br>Результаты проверки</h1>"
                                            document.getElementById("message-bar-text").innerHTML = "<br><h3>"+data.body.product_name+"</h3><br><h4>Код ТНВЭД: "+data.body.product_tnved+"</h4><br><h4>GTIN: "+data.body.product_gtin+"</h4><br><h4>Отмаркировано: "+data.body.producer_name_comp+"</h4><br><h4>Собственник: "+data.body.owner+"</h4><br><h1>Статус: "+data.body.status_check+"</h1><br><h4>Дата производства: "+data.body.produced_date+"</h4><br><h4>Годен до: "+data.body.expire_date+"</h4>";
                                            }
                                    else{
                                            document.getElementById("message-bar").style.display = "block";
                                            document.getElementById("message-bar-header").innerHTML = "<h1><br>КИ не найден</h1>"
                                            document.getElementById("message-bar-text").innerHTML = ""
                                            }
                                }
                    });

}

function play_success() {
  var audio = new Audio('https://interactive-examples.mdn.mozilla.net/media/cc0-audio/t-rex-roar.mp3');
//  audio.play();
}

function ButtonClose(){
    location.reload(true);

}

function openFullscreen() {

var elem = document.documentElement;
  if (elem.requestFullscreen) {
    elem.requestFullscreen();
  } else if (elem.mozRequestFullScreen) { /* Firefox */
    elem.mozRequestFullScreen();
  } else if (elem.webkitRequestFullscreen) { /* Chrome, Safari & Opera */
    elem.webkitRequestFullscreen();
  } else if (elem.msRequestFullscreen) { /* IE/Edge */
    elem.msRequestFullscreen();
  }
}

function ChangeDate(){

    let timeout = null;
    document.querySelector('#searchInput').addEventListener('keyup', function(event) {
    code = $('input[name="change_code"]').val();
    clearTimeout(timeout);
    timeout = setTimeout(function () {
          $.ajax({
                        url: '/check_code/',
                        method: 'post',
                        dataType: 'json',
                        cache: false,
                        timeout: 1000,
                        headers: {
                            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
                        },
                        data: {
                                check_code: code
                                },
                        success: async function(data){
                                alert(data.status)
                                if(data.status === 'error'){
                                    document.getElementById("main_check").style.display = "none";
                                    document.getElementById("producer_invalid").style.display = "block";
                                    svg = '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" class="bi bi-exclamation-triangle text-danger" viewBox="0 0 16 16"><path d="M7.938 2.016A.13.13 0 0 1 8.002 2a.13.13 0 0 1 .063.016.15.15 0 0 1 .054.057l6.857 11.667c.036.06.035.124.002.183a.2.2 0 0 1-.054.06.1.1 0 0 1-.066.017H1.146a.1.1 0 0 1-.066-.017.2.2 0 0 1-.054-.06.18.18 0 0 1 .002-.183L7.884 2.073a.15.15 0 0 1 .054-.057m1.044-.45a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767z"/><path d="M7.002 12a1 1 0 1 1 2 0 1 1 0 0 1-2 0M7.1 5.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0z"/></svg>'
                                    document.getElementById("message-bar-text").innerHTML = svg + "<br><h3>КИ не найден</h3>"
                                    setTimeout(function () {
                                        document.getElementById("main_check").style.display = "block";
                                        document.getElementById("producer_invalid").style.display = "none";
                                        location.reload(true);

                                    }, 3200);
                                }else{

                            let str = data.body.owner;
                            let substr = "АВТО-ЕВРО";

                            if (str.indexOf(substr) !== -1)
                            {
                            if (data.body.produced_date === "Отсутствует") {
                                 document.getElementById("main_check").style.display = "none";
                             document.getElementById("producer_invalid").style.display = "block";
                             svg = '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" class="bi bi-exclamation-triangle text-danger" viewBox="0 0 16 16"><path d="M7.938 2.016A.13.13 0 0 1 8.002 2a.13.13 0 0 1 .063.016.15.15 0 0 1 .054.057l6.857 11.667c.036.06.035.124.002.183a.2.2 0 0 1-.054.06.1.1 0 0 1-.066.017H1.146a.1.1 0 0 1-.066-.017.2.2 0 0 1-.054-.06.18.18 0 0 1 .002-.183L7.884 2.073a.15.15 0 0 1 .054-.057m1.044-.45a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767z"/><path d="M7.002 12a1 1 0 1 1 2 0 1 1 0 0 1-2 0M7.1 5.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0z"/></svg>'
                             document.getElementById("message-bar-text").innerHTML = svg + "<br><br><h6>Отсутствует дата производства</h6>"
                             setTimeout(function () {
                                document.getElementById("main_check").style.display = "block";
                                document.getElementById("producer_invalid").style.display = "none";
                                location.reload(true);

                                    }, 5000);
                            }else{

                             document.getElementById("main_check").style.display = "none";
                             document.getElementById("producer_valid").style.display = "block";
                             document.getElementById("ki").value = data.body.spl_string;
                             document.getElementById("pr_date").value = data.body.produced_date;
                             document.getElementById("exp_date").value = data.body.expire_date;
                             document.getElementById("bar-text").innerHTML = '<h6 class="text-primary">'+data.body.product_name+"</h3><h6>GTIN: "+data.body.product_gtin+"</h4>"
                                }
                             }
                             else
                             {
                             document.getElementById("main_check").style.display = "none";
                             document.getElementById("producer_invalid").style.display = "block";
                             svg = '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" class="bi bi-exclamation-triangle text-danger" viewBox="0 0 16 16"><path d="M7.938 2.016A.13.13 0 0 1 8.002 2a.13.13 0 0 1 .063.016.15.15 0 0 1 .054.057l6.857 11.667c.036.06.035.124.002.183a.2.2 0 0 1-.054.06.1.1 0 0 1-.066.017H1.146a.1.1 0 0 1-.066-.017.2.2 0 0 1-.054-.06.18.18 0 0 1 .002-.183L7.884 2.073a.15.15 0 0 1 .054-.057m1.044-.45a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767z"/><path d="M7.002 12a1 1 0 1 1 2 0 1 1 0 0 1-2 0M7.1 5.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0z"/></svg>'
                             document.getElementById("message-bar-text").innerHTML = svg + "<br><br><h6>Редактировать параметры может только участник, осуществлявший нанесение либо ввод в оборот кода идентификации</h6>"
                             setTimeout(function () {
                                document.getElementById("main_check").style.display = "block";
                                document.getElementById("producer_invalid").style.display = "none";
                                location.reload(true);

                                    }, 5000); }
                                    }


                        },
                        error: function(jqxhr, status, errorMsg) {
                              if (status === 'timeout'){
                                     document.getElementById("main_check").style.display = "none";
                                    document.getElementById("producer_invalid").style.display = "block";
                                    svg = '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" class="bi bi-exclamation-triangle text-danger" viewBox="0 0 16 16"><path d="M7.938 2.016A.13.13 0 0 1 8.002 2a.13.13 0 0 1 .063.016.15.15 0 0 1 .054.057l6.857 11.667c.036.06.035.124.002.183a.2.2 0 0 1-.054.06.1.1 0 0 1-.066.017H1.146a.1.1 0 0 1-.066-.017.2.2 0 0 1-.054-.06.18.18 0 0 1 .002-.183L7.884 2.073a.15.15 0 0 1 .054-.057m1.044-.45a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767z"/><path d="M7.002 12a1 1 0 1 1 2 0 1 1 0 0 1-2 0M7.1 5.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0z"/></svg>'
                                    document.getElementById("message-bar-text").innerHTML = svg + "<br><h3>Timeout</h3>"
                                    setTimeout(function () {

                                        location.reload(true);



                                    }, 1500);
                                         }
                            }
                    });
    }, 500);
                    });
}

function ApplyChangeDate(){
        let dateReg = /^\d{4}[./-]\d{2}[./-]\d{2}$/
        ki = $('input[name="ki"]').val();
        pr_date = $('input[name="pr_date"]').val();
        exp_date = $('input[name="exp_date"]').val();

        if (!dateReg.test(pr_date) && !dateReg.test(exp_date)){
            document.getElementById("exp_date").classList.add("is-invalid");
            document.getElementById("pr_date").classList.add("is-invalid");
                setTimeout(function () {
                    document.getElementById("exp_date").classList.remove("is-invalid");
                    document.getElementById("pr_date").classList.remove("is-invalid");
                }, 1500);
        }



        else if (!dateReg.test(exp_date)){
            document.getElementById("exp_date").classList.add("is-invalid");
            setTimeout(function () {
                document.getElementById("exp_date").classList.remove("is-invalid");
            }, 1500);
        }
        else if (!dateReg.test(pr_date)) {

                document.getElementById("pr_date").classList.add("is-invalid");
                setTimeout(function () {
                    document.getElementById("pr_date").classList.remove("is-invalid");
                }, 1500);
            }
        else {


        $.ajax({
                        url: '/change_date/',
                        method: 'post',
                        dataType: 'json',
                        headers: {
                            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
                        },
                        data: {
                                apply_request: 'true',
                                ki: ki,
                                pr_date: pr_date,
                                exp_date: exp_date

                                },
                                success: async function(data){
                                    if (data.status === 'success'){
                                        document.getElementById("main_check").style.display = "none";
                                        document.getElementById("producer_invalid").style.display = "none";
                                        document.getElementById("producer_valid").style.display = "none";
                                        document.getElementById("apply_change").style.display = "block";
                                        document.getElementById("apply-bar-text").innerHTML = '<br><h3 class="text-success">Обработан успешно</h3><br><h4>'+data.doc_num+"</h4><br>"
                                        }
                                     if (data.status === 'error'){
                                        document.getElementById("main_check").style.display = "none";
                                        document.getElementById("producer_invalid").style.display = "none";
                                        document.getElementById("producer_valid").style.display = "none";
                                        document.getElementById("apply_change").style.display = "block";
                                         svg = '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" class="bi bi-exclamation-triangle text-danger" viewBox="0 0 16 16"><path d="M7.938 2.016A.13.13 0 0 1 8.002 2a.13.13 0 0 1 .063.016.15.15 0 0 1 .054.057l6.857 11.667c.036.06.035.124.002.183a.2.2 0 0 1-.054.06.1.1 0 0 1-.066.017H1.146a.1.1 0 0 1-.066-.017.2.2 0 0 1-.054-.06.18.18 0 0 1 .002-.183L7.884 2.073a.15.15 0 0 1 .054-.057m1.044-.45a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767z"/><path d="M7.002 12a1 1 0 1 1 2 0 1 1 0 0 1-2 0M7.1 5.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0z"/></svg>'
                                         document.getElementById("apply-bar-text").innerHTML = svg + '<br><br><h3 class="text-danger">Обработан с ошибками</h3>'
                                         setTimeout(function () {
                                            document.getElementById("main_check").style.display = "block";
                                            document.getElementById("apply_change").style.display = "none";
                                            location.reload(true);

                                            }, 5000);
                                     }
                                },
                        error: function(jqxhr, status, errorMsg) {
                              if (status === 'timeout'){
                                    document.getElementById("main_check").style.display = "none";
                                        document.getElementById("producer_invalid").style.display = "none";
                                        document.getElementById("producer_valid").style.display = "none";
                                        document.getElementById("apply_change").style.display = "block";
                                    svg = '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" class="bi bi-exclamation-triangle text-danger" viewBox="0 0 16 16"><path d="M7.938 2.016A.13.13 0 0 1 8.002 2a.13.13 0 0 1 .063.016.15.15 0 0 1 .054.057l6.857 11.667c.036.06.035.124.002.183a.2.2 0 0 1-.054.06.1.1 0 0 1-.066.017H1.146a.1.1 0 0 1-.066-.017.2.2 0 0 1-.054-.06.18.18 0 0 1 .002-.183L7.884 2.073a.15.15 0 0 1 .054-.057m1.044-.45a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767z"/><path d="M7.002 12a1 1 0 1 1 2 0 1 1 0 0 1-2 0M7.1 5.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0z"/></svg>'
                                    document.getElementById("apply-bar-text").innerHTML = svg + "<br><h3>Timeout</h3>"
                                    setTimeout(function () {
                                        location.reload(true);
                                    }, 1500);
                                         }
                              if (status === 500){
                                window.open('/error_server/');
                              }
                              if (status === 404){
                                window.open('/error_not_found/');
                              }
                            }
                    });
                    }
}


