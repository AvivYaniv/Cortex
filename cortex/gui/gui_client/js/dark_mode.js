
class DarkModeHandler { 

    #DARK_MODE_LOCAL_STORAGE_ITEM_NAME = 'dark_mode';
    #is_dark_mode = false;

    constructor()
    {    
        this.is_dark_mode = (localStorage.getItem(this.DARK_MODE_LOCAL_STORAGE_ITEM_NAME) == 'true');
        if (this.is_dark_mode)
        {
            this.toggleDarkMode();
        }   
    };

    toggleDarkMode() {
        // Switch body to dark mode
        var element = document.body;
        element.classList.toggle("dark-mode");
        // Switch jQuery items to dark mode
        $("body > *").not("#dark_mode_button").toggleClass("dark-mode");
        // Switch D3.js charts to dark mode
        if (typeof d3 != 'undefined')
        {
            d3.selectAll("text").style("fill", getComputedStyle(document.body).color);
            // TODO : put from callback and not hard-coded
            d3.selectAll(".mouse-line").style(
            "stroke",
            getComputedStyle(document.body).color
            );
        }
        // Switch Chart.js charts to dark mode
        if (typeof Chart != 'undefined')
        {
            Chart.defaults.global.defaultFontColor = getComputedStyle(
            document.body
            ).color;
            Chart.helpers.each(Chart.instances, function (instance) {
            instance.chart.update();
            });
        }
    };

    toggleDarkModeForSession() {
        // Code Section
        // Toggle dark-mode in local storage
        this.is_dark_mode = !this.is_dark_mode;
        localStorage.setItem(this.DARK_MODE_LOCAL_STORAGE_ITEM_NAME, this.is_dark_mode);
        // Se
        this.toggleDarkMode();
      };
  }

  
  