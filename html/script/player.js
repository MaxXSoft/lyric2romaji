var Player = function() {
    var p = {
        paused: false,
    }
    p.playButton = $('play-button')
    p.controller = $('music-control')
    p.showButtonImage = function() {
        imageUrl = "url('pic/" + (p.paused ? 'play' : 'pause') + ".svg')"
        p.playButton.style.backgroundImage = imageUrl
    }
    p.clearButtonImage = function() {
        p.playButton.style.backgroundImage = 'none'
    }
    p.switchPlayStatus = function() {
        p.paused = !p.paused
        p.showButtonImage()
        if (p.paused) {
            p.controller.pause()
        }
        else {
            p.controller.play()
        }
    }
    p.setAlbumCover = function(url) {
        $('album').style.backgroundImage = url
        $('top-banner').style.backgroundImage = url
    }
    p.setSongInfo = function(name, artists, album) {
        $('song-name').innerText = name
        $('song-name').title = name
        info = ''
        for (var i in artists) {
            info += artists[i]
        }
        info += ' - ' + album
        $('song-info').innerText = info
        $('song-info').title = info
    }
    p.playButton.onmouseover = p.showButtonImage
    p.playButton.onclick = p.switchPlayStatus
    p.playButton.onmouseout = p.clearButtonImage
    return p
}
