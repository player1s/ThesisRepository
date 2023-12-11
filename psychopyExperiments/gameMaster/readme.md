Gigantic game experiment!!44!!

dont forget to modify: 
    
    pvt length in total
    
    pvt amount of trials
    
    maths amount of trials
    
    maths overall length
    
    tetris overall time
    
    tetris time until break
    
    tetris amount of breaks
    
    snake overall time
    
    snake time until break
    
    snake amount of breaks
    
    
    The structure: self eval, baseline, pvt, maths, tetris, pvt, maths, snake, pvt, maths, self eval
    
    TODO: add events
    
    events and saved data (the ones with number are an event injected into the lsl stream. The ones without a number is a value(s) saved ): 
        
        - 1: startBaseline
- 2: startPvt
    - 3: pvt itemAppears
    - reaction time
- 4: startMaths
    - 5: correct answer
    - amount of submitted answers
    - amount of correct answers
- 6: startTetris
    - 7: tetrisFail
    - 8: tetrisLvlUp
    - total score
    - total fail amount
- 9: startSnake
    - 10: snakeFail
    - 11: snakeLvlUp
    - total score
    - total fail amount