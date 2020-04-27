//
var socket = io('http://127.0.0.1:5000');
const tile = 10;
const player_id = Math.ceil(Math.random() * 1000)+10000

const playerMenu = new PlayerMenu();
const shopMenu = new ShopMenu();

var xmlhttp = new XMLHttpRequest();


$(document).ready(function(){
    var display = new Display(document.getElementById("game_canvas"), {x:900, y:700}, tile);

    let player_data;
    let entity_list;

    socket.on('connect', function() {
        socket.emit('socket/v1/get_player_data', player_id);
        socket.emit('socket/v1/get_entities', player_id);
    });


    socket.on('player_data', function(rev) {
        if (rev.id == player_id) {
            player_data = rev.data;
        }
    });


    socket.on('env_entities', function(ent_list) {
        entity_list = ent_list
    });


    let currentMenu;


    function keyDownAction(event){
        isMove = false;
        if (event.keyCode == 37 || event.keyCode == 65){
            //move left
            d="left";
            isMove = true;
        } else if (event.keyCode == 38 || event.keyCode == 87){
            // move up
            d="up";
            isMove = true;
        } else if (event.keyCode == 39 || event.keyCode == 68){
            //move right
            d="right";
            isMove = true;
        } else if (event.keyCode == 40 || event.keyCode == 83){
            // move down
            d="down";
            isMove = true;
        }

        if (isMove == true) {
            if (player_data.inMenu == false) {
                socket.emit('socket/v1/get_player_action', {
                    'player_id':player_id, 
                    'action':'move', 
                    'direction':d});
            } else {
                if (currentMenu.navagateable){
                    switch (d) {
                        case 'up':
                            if (currentMenu.index < 1) {
                                currentMenu.index = currentMenu.elements.length;}
                            currentMenu.index -= 1;
                            break;
                        case 'down':
                            currentMenu.index += 1;
                            if (currentMenu.index == currentMenu.elements.length) {
                                currentMenu.index = 0;}
                            break;
                    }
                }
            }
        }
    }


    function keyUpAction(event){
        keyUp = false;

        if (event.keyCode == 27){
            // quit current (ESC)
            a="esc";
            player_data.inMenu = false;
            player_data.currMenu = "None";
            keyUp = true;

        } else if (event.keyCode == 69 && player_data.inMenu == false){
            // interact (E)
            a="interact";
            player_data.inMenu = true;
            player_data.currMenu = "shop";

            xmlhttp.open("GET", "/rest-api/v1/get_shop_stock", true);
            xmlhttp.send();

            shopMenu.SELL_MENU.elements = player_data.inventory;

            currentMenu = shopMenu.get_current_menu(-1);
            keyUp = true;

        } else if (event.keyCode == 73 && player_data.inMenu == false){
            // open inventory (I)
            player_data.inMenu = true;
            a="inventory";
            player_data.currMenu = "inventory";

            playerMenu.STATS_MENU.elements = [
                "Health: "+player_data.health,
                "Armour: "+player_data.armour,
                "Attack: "+player_data.attack,
                "Gold: "+player_data.gold];

            playerMenu.INVENTORY_MENU.elements = player_data.inventory;

            currentMenu = playerMenu.get_current_menu(-1);
            keyUp = true;

        } else if (event.keyCode == 32){
            // melee attack (SPACE)
            a="attack";
            keyUp = true;

        } else if (event.keyCode == 81){
            // shoot bolt (Q)
            a="shoot";
            keyUp = true;

        } else if (event.keyCode == 13 && player_data.inMenu == true){
            // hit enter (ENTER)
            if (currentMenu.navagateable){
                if (currentMenu.expandable){
                    if (a == "inventory") {
                        // Update for the player menu.
                        currentMenu = playerMenu.get_current_menu(currentMenu.index);

                    } else if (a == "interact"){
                        // Update for the shop menu
                        currentMenu = shopMenu.get_current_menu(currentMenu.index);
                    }
                } else {
                    if (currentMenu.title == "Inventory Menu"){
                        // If the player has accessed their inventory then they can use items as long as they exist.
                        d = currentMenu.elements[currentMenu.index][0];
                        if (d != undefined){
                            a="use";
                        }
                    }
                }
            }
            keyUp = true;
        }

        if (keyUp == true) {
            if (a == "attack" || a == "shoot"){
                // If the user is about to launch and attack then find the attack direction for the user.
                socket.emit('socket/v1/update_player_data', {
                    'player_id':player_id, 
                    'action':a,
                    'direction':d});

            } else if (a == "use"){
                // If the user is about to use an item in their inventory then update the users inventory.
                socket.emit('socket/v1/get_player_action', {
                    'player_id':player_id, 
                    'action':a, 
                    'item':d});

            } else if (a == "interact" || a == "inventory" || a == "esc"){
                // If the user is interacting, escaping or accessing the inventory then update the users current state.
                socket.emit('socket/v1/update_player_data', {
                    'player_id':player_id,
                    'action':a,
                    'inMenu':player_data.inMenu,
                    'currMenu':player_data.currMenu});
            }
        }
    }


    function main(){
        // call required function of render.
        if (entity_list != undefined) {
            if (player_data.inMenu == true) {
                display.currentMenu = currentMenu;
            }
            display.render(entity_list, player_data, player_id);
        }
    }


    xmlhttp.onreadystatechange = function() {
        // Handle rest call for current shop stock.
        if (this.readyState == 4 && this.status == 200) {
            response = JSON.parse(this.responseText);
            shopMenu.BUY_MENU.elements = response.data;
        } 
    }


    // Handle user input for key up and key down event.
    document.addEventListener("keydown", keyDownAction);
    document.addEventListener("keyup", keyUpAction);

    // Set a base interval for the loop to update.
    let game = setInterval(main, 1000/30);
});



