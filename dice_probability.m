dice = 1:6;

dice_p = 1:6;
% dice_p = [6,5,4,3,2,1];

y = pdf('Poisson',dice,dice_p);

plot(6:-1:1,y*100)
title("Dice Throw Propability")
xlabel("Dice Face")
ylabel("Propability [%]")

