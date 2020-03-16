class Solution:
    def judgeCircle(self, moves: str) -> bool:
        num_U=moves.count('U')
        num_D=moves.count('D')
        if(num_U !=num_D):
            return False
        num_L=moves.count('L')
        num_R=moves.count('R')
        if(num_L !=num_R):
            return False
        return True