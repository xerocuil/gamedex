// LIBRARY FUNCTIONS

/**
 * Launch installed game
 * @param  {string} platformSlug - Platform slug ID
 * @param  {string} fileName - Game file name
 */
function launch_game(platformSlug, fileName) {
    fetch(`/launch/game/${platformSlug}/${fileName}`)
}

/**
 * Search Game database
 * @return {object} results - Game table object
 */
function search_query() {
    let query = document.getElementById("query").value.valueOf();
    url_base = "/library/search?query="
    window.location.href = url_base+query;
}


// WINDOW FUNCTIONS

/**
 * Close application window
 */
function closeWindow() {
    pywebview.api.close_window()
}

/**
 * Toggle app fullscreen mode
 */
function toggleFullscreen() {
    pywebview.api.toggle_fullscreen()
}

/**
 * Show pop-up window with
 * response.message as string
 * 
 * @param  {object} response - function response
 */
function showConsole(response) {
    const consoleDiv = document.getElementById("console");
    let message  = document.getElementById("console-text")
    message.innerText = '';
    message.innerText = response.message;
    consoleDiv.style.display = "block";
}

/**
 * Hide pop-up window
 */ 
function hideConsole() {
    document.getElementById("console").style.display = "none";
}


// DEVICE FUNCTIONS

/**
 * Install Game to device
 * 
 * @param  {string} device_slug     - Game slug ID
 * @param  {string} platformSlug    - Platform slug ID
 * @param  {string} fileName        - Game file name
 */
function installGame(device_slug, platformSlug, fileName) {
    let message = {"message":"Installing "+fileName+" ..."}
    const confirmDiv = document.getElementById("console-confirm")
    showConsole(message);
    pywebview.api.install_game(device_slug, platformSlug, fileName)
        .then(showConsole)
        .then(confirmDiv.style.display = "block");
}

/**
 * Uninstall game from device
 * 
 * @param  {string} device_slug     - Game slug ID
 * @param  {string} platformSlug    - Platform slug ID
 * @param  {string} fileName        - Game file name
 */
function unInstallGame(device_slug, platformSlug, fileName) {
    let test = window.confirm(`Are you sure you want to remove ${fileName}?`);
    if (test == true){
        pywebview.api.uninstall_game(device_slug, platformSlug, fileName)
        window.alert(`${fileName} has been removed.`)
        window.location.reload()
    }
    
}
