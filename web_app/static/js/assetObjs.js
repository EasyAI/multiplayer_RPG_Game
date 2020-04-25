const PlayerMenu = function() {
    this.currentMenu = -1;

    this.BASE_MENU = {
        parent      :-1,
        menuId      :0,
        title       :"Player Menu",
        elements    :["Inventory", "Stats"],
        expandable  :true,
        navagateable:true,
        index       :0};

    this.INVENTORY_MENU = {
        parent      :0,
        menuId      :1,
        title       :"Inventory Menu",
        elements    :[],
        expandable  :false,
        navagateable:true,
        index       :-1};

    this.STATS_MENU = {
        parent      :0,
        menuId      :2,
        title       :"Stats Menu",
        elements    :["Health", "Armour", "Attack", "Gold"],
        expandable  :false,
        navagateable:false,
        index       :-1};


    this.update_current_menu = function(newMenuID){
        this.currentMenu = newMenuID
    };


    this.get_current_menu = function(currentIndex){
        switch (currentIndex){
            case -1:
                return(this.BASE_MENU);
            break;
            case 0:
                return(this.INVENTORY_MENU);
            break;
            case 1:
                return(this.STATS_MENU);
            break;
        };
    };
};


const ShopMenu = function() {
    this.currentMenu = -1;

    this.BASE_MENU = {
        parent      :-1,
        menuId      :0,
        title       :"Shop",
        elements    :["Buy", "Sell"],
        expandable  :true,
        navagateable:true,
        index       :0};

    this.BUY_MENU = {
        parent      :0,
        menuId      :1,
        title       :"Buy Menu",
        elements    :[],
        expandable  :false,
        navagateable:true,
        index       :-1};

    this.SELL_MENU = {
        parent      :0,
        menuId      :2,
        title       :"Sell Menu",
        elements    :[],
        expandable  :false,
        navagateable:true,
        index       :-1};


    this.update_current_menu = function(newMenuID){
        this.currentMenu = newMenuID
    };


    this.get_current_menu = function(currentIndex){
        switch (currentIndex){
            case -1:
                return(this.BASE_MENU);
            break;
            case 0:
                console.log("test");
                return(this.BUY_MENU);
            break;
            case 1:
                return(this.SELL_MENU);
            break;
        };
    };
};