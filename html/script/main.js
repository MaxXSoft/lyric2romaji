var applyInfo = function(player) {
    loadJSON('info.json', function(json) {
        albumPicUrl = "url('" + json.album.pic + "')"
        player.setAlbumCover(albumPicUrl)
        player.setSongInfo(json.name, json.artists, json.album.name)
        document.title = json.name + ' - [Lyric->Romaji]'
    })
}

var __main = function() {
    p = Player()
    p.startUpdateLoop()
    applyInfo(p)
}

window.onload = function() {
    __main()
}
