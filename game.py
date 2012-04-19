import sys, pygame, random
pygame.init()

size = width, height = 500,500
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)

terrainSize = 2

screen.fill((0,0,0))

terrain = {'DEEP_OCEAN',
           'SHALLOW_OCEAN',
           'SHALLOW_WATER',
           'SAND',
           'GRASS',
           'HILL',
           'LOW_MOUNTAIN',
           'HIGH_MOUNTAIN'}

terrain_val = {0:(0,0,128),
               1:(0,0,255),
               2:(163,163,255),
               3:(255,229,148),
               4:(20,210,24),
               5:(14,140,17),
               6:(162,162,162),
               7:(220,220,220)}


class Generator:
    
    canDraw = True
    location = locationX, locationY = 0,0
    tType = 0
    colorList = [[]]
    next_terrain = random.choice(terrain_val.values())
    
    def __init__(self):
        self.generate()
    
    def generate(self):
        while 1:
            if self.canDraw:
                #self.tType = random.choice(terrain_val.values())
                print "Next terrain: ", self.next_terrain
                self.next_terrain = self.draw_terrain(self.next_terrain)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit();
            #self.color()
            pygame.display.flip()
            #clock.tick(1)
    
    def next_color(self):
        
        print "Location Y: ", self.locationY, " Location X: ", self.locationX, " next: ", self.locationX, " , ", self.locationY - terrainSize + 1
        #if self.locationX >= terrainSize:
        #    lpix = screen.get_at((self.locationX - terrainSize + 1, self.locationY))
        #else:
        #    lpix = -1
        #print "Pixel at ", self.locationX,", ", self.locationY - terrainSize + 1,": ", screen.get_at((self.locationX, self.locationY - terrainSize + 1)), " and pixel: ", lpix
        
        if self.locationY > 0 and self.locationY <= height:
            try:
                top_val = self.terrain_value(terrain_val, screen.get_at((self.locationX, self.locationY - terrainSize + 1)))
            except Exception,e:
                print e
                print "tPixels: ", self.locationX, ", ",self.locationY - terrainSize + 1
                
        else:
            top_val = -1
        if self.locationX > 0 and self.locationX <= width:
            try:
                left_val = self.terrain_value(terrain_val, screen.get_at((self.locationX - terrainSize + 1, self.locationY)))
            except Exception,e:
                print e
                print "lPixels: ", self.locationX - terrainSize + 1, ", ",self.locationY
        else:
            left_val = -1
        
        print "Top: ",top_val, " Left:", left_val
        
        if top_val == -1:
            weight = 8
            ran_list = []
            while weight > 0:
                ran_list.append(left_val)
                weight -= 1
            if left_val < 7:
                ran_list.append(left_val+1)
            if left_val > 0:
                ran_list.append(left_val-1)
            return terrain_val[random.choice(ran_list)]
        elif left_val == -1:
            weight = 8
            ran_list = []
            while weight > 0:
                ran_list.append(top_val)
                weight -= 1
            if top_val < 7:    
                ran_list.append(top_val+1)
            if top_val > 0:
                ran_list.append(top_val-1)
            return terrain_val[random.choice(ran_list)]
            
        if top_val == left_val:
            weight = 8
            ran_list = []
            while weight > 0:
                ran_list.append(top_val)
                weight -= 1
            if top_val < 7:    
                ran_list.append(top_val+1)
            if top_val > 0:
                ran_list.append(top_val-1)
            return terrain_val[random.choice(ran_list)]
        else:
            difference = abs(top_val - left_val)
            print "zTop: ",top_val," Left: ",left_val
            weight = difference % 3
            print "Weight: ", weight
            ran_list = []
            while weight > 0:
                ran_list.append(top_val)
                ran_list.append(left_val)
                weight -= 1
            if difference < 0:
                difference = -difference
            while difference > 0:
                if top_val > 0:
                    top_val = top_val - 1
                ran_list.append(top_val)
                difference -= difference
            return terrain_val[random.choice(ran_list)]
        
    def terrain_value(self, dic, val):
        """return the key of dictionary dic given the value"""
        try:
            return [k for k, v in dic.iteritems() if v == val][0]
        except IndexError, e:
            print e
    
    def next_location(self):
        
        self.location = self.locationX, self.locationY = self.locationX,self.locationY + terrainSize
        
        if self.locationY >= height:
            self.locationX = self.locationX + terrainSize
            self.locationY = 0
            
        if self.locationX >= width:
            self.canDraw = False
        return self.next_color()
    #def storeLocation(self,tType):
    #    self.colorList[self.locationX][self.locationY] = tType
    
    def draw_terrain(self, tType):
        pygame.draw.rect(screen, tType, (self.locationX, self.locationY, terrainSize, terrainSize))
        #self.storeLocation(tType)
        return self.next_location()
        
if __name__ == "__main__" :
    Generator()
    
    
    
    
    
    
    