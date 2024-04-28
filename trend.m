figure;
titles={'weight','water','trial number','total time'};
for ii=1:4
    subplot(4,1,ii); hold on
    plot(a(:,ii),'Color','k','Marker','o','MarkerFaceColor','k')
    plot([42.5,42.5],[min(a(:,ii))*0.9,max(a(:,ii))*1.1],'r--')
    title(titles{ii})
end