# Air Quality Report (Draft Version)

get_all_info `https://airquality.zeqa.net/get_all_info`
```
[{"datetime":"2023-02-09T22:50:53.115000","temperature":26,"humidity":70,"CO":4.99},...]

```

endpoint `https://airquality.zeqa.net/color`

body
```
{
    "temperature" : 26,
    "humidity" : 70,
    "co" : 4.99
}
```

response
```
{
    "temperature_R": 0,
    "temperature_G": 255,
    "temperature_B": 0,
    "humidity_R": 86,
    "humidity_G": 105,
    "humidity_B": 177,
    "CO_R": 0,
    "CO_G": 255,
    "CO_B": 0
}
```

## color range reference

temperature (from cold to very hot)

![](img/2.png)

humidity

![](img/1.png)

CO (from good to worst)

![](img/3.png)

