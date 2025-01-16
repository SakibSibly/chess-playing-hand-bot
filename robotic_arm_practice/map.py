from math import fabs
import new_chess_play
class Arm:
    def __init__(self, chessboard):
        a,b,c                 = 30,10,20
        self.initial_position = [a,b,c]
        self.current_position = self.initial_position
        self.chessMap         = chessboard
        pass

    def lift(self):
        # print("assume lifted")
        self.current_position = self.initial_position # Needs to be implemented this actually
        print("Lifted to initial",self.current_position)
        pass

    def move(self, move_string):
        source      = move_string[:2]
        destination = move_string[2:]

        self.goto(source)
        self.lift()
        self.goto(destination)

        return source, destination
    
    def goto(self,position):
        base_i, shoulder_i, farm_i = self.initial_position
        base,   shoulder,   farm   = self.chessMap[position]


        while base != base_i:
            base_i += 1     if base_i < base else -1

        while shoulder != shoulder_i:
            shoulder_i += 1 if shoulder_i < shoulder else -1
        
        while farm != farm_i:
            farm_i += 1     if farm_i < farm else -1

        self.current_position = (base_i, shoulder_i, farm_i) 

        print("Position",position,":",self.current_position)       


chessboard = {
              "e2" : [0, 0, 0],
              "e4" : [10, 0, 0]
             }

arm = Arm(chessboard)
arm.move(new_chess_play.main())