clc, clear all, format compact

% Windows
% files = ["F:\Dropbox\3rd Semester Master\Tools of Artificial Intelligence\LudoGame\Ludo64bitVersion\data\69\fitness.csv",
%          "F:\Dropbox\3rd Semester Master\Tools of Artificial Intelligence\LudoGame\Ludo64bitVersion\data\69\fitness_avg.csv",
%          "F:\Dropbox\3rd Semester Master\Tools of Artificial Intelligence\LudoGame\Ludo64bitVersion\data\69\win_percent.csv"];
% Linux

version = "24";
% /home/jacoboffersen/Dropbox/3rd Semester Master/Tools of Artificial Intelligence/LudoGame/Ludo64bitVersion/data/106/fitness.csv
files = [strcat("/home/jacoboffersen/Dropbox/3rd Semester Master/Tools of Artificial Intelligence/LudoGame/Ludo64bitVersion/data/",version,"/fitness.csv"),
         strcat("/home/jacoboffersen/Dropbox/3rd Semester Master/Tools of Artificial Intelligence/LudoGame/Ludo64bitVersion/data/",version,"/win_percent.csv")];
%      /home/jacoboffersen/Dropbox/3rd Semester Master/Tools of Artificial Intelligence/LudoGame/
winners = strcat("/home/jacoboffersen/Dropbox/3rd Semester Master/Tools of Artificial Intelligence/LudoGame/Ludo64bitVersion/data/",version,"/winners.csv");
avg_gen_fit = strcat("/home/jacoboffersen/Dropbox/3rd Semester Master/Tools of Artificial Intelligence/LudoGame/Ludo64bitVersion/data/",version,"/avg_gen_fitness.csv");


% while(1)
    figure(1)
    clf(1)
    % Fitness
    M = csvread(files(1));
    x = M(:,1);
    y = M(:,2);
    M1 = csvread(avg_gen_fit);
    x1 = M1(:,1);
    y1 = M1(:,2);
    subplot(3,1,1)
    hold all
    plot(x,y)
    plot(x1,y1)
    legend("Max", "Avg")
%     title(titles(1))

    % Rolling average fitness
    y = movmean(y,10);
    y1 = movmean(y1,10);
    subplot(3,1,2)
    hold all
    plot(x,y)
    plot(x1,y1)
    legend("Max", "Avg")
%     title("Rolling average of fitness")
    
    % Win percent
    try
        M = csvread(files(2));
        x = M(:,1);
        y = M(:,2);
        subplot(3,1,3)
        plot(x,y)
%     title(titles(2)) 
    catch
        a = 0;
    end

    subplot(3,1,1)
    title("Best generation fitness")
    ylabel("Fitness points [-1000, 1000]")
    ylim([-1000,1000])
    subplot(3,1,2)
    title("Best generation fitness rolling average (10 generations)")
    ylabel("Fitness points [-1000, 1000]")
    ylim([-1000,1000])
    subplot(3,1,3)
    title("Win percentage in 100 games for best individual from every 100th generation")
    ylabel("%")
    ylim([0,100])
    
    
    figure(2)
    clf(2)
    M = csvread(winners);
    x = M(:,1);
    tie = M(:,2);
    AI = M(:,3);
    p = sum(M(:,4:6),2);
    subplot(3,1,1)
    hold all
    plot(x, tie)
    plot(x,movmean(tie,20))
    title("Ties")
    ylabel("%")
    xlabel("Generation")
    ylim([0,100])
    
    subplot(3,1,2)
    hold all
    plot(x, AI)
    plot(x,movmean(AI,20))
    title("AI wins") 
    ylabel("%")
    xlabel("Generation")
    ylim([0,100])
    
    
    subplot(3,1,3)
    hold all
    plot(x, p)
    plot(x,movmean(p,20))
    title("Random player wins")
    ylabel("%")
    xlabel("Generation")
    ylim([0,100])
    
    
    
%     pause(10)
% end 