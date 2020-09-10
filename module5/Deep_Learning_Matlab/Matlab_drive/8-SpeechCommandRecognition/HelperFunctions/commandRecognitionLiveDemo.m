specMin = min(XTrain(:));
specMax = max(XTrain(:));

frameLength = frameDuration*fs;
hopLength = hopDuration*fs;
waveBuffer = zeros([fs,1]);

labels = trainedNet.Layers(end).Classes;
YBuffer(1:classificationRate/2) = categorical("background");
probBuffer = zeros([numel(labels),classificationRate/2]);


h = figure('Units','normalized','Position',[0.2 0.1 0.6 0.8]);
set(gcf,'Visible','on')

while ishandle(h)
    
    % Extract audio samples from the audio device and add the samples to
    % the buffer.
    x = audioIn();
    waveBuffer(1:end-numel(x)) = waveBuffer(numel(x)+1:end);
    waveBuffer(end-numel(x)+1:end) = x;
    
    % Compute the spectrogram of the latest audio samples.
    spec = auditorySpectrogram(waveBuffer,fs, ...
        'WindowLength',frameLength, ...
        'OverlapLength',frameLength-hopLength, ...
        'NumBands',numBands, ...
        'Range',[50,7000], ...
        'WindowType','Hann', ...
        'WarpType','Bark', ...
        'SumExponent',2);
    spec = log10(spec + epsil);
    
    % Classify the current spectrogram, save the label to the label buffer,
    % and save the predicted probabilities to the probability buffer.
    
    [YPredicted,probs] = classify(trainedNet,spec,'ExecutionEnvironment','cpu');
    YBuffer(1:end-1)= YBuffer(2:end);
    YBuffer(end) = YPredicted;
    probBuffer(:,1:end-1) = probBuffer(:,2:end);
    probBuffer(:,end) = probs';
    
    % Plot the current waveform and spectrogram.
    subplot(2,1,1);
    plot(waveBuffer)
    axis tight
    ylim([-0.2,0.2])
    
    subplot(2,1,2)
    pcolor(spec)
    caxis([specMin+2 specMax])
    shading flat
    
    % Now do the actual command detection by performing a very simple
    % thresholding operation. Declare a detection and display it in the
    % figure title if all of the following hold:
    % 1) The most common label is not |background|.
    % 2) At least |countThreshold| of the latest frame labels agree.
    % 3) The maximum predicted probability of the predicted label is at
    % least |probThreshold|. Otherwise, do not declare a detection.
    [YMode,count] = mode(YBuffer);
    countThreshold = ceil(classificationRate*0.2);
    maxProb = max(probBuffer(labels == YMode,:));
    probThreshold = 0.7;
    subplot(2,1,1);
    if YMode == "background" || count<countThreshold || maxProb < probThreshold
        title(" ")
    else
        title(string(YMode),'FontSize',20)
    end
    
    drawnow
    
end