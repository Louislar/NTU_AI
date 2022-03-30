# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from operator import truediv
from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        score=0.0
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        oldFood = currentGameState.getFood()
        # 10 points for every food you eat 
        """
        Returns a Grid of boolean food indicator variables.

        Grids can be accessed via list notation, so to check
        if there is food at (x,y), just call

        currentFood = state.getFood()
        if currentFood[x][y] == True: ...
        """        
        newCapsule = successorGameState.getCapsules()
        # 200 points for every ghost you eat
        # but no point for capsule
        
        # For Ghost
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        # Position of ghost do not change regardless of your state 
        # because you can't predict the future
        ghostPositions = [ghostState.getPosition() for ghostState in newGhostStates]
        # Count down from 40 moves
        ghostStartPos = [ghostState.start.getPosition() for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"
        '''
        Define a function that will eat all the food up in the end, 
        add score if any food is closer. 
        Should use current state's food position to count the score. 
        '''
        # print(currentGameState.getPacmanPosition())
        # print(newPos)
        foodScore = 0.0
        newFoodList = newFood.asList()
        oldFoodList = oldFood.asList()
        numFood = len(oldFoodList)
        for _foodPos in oldFoodList: 
          _dis = util.manhattanDistance(newPos, _foodPos)
          # print(_foodPos)
          # print(_dis)
          if _dis == 0: 
            foodScore += 3.0
          else: 
            foodScore += 1.0/_dis
        # print(action)
        # print(foodScore)
        # print(successorGameState.getScore())
        '''
        Define a function that will escape from the ghosts, 
        decrease the score when ghost is getting closer. 
        (May be more important than eating food)
        '''
        numGhost = len(ghostPositions)
        ghostScore = 0.0
        for _ghostPos in ghostPositions: 
          _dis = util.manhattanDistance(newPos, _ghostPos)
          if _dis == 0:
            ghostScore += 3.5
          else: 
            ghostScore += 1.0/_dis
        ratio = float(numFood)/float(numGhost) if numGhost!=0 else 0
        return foodScore - ratio * ghostScore
        return successorGameState.getScore() #default scoure
        #please change the return score as the score you want

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        '''
        Maybe i can try to implement minmax by a stack, 
        also maybe a stack counting the depth is needed. 
        Or just implement by a recursive version maybe easiler?
        '''
        def minmaxExpand(startGameState): 
          '''
          return a action after minmax expanding and computing
          '''
          return maxMove(startGameState, 1)
        def maxMove(curGameState, curDepth): 
          '''
          Expand moves from the Pacman
          return a action with maximum value
          '''
          # return the eval val when the game is either win or lose
          if curGameState.isWin() or curGameState.isLose():
            return [[], self.evaluationFunction(curGameState)]
          # after max expand then do the min expand
          expandMoveAndValues = []
          legalMoves = curGameState.getLegalActions(0)
          for _aMove in legalMoves: 
            expandMoveAndValues.append(
              [_aMove, minMove(
                curGameState.generateSuccessor(0, _aMove), 
                curDepth, 
                1
              )[1]]
            )
          # print('max')
          # print(expandMoveAndValues)
          return max(expandMoveAndValues, key=lambda x: [i[1] for i in expandMoveAndValues if i[0]==x[0]][0])
        def minMove(curGameState, curDepth, ghostIdx): 
          '''
          Expand moves from all the ghosts
          return a action with minimum value
          '''
          # return the eval val when the game is either win or lose
          if curGameState.isWin() or curGameState.isLose():
            return [[], self.evaluationFunction(curGameState)]
          # 1. if ghost idx is not the last one, then expand to current ghost's moves, 
          # then move to next ghost moves, which is also a min expand
          if ghostIdx < (curGameState.getNumAgents()-1):
            expandMoveAndValues = []
            legalMoves = curGameState.getLegalActions(ghostIdx)
            for _aMove in legalMoves: 
              expandMoveAndValues.append(
                [_aMove, minMove(
                  curGameState.generateSuccessor(ghostIdx, _aMove), 
                  curDepth, 
                  ghostIdx+1
                )[1]]
              )
            # print('Expand min')
            # print(expandMoveAndValues)
            return min(expandMoveAndValues, key=lambda x: [i[1] for i in expandMoveAndValues if i[0]==x[0]][0])

          # 2. if ghost idx is the last one, 
          # but the desire depth is greater than current depth, 
          # then do another max expand
          if ghostIdx == (curGameState.getNumAgents()-1):
            if curDepth < self.depth: 
              expandMoveAndValues = []
              legalMoves = curGameState.getLegalActions(ghostIdx)
              for _aMove in legalMoves: 
                expandMoveAndValues.append(
                  [_aMove, maxMove(
                    curGameState.generateSuccessor(ghostIdx, _aMove), 
                    curDepth+1
                  )[1]]
                )
              # print('Expand max')
              # print(expandMoveAndValues)
              return min(expandMoveAndValues, key=lambda x: [i[1] for i in expandMoveAndValues if i[0]==x[0]][0])

          # 3. if ghost idx is the last one
          # and current depth is the desire depth, then return the min expand value
          if ghostIdx == (curGameState.getNumAgents()-1):
            if curDepth == self.depth: 
              expandMoveAndValues = []
              legalMoves = curGameState.getLegalActions(ghostIdx)
              for _aMove in legalMoves: 
                expandMoveAndValues.append(
                  [_aMove, self.evaluationFunction(curGameState.generateSuccessor(ghostIdx, _aMove))]
                )
              # print(curDepth)
              # print(curGameState.getPacmanPosition())
              # print(curGameState.getGhostStates()[ghostIdx-1].getPosition())
              # print(curGameState.getGhostStates()[ghostIdx-2].getPosition())
              # print(curGameState.getGhostStates()[ghostIdx-3].getPosition())
              # print(curGameState)
              # print(ghostIdx)
              # print(legalMoves)
              # print(expandMoveAndValues)
              return min(expandMoveAndValues, key=lambda x: [i[1] for i in expandMoveAndValues if i[0]==x[0]][0])
        max_move=minmaxExpand(gameState)
        return max_move[0]
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def minmaxExpand(startGameState): 
          '''
          return a action after minmax expanding and computing
          '''
          alpha=-1e6
          beta=1e6
          return maxMove(startGameState, 1, alpha, beta)
        def maxMove(curGameState, curDepth, alpha, beta): 
          '''
          Expand moves from the Pacman
          return a action with maximum value
          '''
          # return the eval val when the game is either win or lose
          if curGameState.isWin() or curGameState.isLose():
            return [[], self.evaluationFunction(curGameState)]
          # after max expand then do the min expand
          curMaxSuccessor=None
          legalMoves = curGameState.getLegalActions(0)
          for _aMove in legalMoves: 
            if curMaxSuccessor is None: 
              curMaxSuccessor = [_aMove, minMove(
                curGameState.generateSuccessor(0, _aMove), 
                curDepth, 1, alpha, beta
              )[1]]
            else: 
              curMaxSuccessor = max([curMaxSuccessor, [_aMove, minMove(
                curGameState.generateSuccessor(0, _aMove), 
                curDepth, 1, alpha, beta
              )[1]]], key=lambda x: x[1])
            if curMaxSuccessor[1] > beta: 
              return curMaxSuccessor
            alpha = max(alpha, curMaxSuccessor[1])
          return curMaxSuccessor
        def minMove(curGameState, curDepth, ghostIdx, alpha, beta): 
          '''
          Expand moves from all the ghosts
          return a action with minimum value
          '''
          # return the eval val when the game is either win or lose
          if curGameState.isWin() or curGameState.isLose():
            return [[], self.evaluationFunction(curGameState)]
          # 1. if ghost idx is not the last one, then expand to current ghost's moves, 
          # then move to next ghost moves, which is also a min expand
          if ghostIdx < (curGameState.getNumAgents()-1):
            curMinSuccessor=None
            legalMoves = curGameState.getLegalActions(ghostIdx)
            for _aMove in legalMoves: 
              if curMinSuccessor is None: 
                curMinSuccessor = [_aMove, minMove(
                  curGameState.generateSuccessor(ghostIdx, _aMove), 
                  curDepth, 
                  ghostIdx+1, 
                  alpha, 
                  beta
                )[1]]
              else: 
                curMinSuccessor = min([curMinSuccessor, [_aMove, minMove(
                  curGameState.generateSuccessor(ghostIdx, _aMove), 
                  curDepth, 
                  ghostIdx+1, 
                  alpha, 
                  beta
                )[1]]], key=lambda x: x[1])
              if curMinSuccessor[1] < alpha: 
                return curMinSuccessor
              beta = min(beta, curMinSuccessor[1])
            return curMinSuccessor

          # 2. if ghost idx is the last one, 
          # but the desire depth is greater than current depth, 
          # then do another max expand
          if ghostIdx == (curGameState.getNumAgents()-1):
            if curDepth < self.depth: 
              curMinSuccessor=None
              expandMoveAndValues = []
              legalMoves = curGameState.getLegalActions(ghostIdx)
              for _aMove in legalMoves: 
                if curMinSuccessor is None: 
                  curMinSuccessor = [_aMove, maxMove(
                    curGameState.generateSuccessor(ghostIdx, _aMove), 
                    curDepth+1, 
                    alpha, 
                    beta
                  )[1]]
                else: 
                  curMinSuccessor = min([curMinSuccessor, [_aMove, maxMove(
                    curGameState.generateSuccessor(ghostIdx, _aMove), 
                    curDepth+1, 
                    alpha, 
                    beta
                  )[1]]], key=lambda x: x[1])
                if curMinSuccessor[1] < alpha: 
                  return curMinSuccessor
                beta = min(beta, curMinSuccessor[1])
              return curMinSuccessor

          # 3. if ghost idx is the last one
          # and current depth is the desire depth, then return the min expand value
          if ghostIdx == (curGameState.getNumAgents()-1):
            if curDepth == self.depth: 
              curMinSuccessor=None
              legalMoves = curGameState.getLegalActions(ghostIdx)
              for _aMove in legalMoves: 
                if curMinSuccessor is None: 
                  curMinSuccessor = [_aMove, self.evaluationFunction(curGameState.generateSuccessor(ghostIdx, _aMove))]
                else: 
                  curMinSuccessor = min(
                    [
                      curMinSuccessor, 
                      [_aMove, self.evaluationFunction(curGameState.generateSuccessor(ghostIdx, _aMove))]
                    ], 
                    key = lambda x: x[1]
                  )
                if curMinSuccessor[1] < alpha: 
                  return curMinSuccessor
                beta = min(beta, curMinSuccessor[1])
              return curMinSuccessor
        optimalMove=minmaxExpand(gameState)
        return optimalMove[0]
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


