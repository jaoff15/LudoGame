clc, clear all, format compact
POINTS_STEP = 1;
POINTS_PIECE_FINISH = 140;
POINTS_PIECE_FINISHING_LANE = 10;
POINTS_PIECE_AT_HOME = -250;

MAX_PIECES = 3;
MAX_STEPS = 50;
MAX_FINISH_LANE_POSITIONS = 6;

totalSteps = MAX_PIECES * MAX_STEPS;
piecesFinished = MAX_PIECES;
stepsFinishingLane = MAX_PIECES * MAX_FINISH_LANE_POSITIONS;

piecesAtHome = 0;

fitness = totalSteps*POINTS_STEP;
fitness = fitness + piecesFinished*POINTS_PIECE_FINISH;
fitness = fitness + stepsFinishingLane*POINTS_PIECE_FINISHING_LANE;
fitness = fitness + piecesAtHome*POINTS_PIECE_AT_HOME;

maxFitness = fitness
minFitness = MAX_PIECES * POINTS_PIECE_AT_HOME