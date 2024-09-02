import pygame
import random as r
import speech_recognition as sr
pygame.init()
 
clock = pygame.time.Clock()
screen_width = 900
screen_height = 600
 #creating window
window = pygame.display.set_mode((screen_width,screen_height))

# initializing colours with rgb values this ranges from 255 to 0
white = (255,255,255)
red = (255,0,0)
black = (0,0,0)
   
#creating caption
pygame.display.set_caption("Mounika (snake) Game")
pygame.display.update()
 

#used to take commands from user and convert it to txt
def takeCommand():
    # r = sr.Recognizer()
    # with sr.Microphone() as source:
    #     print("Listening.....")
    #     r.pause_threshold = 1
    #     r.energy_threshold = 300
    #     audio = r.listen(source,0,4)

    # try:
    #     print("Understanding..")
    #     query=sr.recognize_google(audio,language='en-in')
    #     print(f"You Said: {query}\n")
    # except Exception as e:
    #     print("Say that again")
    #     return "None"

            r = sr.Recognizer()
            m = sr.Microphone()

            try:
                print("A moment of silence, please...")
                with m as source: r.adjust_for_ambient_noise(source)
                print("Set minimum energy threshold to {}".format(r.energy_threshold))
                while True:
                    print("Say something!")
                    with m as source: audio = r.listen(source)
                    print("Got it! Now to recognize it...")
                    try:
                        # recognize speech using Google Speech Recognition
                        value = r.recognize_google(audio)

                        print("You said {}".format(value))
                    except sr.UnknownValueError:
                        print("Oops! Didn't catch that")
                    except sr.RequestError as e:
                        print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
            
            except KeyboardInterrupt:
                   pass    

            return value

 # to increase the length of snake
def  plot_snake(window,color,snk_list,snake_size ) :
    for x,y in snk_list :
       pygame.draw.rect(window,color,[x,y,snake_size,snake_size])
#in this we are using list to build the rectangles as the for loop iterate 
# using x,y we get new co-ordinates and using it we build rectangle
 
font = pygame.font.SysFont(None,55)
#screen score
def txt_screen(txt,color,x,y) :
    screen_txt = font.render(txt,True,color)
    window.blit(screen_txt,[x,y])

# home screen function 
def home() :
    exit_game = False
    while not exit_game :
        window.fill("purple")
        txt_screen("Mounika (snakes) game  ",black,230,220)
        txt_screen ("Press space to enter ", black, 250 ,260)
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                exit_game = True
            if  event.type == pygame.KEYDOWN :
                if event.key == pygame.K_SPACE :
                    game_loop()
        pygame.display.update() #it is used to update the screen if u not use this after making changes then changes won't reflect
        clock.tick(30) #it generates the frames per second according to your requirements




def game_loop() :
    

    # specific variables
    exit_game = False
    game_over = False
    init_velocity = 10
    snake_x = 45
    snake_y =55
    snake_size = 30
    velocity_x = 0
    velocity_y = 0
    fps = 30 
    food_x = r.randint(20,450)
    food_y = r.randint(20,300)
    food_size = 30
    score = 0
   
    
    snk_list = []
    snk_length = 1

    #game loop
    while not exit_game :
        query = takeCommand()
        #using snake_hiscore.txt file to store high score
        with open("snake_hiscore.txt","r") as f :
            hiscore = f.read()

        if game_over :

            with open("snake_hiscore.txt","w") as f :
                 f.write(str(hiscore))

            window.fill(white)
            txt_screen("Game over....! Press Enter to continue",red , screen_width /2 - 350 , screen_height/2 - 100)
#This is to end the game if game_over is true and display the message
            
            for event in pygame.event.get() :
                    
                if event.type == pygame.QUIT:
                    exit_game = True 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN :
                        home()
        else :


                for event in pygame.event.get() :
                    
                    if event.type == pygame.QUIT:
                        exit_game = True 
                    

                    if "right" in query :
                        
                            velocity_x = init_velocity
                            velocity_y = 0
                            #it increments the x position as we press right arrow
                    if "left" in query :
                            velocity_x =  -init_velocity
                            velocity_y = 0
                            #it decrements the x position as we press right arrow
                    if "up" in query :
                            velocity_y = - init_velocity
                            velocity_x = 0                    
                            #it decrements the y position as we press right arrow 
                    if "down " in query:
                            velocity_y = init_velocity
                            velocity_x = 0


                        #it increments the y position as we press right arrow
                snake_x += velocity_x
                snake_y += velocity_y
                
                if abs(snake_x - food_x) < 6 and abs(snake_y - food_y) < 6 :
                    score += 10  
                    food_x = r.randint(20,450)
                    food_y = r.randint(20,300)
                    snk_length += 5
                    if score >= int(hiscore) :
                        hiscore = score
                window.fill(white)
                txt_screen("score :" +str(score)+ "High Score:" + str(hiscore),red,5,5)
                #food ploting 
                pygame.draw.rect(window,red,[food_x,food_y,food_size,food_size])

                head = []
                head.append(snake_x)
                head.append(snake_y)
                snk_list.append(head)
                
                if len(snk_list) > snk_length :
                    del snk_list[0]
                    #to control the length of snake 
                
                # It is for is snake bites itself then the game_over = true
                if head in snk_list[ : -1] :
                    game_over = True

                if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height :
                    game_over = True
                    #this is to end the game if the snake touches boundaries

                # it draws the shape or snake 1st argument is where to draw and 2nd color 3rd its location on screen
                plot_snake(window, black,snk_list,snake_size)
        pygame.display.update() #it is used to update the screen if u not use this after making changes then changes won't reflect
        clock.tick(fps) #it generates the frames per second according to your requirements

    pygame.quit()
    quit()
home()






