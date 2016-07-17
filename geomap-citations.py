
import sys
import operator

import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import matplotlib.patches as mpatches


def get_country_counts(txtinfile):
    """ Read input file which maps country to its frequency/count.
    """
    cite_count = {}
    with open(txtinfile) as inf:
        for line in inf:
            if line.startswith('#'):
                continue
            country, count = line.strip().split(',')
            cite_count[country] = int(count)

    return cite_count


def plot_world(txtinfile, pdfoutfile):
    """ Plot the cartopy map based on Robinson projection.
    """
    cite_count = get_country_counts(txtinfile)

    RED, YELLOW, GREEN, BLUE = '#FF4500', '#FFFF00', '#26B81C', '#0000FF'
    shapename = 'admin_0_countries'
    countries_shp = shpreader.natural_earth(resolution='110m',
                                            category='cultural',
                                            name=shapename)
    ax = plt.axes(projection=ccrs.Robinson())
    mapped_countries = set()

    for i, country in enumerate(shpreader.Reader(countries_shp).records()):
        country_name = country.attributes['name_long']
        if country_name not in cite_count:
            # Do not assign color to the country not in input file
            ax.add_geometries(country.geometry, ccrs.PlateCarree(), facecolor='none')
            continue

        mapped_countries.add(country_name)
        country_count = cite_count[country_name]
        if country_count > 50:
            gcolor = BLUE
        elif country_count > 10:
            gcolor = RED
        elif country_count > 5:
            gcolor = YELLOW
        else:
            gcolor = GREEN

        # Add the country to be colored
        ax.add_geometries(country.geometry, ccrs.PlateCarree(),
                          facecolor=gcolor)

    plt.title('Geographic distribution of citations')
    handles, labels = ax.get_legend_handles_labels()

    # Build legend
    ge50 = mpatches.Rectangle((0,0), 1, 1, facecolor=BLUE)
    label_ge50 = 'Citations > 50'
    ge25 = mpatches.Rectangle((0,0), 1, 1, facecolor=RED)
    label_ge25 = '10 < Citations <= 50'
    ge5 = mpatches.Rectangle((0,0), 1, 1, facecolor=YELLOW)
    label_ge5 = '5 < Citations <= 10'
    lt5 = mpatches.Rectangle((0,0), 1, 1, facecolor=GREEN)
    label_lt5 = 'Citations <= 5'
    handles = [ge50, ge25, ge5, lt5]
    labels = [label_ge50, label_ge25, label_ge5, label_lt5]

    # Fix the legend to <loc>
    ax.legend(handles, labels, loc='lower left', prop={'size': 8})
    ax.coastlines()
    plt.savefig(pdfoutfile)
    plt.close()
    return


def main(argv=sys.argv):
    if len(argv) != 3:
        print 'Usage: python %s txtinputfile pdfoutputfile' % (argv[0])
        return -1
    plot_world(argv[1], argv[2])
    return


if __name__ == '__main__':
    sys.exit(main())
