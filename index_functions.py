
#%%

def ndvi(image, satelite):

# Defaults to Landsat 8 

# Landsat 4-7, NDVI = (Band 4 – Band 3) / (Band 4 + Band 3)
# Landsat 8, NDVI = (Band 5 – Band 4) / (Band 5 + Band 4)

    if satelite == 'Landsat 8': 
        red = image[3]
    elif satelite == 'Landsat 4-7':
        red = image[2]
    else:
        red = image[3]

    if satelite == 'Landsat 8': 
        nir = image[4]
    elif satelite == 'Landsat 4-7':
        nir = image[3]
    else:
        nir = image[4]

    NDVI = (nir - red) / (nir + red)

    return NDVI 


def evi(image, satelite):

# Defaults to Landsat 8 

# EVI = G * ((NIR - R) / (NIR + C1 * R – C2 * B + L))
# Landsat 4-7, EVI = 2.5 * ((Band 4 – Band 3) / (Band 4 + 6 * Band 3 – 7.5 * Band 1 + 1))
# Landsat 8, EVI = 2.5 * ((Band 5 – Band 4) / (Band 5 + 6 * Band 4 – 7.5 * Band 2 + 1))

    if satelite == 'Landsat 8': 
        red = image[3]
    elif satelite == 'Landsat 4-7':
        red = image[2]
    else:
        red = image[3]

    if satelite == 'Landsat 8': 
        nir = image[4]
    elif satelite == 'Landsat 4-7':
        nir = image[3]
    else:
        nir = image[4]

    if satelite == 'Landsat 8': 
        blue = image[1]
    elif satelite == 'Landsat 4-7':
        blue = image[0]
    else:
        blue = image[1]

    G = 2.5 
    L = 1
    C1 = 6
    C2 = 7.5

    EVI = G * ((nir - red) / (nir + C1 * red - C2 * blue +L))

    return EVI



#%% EVI 2 Fucnction
 
def evi2(image, satelite):
 
# Defaults to Landsat 8 

# EVI2 = G * ((NIR - R) / (NIR + C1 * R + L))
# Landsat 4-7, EVI = 2.5 * ((Band 4 – Band 3) / (Band 4 + 2.4 * Band 3 + 1))
# Landsat 8, EVI = 2.5 * ((Band 5 – Band 4) / (Band 5 + 2.4 * Band 4 + 1))

    if satelite == 'Landsat 8': 
        red = image[3]
    elif satelite == 'Landsat 4-7':
        red = image[2]
    else:
        red = image[3]

    if satelite == 'Landsat 8': 
        nir = image[4]
    elif satelite == 'Landsat 4-7':
        nir = image[3]
    else:
        nir = image[4]

    G = 2.5
    C1 = 2.4
    L = 1 
 
    EVI2 = G * ((nir - red) / (nir + C1 * red + L))
 
    return(EVI2)


def gndvi(image, satelite):

# Defaults to Landsat 8 

# Landsat 4-7, NDVI = (Band 4 – Band 2) / (Band 4 + Band 2)
# Landsat 8, NDVI = (Band 5 – Band 3) / (Band 5 + Band 3)

    if satelite == 'Landsat 8': 
        nir = image[4]
    elif satelite == 'Landsat 4-7':
        nir = image[3]
    else:
        nir = image[4]

    if satelite == 'Landsat 8': 
        green = image[2]
    elif satelite == 'Landsat 4-7':
        green = image[1]
    else:
        green = image[2]

    GNDVI = (nir - green) / (nir + green)

    return GNDVI 


def avi(image, satelite):

# Defaults to Landsat 8 

# Landsat 4-7, NDVI = (Band 4 * (1 – Band 3) * (Band 4 - Band 3) ^ (1/3)
# Landsat 8, NDVI = (Band 5 * (1 – Band 4) * (Band 5 - Band 4) ^ (1/3)

    if satelite == 'Landsat 8': 
        red = image[3]
    elif satelite == 'Landsat 4-7':
        red = image[2]
    else:
        red = image[3]

    if satelite == 'Landsat 8': 
        nir = image[4]
    elif satelite == 'Landsat 4-7':
        nir = image[3]
    else:
        nir = image[4]

    AVI = [nir * (1 - red) * (nir - red)] ^ (1/3)

    return AVI 


def savi(image, satelite):

# Defaults to Landsat 8 

# Landsat 4-7, NDVI = ((Band 4 – Band 3) / (Band 4 + Band 3)) * (1-L)
# Landsat 8, NDVI = ((Band 5 – Band 4) / (Band 5 + Band 4)) * (1-L)

    if satelite == 'Landsat 8': 
        red = image[3]
    elif satelite == 'Landsat 4-7':
        red = image[2]
    else:
        red = image[3]

    if satelite == 'Landsat 8': 
        nir = image[4]
    elif satelite == 'Landsat 4-7':
        nir = image[3]
    else:
        nir = image[4]

    L = 0.5

    SAVI = ((nir - red) / (nir + red + L)) * (1+L)

    return SAVI

def ndmi(image, satelite):

# Defaults to Landsat 8 

# Landsat 4-7, NDVI = (Band 4 – Band 5) / (Band 4 + Band 5)
# Landsat 8, NDVI = (Band 5 – Band 6) / (Band 5 + Band 6)

    if satelite == 'Landsat 8': 
        swir = image[5]
    elif satelite == 'Landsat 4-7':
        swir = image[4]
    else:
        swir = image[5]

    if satelite == 'Landsat 8': 
        nir = image[4]
    elif satelite == 'Landsat 4-7':
        nir = image[3]
    else:
        nir = image[4]

    NDVI = (nir - swir) / (nir + swir)

    return NDVI 


