"""
This program will read in a spectral data file and plot the spectrum. 
It will also compute data such as the peak wavelength, star temperature, star type, star color, star luminosity, and star radius. 
The program will then plot the spectrum and display the computed data.

"""

# Import the necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy
import astropy
from astropy.modeling import models, fitting

#Define the File Name
fileName = 'sunSpectrum.csv'

#Planck's constant
b = 2.8977721e-3

#Stephan-Boltzmann constant
sigma = 5.670367e-8

# Define the wavelength range to plot for hydrogen alpha
wmin, wmax = 6563-10, 6563+10

# Define the minimum and maximum wavelength of the spectrum
minWavelength = 0
maxWavelength = 0

def getMinWavelength(df):
    # Find the minimum wavelength of the spectrum
    minWavelength = df['wavelength'].min()
    minWavelength  = float(minWavelength)
    return minWavelength

def getMaxWavelength(df):
    # Find the maximum wavelength of the spectrum
    maxWavelength = df['wavelength'].max()
    maxWavelength = float(maxWavelength)
    return maxWavelength

def getStarTemp(peakWavelength):
    # Determine the star temperature based on the peak wavelength

    # Convert the peak wavelength from nanometers to meters
    convertedPeakWavelength = peakWavelength * 1e-9

    # Compute the star temperature using Planck's law
    T = b/convertedPeakWavelength
    T_rounded = round(T, 1)
    return T_rounded

def getPeakWavelength(df):
    # Find the peak wavelength of the spectrum
    peakWavelength = df['wavelength'][df['flux'].idxmax()]
    return peakWavelength

def getStarType(starTemp):
    # Determine the star type based on the temperature
    if starTemp >30000:
        starType = 'O'
    elif starTemp >=20000:
        starType = 'B'
    elif starTemp >=10000:
        starType = 'A'
    elif starTemp >=7000:
        starType = 'F'
    elif starTemp >=6000:
        starType = 'G'
    elif starTemp >=5000:
        starType = 'K'
    else:
        starTemp = 'M'
    return starType

def getStarColor(starType):
    # Determine the star color based on the star type
    if starType == 'O':
        starColor = 'Blue'
    elif starType == 'B':
        starColor = 'Blue-White'
    elif starType == 'A':
        starColor = 'White'
    elif starType == 'F':
        starColor = 'Yellow-White'
    elif starType == 'G':
        starColor = 'Yellow'
    elif starType == 'K':
        starColor = 'Orange'
    else:
        starColor = 'Red'
    return starColor

def getStarLuminosity(starTemp):
    # Determine the star luminosity based on the star temperature
    # Not yet implemented
    starLuminosity = 0
    return starLuminosity

def getStarRadius(starTemp):
    # Determine the star radius based on the star temperature
    # Not yet implemented
    starRadius = 0
    return starRadius

# Load the spectral data into a DataFrame
def loadSpectrum():
    df = pd.read_csv(fileName, sep=',', engine='python')
    return df 

def normalizeSpectrum(df):
    # Normalize the flux values
    df['flux'] = df['flux'] / df['flux'].max()
    return df

def standardizeSpectrum(df):
    # Standardize the flux values
    df['flux'] = df['flux'] / df['flux'].std()
    return df

def plotSpectrum(df):
    # Plot the spectrum
    plt.plot(df['wavelength'], df['flux'])
    plt.style.use('bmh') 

    plt.xlabel('Wavelength (nm)', fontsize = 20)
    plt.ylabel('Relative Intensity', fontsize = 20)
    plt.title('Solar Spectrum 12/21/22', fontsize = 40)
    plt.xticks([325,350,375,400,425,450,475,500,525,550,575,600,625,650,675,700,725,750,775,800,825,850,875,900])

    x = numpy.arange(0, maxWavelength, 10)
    # Plot the standardized spectrum
    #plt.plot(df['wavelength'], df['flux'])
    plt.annotate('Peak Wavelength: ' + str(peakWavelength) + " nm", xy=(peakWavelength, 0.25), xytext=(peakWavelength, 0.25), fontsize = 20)
    plt.annotate('Star Temperature: ' + str(starTemp) + " Kelvin", xy=(peakWavelength, 0.2), xytext=(peakWavelength, 0.2), fontsize = 20)
    plt.annotate('Star Type: ' + starType, xy=(peakWavelength, 0.15), xytext=(peakWavelength, 0.15), fontsize = 20)
    plt.annotate('Star Color: ' + starColor, xy=(peakWavelength, 0.1), xytext=(peakWavelength, 0.1), fontsize = 20)
    plt.annotate('Star Radius: ' + str(starRadius) + " km", xy=(peakWavelength, 0.05), xytext=(peakWavelength, 0.05), fontsize = 20)


def hAlphaGauss(df):
    # Fit a Gaussian to the H-alpha line
    # Not yet implemented
    mask = (df['wavelength'] > wmin) & (df['wavelength'] < wmax)
    wavelengthRange = df.wavelength[mask]
    fluxRange = df.flux[mask]

    gauss = models.Gaussian1D( 1, 656.28, 1)
    gauss.fit_deriv(wavelengthRange, fluxRange)
    # fitted_gauss = fitting(gauss,wavelengthRange, fluxRange)
    print(gauss.fwhm)
    plt.plot(wavelengthRange, gauss(wavelengthRange), label='Gaussian Fit')


def wholeSpectrumGauss(df):
    # Fit a Gaussian to the whole spectrum
    # Not yet implemented
    gauss = models.Gaussian1D( 1, peakWavelength, 1)
    fitted_gauss =fitting.LevMarLSQFitter()
    g = fitted_gauss(gauss, df['wavelength'], df['flux'])
    # gauss.fit_deriv(df['wavelength'], df['flux'], stddev=1, mean=656.28)
    print("FWHM: "+ str(gauss.fwhm))
    plt.plot(df['wavelength'], g, label='Gaussian Fit')

def annotateElements():
    # Annotate the elements
    plt.annotate('H α', xy=(656.3,0.2), xytext = (650,0.1))
    plt.axvline(x=656.3, color='DimGray', linestyle='--', linewidth=0.9)
    plt.annotate('Ca II', xy=(396.8,0.15), xytext = (400,0.05))
    plt.axvline(x=396.8, color='DimGray', linestyle='--', linewidth=0.9)
    plt.annotate('Na I', xy=(589.6,0.4), xytext = (589.6,0.2))
    plt.axvline(x=589.6, color='DimGray', linestyle='--', linewidth=0.9)
    plt.annotate('Ca II', xy=(393.4,0.15), xytext = (375,0.01))
    plt.axvline(x=393.4, color='DimGray', linestyle='--', linewidth=0.9)
    plt.annotate('H ß', xy=(486.1,0.63), xytext = (486,0.45))
    plt.axvline(x=486.1, color='DimGray', linestyle='--', linewidth=0.9)
    plt.annotate('O (terrestrial)', xy=(759.4,0.1), xytext = (760,0.3))
    plt.axvline(x=759.4, color='DimGray', linestyle='--', linewidth=0.9)
    plt.annotate('O (terrestrial)', xy=(686.7,0.28), xytext = (687,0.45))
    plt.axvline(x=686.7, color='DimGray', linestyle='--', linewidth=0.9)

#Main Loop
df = loadSpectrum()

peakWavelength = getPeakWavelength(df)
print('Peak Wavelength: ' + str(peakWavelength))

starTemp = getStarTemp(peakWavelength)
print('Star Temperature: ' + str(starTemp))

starType = getStarType(starTemp)
print('Star Type: ' + starType)

starColor = getStarColor(starType)
print('Star Color: ' + starColor)

starRadius = getStarRadius(starTemp)
print('Star Radius: ' + str(starRadius))

plotSpectrum(df)

annotateElements()

#hAlphaGauss(df)

#wholeSpectrumGauss(df)

plt.show()

# Shift the wavelengths (optional)
#df['wavelength'] = df['wavelength'] - df['wavelength'].min()


# Get the peak wavelength of the spectrum

