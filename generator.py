import sys, pygame, random
pygame.init()

#Define game area
size = width, height = 500,500
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)
screen.fill((0,0,0))

#debug mode
i_have_no_idea_what_im_doing = True

#Set the terrain pixel size
terrainSize = 5

#terrain = {'DEEP_OCEAN',
#           'SHALLOW_OCEAN',
#           'SHALLOW_WATER',
#           'SAND',
#           'GRASS',
#           'HILL',
#           'LOW_MOUNTAIN',
#           'HIGH_MOUNTAIN'}

terrain_val = {0:(0,0,128),     #DEEP_OCEAN
               1:(0,0,255),     #SHALLOW_OCEAN
               2:(163,163,255), #SHALLOW_WATER
               3:(255,229,148), #SAND
               4:(20,210,24),   #GRASS
               5:(14,140,17),   #HILL
               6:(162,162,162), #LOW_MOUNTAIN
               7:(220,220,220)} #HIGH_MOUNTAIN

threading = False

threaded_count = 0

class Generator:
    """
    Generate 2D terrain
    """
    
    #Can we draw terrain?
    #Sets false at the end of the screen
    canDraw = True
    done = False
    
    #Start location
    location = locationX, locationY = 0,0
    
    #Default terrain type
    tType = 0
    colorList = [[]]
    
    #Get a random terrain block to start
    next_terrain = random.choice(terrain_val.values())
    
    def __init__(self):
        self.generate()
        
    def generate(self):
        """
        The main generation loop.
        Handles setting up the next draw, as well as window events
        """
        while 1:
            if self.canDraw:
                
                if i_have_no_idea_what_im_doing:
                    print "Next terrain: ", self.next_terrain
                    
                if threading:
                    self.next_terrain = self.draw_terrain(self.next_terrain, threaded_count)
                    threaded_count += 1
                else:
                    self.next_terrain = self.draw_terrain(self.next_terrain)
            elif i_have_no_idea_what_im_doing and not self.canDraw and not self.done:
                print "All done captain!"
                self.done = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit();
            pygame.display.flip()
            
            #Set FPS
            #clock.tick(1)
    
    def next_color(self):
        
        """
        Get the next terrain color based on either the terrain above and/or to the left of the next tile
        """
        if i_have_no_idea_what_im_doing:
            print "Location Y: ", self.locationY, " Location X: ", self.locationX, " next: ", self.locationX, " , ", self.locationY - terrainSize + 1

        #Get the pixel value of the terrain block above the current location
        if self.locationY > 0 and self.locationY <= height:
            try:
                top_val = self.terrain_value(terrain_val, screen.get_at((self.locationX, self.locationY - terrainSize + 1)))
            except Exception,e:
                print e
                print "tPixels: ", self.locationX, ", ",self.locationY - terrainSize + 1
        #If there is no block above the current one, set to -1
        else:
            top_val = -1
            
        #Get the pixel to the left of the current block
        if self.locationX > 0 and self.locationX <= width:
            try:
                left_val = self.terrain_value(terrain_val, screen.get_at((self.locationX - terrainSize + 1, self.locationY)))
            except Exception,e:
                print e
                print "lPixels: ", self.locationX - terrainSize + 1, ", ",self.locationY
        #If there is no block to the left, set value to -1
        else:
            left_val = -1
        
        if i_have_no_idea_what_im_doing:
            print "Top: ",top_val, " Left:", left_val
        
        """
        This is an attempt at adding "weight" to the terrain
        
        What this does is takes the weight value and adds the terrain to the left into an array that amount of times.
        In theory this will make the weighted value roughly the percentage chance of generating the left terrain again.
        
        Example: the weight is set to 6 the terrain to the, which you would set if you want the terrain left of the current
                 position to be generated roughly 60% of the time. This will loop through and add that terrain to an array 6 times
                 and with the target_weight set to 10, this would achieve roughly a 60% chance.
                 
        Once the array is loaded with possible terrain choices, a random terrain is selected using the random function and a terrain value
        is chosen.
        """
        
        #the rough amount of terrains you want in the array
        target_weights = 10
        
        #If there is no top terrain value, should only be the case when in the topmost row
        if top_val == -1:
            weight = 6
            ran_list = []
            while target_weights > 0: 
                while weight > 0:
                    ran_list.append(left_val)
                    weight -= 1
                    target_weights -= 1
                if left_val < 7:
                    ran_list.append(left_val+1)
                    target_weights -= 1
                if left_val > 0:
                    ran_list.append(left_val-1)
                    target_weights -= 1
            return terrain_val[random.choice(ran_list)]
        
        #If there is no left value, should only be the case in the first column
        elif left_val == -1:
            weight = 6
            ran_list = []
            while target_weights > 0: 
                while weight > 0:
                    ran_list.append(top_val)
                    weight -= 1
                    target_weights -= 1
                if top_val < 7:    
                    ran_list.append(top_val+1)
                    target_weights -= 1
                if top_val > 0:
                    ran_list.append(top_val-1)
                    target_weights -= 1
            return terrain_val[random.choice(ran_list)]
        
        #If the top terrain and the left terrain are the same terrain
        if top_val == left_val:
            #higher weight here... seems logical
            weight = 8
            ran_list = []
            while target_weights > 0: 
                while weight > 0:
                    ran_list.append(top_val)
                    weight -= 1
                    target_weights -= 1
                if top_val < 7:    
                    ran_list.append(top_val+1)
                    target_weights -= 1
                if top_val > 0:
                    ran_list.append(top_val-1)
                    target_weights -= 1
            return terrain_val[random.choice(ran_list)]
        
        #If there is a top and left terrain and they are not the same
        else:
            
            #What's the difference in height between the two terrains?
            #We want the possibility of any terrain between the two to have the cahnce
            #to appear here
            difference = abs(top_val - left_val)
            
            #we want more weights for this since it's a bit more complicated
            target_weights = 100
            
            if i_have_no_idea_what_im_doing:
                print "zTop: ",top_val," Left: ",left_val
            
            #we want the weight to be higher if the top and left terrains are closer in
            #toporaphy, but less if they are more different in topography.
            #
            #The theory behind this is that if the top terrain is ocean and the left terrain is
            #mountain, you're more likely to get someting between the two to create a 'smoother'
            #overall terrain
            
            weight = ((7/difference) * (.7*target_weights))/2 #gives up to an 80% chance that the terrain will
                                                              #be either the top of left terrain (when they are one
                                                              #value away from one another)
            
            if i_have_no_idea_what_im_doing:
                print "Weight: ", weight
                
            ran_list = []
            #set large_val to the largest of left_val and top_val
            large_val = top_val if top_val > left_val else left_val
            while target_weights > 0: 
                while weight > 0:
                    ran_list.append(top_val)
                    ran_list.append(left_val)
                    weight -= 1
                    target_weights -= 2
                while difference > 0:
                    #Get the terrain value that's one less than the large value
                    #This loop will add every value of terrain down to the lower value of either top_val or left_val
                    if large_val > 0:
                        large_val = large_val - 1
                    ran_list.append(large_val)
                    difference -= 1
                    target_weights -= 1
                if top_val < 7:    
                    ran_list.append(top_val+1)
                    target_weights -= 1
                if top_val > 0:
                    ran_list.append(top_val-1)
                    target_weights -= 1
            return terrain_val[random.choice(ran_list)]
        
    def terrain_value(self, dic, val):
        """Return the key of dictionary given the value"""
        try:
            return [k for k, v in dic.iteritems() if v == val][0]
        except IndexError, e:
            print e
    
    def next_location(self):
        
        """
        Set the location to the next block, then get the color for this block
        """
        
        self.location = self.locationX, self.locationY = self.locationX,self.locationY + terrainSize
        
        #If we went below the screen, go back to the top
        if self.locationY >= height:
            self.locationX = self.locationX + terrainSize
            self.locationY = 0
            
        #If we went off the side of the screen, stop drawing terrain
        if self.locationX >= width:
            self.canDraw = False
        return self.next_color()

    
    def draw_terrain(self, tType):
        """
        Draw the next block to the screen
        """
        pygame.draw.rect(screen, tType, (self.locationX, self.locationY, terrainSize, terrainSize))
        return self.next_location()
        
if __name__ == "__main__" :
    #GENERATE!
    Generator()
    
    
    
    
    
    
    