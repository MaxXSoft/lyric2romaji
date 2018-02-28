var Player = function() {
    var p = {
        paused: false,
        seeking: false,
        changingVolume: false,
        mouseInVolumeBox: false,
    }

    p.playButton = $('play-button')
    p.controller = $('music-control')

    p.progressBar = $('progress-bar')
    p.progress = $('progress')
    p.handle = $('handle')
    p.timeCode = $('time-code')
    p.total = p.progressBar.offsetWidth

    p.volumeButton = $('volume-button')
    p.volumeBox = $('volume-container')
    p.volumeBar = $('volume-bar')
    p.volume = $('volume')
    p.volumeHandle = $('volume-handle')

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
    p.seek = function(percent) {
        p.controller.currentTime = p.controller.duration * percent
    }

    p.handle.onmousedown = function(e) {
        p.seeking = true
        p.handleX = p.handle.offsetLeft
        p.mouseX = e.clientX
    }
    p.handle.onmouseup = function(e) {
        if (p.seeking) {
            p.seeking = false
            p.seek(p.progress.offsetWidth / p.total)
        }
    }
    p.handle.onmousemove = function(e) {
        if (p.seeking) {
            p.moveProgress(p.handleX + e.clientX - p.mouseX)
        }
    }
    p.progressBar.onmouseup = function(e) {
        p.seek((e.clientX - p.progressBar.getBoundingClientRect().left) / p.total)
    }
    p.progress.onmouseup = p.progressBar.onmouseup
    document.body.addEventListener('mousemove', p.handle.onmousemove)
    document.body.addEventListener('mouseup', p.handle.onmouseup)

    window.addEventListener('resize', function() {
        p.total = $('progress-bar').offsetWidth
        p.updateProgress()
    })

    p.setVolume = function(percent) {
        p.controller.volume = percent
    }
    p.updateVolumeIcon = function(percent) {
        var levels = [
            "url('pic/volume0.svg')",
            ", url('pic/volume1.svg')",
            ", url('pic/volume2.svg')",
            ", url('pic/volume3.svg')",
        ]
        var bg
        if (percent < 0.25) {
            bg = levels[0]
        }
        else if (percent < 0.5) {
            bg = levels[0] + levels[1]
        }
        else if (percent < 0.75) {
            bg = levels[0] + levels[1] + levels[2]
        }
        else {
            bg = levels[0] + levels[1] + levels[2] + levels[3]
        }
        p.volumeButton.style.backgroundImage = bg
    }
    p.moveVolume = function(width) {
        if (width > p.volumeBar.offsetWidth) {
            width = parseInt(p.volumeBar.offsetWidth)
        }
        else if (width < 0) {
            width = parseInt(0)
        }
        else {
            width = parseInt(width)
        }
        p.volume.style.width = width + 'px'
        p.volumeHandle.style.left = width + 'px'
        p.updateVolumeIcon(width / p.volumeBar.offsetWidth)
    }
    p.volumeButton.onmouseover = function() {
        p.volumeBox.style.opacity = '1'
    }
    p.volumeButton.onmouseout = function() {
        if (!p.changingVolume) {
            setTimeout(function() {
                if (!p.mouseInVolumeBox) {
                    p.volumeBox.style.opacity = '0'
                }
            }, 100)
        }
    }
    p.volumeBox.onmouseenter = function() {
        p.mouseInVolumeBox = true
    }
    p.volumeBox.onmouseleave = function() {
        p.mouseInVolumeBox = false
        if (p.changingVolume) {
            var id = setInterval(function() {
                if (!p.changingVolume && !p.mouseInVolumeBox) {
                    p.volumeBox.style.opacity = '0'
                    clearInterval(id)
                }
            }, 100)
        }
        else {
            p.volumeBox.style.opacity = '0'
        }
    }
    p.volumeHandle.onmousedown = function(e) {
        p.changingVolume = true
        p.handleX = p.volumeHandle.offsetLeft
        p.mouseX = e.clientX
    }
    p.volumeHandle.onmouseup = function(e) {
        if (p.changingVolume) {
            p.changingVolume = false
        }
    }
    p.volumeHandle.onmousemove = function(e) {
        if (p.changingVolume) {
            p.moveVolume(p.handleX + e.clientX - p.mouseX)
            p.setVolume(p.volume.offsetWidth / p.volumeBar.offsetWidth)
        }
    }
    p.volumeBar.onmouseup = function(e) {
        var width = e.clientX - p.volumeBar.getBoundingClientRect().left
        p.moveVolume(width)
        p.setVolume(width / p.volumeBar.offsetWidth)
    }
    p.volume.onmouseup = p.volumeBar.onmouseup
    document.body.addEventListener('mousemove', p.volumeHandle.onmousemove)
    document.body.addEventListener('mouseup', p.volumeHandle.onmouseup)
    p.moveVolume(p.volumeBar.offsetWidth)
    p.setVolume(1)

    return p
}
