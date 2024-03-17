## GEOCODE helper functions

refer to [geopy docs](https://geopy.readthedocs.io/en/stable/#nominatim)

Instantiate geocode object - if error consider changing user-agent
```
    from geocode import geocode

    geocode_object = geocode(user-agent = 'regex')
```

Run with asyncio
```
    import asyncio

    //forwards takes in address(str), returns coordinates
    coords = asyncio.run(geocode_object.forward("upper thomson road"))

    //forwards takes in coordinate(str), returns address
    location = asyncio.run(geocode_object.reverse("1.356520, 103.829805"))

    print(coords)
    // -37.7274611, 146.2244904
    print(location)
    // Upper Thomson Road, Sin Ming, Bishan, Singapore, Central, 571448, Singapore
```

Looping
```
    coords_list = ["1.356520, 103.829805","1.354520, 103.829805","1.356530, 103.829805","1.336520, 103.429805"]    
    for coords in coords_list:
        address = asyncio.run(geocode_object.reverse(coords))
        print(address)
```

