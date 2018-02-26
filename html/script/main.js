var applyInfo = function() {
    loadJSON('info.json', function(json) {
        albumPicUrl = "url('" + json.album.pic + "')"
        document.getElementById('top-banner').style.backgroundImage = albumPicUrl
        document.getElementById('album').style.backgroundImage = albumPicUrl
    })
}

applyInfo()
