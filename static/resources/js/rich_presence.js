const app = require('electron').app
const child  = require('child_process').execFile;
const { net } = require('electron');
const fs = require('fs');

let rich_presence_path = null
let rich_presence_host = null
let rich_presence_port = null
let rich_presence_process = null
let app_location = null



module.exports = {
    /**
     * Функция определения местоположения приложения и api
     *
     * @returns {null}
     */
   init_discord_path: function(){
        let app_full_location = app.getAppPath();
        app_location = app_full_location.replace("\\resources\\app.asar", "")
        rich_presence_path = `${app_location}\\discord`;
        rich_presence_process = child(`${rich_presence_path}\\main.exe`);
        return null
   },

    /**
     * Функция установки порта и хоста api для запросов
     *
     * @returns {null}
     */
    set_api_settings: function() {
        const api_json_settings = JSON.parse(fs.readFileSync(`${rich_presence_path}\\config\\settings.json`));
        rich_presence_host = api_json_settings["host"];
        rich_presence_port = api_json_settings["port"];
        return null
    },

    /**
     * Функция закрытия процесса api
     *
     * @returns {null}
     */
    kill_discord_api_process: function () {
        if (rich_presence_process === null) {
            return null
        } else {
            rich_presence_process.kill();
            return null
        }
    },

    /**
     * Функция запросов к api для установки состояний discord
     *
     * @returns {null}
     */
    set_state: function(state) {
        const request = net.request({
            method: 'GET', protocol: 'http:',
            hostname: rich_presence_host, port: rich_presence_port,
            path: `handler/${state}/`
        });
         request.on('response', (response) => {
            console.log(`STATUS: ${response.statusCode}`);
        });
        request.end();
        return null
    }
}