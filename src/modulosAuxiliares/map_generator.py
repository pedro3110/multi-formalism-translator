import random
from scipy import misc


class map_generator(object):

    def __init__(self, dim, img_src_file):
        self.img_src_file = img_src_file
        self.dim = dim

    def generate(self):
        street_map = self.get_street_map(self.img_src_file)

        coords = [[0 for j in range(street_map.shape[1])] for i in range(street_map.shape[0])]
        for i in range(street_map.shape[0]):
            for j in range(street_map.shape[1]):
                coords[i][j] = self.pixel_to_number(street_map[i][j])

        # Save 
        ans = []
        for i in range(street_map.shape[0]):
            for j in range(street_map.shape[1]):
                row = '(' + str(i) + ',' + str(j) + ',0)=' + str(coords[i][j]) + '\n'
                ans.append(row)
        for i in range(street_map.shape[0]):
            for j in range(street_map.shape[1]):
                row = '(' + str(i) + ',' + str(j) + ',1)=' + str(random.randint(1,4)) + '\n'
                ans.append(row)
        return ans

    # Get street map
    def get_street_map(self, img_file):
        lim = 250

        street_map = misc.imread(img_file)
        street_map = misc.imresize(street_map, (self.dim[0], self.dim[1]))

        street_map[street_map < lim] = 0
        street_map[street_map >= lim] = 255

        # print 'Street map resized to shape = ' + str(street_map.shape)

        return street_map

    # Aux functions
    def pixel_to_number(self, pixel):
        if list(pixel) == [0,0,0]:
            return 0
        return 1