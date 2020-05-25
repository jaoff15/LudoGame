

popFit = 1:-0.01:0;

popFitScaled = popFit .* logspace(2,0,length(popFit));

fitnessList = popFitScaled + 1

% 
Flist = [];
for i = 1:length(popFit)
   val = popFit(i) * 10^(popFit(i)*2) 
   Flist = [Flist, val]; 
end

figure(1)
clf(1)
hold all
% plot(1:-0.01:0, popFitScaled)
plot(0:100, Flist)
ylabel("Fitness Scale Factor")
xlabel("Individual Index, Sorted Best \Rightarrow Worst")
ylim([1,101])
xlim([0,101])
% set(gca,'XTick',[])
grid on