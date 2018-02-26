var loadJSON = function(url, success) {
    var xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            if (xhr.status == 200 && success) {
                success(JSON.parse(xhr.responseText))
            }
        }
    }
    xhr.open("GET", url, true)
    xhr.send()
}
