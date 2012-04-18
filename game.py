import sys, pygame, random
pygame.init()

size = width, height = 500,500
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)

screen.fill((0,0,0))

terrain = {'DEEP_OCEAN':(0,0,128),
           'SHALLOW_OCEAN':(0,0,255),
           'SHALLOW_WATER':(163,163,255),
           'SAND':(255,229,148),
           'GRASS':(20,210,24),
           'HILL':(14,140,17),
           'LOW_MOUNTAIN':(162,162,162),
           'HIGH_MOUNTAIN':(220,220,220)}



class Generator:
    
    canDraw = True
    location = locationX, locationY = 0,0
    tType = 0
    
    def __init__(self):
        self.generate()
    
    def generate(self):
        while 1:
            if self.canDraw:
                self.tType = random.choice(terrain.values())
                self.drawTerrain(self.location, self.tType)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit();
            self.color()
            pygame.display.flip()
            #clock.tick(30)
    
    def color(self):
        surface = pygame.surfarray.pixel2d(screen)
        surface.get_at(0,0)
        del surface
    
    def nextLocation(self, location):
        self.location = self.locationX, self.locationY = self.locationX,self.locationY+10
        
        if self.locationY > height:
            self.locationX = self.locationX + 10
            self.locationY = 0
            
        if self.locationX > width:
            self.canDraw = False
    
    def drawTerrain(self, location, tType):
        pygame.draw.rect(screen, tType, (self.locationX, self.locationY, 10, 10))
        self.nextLocation(self.location)
        
if __name__ == "__main__" :
    Generator()
    
    
    
    
    
    
    