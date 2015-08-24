//Declaring the variable earth
      var earth;
      
      //function to show the LightBox
      function showLightBox(){
          document.getElementById('light').style.display='block';
          document.getElementById('fade').style.display='block';
        }

      //Intialise the webGl Earth
      function initialize() {
        if (window.location.href.substr(0, 5) === 'file:')
          alert("This file must be accessed via http:// or https:// to run properly.");
        earth = new WE.map('earth_div');
        earth.setView([46.8011, 8.2266], 2);
        WE.tileLayer('{z}/{x}/{y}.jpg', {
          tileSize: 256,
          bounds: [[-85, -180], [85, 180]],
          minZoom: 0,
          maxZoom: 16,
          attribution: 'Around The World - Checkmate',
          tms: true
        }).addTo(earth);
        
        //Displaying Marker
        var marker=WE.marker([51.5, -0.09]).addTo(earth);
          marker.bindPopup(
            "<a href = '#' onclick = 'showLightBox()'><div><b><center>London</center></b><br><span style='font-size:10px;color:#999'>'Cost of Accomodation: $40/min'</span></div></a>", {maxWidth: 150, closeButton: true}).openPopup();
      }

      //function to Fly to a place
      function panTo(coords) {
        earth.panTo(coords);
      }