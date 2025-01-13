const app = require('electron').app
const child  = require('child_process').execFile;
const fs = require('fs');

let rich_presence_host = null
let rich_presence_port = null
let rich_presence_path = null
let rich_presence_process = null
let app_location = null
let track_id = null // id трека который искать
let track_data = null // сохраненая информация о треке
let track_new = null // новый трек или нет
let player_state = null // новый трек или нет
let stop = null // timestamp паузы


module.exports = {
    "avatar":  null,

   init_discord_path: function(){
    let app_full_location = app.getAppPath();
    app_location = app_full_location.replace("\\resources\\app.asar", "")
    rich_presence_path = `${app_location}\\discord`;
    rich_presence_process = child(`${rich_presence_path}\\main.exe`);
    return null
   },

    kill_discord_api_process: function () {
        if (rich_presence_process === null) {
            return null
        } else {
            rich_presence_process.kill();
            return null
        }
    },

    set_api_settings: function() {
        const api_json_settings = JSON.parse(fs.readFileSync(`${rich_presence_path}\\config\\settings.json`));
        rich_presence_host = api_json_settings["host"]
        rich_presence_port = api_json_settings["port"]
        return null
    },

    get_track_url_by_handler: function (detail_url) { // framesHandler
        let track_url = new URL(detail_url);
        track_id = new URLSearchParams(track_url.search).get("trackId")
        return null
    },

    get_track_info: function () {
        const api_url = `https://api.music.yandex.net/tracks?trackIds=${track_id}`
        return fetch(api_url).then(response => response.json());
    },

    set_state: function(state) {
        fetch(`http://${rich_presence_host}:${rich_presence_port}/handler/${state}/`, {
            method: "GET"
        }).then()
        return null
    },

    set_new_state: function (status) {
        track_new = status
    },

    set_player_state: function (status) {
        player_state = status
    },

    get_player_state: function () {
        return player_state
    },

    set_pause_state: function () {
        let title = track_data["title"]
        let author = track_data["author"]
        let cover_url = track_data["cover"]
        stop = +new Date; // устанавливаем timestamp паузы
        let request_body = {
            title: title,
            author: author,
            cover: cover_url,
        }
        let json = JSON.stringify(request_body);
        let request = fetch(`http://${rich_presence_host}:${rich_presence_port}/handler/pause-music/`, {
            method: "POST",
            body: json,
            headers: {
                'Content-Type': 'application/json'
            },
        }).then()
        return null
    },

    set_play_state: function (music_data) {
        let title = music_data["result"][0]["title"]
        let author = music_data["result"][0]["artists"][0]["name"]
        let cover_url = music_data["result"][0]["coverUri"]
        let cover_full_url = `https://${cover_url}`
        let duration = music_data["result"][0]["durationMs"]
        let cover_fixed_url = cover_full_url.replace("%%", "200x200")
        let request_body = null
        if (track_new === true) { // если трек впервые включается
            request_body = {
            title: title, // название
            author: author, // автор
            cover: cover_fixed_url, // url обложки
            start_timestamp: +new Date, // timestamp начала проигрывания музыки
            pause_timestamp: null, // timestamp постановки на паузу
            duration: duration, // длительность трека в мс
            new: true // новый трек или снят с паузы
        };
            track_data = request_body
            track_new = false
        } else if (track_new === false) {
            request_body = track_data
            request_body["new"] = false // ставим что трек не новый(был поставлен и снят с паузы)
            request_body["pause_timestamp"] = stop // устанавливаем timestamp паузы
        }
        let json = JSON.stringify(request_body);
        let request = fetch(`http://${rich_presence_host}:${rich_presence_port}/handler/listen-music/`, {
            method: "POST",
            body: json,
            headers: {
                'Content-Type': 'application/json'
            },
        }).then()
        return null
    }
}