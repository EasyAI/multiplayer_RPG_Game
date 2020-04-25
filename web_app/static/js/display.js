
const Display = function(canvas, dimensions, tileSize) {

    this.context = canvas.getContext("2d");
    this.dimensions = dimensions;
    this.tileSize = tileSize;
    this.baseOffsetX = tileSize*10;

    //MenuInfo
    this.currentMenu;

    this.render = function(entities, player_data, player_id){
        this.draw_map();
        this.draw_entities(entities, player_id);
        this.draw_id(player_id);

        if (player_data.inMenu == true) {
            this.draw_menu(this.currentMenu)
        }
    }


    this.draw_entities = function(entities, player_id){

        for (let i = 0; i<entities.length; i++){
            if (entities[i].type == "wall") {
                this.context.fillStyle="black";
            } else if (entities[i].type == "shop") {
                this.context.fillStyle="orange";
            } else if (entities[i].type == "player") {
                if (entities[i].id != player_id) {
                    this.context.fillStyle="green";
                } else {
                    this.context.fillStyle="blue";
                }
            } else if (entities[i].type == "monster") {
                this.context.fillStyle="red";
            } else if (entities[i].type == "loot_bag") {
                 this.context.fillStyle="yellow";
            } else if (entities[i].type == "bolt") {
                this.context.fillStyle="black";
            }

            this.context.fillRect(entities[i].x+this.baseOffsetX, entities[i].y, entities[i].sizeX, entities[i].sizeY);
        }
    }


    this.draw_id = function(player_id){
        this.context.fillStyle="white";
        this.context.font = "15px Changa one";
        this.context.fillText("ID:"+player_id, this.tileSize, this.tileSize);
    }


    this.draw_menu = function(menu){
        this.context.fillStyle="white";
        this.context.font = "15px Changa one";
        fontSize = 15;
        yPosition = fontSize + 20;
        this.context.fillText(menu.title, this.tileSize, yPosition);

        for (let i = 0; i<menu.elements.length; i++){
            if (menu.index == i) {
                this.context.fillStyle="red";
            } else {
                this.context.fillStyle="white";
            }
            this.context.fillText(menu.elements[i], this.tileSize, (fontSize*(i+1))+yPosition);
        }
    }


    this.draw_map = function(){
        // draw plane
        this.context.fillStyle="white";
        this.context.fillRect(0, 0, this.dimensions.x, this.dimensions.y);
        this.context.fillStyle="black";
        this.context.fillRect(0, 0, this.baseOffsetX, this.dimensions.y);
    }
}