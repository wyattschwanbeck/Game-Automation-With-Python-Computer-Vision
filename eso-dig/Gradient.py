def Gradient(percentSure):
        #Takes percent sure, calculates the respective gradient from
        # Red -> Orange -> Yellow -> Green
        red_min = 0.0 
        orange_min = .33
        yellow_min = .66
        green_min = 1
        red = [255,0,0]
        orange = [255, 127, 0]
        yellow = [255,255,0]
        green = [0,255,0]
        if(percentSure<=orange_min):
            R = 255
            G= ((orange_min-percentSure)/(orange_min-red_min) * (orange[1]-red[1]))+red[1]
            B = 0
            
        elif(percentSure<yellow_min):
            R=255
            G = 255
            B = ((yellow_min-percentSure)/(yellow_min-orange_min) * (yellow[2]-orange[2]))+orange[2]
        elif(percentSure<green_min):
            R = ((green_min-percentSure)/(green_min-yellow_min) * (green[0]-yellow[0]))+yellow[0]
            G= 255
            B = 0
        return  "#%02x%02x%02x" % (R, G, B)   

