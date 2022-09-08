let autocomplete;

function initAutoComplete(){
autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id_address'),
    {
        types: ['geocode', 'establishment'],
        //default in this app is "IN" - add your country code
        componentRestrictions: {'country': ['pl']},
    })
// function to specify what should happen when the prediction is clicked
autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged (){
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry){
        document.getElementById('id_address').placeholder = "Start typing...";
    }
    else{
        // console.log('place name=>', place.name)
    }

    // get the address components and assign them to the fields
    // console.log(place);
    var geocoder = new google.maps.Geocoder()
    var address = document.getElementById('id_address').value

    geocoder.geocode({'address': address}, function(results, status){
        // console.log('results=>', results)
        // console.log('status=>', status)
        if(status === google.maps.GeocoderStatus.OK){
            var latitude = results[0].geometry.location.lat();
            var longitude = results[0].geometry.location.lng();

            // console.log('lat=>', latitude);
            // console.log('long=>', longitude);
            $('#id_latitude').val(latitude);
            $('#id_longitude').val(longitude);

            $('#id_address').val(address);
        }
    });

    // loop through the address components and assign other address data
    console.log(place.address_components);
    for(const element of place.address_components) {
        for (var j = 0; j < element.types.length; j++) {
            // get country
            if (element.types[j] === 'country') {
                $('#id_country').val(element.long_name);
            }
            // get state
            if (element.types[j] === 'administrative_area_level_1') {
                $('#id_state').val(element.long_name);
            }
            // get city
            if (element.types[j] === 'locality') {
                $('#id_city').val(element.long_name);
            }
            // get pincode
            if (element.types[j] === 'postal_code') {
                $('#id_pin_code').val(element.long_name);
            }else{
                $('#id_pin_code').val("");
            }
        }
    }
}