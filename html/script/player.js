var Player = function() {
    var p = {
        paused: false,
        seeking: false,
    }

    p.playButton = $('play-button')
    p.controller = $('music-control')
    p.progress = $('progress')
    p.handle = $('handle')
    p.timeCode = $('time-code')
    p.total = $('progress-bar').offsetWidth

    p.showButtonImage = function() {
        var imageUrl = ''
        var color = ''
        if (p.paused) {
            imageUrl = "url('pic/play.svg')"
            color = 'rgba(0, 0, 0, 0.3)'
        }
        else {
            imageUrl = "url('pic/pause.svg')"
            color = 'rgba(0, 0, 0, 0.2)'
        }
        p.playButton.style.backgroundImage = imageUrl
        p.playButton.style.backgroundColor = color
    }
    p.clearButtonImage = function() {
        if (!p.paused) {
            p.playButton.style.backgroundImage = 'none'
            p.playButton.style.backgroundColor = 'unset'
        }
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
    p.playButton.onmouseover = p.showButtonImage
    p.playButton.onmouseout = p.clearButtonImage
    p.playButton.onclick = p.switchPlayStatus
    window.addEventListener('keypress', function(e) {
        if (e.key == ' ') {
            p.switchPlayStatus()
            p.clearButtonImage()
            var origin = $('album').style.transform
            $('album').style.transform = 'scale(1.02)'
            setTimeout(function () {
                $('album').style.transform = origin
            }, 200)
        }
    })

    p.setAlbumCover = function(url) {
        $('album').style.backgroundImage = url
        $('top-banner').style.backgroundImage = url
    }
    p.setSongInfo = function(name, artists, album) {
        $('song-name').innerText = name
        $('song-name').title = name
        var info = ''
        for (var i in artists) {
            info += artists[i]
        }
        info += ' - ' + album
        $('song-info').innerText = info
        $('song-info').title = info
    }

    p.__getMinute = function(second) {
        var minute = ''
        minute += parseInt(second / 60) + ':'
        var s = parseInt(second % 60)
        minute += (s < 10 ? '0' : '') + s
        return minute
    }
    p.updateTimecode = function() {
        var duration = p.controller.duration
        if (!isNaN(duration)) {
            var time = p.__getMinute(duration)
            time = p.__getMinute(p.controller.currentTime) + '/' + time
            p.timeCode.innerText = time
        }
    }
    p.moveProgress = function(width) {
        if (width > p.total) {
            width = parseInt(p.total)
        }
        else if (width < 0) {
            width = parseInt(0)
        }
        else {
            width = parseInt(width)
        }
        p.progress.style.width = width + 'px'
        p.handle.style.left = width + 'px'
    }
    p.updateProgress = function() {
        var percent = p.controller.currentTime / p.controller.duration
        p.moveProgress(p.total * percent)
    }
    p.startUpdateLoop = function() {
        if (!p.seeking) {
            p.updateTimecode()
            p.updateProgress()
        }
        setTimeout(function() {
            p.startUpdateLoop()
        }, 500)
    }

    p.handle.onmousedown = function(e) {
        p.seeking = true
        p.handleX = p.handle.offsetLeft
        p.mouseX = e.clientX
    }
    p.handle.onmouseup = function(e) {
        if (p.seeking) {
            p.seeking = false
            var percent = p.progress.offsetWidth / p.total
            p.controller.currentTime = p.controller.duration * percent
        }
    }
    p.handle.onmousemove = function(e) {
        if (p.seeking) {
            p.moveProgress(p.handleX + e.clientX - p.mouseX)
        }
    }
    document.body.onmousemove = p.handle.onmousemove
    document.body.onmouseup = p.handle.onmouseup

    window.addEventListener('resize', function() {
        p.total = $('progress-bar').offsetWidth
        p.updateProgress()
    })

    return p
}
