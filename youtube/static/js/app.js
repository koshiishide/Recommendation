//リクエストパラメータのセット
var KEY = 'AIzaSyASORMR-r0SzjyvaRN4dcIUjIsEKOWIWWM';    //API_KEY
var url = 'https://www.googleapis.com/youtube/v3/search?'; //API URL

ulr += 'type=video';        //動画の検索
url += '&part=snippet';     //検索結果にすべてのプロパティを含める
url += '&videoEmbeddable';  //検索ワードこのサンプルでは music に指定
url += '&videoSyndicated';  //youtube.com以外で再生できる動画のみ限定
url += '&maxResults = 6';   //動画の最大取得件数
url += '&key=' + KEY;       // APIKEY   

//動作確認が終わったら消す。
console.log(url);

//HTMLが読み込まれてから実行する処理

$(function() {
    //youtubeの動画を検索して取得
    $.ajax({
        url: url,
        dataType : 'jsonp'
}).done(function(data) {
    if (data.items) {
    setData(data);  //データ取得に成功したときの処理
    } else {
        console.log(data);
        alert('該当するデータが見つかりませんでした');
    }
}).fail(function(data) {
    alert('通信に失敗しました');
});
});

//データ取得が成功したときの処理

function setData(data) {
    var result = '';
    var video = '';
    // 動画を表示するHTMLを作る
    for (var i = 0; i < data.items.length; i++) {
        video  = '<iframe src="https://www.youtube.com/embed/';
        video  +=  data.items[i].id.videoId;
        video  += '" allowfullscreen></iframe>';
        result += '<div class="video">' + video + '</div>'
    }
    // HTMLに反映する
    $('#videoList').html(result);
}