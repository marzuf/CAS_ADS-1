function visualizeAndPlayClips(XTrain, adsTrain)
    specMin = min(XTrain(:));
    specMax = max(XTrain(:));
    %idx = randperm(size(XTrain,4),3);
    figure('Units','normalized','Position',[0.2 0.2 0.6 0.6]);
    dsLength = length(adsTrain.Files)
    for i = 1:dsLength
        [x,fs] = audioread(adsTrain.Files{i});
        subplot(2,dsLength,i)
        plot(x)
        axis tight
        title(string(adsTrain.Labels(i)))
        xlabel('Time')
        ylabel('Amplitude')
        
        
        subplot(2,dsLength,i + dsLength)
        spect = XTrain(:,:,1,i);
        pcolor(spect)
        %caxis([specMin+2 specMax])
        title(['Mel Spectrogram: ',string(adsTrain.Labels(i))])
        shading flat
        xlabel('Time')
        ylabel('Frequency')
        
        %sound(x,fs)
        %pause(2)
    end
end